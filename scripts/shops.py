import requests
import pandas as pd
import json
from urllib.parse import quote
from bs4 import BeautifulSoup
import unicodedata
import re

def convert_to_utc(df: pd.DataFrame):
    df["活动开始时间"] -= pd.Timedelta(hours=8)
    df["活动开始时间"] = df["活动开始时间"].dt.tz_localize("UTC")
    return df

def get_name_of_latest(df: pd.DataFrame) -> str:
    latest_event = df.iloc[0]
    name = latest_event["name"].replace("·复刻", str(latest_event["活动开始时间"].year))
    return name

def get_cc_page_url(name: str):
    return f"https://prts.wiki/w/{quote('危机合约')}/{quote(name)}"

def remove_punctuation(text: str):
    return "".join(ch for ch in text if unicodedata.category(ch)[0] != "P")

def get_ss_page_url(name: str, year: int):
    formatted_name = remove_punctuation(name.replace("·复刻", str(year)))
    return f"https://prts.wiki/w/{quote(formatted_name)}"

def get_shop_table(url: str):
    shop = (
        pd.read_html(url,
                     match="可兑换道具")
          [0]
          .iloc[:-1, 1:]
          .pipe(lambda df: df[df["单价"].str.isdecimal()])
    )
    return shop

def get_shop_effics(shop: pd.DataFrame, msvs: dict[str, float]) -> list[dict[str, str|int|float]]:
    shop_effics = []
    for item in shop.itertuples(index=False):
        name, _, qty = item.可兑换道具.partition("×")
        qty = int(qty) if qty else 1
        cost = int(item.单价)
        if (item_id := item_name_to_id.get(name)) and (value := msvs.get(item_id)):
            shop_effics.append({
                "id": item_id,
                "count": qty,
                "effic": value * qty / cost
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
    event["label_i18n"]["zh"]: event["label_i18n"]["en"] for event in all_events
}

cn_events = (
    pd.concat(
        pd.read_html("https://prts.wiki/w/%E6%B4%BB%E5%8A%A8%E4%B8%80%E8%A7%88",
                     parse_dates=["活动开始时间"])
          [:2],
        ignore_index=True)
      .pipe(convert_to_utc)
      .pipe(lambda df: df[df["活动开始时间"] < pd.Timestamp.utcnow()])
      .assign(name = lambda df: df["活动页面"].str.partition("(")[0]
                                             .str.rstrip())
      .drop(columns=["活动页面", "官网公告"])
)

cc_events = (
    cn_events.pipe(lambda df: df[df["活动分类"] == "危机合约"])
             .reset_index(drop=True)
)

ss_events = (
    cn_events.pipe(lambda df: df[df["活动分类"].isin({"支线故事", "故事集"})])
             .reset_index(drop=True)
)

en_events = (
    pd.read_html(requests.get("https://gamepress.gg/arknights/other/event-and-campaign-list")
                         .text)
      [0]
      .assign(end_time = lambda df: (pd.to_datetime(df["Period"].str.partition(" ~ ")[2])
                                     + pd.Timedelta(hours=10, minutes=59))
                                    .dt.tz_localize("UTC"))
)

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


 
with open("./scripts/msv.json", "r") as f1, open("./src/lib/data/shops.json", "w") as f2:
    sanity_values = json.load(f1)

    for ss in ss_events.itertuples():
        page_url = get_ss_page_url(ss.name, ss.活动开始时间.year)
        en_ss_name = cn_to_en_event_name[ss.name]
        en_ss_event = en_events.pipe(lambda df: df[df["Event / Campaign"].str.lower()
                                                                         .str.contains(remove_punctuation(en_ss_name).lower())])

        if ss.Index == 0:
            soup = BeautifulSoup(requests.get(page_url)
                                         .text,
                                 "lxml")
            news_link = soup.select_one("a[href*='https://ak.hypergryph.com/news/']")["href"]

            soup = BeautifulSoup(requests.get(news_link)
                                         .content
                                         .decode("utf-8", "ignore"),
                                 "lxml")
            event_period = (
                soup("strong",
                     text=re.compile("活动时间|关卡开放时间", flags=re.U))
                    [0].parent.contents[1]
                    .rstrip()
            )
            end_time = pd.to_datetime(str(pd.Timestamp.now().year) + "年" + event_period.partition(" - ")[2],
                                      format="%Y年%m月%d日 %H:%M")
            end_time_utc = (end_time - pd.Timedelta(hours=8)).tz_localize("UTC")

            if end_time_utc > pd.Timestamp.utcnow():
                cn_ss_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["cn"].update({
                    "ss": get_shop_effics(cn_ss_shop, sanity_values["cn"]) 
                })
                all_shop_effics["events"]["cn"].update({
                    "ss": en_ss_name
                })

        if not en_ss_event.empty:
            if en_ss_event.iloc[0]["end_time"] > pd.Timestamp.utcnow():
                en_ss_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["glb"].update({
                    "ss": get_shop_effics(en_ss_shop, sanity_values["glb"])
                })
                all_shop_effics["events"]["glb"].update({
                    "ss": en_ss_name
                })
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
        en_cc_event = en_events.pipe(lambda df: df[df["Event / Campaign"].str.contains(en_cc_name)])

        if cc.Index == 0:
            event_period = (
                soup("b",
                     text=re.compile("赛季开启时间", flags=re.U))
                    [0].parent.contents[1]
                    .rstrip()
            )
            end_time = pd.to_datetime(str(pd.Timestamp.now().year) + "年" + event_period.partition(" - ")[2],
                                      format="%Y年%m月%d日 %H:%M")            
            end_time_utc = (end_time - pd.Timedelta(hours=8)).tz_localize("UTC")

            if end_time_utc > pd.Timestamp.utcnow():
                cn_cc_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["cn"].update({
                    "cc": get_shop_effics(cn_cc_shop, sanity_values["cn"])
                })
                all_shop_effics["events"]["cn"].update({
                    "cc": en_cc_name
                })

        if not en_cc_event.empty:
            if en_cc_event.iloc[0]["end_time"] > pd.Timestamp.utcnow():
                en_cc_shop = get_shop_table(page_url)
                all_shop_effics["shops"]["glb"].update({
                    "cc": get_shop_effics(en_cc_shop, sanity_values["glb"])
                })
                all_shop_effics["events"]["glb"].update({
                    "cc": en_cc_name
                })
            break

    json.dump(all_shop_effics, f2, ensure_ascii=False)