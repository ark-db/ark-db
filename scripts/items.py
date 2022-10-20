import utils
import requests
import json



EXCLUDED_RECIPES = (
    "3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281",
    "3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282",
)

CN_ITEMS = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json")
            .json()
            ["items"]
)

EN_ITEMS = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/item_table.json")
            .json()
            ["items"]
)

BASE_DATA = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json")
            .json()
)

RECIPES = (
    list(BASE_DATA["manufactFormulas"].values())
    + list(BASE_DATA["workshopFormulas"].values())
)

ITEM_ID_TO_RECIPE_COST = {
    id: recipe["costs"]
    for recipe in RECIPES
    if (id := recipe["itemId"]) not in EXCLUDED_RECIPES
}

all_item_data = dict()

for type, items in utils.VALID_ITEMS.items():
    for id in items:
        item_info = CN_ITEMS[id]
        item_data = {
            "name": EN_ITEMS.get(id, CN_ITEMS[id])["name"],
            "type": type,
            "rarity": item_info["rarity"],
            "sortId": item_info["sortId"]
        }

        if (cost := ITEM_ID_TO_RECIPE_COST.get(id)):
            item_data.update({"recipe": utils.format_cost(cost)})

        icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/items/{item_info['iconId']}.png"
        utils.save_image(icon_url, utils.Asset.ITEM, name=id, warn=True)

        all_item_data.update({id: item_data})

with open("./src/lib/data/items.json", "w") as f:
    json.dump(all_item_data, f)