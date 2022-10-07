import utils
import en_scraper
import requests
import pandas as pd
import json
from urllib.parse import quote # request URLs need to be encoded
from bs4 import BeautifulSoup
import unicodedata
import re
import dateparser



Effics = list[dict[str, str|int|float]]

en_period_regex = re.compile("DURATION:")
cn_period_regex = re.compile("活动时间|关卡开放时间", flags=re.U)
cc_start_regex = re.compile("赛季开启时间", flags=re.U)

all_shop_effics = {
    "shops": {
        "glb": dict(),
        "cn": dict()
    },
    "events": {
        "glb": dict(),
        "cn": dict()
    }
}



# for prts.wiki datetimes
def convert_to_utc(df: pd.DataFrame) -> pd.DataFrame:
    # prts.wiki uses Beijing Time
    df["活动开始时间"] = (df["活动开始时间"] - pd.Timedelta(hours=8)).dt.tz_localize("UTC")
    return df

def get_cc_page_url(name: str) -> str:
    return f"https://prts.wiki/w/{quote('危机合约')}/{quote(name)}"

def remove_punctuation(text: str) -> str:
    return "".join(ch for ch in text if unicodedata.category(ch)[0] != "P")

def get_ss_page_url(name: str, year: int) -> str:
    formatted_name = remove_punctuation(name.replace("·复刻", str(year)))
    return f"https://prts.wiki/w/{quote(formatted_name)}"

def save_banner_img(soup: BeautifulSoup, name: str) -> None:
    banner_url = soup.select_one("img[alt*='活动预告']")["data-src"]
    utils.save_image(
        f"https://prts.wiki{banner_url}", 
        category="events",
        name=name,
        overwrite=True
    )

def remove_multiindex(df: pd.DataFrame) -> pd.DataFrame:
    if df.columns.nlevels > 1:
        return df.droplevel([i for i in range(1, df.columns.nlevels)],
                            axis=1)
    return df

def get_shop_table(url: str) -> pd.DataFrame:
    shop = (
        pd.read_html(url,
                     match="可兑换道具")
          [0]
          # remove column of checkboxes and row of total item costs
          .iloc[:-1, 1:]
          # remove shop section divider rows
          .pipe(remove_multiindex)
          .pipe(lambda df: df[df["单价"].str.isdecimal()])
    )
    return shop

def get_shop_effics(shop: pd.DataFrame, msvs: dict[str, float]) -> Effics:
    shop_effics = []
    for item in shop.itertuples(index=False):
        name, _, qty = item.可兑换道具.partition("×")
        if (item_id := item_name_to_id.get(name)) and (value := msvs.get(item_id)):
            qty = int(qty) if qty else 1
            # -1 in data represents unlimited stock
            stock = int(item.库存) if item.库存 != "∞" else -1
            cost = int(item.单价)
            shop_effics.append({
                "id": item_id,
                "count": qty,
                "stock": stock,
                # -1 in data represents unvalued item
                "value": round(value * qty / cost, 3) if value != -1 else -1
            })
    return shop_effics

def condense_str(text: str) -> str:
    return remove_punctuation(text).replace(" ", "").lower()

def update_en_data(prts_url: str, event_name: str, event_type: str) -> bool:
    search_str = condense_str(event_name)

    for news_title, news_url in en_scraper.events.items():
        if search_str in condense_str(news_title):
            soup = en_scraper.get_soup(news_url)
            event_period = (
                soup("strong", text=en_period_regex)
                [0].parent.contents[1]
            )
            end_time = dateparser.parse(event_period.partition(" – ")[2])
            # if event hasn't ended already
            if pd.Timestamp(end_time) > pd.Timestamp.utcnow():
                soup = BeautifulSoup(requests.get(prts_url)
                                             .text,
                                     "lxml")
                save_banner_img(soup, f"glb_{event_type}_banner")
                shop_table = get_shop_table(prts_url)
                all_shop_effics["shops"]["glb"].update({
                    event_type: get_shop_effics(shop_table, sanity_values["glb"])
                })
                all_shop_effics["events"]["glb"].update({
                    event_type: event_name
                })
            return True

    return False


cn_items = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json")
            .json()
            ["items"]
)

item_name_to_id = {data["name"]: data["itemId"] for data in cn_items.values()}

all_events = (
    requests.get("https://penguin-stats.io/PenguinStats/api/v2/period")
            .json()
)

cn_to_en_event_name = {
    condense_str(event["label_i18n"]["zh"]): event["label_i18n"]["en"] for event in all_events
}

cn_events = (
    pd.concat(
        pd.read_html("https://prts.wiki/w/%E6%B4%BB%E5%8A%A8%E4%B8%80%E8%A7%88",
                     parse_dates=["活动开始时间"])
          [:2],
        ignore_index=True)
      .pipe(convert_to_utc)
      .pipe(lambda df: df[df["活动开始时间"] < pd.Timestamp.utcnow()])
      # remove inlined JS in chips that appear next to latest events
      .assign(name = lambda df: df["活动页面"].str.partition("(")[0]
                                             .str.rstrip())
      .drop(columns=["活动页面", "官网公告"])
)

cc_events = (
    cn_events.pipe(lambda df: df[df["活动分类"] == "危机合约"])
             .reset_index(drop=True)
)

ss_events = (
    cn_events.pipe(lambda df: df[df["活动分类"].str.contains(r"支线故事|故事集")])
             .reset_index(drop=True)
)



with (open("./scripts/msv.json", "r") as f1,
      open("./src/lib/data/event_shops.json", "w") as f2):
    sanity_values = json.load(f1)

    for ss in ss_events.itertuples():
        page_url = get_ss_page_url(ss.name, ss.活动开始时间.year)
        en_ss_name = cn_to_en_event_name[condense_str(ss.name)]

        # latest side-story event
        if ss.Index == 0:
            prts_soup = BeautifulSoup(requests.get(page_url)
                                              .text,
                                      "lxml")
            news_link = prts_soup.select_one("a[href*='https://ak.hypergryph.com/news/']")["href"]

            hg_soup = BeautifulSoup(requests.get(news_link)
                                         .content
                                         .decode("utf-8", "ignore"),
                                 "lxml")
            event_period = (
                hg_soup("strong", text=cn_period_regex)
                       [0].parent.contents[1]
                       .rstrip()
            )
            end_time = pd.to_datetime(
                str(pd.Timestamp.now().year) + "年" + event_period.partition(" - ")[2],
                format="%Y年%m月%d日 %H:%M"
            )
            end_time_utc = (end_time - pd.Timedelta(hours=8)).tz_localize("UTC")

            # if event hasn't ended already
            if end_time_utc > pd.Timestamp.utcnow():
                save_banner_img(prts_soup, "cn_ss_banner")

                cn_ss_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["cn"].update({
                    "ss": get_shop_effics(cn_ss_shop, sanity_values["cn"]) 
                })
                all_shop_effics["events"]["cn"].update({
                    "ss": en_ss_name
                })

        if update_en_data(prts_url=page_url, 
                          event_name=en_ss_name,
                          event_type="ss"):
            break

    for cc in cc_events.itertuples():
        page_url = get_cc_page_url(cc.name)
        soup = BeautifulSoup(requests.get(page_url)
                                     .text,
                             "lxml")
        en_cc_name = (
            soup.select_one("td > .nodesktop")
                .text
        )

        # latest Contingency Contract event
        if cc.Index == 0:
            event_period = (
                soup("b", text=cc_start_regex)
                    [0].parent.contents[1]
                    .rstrip()
            )
            end_time = pd.to_datetime(
                str(pd.Timestamp.now().year) + "年" + event_period.partition(" - ")[2],
                format="%Y年%m月%d日 %H:%M"
            )            
            end_time_utc = (end_time - pd.Timedelta(hours=8)).tz_localize("UTC")

            # if event hasn't ended already
            if end_time_utc > pd.Timestamp.utcnow():
                save_banner_img(soup, "cn_cc_banner")

                cn_cc_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["cn"].update({
                    "cc": get_shop_effics(cn_cc_shop, sanity_values["cn"])
                })
                all_shop_effics["events"]["cn"].update({
                    "cc": en_cc_name
                })

        if update_en_data(prts_url=page_url,
                          event_name=en_cc_name,
                          event_type="cc"):
            break

    json.dump(all_shop_effics, f2)

en_scraper.driver.close()

print("Successfully updated event shop data")