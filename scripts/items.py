import utils
import requests
from collections import defaultdict
import json

VALID_ITEMS = (
    "30011", "30021", "30031", "30041", "30051", "30061",
    "30012", "30022", "30032", "30042", "30052", "30062",
    "30013", "30023", "30033", "30043", "30053", "30063", "30073", "30083", "30093", "30103", "31013", "31023", "31033", "31043", "31053",
    "30014", "30024", "30034", "30044", "30054", "30064", "30074", "30084", "30094", "30104", "31014", "31024", "31034", "31044", "31054",
    "30115", "30125", "30135", "30145",
    "3301", "3302", "3303",
    "mod_unlock_token", "mod_update_token_1", "mod_update_token_2",
    "3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281",
    "3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282",
    "3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283",
    "4001", "32001",
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

base_data = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json")
            .json()
)

recipes = base_data["manufactFormulas"] | base_data["workshopFormulas"]

item_id_to_recipe_cost = {recipes[id]["itemId"]: recipes[id]["costs"] for id in recipes}

item_data = defaultdict(dict)

for item_id, item_info in cn_items.items():
    if item_id in VALID_ITEMS:
        item_data[item_id] = {
            "itemId": item_info["itemId"],
            "name": en_items.get(item_id, cn_items[item_id])["name"],
            "rarity": item_info["rarity"],
            "sortId": item_info["sortId"],
        }
        if (cost := item_id_to_recipe_cost.get(item_id)):
            item_data[item_id].update({"recipe": utils.format_cost(cost)})

        icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/items/{item_info['iconId']}.png"
        utils.save_image(icon_url, "items", item_id)

with open("./src/lib/data/items.json", "w") as f:
    json.dump(item_data, f)