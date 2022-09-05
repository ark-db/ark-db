import requests
import pandas as pd
import json
from urllib.parse import quote

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
    name, _, _ = (
        df.iloc[0]
          ["活动页面"]
          .partition("(")
    )
    return name



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

'''
latest_ss = get_name_of_latest(
     events.pipe(lambda df: df[df["活动分类"].isin({"支线故事", "故事集"})])
)
'''

with open("./scripts/msv.json", "r") as f:
    sanity_values = json.load(f)

    for item in cc_shop.itertuples(index=False):
        name, _, qty = item.可兑换道具.partition("×")
        qty = int(qty) if qty else 1
        cost = item.单价
        if (value := sanity_values["cn"].get(item_name_to_id[name])):
            pass