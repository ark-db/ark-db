import requests
from collections import defaultdict, Counter
from itertools import chain
from PIL import Image
from io import BytesIO
import json

VALID_ITEMS = {
    "t1": ["30011", "30021", "30031", "30041", "30051", "30061"],
    "t2": ["30012", "30022", "30032", "30042", "30052", "30062"],
    "t3": ["30013", "30023", "30033", "30043", "30053", "30063", "30073", "30083", "30093", "30103", "31013", "31023", "31033", "31043", "31053"],
    "t4": ["30014", "30024", "30034", "30044", "30054", "30064", "30074", "30084", "30094", "30104", "31014", "31024", "31034", "31044", "31054"],
    "t5": ["30115", "30125", "30135", "30145"],
    "skill": ["3301", "3302", "3303"],
    "module": ["mod_unlock_token", "mod_update_token_1", "mod_update_token_2"],
    "chip": ["3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281"],
    "chippack": ["3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282"],
    "dualchip": ["3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283"],
    "currency": ["4001"],
}

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

recipes = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json")
            .json()
            ["workshopFormulas"]
)

item_id_to_recipe_cost = {recipes[recipe_id]["itemId"]: recipes[recipe_id]["costs"] for recipe_id in recipes}

item_data = defaultdict(dict)

for item_id, item_info in cn_items.items():
    if item_id in chain.from_iterable(VALID_ITEMS.values()):
        item_data[item_id] = {
            "itemId": item_info["itemId"],
            "name": en_items.get(item_id, cn_items[item_id])["name"],
            "rarity": item_info["rarity"],
            "sortId": item_info["sortId"],
        }  

        icon_data = (
            requests.get(f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/items/{item_info['iconId']}.png")
                    .content
        )
        Image.open(BytesIO(icon_data)) \
             .convert("RGBA") \
             .save(f"./src/lib/images/items/{item_id}.webp", "webp")

composition_data = defaultdict(list)

for item_id in VALID_ITEMS["t3"]:
    composition_data[item_id].append({"id": item_id, "count": 1})

for item_id in VALID_ITEMS["t4"]:
    recipe = item_id_to_recipe_cost[item_id]
    for mat in recipe:
        composition_data[item_id].append({"id": mat["id"], "count": mat["count"]})

for item_id in VALID_ITEMS["t5"]:
    recipe = item_id_to_recipe_cost[item_id]
    costs = Counter()
    for mat in recipe:
        for submat in composition_data[mat["id"]]:
            costs.update({submat["id"]: submat["count"]*mat["count"]})
    composition_data[item_id] = [{"id": k, "count": v} for k, v in costs.items()]

for item_id, item_info in item_data.items():
    if (mats := composition_data.get(item_id)):
        item_info.update({"asT3": mats})

with open("./src/lib/data/items.json", "w") as f:
    json.dump(item_data, f)