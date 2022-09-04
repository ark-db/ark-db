import utils
import requests
from enum import Enum
import pandas as pd
from collections import defaultdict
from scipy.optimize import linprog
import numpy as np
import json

MIN_RUN_THRESHOLD = 100
ALLOWED_ITEMS = utils.VALID_ITEMS["material"] | utils.VALID_ITEMS["misc"]
BYPROD_RATE_BONUS = 1.8
# EXP_DEVALUE_FACTOR = 0.8
RECORDED_ITEMS = utils.VALID_ITEMS["material"]

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
    GLB = "US"
    CN = "CN"

def update_mat_relations(df: pd.DataFrame) -> pd.DataFrame:
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
    # adds recipes' outcome quantities to the recipe matrix
    for item_id, count in zip(df.index.get_level_values("itemId"), df.index.get_level_values("count")):
        df.at[item_id, item_id] = count
    return df

def get_stage_ids(region: Region) -> set[str]:
    current_drops = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )
    current_stage_ids = set(
        # GT (a001) and OF (a003) event stage IDs don't start with "act"
        item["stageId"] for item in current_drops if item["stageId"].startswith(("main", "sub", "wk", "act", "a001", "a003"))
    )
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
        "main_10-07": 3480, # same as tough_10-07
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
      .fillna(0)
      # below: combine "tough" and "normal" stage drop data (for ch.10+)
      .assign(norm_id = lambda df: df.index.str.replace("tough", "main"))
      .groupby("norm_id")
      .mean()
      .rename_axis("stageId")
)

stage_data = (
    pd.DataFrame(data=stages,
                 columns=["stageId", "code", "apCost"])
      .set_index("stageId")
)

# handle entries for non-stages and things without drop info
for stage in stages:
    if (not stage.get("dropInfos")) or stage["stageId"] == "recruit":
        stage.update({"dropInfos": []})

main_drops = (
    pd.json_normalize(data=stages,
                      record_path="dropInfos",
                      meta="stageId")
      .pipe(lambda df: df[df["dropType"] == "NORMAL_DROP"]) # NORMAL_DROP = main drop of a stage
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
                      record_prefix="ingred_")
      .pipe(lambda df: df[df["itemId"].isin(ALLOWED_ITEMS)])
      .pivot(index=["itemId", "count", "goldCost"],
             columns="ingred_id",
             values="ingred_count")
      .reset_index("goldCost")
      .rename(columns={"goldCost": "4001"})
      .reindex(columns=ALLOWED_ITEMS)
      .pipe(update_mat_relations)
      .pipe(lambda df: -df)
      .pipe(fill_diagonal)
)

byprod_value_matrix = (
    pd.json_normalize(data=recipes,
                      record_path="extraOutcomeGroup",
                      meta=["itemId", "extraOutcomeRate"],
                      record_prefix="byprod_")
      .pipe(lambda df: df[df["itemId"].isin(ALLOWED_ITEMS)])
      .assign(total_weight = lambda df: df.groupby("itemId")
                                          ["byprod_weight"]
                                          .transform("sum"))
      .assign(byprod_value = lambda df: BYPROD_RATE_BONUS *
                                        df["extraOutcomeRate"] *
                                        df["byprod_weight"] /
                                        df["total_weight"])
      .pivot(index="itemId",
             columns="byprod_itemId",
             values="byprod_value")
      .reindex(index=recipe_matrix.index.get_level_values("itemId"),
               columns=ALLOWED_ITEMS)
)

item_rel_matrix = recipe_matrix.to_numpy(na_value=0) + byprod_value_matrix.to_numpy(na_value=0)
num_rows, _ = item_rel_matrix.shape



all_sanity_values = dict()
all_farming_stages = dict()

for region in Region:
    valid_stage_ids = get_stage_ids(region)

    curr_drop_data = (
        drop_data.pipe(lambda df: df[df.index.isin(valid_stage_ids)])
                 .assign(lmd = stage_data["apCost"] * 12) # implicit reindexing of stage_data
                 .pipe(update_lmd_stages, valid_stage_ids)
                 .rename(columns={"lmd": "4001"})
                 .reindex(columns=ALLOWED_ITEMS)
    )

    sanity_cost_vec = (
        stage_data["apCost"]
                  .reindex(curr_drop_data.index)
                  .to_numpy()
                  .flatten()
    )

    drop_matrix = curr_drop_data.to_numpy(na_value=0)

    sanity_values = (
        linprog(-drop_matrix.sum(axis=0),
                drop_matrix,
                sanity_cost_vec,
                item_rel_matrix,
                np.zeros(num_rows))
        .x
    )

    all_sanity_values.update({
        region.name.lower(): {
            item_id: sanity_value for item_id, sanity_value in zip(ALLOWED_ITEMS, sanity_values)
        }
    })

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
            if main_drop in RECORDED_ITEMS and (drop_rate := curr_drop_data.at[stage.stageId, main_drop]) > 0:
                farming_stages_by_item[main_drop].append({
                    "stage": stage.code,
                    "effic": round(stage.effic, 3),
                    "rate": round(drop_rate, 3),
                    "espd": round(stage.apCost / drop_rate, 2)
                })

    all_farming_stages.update({
        region.name.lower(): [
            {"id": item, "stages": stages} 
            for item, stages in farming_stages_by_item.items()
        ]
    })

with open("./scripts/msv.json", "w") as f:
    json.dump(all_sanity_values, f)

with open("./src/lib/data/farming.json", "w") as f:
    json.dump(all_farming_stages, f)