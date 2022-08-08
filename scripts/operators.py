import requests
from collections import defaultdict
from PIL import Image
from io import BytesIO
import json

chars = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json")
            .json()
)

patch_chars = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/char_patch_table.json")
            .json()
            ["patchChars"]
)

skills = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/skill_table.json")
            .json()
)

modules = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/uniequip_table.json")
            .json()
)

elite_lmd_costs = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/gamedata_const.json")
            .json()
            ["evolveGoldCost"]
)

name_changes = {
    "char_118_yuki": "Shirayuki",
    "char_196_sunbr": "Gummy",
    "char_115_headbr": "Zima",
    "char_195_glassb": "Istina",
    "char_197_poca": "Rosa",
    "char_1001_amiya2": "Amiya (Guard)"
}

chars.update(patch_chars)

char_data = defaultdict(dict)
skill_ids = set()
bad_ids = []

def is_operator(char_info):
    return char_info["profession"] != "TOKEN" \
           and char_info["profession"] != "TRAP" \
           and not char_info["isNotObtainable"]

def format_cost(cost):
    if cost:
        return [{k: v for k, v in mat.items() if k != "type"} for mat in cost]
    return []

def get_skill_id(skill):
    skill_info = skills[skill["skillId"]]
    return skill_info["iconId"] or skill_info["skillId"]

def save_image(url, type, id):
    if (res := requests.get(url)): # check if 4xx/5xx error 
        Image.open(BytesIO(res.content)) \
             .convert("RGBA") \
             .save(f"./src/lib/images/{type}/{id}.webp", "webp")
    else: # currently applies to uniequip_002_mm & uniequip_003_mgllan
        bad_ids.append(f"{type}: {id}")

for char_id, char_info in chars.items():
    if is_operator(char_info) and char_info["rarity"] > 1:
        char_data[char_id] = {
            "charId": char_id,
            "name": name_changes.get(char_id, char_info["appellation"]),
            "rarity": char_info["rarity"] + 1,
            "upgrades": [
                {"data": [{"name": f"Elite {i+1}",
                           "cost": format_cost(phase["evolveCost"])
                                   + [{"id": "4001", "count": elite_lmd_costs[char_info["rarity"]][i]}]}
                          for i, phase in enumerate(char_info["phases"][1:])]},
                {"data": [{"name": f"Skill Level {i+2}",
                           "cost": format_cost(level["lvlUpCost"])}
                          for i, level in enumerate(char_info["allSkillLvlup"])]}
            ]
        }

        for i, skill in enumerate(char_info["skills"]):
            if char_info["rarity"] > 2:
                skill_ids.add(get_skill_id(skill))
            char_data[char_id]["upgrades"].append(
                {"cls": f"mastery",
                 "skillId": get_skill_id(skill),
                 "data":[{"name": f"Skill {i+1} Mastery {j+1}",
                          "cost": format_cost(mastery["levelUpCost"])}
                         for j, mastery in enumerate(skill["levelUpCostCond"])]
                })


        module_ids = modules["charEquip"].get(char_id, [])[1:]
        for i, module_id in enumerate(module_ids):
            module_info = modules['equipDict'][module_id]
            char_data[char_id]["upgrades"].append(
                {"cls": f"module",
                 "moduleId": module_info["uniEquipId"],
                 "data": [{"name": f"{module_info['typeIcon'].upper()} Stage {i+1}",
                           "cost": format_cost(cost)}
                          for i, cost in enumerate(module_info["itemCost"].values())]
                })

        icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/avatars/{char_id}.png"
        save_image(icon_url, "operators", char_id)

        for module_id in module_ids:
            icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/equip/icon/{module_id}.png"
            save_image(icon_url, "modules", module_id)

for skill_id in skill_ids:
    icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/skills/skill_icon_{skill_id}.png"
    save_image(icon_url, "skills", skill_id)

with open("./scripts/errors.txt", "w") as f:
    for id in bad_ids:
        f.write(f"{id}\n")

with open("./src/lib/data/operators.json", "w") as f:
    json.dump(char_data, f)