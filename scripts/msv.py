import utils
from enum import Enum
import requests
import pandas as pd
from scipy.optimize import linprog

MIN_RUN_THRESHOLD = 100
ALLOWED_ITEMS = utils.VALID_ITEMS["material"] + utils.VALID_ITEMS["misc"]
BYPRODUCT_RATE_BONUS = 1.8
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
# PURE_GOLD_TO_EXP = 1000/(3/1.2) # value of pure gold = value of exp produced in factory for the same duration as 1 pure gold
# EXP_DEVALUE_FACTOR = 0.8

class Region(Enum):
    GLOBAL = "US"
    CN = "CN"

def is_valid_stage(stage_id: str) -> bool:
    return stage_id.startswith(("main", "tough", "sub", "wk")) or stage_id.endswith("perm")

def patch_lmd_stages(df: pd.DataFrame) -> pd.DataFrame:
    for stage_id, lmd in LMD_STAGES.items():
        df.at[stage_id, "lmd"] = lmd
    return df

def get_stage_data(region: Region) -> tuple[pd.DataFrame, pd.Series]:
    current_drops = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )

    current_stage_ids = set(item["stageId"] for item in current_drops if is_valid_stage(item["stageId"]))

    stages = (
        requests.get("https://penguin-stats.io/PenguinStats/api/v2/stages")
                .json()
    )

    sanity_costs = (
        pd.DataFrame(data=stages,
                     columns=["stageId", "apCost"])
          .set_index("stageId")
    )

    drop_data = (
        pd.DataFrame(data=requests.get("https://penguin-stats.io/PenguinStats/api/v2/result/matrix?show_closed_zones=true")
                                  .json()
                                  ["matrix"],
                     columns=["stageId", "itemId", "times", "quantity"])
          .query("stageId in @current_stage_ids \
                  and times >= @MIN_RUN_THRESHOLD \
                  and itemId in @ALLOWED_ITEMS")
          .assign(drop_rate = lambda df: df["quantity"] / df["times"])
          .pivot(index="stageId",
                 columns="itemId",
                 values="drop_rate")
          .assign(lmd = lambda df: sanity_costs.reindex(df.index)["apCost"] * 12)
          .pipe(patch_lmd_stages)
          .rename(columns={"lmd": "4001"})
    )
    return drop_data, sanity_costs.reindex(drop_data.index)

def fill_diagonal(df: pd.DataFrame, values: pd.Index) -> pd.DataFrame:
    for id, val in zip(df.index, values):
        df.at[id, id] = val
    return df



drop_matrix, sanity_costs = get_stage_data(Region.CN)

print(drop_matrix.at["main_10-07", "4001"])
print(drop_matrix.at["wk_melee_6", "4001"])
print(drop_matrix)
print(sanity_costs)


'''
recipes = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json")
            .json()
            ["workshopFormulas"]
            .values()
)

recipe_data = (
    pd.json_normalize(data=recipes,
                      record_path="extraOutcomeGroup",
                      meta=["itemId", "count", "extraOutcomeRate"],
                      record_prefix="bp_")
      .assign(total_bp_weight = lambda df: df.groupby("itemId")
                                             ["bp_weight"]
                                             .transform("sum"))
      .assign(bp_sanity_coeff = lambda df: BYPRODUCT_RATE_BONUS *
                                           df["extraOutcomeRate"] *
                                           df["bp_weight"] /
                                           df["total_bp_weight"])
      .pivot(index=["itemId", "count"],
             columns="bp_itemId",
             values="bp_sanity_coeff")
)

recipe_matrix = (
    pd.json_normalize(data=recipes,
                      record_path="costs",
                      meta=["itemId", "goldCost"])
      .pivot(index=["itemId", "goldCost"],
             columns="id",
             values="count")
      .reset_index("goldCost")
      .rename(columns={"goldCost": "4001"})
      .pipe(lambda df: -df)
      .pipe(fill_diagonal, recipe_data.index.get_level_values("count"))
      #.to_numpy(na_value=0)
)

print(recipe_matrix)
'''


'''
def finalize_drops(df):
    matrix = df.to_numpy(na_value=0)
    return matrix, -matrix.sum(axis=0)

stage_drops, sanity_profit = finalize_drops(drop_matrix)
item_equiv_matrix = recipe_matrix + recipe_data.to_numpy(na_value=0)

sln = linprog(sanity_profit, stage_drops, sanity_costs, item_equiv_matrix, <something with np.zeros>).x
'''