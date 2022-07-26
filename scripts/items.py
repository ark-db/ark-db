import requests
from collections import defaultdict, Counter
from itertools import chain
import pprint

VALID_ITEMS = {
    "t1": ["30011", "30021", "30031", "30041", "30051", "30061"],
    "t2": ["30012", "30022", "30032", "30042", "30052", "30062"],
    "t3": ["30013", "30023", "30033", "30043", "30053", "30063", "30073", "30083", "30093", "30103", "31013", "31023", "31033", "31043", "31053"],
    "t4": ["30014", "30024", "30034", "30044", "30054", "30064", "30074", "30084", "30094", "30104", "31014", "31024", "31034", "31044", "31054"],
    "t5": ["30115", "30125", "30135", "30145"],
    "skill": ["3301", "3302", "3303"],
    "module": ["mod_unlock_token", "mod_update_token_1", "mod_update_token_2"],
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

item_data = defaultdict(dict)

def get_item_name(item_id):
    item = en_items.get(item_id, cn_items[item_id])
    return item["name"]

for item, data in cn_items.items():
    if item in chain.from_iterable(VALID_ITEMS.values()):
        item_data[item] = {"itemId": data["itemId"],
                           "name": get_item_name(item),
                           "rarity": data["rarity"],
                           "iconId": data["iconId"],
                           "sortId": data["sortId"]}


item_id_to_recipe_cost = {recipes[recipe_id]["itemId"]: recipes[recipe_id]["costs"] for recipe_id in recipes}

recipe_data = defaultdict(list)

for item_id in VALID_ITEMS["t4"]:
    recipe = item_id_to_recipe_cost[item_id]
    for mat in recipe:
        recipe_data[item_id].append({"id": mat["id"], "count": mat["count"]})

for item_id in VALID_ITEMS["t5"]:
    recipe = item_id_to_recipe_cost[item_id]
    costs = Counter()
    for mat in recipe:
        for submat in recipe_data[mat["id"]]:
            costs.update({submat["id"]: submat["count"]*mat["count"]})

    recipe_data[item_id] = [{"id": k, "count": v} for k, v in dict(costs).items()]



for item in item_data:
    item_data[item].update({"asT3": recipe_data.get(item, [])})

pprint.pprint(item_data)