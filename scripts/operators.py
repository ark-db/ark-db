import utils
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import quote

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

def get_prts_image_src(soup: BeautifulSoup, search_text: str):
    img_url = soup.select_one(f"img[alt*='{search_text}']")["data-src"]
    return f"https://prts.wiki{img_url}"



char_soup = BeautifulSoup(requests.get("https://prts.wiki/w/%E5%88%86%E6%94%AF%E4%B8%80%E8%A7%88")
                                  .text,
                          "lxml")

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

existing_char_data = dict()



with open("./src/lib/data/operators.json", "r+") as f:
    existing_char_data = json.load(f)
    existing_char_ids = set(existing_char_data.keys())
    for char_id, char_info in chars.items():
        if char_id not in existing_char_ids and is_operator(char_info) and char_info["rarity"] > 1:
            soup = BeautifulSoup(requests.get(f"https://prts.wiki/w/{quote(char_info['name'])}")
                                         .text,
                                 "lxml")

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
                    if  char_info["rarity"] > 2:
                        icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/skills/skill_icon_{skill_id}.png"
                        if not utils.save_image(icon_url, "skills", skill_id):
                            skill_name = skills[skill_id]["levels"][0]["name"]
                            icon_url = get_prts_image_src(soup, skill_name)
                            if not utils.save_image(icon_url, "skills", skill_id):
                                raise RuntimeError(f"Could not save image of skill with ID \"{skill_id}\"")

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
                module_info = modules["equipDict"][module_id]
                upgrade_names = []

                icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/equip/icon/{module_id}.png"
                if not utils.save_image(icon_url, "modules", module_id):
                    module_name = module_info["uniEquipName"]
                    icon_url = get_prts_image_src(soup, module_name)
                    if not utils.save_image(icon_url, "modules", module_id):
                        raise RuntimeError(f"Could not save image of module with ID \"{skill_id}\"")

                
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
            if not utils.save_image(icon_url, "operators", char_id):
                icon_url = get_prts_image_src(char_soup, char_info["name"])
                if not utils.save_image(icon_url, "operators", char_id):
                    raise RuntimeError(f"Could not save image of operator with ID \"{char_id}\"")

            existing_char_data.update({char_id: char_data})



with open("./src/lib/data/operators.json", "w") as f:
    json.dump(existing_char_data, f)

print("Successfully updated operator data")