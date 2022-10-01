import utils
import requests
from enum import Enum
import pandas as pd
from collections import defaultdict
from scipy.optimize import linprog
from numpy import zeros
import json



MIN_RUN_THRESHOLD = 100

ALLOWED_ITEMS = utils.VALID_ITEMS["material"] | utils.VALID_ITEMS["skill"] | utils.VALID_ITEMS["misc"]

BYPROD_RATE_BONUS = 1.8

# hardcoded sanity values for some materials that don't drop in story stages
# -1 in data represents unvalued item
MISC_SANITY_VALUES = {
    "4003": -1,
    "7003": -1,
    "7004": -1,
    "7001": -1,
    "7002": 0,
    "3401": 0,
    "32001": -1,
    "mod_unlock_token": -1,
    "mod_update_token_1": -1,
    "mod_update_token_2": -1,
}

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

def update_mat_relations(df: pd.DataFrame):
    '''
    Ties values of EXP cards and Pure Gold together.
    The base unit is the Drill Battle Record (worth 200 EXP).
    Value of Pure Gold = value of EXP that can be produced in the same amount of time as 1 Pure Gold
    '''
    MAT_RELATIONS = {
        "2002": 2,
        "2003": 5,
        "2004": 10,
        "3003": 2,
    }

    for item_id, count in MAT_RELATIONS.items():
        df.at[(item_id, 1), "2001"] = count

    return df

def fill_diagonal(df: pd.DataFrame):
    '''
    Adds recipes' yield quantities to the recipe matrix.
    Sort of like manipulating elements of the main diagonal of a square matrix
    '''
    product_ids = df.index.get_level_values("itemId")
    recipe_yields = df.index.get_level_values("count")

    for item_id, count in zip(product_ids, recipe_yields):
        df.at[item_id, item_id] = count

    return df

def get_stage_ids(region: Region) -> set[str]:
    current_drops = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )

    current_stage_ids = set(
        item["stageId"] for item in current_drops
        # GT (a001) and OF (a003) event stage IDs don't start with "act"
        if item["stageId"].startswith(("main", "sub", "wk", "act", "a001", "a003"))
    )

    return current_stage_ids

def update_lmd_stages(df: pd.DataFrame, valid_stages: set[str]):
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

def calc_drop_stats(stage: tuple, drop_rate: float) -> dict[str, str|float]:
    return {
        "stage": stage.code,
        "effic": round(stage.effic, 3),
        "rate": round(drop_rate, 3),
        "espd": round(stage.apCost / drop_rate, 2)
    }



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
      # combine drop data from "tough" and "normal" stage difficulties (for ch.10+)
      .assign(norm_id = lambda df: df.index.str.replace("tough", "main"))
      .groupby("norm_id")
      .mean()
      .rename_axis("stageId")
)

stage_data = (
    pd.DataFrame(data=stages,
                 columns=["stageId", "code", "apCost", "stageType"])
      .set_index("stageId")
)

# handle entries that aren't stages or don't have drop info so that they can be
# processed by json_normalize() without throwing an error
for stage in stages:
    if (not stage.get("dropInfos")) or stage["stageId"] == "recruit":
        stage.update({"dropInfos": []})

main_drops = (
    pd.json_normalize(data=stages,
                      record_path="dropInfos",
                      meta="stageId")
      # "NORMAL_DROP" = main drop of a stage
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
                                          .transform("sum"),
              byprod_value = lambda df: BYPROD_RATE_BONUS *
                                        df["extraOutcomeRate"] *
                                        df["byprod_weight"] /
                                        df["total_weight"])
      .pivot(index="itemId",
             columns="byprod_itemId",
             values="byprod_value")
      .reindex(index=recipe_matrix.index.get_level_values("itemId"),
               columns=ALLOWED_ITEMS)
)

# Each row of this matrix describes a relationship between an item's value
# and other items' values. The relationships are derived from workshop recipes.
# value of item = value of ingredients + (LMD cost * value of LMD) - (byproduct rate * weighted avg. of byproduct values)
# V(item) - Σ V(ing) - n_lmd * V(lmd) + R * avg(byp) = 0
# In the linear programming problem, A_eq = this matrix; b_eq = vector of 0s
item_rel_matrix = recipe_matrix.to_numpy(na_value=0) \
                  + byprod_value_matrix.to_numpy(na_value=0)



all_sanity_values = dict()
all_farming_stages = dict()

for region in Region:
    valid_stage_ids = get_stage_ids(region)

    curr_drop_data = (
        drop_data.pipe(lambda df: df[df.index.isin(valid_stage_ids)])
                 .assign(lmd = stage_data["apCost"] * 12)
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

    # The assumption behind Moe's calculations is that the "sanity return"
    # of a stage cannot be greater than the sanity cost. So, the vector of all
    # stage sanity costs is b_ub.
    # sanity return = item drop rates @ item sanity values, so drop_matrix is A_ub.
    # The goal is to maximize the total sanity return of all stages. Therefore,
    # the objective function (c) to maximize is the column-wise sum of drop_matrix.
    # linprog() minimizes, so the additive inverse is used instead.
    sanity_values = (
        linprog(-drop_matrix.sum(axis=0),
                drop_matrix,
                sanity_cost_vec,
                item_rel_matrix,
                zeros(item_rel_matrix.shape[0]))
        .x
    )

    all_sanity_values.update({
        region.name.lower(): {
            item: value for item, value in zip(ALLOWED_ITEMS, sanity_values)
        } | MISC_SANITY_VALUES
    })

    stage_effics = drop_matrix @ sanity_values / sanity_cost_vec

    farming_stages = (
        pd.DataFrame(data=stage_effics,
                     columns=["effic"])
          .set_index(curr_drop_data.index)
          .merge(stage_data, on="stageId")
          .reset_index()
    )

    farming_stages_by_item = defaultdict(list)

    for stage in farming_stages.itertuples(index=False):
        if (main_drops := main_drops_by_stage[stage.stageId]):
            for item in main_drops:
                if item in RECORDED_ITEMS \
                   and (drop_rate := curr_drop_data.at[stage.stageId, item]) > 0:
                    farming_stages_by_item[item].append(
                        calc_drop_stats(stage, drop_rate)
                    )
        # sometimes Penguin Statistics doesn't list main drops of event stages
        elif stage.stageType == "ACTIVITY":
            stage_drops = curr_drop_data.loc[stage.stageId].dropna()
            for item, drop_rate in stage_drops.items():
                if item in RECORDED_ITEMS and drop_rate > 0:
                    farming_stages_by_item[item].append(
                        calc_drop_stats(stage, drop_rate)
                    )

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

print("Successfully updated farming data")