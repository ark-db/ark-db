import utils
import requests
from collections import defaultdict
import json

VALID_ITEMS = {
    "material": ["30011", "30021", "30031", "30041", "30051", "30061",
                 "30012", "30022", "30032", "30042", "30052", "30062",
                 "30013", "30023", "30033", "30043", "30053", "30063", "30073", "30083", "30093", "30103", "31013", "31023", "31033", "31043", "31053",
                 "30014", "30024", "30034", "30044", "30054", "30064", "30074", "30084", "30094", "30104", "31014", "31024", "31034", "31044", "31054",
                 "30115", "30125", "30135", "30145"],
    "skill": ["3301", "3302", "3303"],
    "module": ["mod_unlock_token", "mod_update_token_1", "mod_update_token_2"],
    "chip": ["3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281",
             "3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282",
             "3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283",
             "32001"],
    "misc": ["4001"],
}

EXCLUDED_RECIPES = (
    "3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281",
    "3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282",
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

recipes = list(base_data["manufactFormulas"].values()) + list(base_data["workshopFormulas"].values())

item_id_to_recipe_cost = {id: recipe["costs"] for recipe in recipes if (id := recipe["itemId"]) not in EXCLUDED_RECIPES}

all_item_data = defaultdict(dict)

for type, items in VALID_ITEMS.items():
    for id in items:
        data = cn_items[id]
        all_item_data[id] = {
            "itemId": data["itemId"],
            "name": en_items.get(id, cn_items[id])["name"],
            "type": type,
            "rarity": data["rarity"],
            "sortId": data["sortId"],
        }
        if (cost := item_id_to_recipe_cost.get(id)):
            all_item_data[id].update({"recipe": utils.format_cost(cost)})

        icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/items/{data['iconId']}.png"
        utils.save_image(icon_url, "items", id)

with open("./src/lib/data/items.json", "w") as f:
    json.dump(all_item_data, f)