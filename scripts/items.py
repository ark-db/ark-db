import requests
import pandas as pd

VALID_ITEMS = (
    "30011", "30021", "30031", "30041", "30051", "30061", # t1 mats
    "30012", "30022", "30032", "30042", "30052", "30062", # t2 mats
    "30013", "30023", "30033", "30043", "30053", "30063", "30073", "30083", "30093", "30103", "31013", "31023", "31033", "31043", "31053", # t3 mats
    "30014", "30024", "30034", "30044", "30054", "30064", "30074", "30084", "30094", "30104", "31014", "31024", "31034", "31044", "31054", # t4 mats
    "30115", "30125", "30135", "30145", # t5 mats
    "3301", "3302", "3303", # skillbooks
    "mod_unlock_token", "mod_update_token_1", "mod_update_token_2", # module mats
)

cn_items = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json")
            .json()
            ["items"]
)

en_items = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/item_table.json")
            .json()
            ["items"]
)

workshop_formulas = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json")
            .json()
            ["workshopFormulas"]
)

en_names = (
    pd.DataFrame(en_items)
      .filter(["name"], axis=0)
)

def replace_names(df, names):
    df.loc["name"] = names.loc["name"]
    df.loc["name", ['mod_update_token_1', 'mod_update_token_2']] = ["数据增补条", "数据增补仪"]
    return df

item_data = (
    pd.DataFrame(cn_items)
      .filter(VALID_ITEMS)
      .filter(["itemId", "name", "rarity", "iconId", "sortId"], axis=0)
      .pipe(replace_names, en_names)
)