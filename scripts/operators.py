import utils
import requests
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
chars |= patch_chars

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
    "char_1001_amiya2": "Amiya (Guard)",
    "char_4055_bgsnow": "Pozyomka",
}

all_char_data = dict()
skill_ids = set()

def is_operator(char_info):
    return char_info["profession"] != "TOKEN" \
           and char_info["profession"] != "TRAP" \
           and not char_info["isNotObtainable"]

def get_skill_id(skill):
    skill_info = skills[skill["skillId"]]
    return skill_info["iconId"] or skill_info["skillId"]

for char_id, char_info in chars.items():
    if is_operator(char_info) and char_info["rarity"] > 1:
        #all_char_data.update({
        char_data = {
            "charId": char_id, # TODO: check if this is redundant
            "name": name_changes.get(char_id, char_info["appellation"]),
            "rarity": char_info["rarity"] + 1,
            "upgrades": [
                {"data": [
                    {"name": f"Elite {i+1}",
                     "cost": utils.format_cost(phase["evolveCost"])
                             + [{"id": "4001", "count": elite_lmd_costs[char_info["rarity"]][i]}]}
                    for i, phase in enumerate(char_info["phases"][1:])
                ]},
                {"data": [
                    {"name": f"Skill Level {i+2}",
                     "cost": utils.format_cost(level["lvlUpCost"])}
                    for i, level in enumerate(char_info["allSkillLvlup"])
                ]}
            ]
        }

        for i, skill in enumerate(char_info["skills"]):
            skill_id = get_skill_id(skill)

            if skill_id not in skill_ids and char_info["rarity"] > 2:
                skill_ids.add(skill_id)
                icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/skills/skill_icon_{skill_id}.png"
                utils.save_image(icon_url, "skills", skill_id)

            char_data["upgrades"].append({
                "cls": "mastery",
                "skillId": skill_id,
                "data": [
                    {"name": f"Skill {i+1} Mastery {j+1}",
                     "cost": utils.format_cost(mastery["levelUpCost"])}
                    for j, mastery in enumerate(skill["levelUpCostCond"])
                ]
            })

        module_ids = modules["charEquip"].get(char_id, [])[1:]
        for i, module_id in enumerate(module_ids):
            icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/equip/icon/{module_id}.png"
            utils.save_image(icon_url, "modules", module_id)

            module_info = modules["equipDict"][module_id]
            char_data["upgrades"].append({
                "cls": "module",
                "moduleId": module_info["uniEquipId"],
                "data": [
                    {"name": f"{module_info['typeIcon'].upper()} Stage {i+1}",
                     "cost": utils.format_cost(cost)}
                    for i, cost in enumerate(module_info["itemCost"].values())
                ]
            })

        icon_url = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/avatars/{char_id}.png"
        utils.save_image(icon_url, "operators", char_id)

        all_char_data.update({char_id: char_data})

with open("./src/lib/data/operators.json", "w") as f:
    json.dump(all_char_data, f)