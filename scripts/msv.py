import utils
import requests
import pandas as pd
from collections import defaultdict
from enum import Enum
import numpy as np
from scipy.optimize import linprog

MIN_RUN_THRESHOLD = 100
ALLOWED_ITEMS = utils.VALID_ITEMS["material"] + utils.VALID_ITEMS["misc"]
BYPRODUCT_RATE_BONUS = 1.8
# EXP_DEVALUE_FACTOR = 0.8

recipes = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json")
            .json()
            ["workshopFormulas"]
            .values()
)

drops = (
    requests.get("https://penguin-stats.io/PenguinStats/api/v2/result/matrix?show_closed_zones=true")
            .json()
            ["matrix"]
)

stages = (
    requests.get("https://penguin-stats.io/PenguinStats/api/v2/stages")
            .json()
)



class Region(Enum):
    GLOBAL = "US"
    CN = "CN"

def update_material_relations(df: pd.DataFrame) -> pd.DataFrame:
    # relationships between exp cards + pure gold; base unit is Drill Battle Record (200 exp)
    MAT_RELATIONS = {
        "2002": 2,
        "2003": 5,
        "2004": 10,
        "3003": 2, # value of pure gold = value of exp produced in factory for the same duration as 1 pure gold
    }
    for item_id, count in MAT_RELATIONS.items():
        df.at[(item_id, 1), "2001"] = count
    return df

def fill_diagonal(df: pd.DataFrame) -> pd.DataFrame:
    for item_id, count in zip(df.index.get_level_values("itemId"), df.index.get_level_values("count")):
        df.at[item_id, item_id] = count
    return df

def is_valid_stage(stage_id: str) -> bool:
    return stage_id.startswith(("main", "tough", "sub", "wk")) or stage_id.endswith("perm")

def get_stage_ids(region: Region) -> set[str]:
    current_drops = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )
    current_stage_ids = set(item["stageId"] for item in current_drops if is_valid_stage(item["stageId"]))
    return current_stage_ids

def update_lmd_stages(df: pd.DataFrame, valid_stages: set) -> pd.DataFrame:
    LMD_STAGES = {
        "wk_melee_1": 1700,
        "wk_melee_2": 2800,
        "wk_melee_3": 4100,
        "wk_melee_4": 5700,
        "wk_melee_5": 7500,
        "wk_melee_6": 10000,
        "main_01-01": 660,
        "main_02-07": 1500,
        "sub_02-02": 1020,
        "main_03-06": 2040,
        "main_04-01": 2700,
        "sub_04-2-3": 3480,
        "sub_05-1-2": 2700,
        "sub_05-2-1": 1216,
        "main_06-01": 1216,
        "sub_06-2-2": 2700,
        "sub_07-1-1": 2700,
        "sub_07-1-2": 1216,
        "main_08-01": 2700,
        "main_08-04": 1216,
        "main_09-01": 2700,
        "main_10-07": 3480,
        "tough_10-07": 3480,
    }
    for stage_id, lmd in LMD_STAGES.items():
        if stage_id in valid_stages:
            df.at[stage_id, "lmd"] = lmd
    return df



drop_data = (
    pd.DataFrame(data=drops,
                 columns=["stageId", "itemId", "times", "quantity"])
      .query("times >= @MIN_RUN_THRESHOLD \
              and itemId in @ALLOWED_ITEMS")
      .assign(drop_rate = lambda df: df["quantity"] / df["times"])
      .pivot(index="stageId",
             columns="itemId",
             values="drop_rate")
)



stage_data = (
    pd.DataFrame(data=stages,
                 columns=["stageId", "code", "apCost"])
      .set_index("stageId")
)

for stage in stages:
    if (not stage.get("dropInfos")) or stage["stageId"] == "recruit":
        stage.update({"dropInfos": []})

main_drops = (
    pd.json_normalize(data=stages,
                      record_path="dropInfos",
                      meta="stageId")
      .pipe(lambda df: df[df["dropType"] == "NORMAL_DROP"])
      .filter(["stageId", "itemId"])
      .pipe(lambda df: df[~df["itemId"].isna()])
)

main_drops_by_stage = defaultdict(list)

for entry in main_drops.itertuples(index=False):
    main_drops_by_stage[entry.stageId].append(entry.itemId)



recipe_matrix = (
    pd.json_normalize(data=recipes,
                      record_path="costs",
                      meta=["itemId", "count", "goldCost"],
                      record_prefix="ing_")
      .pipe(lambda df: df[df["itemId"].isin(ALLOWED_ITEMS)])
      .pivot(index=["itemId", "count", "goldCost"],
             columns="ing_id",
             values="ing_count")
      .reset_index("goldCost")
      .rename(columns={"goldCost": "4001"})
      .reindex(columns=ALLOWED_ITEMS)
      .pipe(update_material_relations)
      .pipe(lambda df: -df)
      .pipe(fill_diagonal)
)

byproduct_value_matrix = (
    pd.json_normalize(data=recipes,
                      record_path="extraOutcomeGroup",
                      meta=["itemId", "extraOutcomeRate"],
                      record_prefix="bp_")
      .pipe(lambda df: df[df["itemId"].isin(ALLOWED_ITEMS)])
      .assign(total_bp_weight = lambda df: df.groupby("itemId")
                                             ["bp_weight"]
                                             .transform("sum"))
      .assign(bp_sanity_coeff = lambda df: BYPRODUCT_RATE_BONUS *
                                           df["extraOutcomeRate"] *
                                           df["bp_weight"] /
                                           df["total_bp_weight"])
      .pivot(index="itemId",
             columns="bp_itemId",
             values="bp_sanity_coeff")
      .reindex(index=recipe_matrix.index.get_level_values("itemId"),
               columns=ALLOWED_ITEMS)
)

item_equiv_matrix = recipe_matrix.to_numpy(na_value=0) + byproduct_value_matrix.to_numpy(na_value=0)
num_rows, _ = item_equiv_matrix.shape



# TODO: iterate through regions

valid_stage_ids = get_stage_ids(Region.GLOBAL)

curr_drop_data = (
    drop_data.pipe(lambda df: df[df.index.isin(valid_stage_ids)])
             .assign(lmd = stage_data["apCost"] * 12)
             .pipe(update_lmd_stages, valid_stage_ids)
             .rename(columns={"lmd": "4001"})
             .reindex(columns=ALLOWED_ITEMS)
             .fillna(0)
)

sanity_cost_vec = (
    stage_data["apCost"]
              .reindex(curr_drop_data.index)
              .to_numpy()
              .flatten()
)

drop_matrix = curr_drop_data.to_numpy()

sanity_values = (
    linprog(-drop_matrix.sum(axis=0),
            drop_matrix,
            sanity_cost_vec,
            item_equiv_matrix,
            np.zeros(num_rows))
    .x
)

stage_effics = (drop_matrix.dot(sanity_values) - sanity_cost_vec) / sanity_cost_vec + 1

farming_stages = (
    pd.DataFrame(data=stage_effics,
                 columns=["effic"])
      .set_index(curr_drop_data.index)
      .merge(stage_data, on="stageId")
      .reset_index()
)

farming_stages_by_item = defaultdict(list)

for stage in farming_stages.itertuples(index=False):
    for main_drop in main_drops_by_stage[stage.stageId]:
        drop_rate = curr_drop_data.at[stage.stageId, main_drop]
        if drop_rate > 0:
            farming_stages_by_item[main_drop].append({
                "stage": stage.code,
                "effic": round(stage.effic, 3),
                "rate": round(drop_rate, 3),
                "espd": round(stage.apCost / drop_rate, 2)
            })