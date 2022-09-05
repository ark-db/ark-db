import requests
import pandas as pd
import json
from urllib.parse import quote
import unicodedata

cn_items = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json")
            .json()
            ["items"]
)



def convert_to_utc(df: pd.DataFrame):
    df["活动开始时间"] -= pd.Timedelta(hours=8)
    df["活动开始时间"] = df["活动开始时间"].dt.tz_localize("UTC")
    return df

def get_name_of_latest(df: pd.DataFrame) -> str:
    latest_event = df.iloc[0]
    name, _, _ = latest_event["活动页面"].partition("(")
    name = name.replace("·复刻", str(latest_event["活动开始时间"].year))
    return name

def get_shop_effics(shop: pd.DataFrame, msvs: dict[str, float]) -> list[dict[str, str|int|float]]:
    shop_effics = []
    for item in shop.itertuples(index=False):
        name, _, qty = item.可兑换道具.partition("×")
        qty = int(qty) if qty else 1
        cost = int(item.单价)
        item_id = item_name_to_id[name]
        if (value := msvs.get(item_id)):
            shop_effics.append({
                "id": item_id,
                "count": qty,
                "effic": value * qty / cost
            })
    return shop_effics


item_name_to_id = {data["name"]: data["itemId"] for data in cn_items.values()}

events = (
    pd.read_html("https://prts.wiki/w/%E6%B4%BB%E5%8A%A8%E4%B8%80%E8%A7%88",
                 parse_dates=["活动开始时间"])
      [0]
      .pipe(convert_to_utc)
      .pipe(lambda df: df[df["活动开始时间"] < pd.Timestamp.utcnow()])
)
    
latest_cc = get_name_of_latest(
    events.pipe(lambda df: df[df["活动分类"] == "危机合约"])
)
    
cc_shop = (
    pd.read_html(f"https://prts.wiki/w/{quote('危机合约')}/{quote(latest_cc)}",
                 match="可兑换道具")
    [0]
    .iloc[:-1, 1:]
)

latest_ss = get_name_of_latest(
     events.pipe(lambda df: df[df["活动分类"].isin({"支线故事", "故事集"})])
)

formatted_ss_name = "".join(ch for ch in latest_ss if unicodedata.category(ch)[0] != "P")

ss_shop = (
    pd.read_html(f"https://prts.wiki/w/{quote(formatted_ss_name)}",
                 match="可兑换道具")
      [0]
      .iloc[:-1, 1:]
      .pipe(lambda df: df[df["单价"].str.isdecimal()])
)



all_shop_effics = {
    "glb": dict(),
    "cn": dict()
}

with open("./scripts/msv.json", "r") as f:
    sanity_values = json.load(f)

    all_shop_effics["cn"].update({
        "cc": get_shop_effics(cc_shop, sanity_values["cn"])
    })

    all_shop_effics["cn"].update({
        "ss": get_shop_effics(ss_shop, sanity_values["cn"]) 
    })