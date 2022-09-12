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



def is_operator(char_info: dict[str, str|list]):
    return char_info["profession"] != "TOKEN" \
           and char_info["profession"] != "TRAP" \
           and not char_info["isNotObtainable"]

def get_skill_id(skill: str) -> str:
    skill_info = skills[skill["skillId"]]
    return skill_info["iconId"] or skill_info["skillId"]



name_changes = {
    "char_118_yuki": "Shirayuki",
    "char_196_sunbr": "Gummy",
    "char_115_headbr": "Zima",
    "char_195_glassb": "Istina",
    "char_197_poca": "Rosa",
    "char_1001_amiya2": "Amiya (Guard)",
    "char_4055_bgsnow": "Pozyomka",
    "char_4064_mlynar": "Mlynar",
}

all_char_data = dict()
skill_ids = set()



for char_id, char_info in chars.items():
    if is_operator(char_info) and char_info["rarity"] > 1:
        char_data = {
            "charId": char_id,
            "name": name_changes.get(char_id, char_info["appellation"]),
            "rarity": char_info["rarity"] + 1,
            "upgrades": [],
            "costs": dict()
        }

        upgrade_names = []
        for i, phase in enumerate(char_info["phases"][1:], start=1):
            name = f"Elite {i}"
            upgrade_names.append(name)
            char_data["costs"].update({
                name: utils.format_cost(phase["evolveCost"])
                      + [{"id": "4001", "count": elite_lmd_costs[char_info["rarity"]][i-1]}]
            })
        char_data["upgrades"].append({
            "names": upgrade_names
        })



        upgrade_names = []
        for i, level in enumerate(char_info["allSkillLvlup"], start=2):
            name = f"Skill Level {i}"
            upgrade_names.append(name)
            char_data["costs"].update({
                name: utils.format_cost(level["lvlUpCost"])
            })
        char_data["upgrades"].append({
            "names": upgrade_names
        })



        if len(char_info["skills"]) > 1:
            for i, skill in enumerate(char_info["skills"], start=1):
                upgrade_names = []
    
                skill_id = get_skill_id(skill)
                if skill_id not in skill_ids and char_info["rarity"] > 2:
                    skill_ids.add(skill_id)
                    icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/skills/skill_icon_{skill_id}.png"
                    utils.save_image(icon_url, "skills", skill_id)
    
                for j, mastery in enumerate(skill["levelUpCostCond"], start=1):
                    name = f"Skill {i} Mastery {j}"
                    upgrade_names.append(name)
                    char_data["costs"].update({
                        name: utils.format_cost(mastery["levelUpCost"])
                    })
                char_data["upgrades"].append({
                    "cls": "mastery",
                    "skillId": skill_id,
                    "names": upgrade_names
                })



        module_ids = modules["charEquip"].get(char_id, [])[1:]
        for module_id in module_ids:
            upgrade_names = []

            icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/equip/icon/{module_id}.png"
            utils.save_image(icon_url, "modules", module_id)

            module_info = modules["equipDict"][module_id]
            for i, cost in enumerate(module_info["itemCost"].values(), start=1):
                name = f"{module_info['typeIcon'].upper()} Stage {i}"
                upgrade_names.append(name)
                char_data["costs"].update({
                    name: utils.format_cost(cost)
                })
            char_data["upgrades"].append({
                "cls": "module",
                "moduleId": module_info["uniEquipId"],
                "names": upgrade_names
            })



        icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/avatars/{char_id}.png"
        utils.save_image(icon_url, "operators", char_id)

        all_char_data.update({char_id: char_data})

with open("./src/lib/data/operators.json", "w") as f:
    json.dump(all_char_data, f)