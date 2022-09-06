import requests
import pandas as pd
import json
from urllib.parse import quote
from bs4 import BeautifulSoup
import unicodedata

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

en_events = (
    pd.read_html(requests.get("https://gamepress.gg/arknights/other/event-and-campaign-list")
                         .text)
      [0]
)

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



cn_events = (
    pd.concat(
        pd.read_html("https://prts.wiki/w/%E6%B4%BB%E5%8A%A8%E4%B8%80%E8%A7%88",
                     parse_dates=["活动开始时间"])
          [:2],
        ignore_index=True)
      .pipe(convert_to_utc)
      .pipe(lambda df: df[df["活动开始时间"] < pd.Timestamp.utcnow()])
      .assign(name = lambda df: df["活动页面"].str.partition("(")[0])
      .drop(columns=["活动页面", "官网公告"])
)

cc_events = cn_events.pipe(lambda df: df[df["活动分类"] == "危机合约"])

cn_cc_shop = get_shop_table(get_cc_page_url(get_name_of_latest(cc_events)))

for cc in cc_events.itertuples(index=False):
    soup = BeautifulSoup(requests.get(get_cc_page_url(cc.name))
                                 .text,
                         "lxml")

    en_name = soup.select_one("td > .nodesktop").text

    cc_event = en_events.pipe(lambda df: df[df["Event / Campaign"].str.contains(en_name)])

    if not cc_event.empty:
        en_cc_shop = get_shop_table(get_cc_page_url(cc.name))
        break



ss_events = cn_events.pipe(lambda df: df[df["活动分类"].isin({"支线故事", "故事集"})])

cn_ss_shop = get_shop_table(f"https://prts.wiki/w/{quote(remove_punctuation(get_name_of_latest(ss_events)))}")



all_shop_effics = {
    "glb": dict(),
    "cn": dict()
}

with open("./scripts/msv.json", "r") as f1, open("./scripts/shops.json", "w") as f2:
    sanity_values = json.load(f1)

    all_shop_effics["cn"].update({
        "cc": get_shop_effics(cn_cc_shop, sanity_values["cn"])
    })

    all_shop_effics["cn"].update({
        "ss": get_shop_effics(cn_ss_shop, sanity_values["cn"]) 
    })

    all_shop_effics["glb"].update({
        "cc": get_shop_effics(en_cc_shop, sanity_values["glb"])
    })
    
    json.dump(all_shop_effics, f2)