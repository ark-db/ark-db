import utils
import requests
import json



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

item_id_to_recipe_cost = {id: recipe["costs"]
                          for recipe in recipes if (id := recipe["itemId"]) not in EXCLUDED_RECIPES}

all_item_data = dict()

for type, items in utils.VALID_ITEMS.items():
    for id in items:
        item_info = cn_items[id]
        item_data = {
            "name": en_items.get(id, cn_items[id])["name"],
            "type": type,
            "rarity": item_info["rarity"],
            "sortId": item_info["sortId"]
        }

        if (cost := item_id_to_recipe_cost.get(id)):
            item_data.update({"recipe": utils.format_cost(cost)})

        icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/items/{item_info['iconId']}.png"
        utils.save_image(icon_url, category="items", image_id=id)

        all_item_data.update({id: item_data})

with open("./src/lib/data/items.json", "w") as f:
    json.dump(all_item_data, f)