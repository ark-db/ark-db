import utils
import requests
import pandas as pd
import json
from urllib.parse import quote # request URLs need to be encoded
from bs4 import BeautifulSoup
import unicodedata
import re



Effics = list[dict[str, str|int|float]]

# for prts.wiki datetimes
def convert_to_utc(df: pd.DataFrame):
    # prts.wiki uses Beijing Time
    df["活动开始时间"] = (df["活动开始时间"] - pd.Timedelta(hours=8)).dt.tz_localize("UTC")
    return df

def get_cc_page_url(name: str):
    return f"https://prts.wiki/w/{quote('危机合约')}/{quote(name)}"

def remove_punctuation(text: str):
    return "".join(ch for ch in text if unicodedata.category(ch)[0] != "P")

def get_ss_page_url(name: str, year: int):
    formatted_name = remove_punctuation(name.replace("·复刻", str(year)))
    return f"https://prts.wiki/w/{quote(formatted_name)}"

def save_event_banner_img(soup: BeautifulSoup, name: str):
    event_banner_url = soup.select_one("img[alt*='活动预告']")["data-src"]
    utils.save_image(
        f"https://prts.wiki{event_banner_url}", 
        category="events",
        image_id=name,
        overwrite=True
    )

def get_shop_table(url: str) -> pd.DataFrame:
    shop = (
        pd.read_html(url,
                     match="可兑换道具")
          [0]
          # remove column of checkboxes and row of total item costs
          .iloc[:-1, 1:]
          # remove shop section divider rows
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
    # the dot symbols prts.wiki and Penguin Stats use for rerun event names are different
    event["label_i18n"]["zh"].replace("・", "·"): event["label_i18n"]["en"] for event in all_events
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

en_events = (
    pd.read_html(requests.get("https://gamepress.gg/arknights/other/event-and-campaign-list")
                         .text)
      [0]
      # parse Gamepress' datetime format and convert to UTC
      .assign(end_time = lambda df: (pd.to_datetime(df["Period"].str.partition(" ~ ")[2])
                                     + pd.Timedelta(hours=10, minutes=59))
                                    .dt.tz_localize("UTC"))
)

event_period_regex = re.compile("活动时间|关卡开放时间", flags=re.U)

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


 
with (open("./scripts/msv.json", "r") as f1,
      open("./src/lib/data/event_shops.json", "w") as f2):
    sanity_values = json.load(f1)

    for ss in ss_events.itertuples():
        page_url = get_ss_page_url(ss.name, ss.活动开始时间.year)
        en_ss_name = cn_to_en_event_name[ss.name]
        # this DataFrame will be empty if the event does not exist in global yet
        en_ss_event = en_events.pipe(
            lambda df: df[
                df["Event / Campaign"].str.lower()
                                      .str.contains(remove_punctuation(en_ss_name).lower())
            ]
        )

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
                hg_soup("strong", text=event_period_regex)
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
                save_event_banner_img(prts_soup, "cn_ss_banner")

                cn_ss_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["cn"].update({
                    "ss": get_shop_effics(cn_ss_shop, sanity_values["cn"]) 
                })
                all_shop_effics["events"]["cn"].update({
                    "ss": en_ss_name
                })

        # if event exists in global
        if not en_ss_event.empty:
            # if event hasn't ended already
            if en_ss_event.iloc[0]["end_time"] > pd.Timestamp.utcnow():
                soup = BeautifulSoup(requests.get(page_url)
                                             .text,
                                     "lxml")
                save_event_banner_img(soup, "glb_ss_banner")

                en_ss_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["glb"].update({
                    "ss": get_shop_effics(en_ss_shop, sanity_values["glb"])
                })
                all_shop_effics["events"]["glb"].update({
                    "ss": en_ss_name
                })
            # program will have found the latest global event by this point,
            # so no need to keep looking
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
        en_cc_event = en_events.pipe(
            lambda df: df[df["Event / Campaign"].str.contains(en_cc_name)]
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
                save_event_banner_img(soup, "cn_cc_banner")

                cn_cc_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["cn"].update({
                    "cc": get_shop_effics(cn_cc_shop, sanity_values["cn"])
                })
                all_shop_effics["events"]["cn"].update({
                    "cc": en_cc_name
                })

        # if event exists in global
        if not en_cc_event.empty:
            # if event hasn't ended already
            if en_cc_event.iloc[0]["end_time"] > pd.Timestamp.utcnow():
                save_event_banner_img(soup, "glb_cc_banner")

                en_cc_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["glb"].update({
                    "cc": get_shop_effics(en_cc_shop, sanity_values["glb"])
                })
                all_shop_effics["events"]["glb"].update({
                    "cc": en_cc_name
                })
            # program will have found the latest global event by this point,
            # so no need to keep looking
            break

    json.dump(all_shop_effics, f2)

print("Successfully updated event shop data")