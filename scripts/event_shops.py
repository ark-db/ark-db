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

CN_ITEMS = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json")
            .json()
            ["items"]
)

ITEM_NAME_TO_ID = {
    data["name"]: data["itemId"]
    for data in CN_ITEMS.values()
}

ALL_EVENTS = (
    requests.get("https://penguin-stats.io/PenguinStats/api/v2/period")
            .json()
)

EN_PERIOD_REGEX = re.compile("DURATION:")
CN_PERIOD_REGEX = re.compile("活动时间|关卡开放时间", flags=re.U)
CC_START_REGEX = re.compile("赛季开启时间", flags=re.U)

all_shop_effics = {
    category: {
        region.name.lower(): dict()
        for region in utils.Region
    }
    for category in ("shops", "events")
}



def set_timezone_as_cn(df: pd.DataFrame) -> pd.DataFrame:
    df["活动开始时间"] = df["活动开始时间"].dt.tz_localize("Asia/Shanghai")
    return df

def remove_punctuation(text: str) -> str:
    return "".join(ch for ch in text if unicodedata.category(ch)[0] != "P")

def get_ss_page_url(name: str, year: int) -> str:
    formatted_name = remove_punctuation(name.replace("·复刻", str(year)))
    return f"https://prts.wiki/w/{quote(formatted_name)}"

def get_cc_page_url(name: str) -> str:
    return f"https://prts.wiki/w/{quote('危机合约')}/{quote(name)}"

def get_cn_event_end_time(period: str) -> pd.Timestamp:
    return (
        pd.to_datetime(str(pd.Timestamp.now().year) + "年" + period.partition(" - ")[2],
                       format="%Y年%m月%d日 %H:%M")
          .tz_localize("Asia/Shanghai")
    )

def save_banner_img(soup: BeautifulSoup, name: str) -> None:
    banner_url = soup.select_one("img[alt*='活动预告']")["data-src"]
    utils.save_image(f"https://prts.wiki{banner_url}", utils.Asset.EVENT, name=name)

def remove_multiindex(df: pd.DataFrame) -> pd.DataFrame:
    if df.columns.nlevels > 1:
        return df.droplevel(
            [i for i in range(1, df.columns.nlevels)],
            axis=1
        )
    return df

def get_shop_table(soup: BeautifulSoup) -> pd.DataFrame:
    return (
        pd.read_html(str(soup),
                     match="可兑换道具")
          [0]
          # remove column of checkboxes and row of total item costs
          .iloc[:-1, 1:]
          # remove shop section divider rows
          .pipe(remove_multiindex)
          .pipe(lambda df: df[df["单价"].str.isdecimal()])
    )

def get_shop_effics(shop: pd.DataFrame, msvs: dict[str, float]) -> Effics:
    shop_effics = []
    for item in shop.itertuples(index=False):
        name, _, qty = item.可兑换道具.partition("×")
        if (item_id := ITEM_NAME_TO_ID.get(name)) and (value := msvs.get(item_id)):
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

def get_soup(url: str, parse_as_bytes: bool = False) -> BeautifulSoup:
    if parse_as_bytes:
        return BeautifulSoup(
            requests.get(url).content.decode("utf-8", "ignore"),
            "lxml"
        )
    return BeautifulSoup(
        requests.get(url).text,
        "lxml"
    )

def update_data(soup: BeautifulSoup, region: utils.Region, event_type: utils.Event, event_name: str) -> None:
    region = region.name.lower()
    event_type = event_type.value

    save_banner_img(soup, f"{region}_{event_type}_banner")

    shop_table = get_shop_table(soup)
    all_shop_effics["shops"][region].update({
        event_type: get_shop_effics(shop_table, SANITY_VALUES[region])
    })
    all_shop_effics["events"][region].update({
        event_type: event_name
    })

def update_en_data(data: str|BeautifulSoup, event_type: utils.Event, event_name: str) -> bool:
    search_str = condense_str(event_name)

    for news_title, news_url in en_scraper.EVENTS.items():
        if search_str in condense_str(news_title):
            soup = en_scraper.get_soup(news_url)
            event_period = (
                soup("strong", text=EN_PERIOD_REGEX)
                [0].parent.contents[1]
            )
            end_time = dateparser.parse(event_period.partition(" – ")[2])

            if pd.Timestamp(end_time) > pd.Timestamp.utcnow():
                update_data(
                    data if isinstance(data, BeautifulSoup) else get_soup(data),
                    utils.Region.GLB,
                    event_type,
                    event_name
                )

            return True

    return False



CN_TO_EN_EVENT_NAME = {
    condense_str(event["label_i18n"]["zh"]): event["label_i18n"]["en"]
    for event in ALL_EVENTS
}

CN_EVENTS = (
    pd.concat(pd.read_html("https://prts.wiki/w/%E6%B4%BB%E5%8A%A8%E4%B8%80%E8%A7%88",
                           parse_dates=["活动开始时间"])[:2],
              ignore_index=True)
      .pipe(set_timezone_as_cn)
      .pipe(lambda df: df[df["活动开始时间"] < pd.Timestamp.utcnow()])
      # remove inlined JS in chips that appear next to latest events
      .assign(name = lambda df: df["活动页面"].str.partition("(")[0]
                                             .str.rstrip())
      .drop(columns=["活动页面", "官网公告"])
)

CC_EVENTS = (
    CN_EVENTS.pipe(lambda df: df[df["活动分类"] == "危机合约"])
             .reset_index(drop=True)
)

SS_EVENTS = (
    CN_EVENTS.pipe(lambda df: df[df["活动分类"].str.contains(r"支线故事|故事集")])
             .reset_index(drop=True)
)



with (open("./scripts/msv.json", "r") as f1,
      open("./src/lib/data/event_shops.json", "w") as f2):
    SANITY_VALUES = json.load(f1)

    for ss in SS_EVENTS.itertuples():
        page_url = get_ss_page_url(ss.name, ss.活动开始时间.year)
        en_name = CN_TO_EN_EVENT_NAME[condense_str(ss.name)]

        # latest Side Story event
        if ss.Index == 0:
            prts_soup = get_soup(page_url)
            news_link = (
                prts_soup.select_one("a[href*='https://ak.hypergryph.com/news/']")
                         ["href"]
            )
            hg_soup = get_soup(news_link, parse_as_bytes=True)
            event_period = (
                hg_soup("strong", text=CN_PERIOD_REGEX)
                       [0].parent.contents[1]
                       .rstrip()
            )

            if get_cn_event_end_time(event_period) > pd.Timestamp.utcnow():
                update_data(prts_soup, utils.Region.CN, utils.Event.SS, en_name)

        if update_en_data(page_url, utils.Event.SS, en_name):
            break

    for cc in CC_EVENTS.itertuples():
        page_url = get_cc_page_url(cc.name)
        soup = get_soup(page_url)
        en_name = (
            soup.select_one("td > .nodesktop")
                .text
        )

        # latest Contingency Contract event
        if cc.Index == 0:
            event_period = (
                soup("b", text=CC_START_REGEX)
                    [0].parent.contents[1]
                    .rstrip()
            )

            if get_cn_event_end_time(event_period) > pd.Timestamp.utcnow():
                update_data(soup, utils.Region.CN, utils.Event.CC, en_name)

        if update_en_data(soup, utils.Event.CC, en_name):
            break

    json.dump(all_shop_effics, f2)

en_scraper.driver.close()

print("Successfully updated event shop data")
