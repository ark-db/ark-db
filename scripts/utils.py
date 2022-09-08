from pathlib import Path
import requests
from PIL import Image
from io import BytesIO

Cost = list[dict[str, str|int] | None]

VALID_ITEMS = {
    "material": {
        "30011", "30021", "30031", "30041", "30051", "30061",
        "30012", "30022", "30032", "30042", "30052", "30062",
        "30013", "30023", "30033", "30043", "30053", "30063", "30073", "30083", "30093", "30103", "31013", "31023", "31033", "31043", "31053",
        "30014", "30024", "30034", "30044", "30054", "30064", "30074", "30084", "30094", "30104", "31014", "31024", "31034", "31044", "31054",
        "30115", "30125", "30135", "30145"
    },
    "skill": {
        "3301", "3302", "3303"
    },
    "module": {
        "mod_unlock_token", "mod_update_token_1", "mod_update_token_2"
    },
    "chip": {
        "3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281",
        "3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282",
        "3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283",
        "32001"
    },
    "misc": {
        "4001", # LMD
        "2001", "2002", "2003", "2004", # EXP card
        "3112", "3113", "3114", # carbon
        "3003" # pure gold
    },
    "other": {
        "4005", "4004", "REP_COIN", "EPGS_COIN", # green, yellow, intell. cert.; param. model
        "4003", "7003", "7004", # orundum; 1x, 10x headhunting permit
        "7001", "7002", # rec. permit; expedited plan
        "voucher_recruitR3_1", "voucher_recruitR4_1", # 3*, 4* rec. vouchers
        "3401", # furniture part
    }
}

def format_cost(cost: Cost) -> Cost:
    if cost:
        return [{k: v for k, v in mat.items() if k != "type"} for mat in cost]
    return []

def save_image(url: str, category: str, image_id: str, overwrite=False):
    target_path = Path(f"./static/images/{category}/{image_id}.webp")
    if target_path.is_file() and not overwrite:
        pass
    elif (res := requests.get(url)):
        Image.open(BytesIO(res.content)) \
             .convert("RGBA") \
             .save(target_path, "webp")
    else:
        raise RuntimeError(f"Image \"{image_id}\" of type \"{category}\" could not be retrieved")
        #print(f"{category}: {image_id}")