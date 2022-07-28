import requests
from collections import defaultdict
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

def is_operator(char_info):
    return char_info["profession"] != "TOKEN" \
           and char_info["profession"] != "TRAP" \
           and not char_info["isNotObtainable"]

def format_cost(cost):
    if cost:
        return [{k: v for k, v in mat.items() if k != "type"} for mat in cost]
    return []

for char_id, char_info in chars.items():
    if is_operator(char_info) and char_info["rarity"] > 1:
        for skill in char_info["skills"]:
            skill_ids.add(skill["skillId"])
        module_ids = modules["charEquip"].get(char_id, [])[1:]
        char_data[char_id] = {
            "charId": char_id,
            "name": name_changes.get(char_id, char_info["appellation"]),
            "rarity": char_info["rarity"] + 1,
            "elite": [format_cost(phase["evolveCost"]) + [{"id": "4001", "count": elite_lmd_costs[char_info["rarity"]][i]}]
                      for i, phase in enumerate(char_info["phases"][1:])],
            "skill": [format_cost(level["lvlUpCost"]) for level in char_info["allSkillLvlup"]],
            "mastery": [{"skillId": skill["skillId"], 
                         "costs": [format_cost(mastery["levelUpCost"]) for mastery in skill["levelUpCostCond"]],} 
                         for skill in char_info["skills"]],
            "modules": [{"moduleId": module_id,
                         "type": modules["equipDict"][module_id]["typeIcon"].upper(),
                         "costs": [format_cost(cost) for cost in modules["equipDict"][module_id]["itemCost"].values()],}
                         for module_id in module_ids],
        }

        icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/avatars/{char_id}.png"
        icon_data = requests.get(icon_url).content
        with open(f"./src/lib/images/operators/{char_id}.png", "wb") as f:
            f.write(icon_data)

        for module_id in module_ids:
            module_icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/equip/icon/{module_id}.png"
            module_icon_data = requests.get(module_icon_url).content
            with open(f"./src/lib/images/modules/{module_id}.png", "wb") as f:
                f.write(module_icon_data)

for skill_id in skill_ids:
    skill_icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/skills/skill_icon_{skill_id}.png"
    skill_icon_data = requests.get(skill_icon_url).content
    with open(f"./src/lib/images/skills/{skill_id}.png", "wb") as f:
        f.write(skill_icon_data)

with open("./src/lib/data/operators.json", "w") as f:
    json.dump(char_data, f)