from operator import is_
import utils
from enum import Enum
import requests
import pandas as pd
from scipy.optimize import linprog

MIN_RUN_THRESHOLD = 100
ALLOWED_ITEMS = utils.VALID_ITEMS["material"] + utils.VALID_ITEMS["misc"]
BYPRODUCT_RATE_BONUS = 1.8
# PURE_GOLD_TO_EXP = 1000/(3/1.2) # value of pure gold = value of exp produced in factory for the same duration as 1 pure gold
# EXP_DEVALUE_FACTOR = 0.8

class Region(Enum):
    GLOBAL = "US"
    CN = "CN"

def is_valid_stage(stage: dict) -> bool:
    stage_id = stage["stageId"]
    return stage_id.startswith(("main", "sub", "wk")) or stage_id.endswith("perm")

def get_drop_data(region: Region) -> pd.DataFrame:
    current_stages = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )
    current_stage_ids = set(stage["stageId"] for stage in current_stages if is_valid_stage(stage))
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
          .rename(index=lambda id: id.removesuffix("_perm"))
    )
    return drop_data

def patch_stage_costs(stages: pd.DataFrame) -> pd.DataFrame:
    MISSING_STAGE_COSTS = {
        "a003_f03": 15, # OF-F3
        "a003_f04": 18, # OF-F4
    }
    stage_ids, sanity_costs = zip(*MISSING_STAGE_COSTS.items())
    stages.loc[stage_ids, "apCost"] = sanity_costs
    return stages

def fill_diagonal(df, values):
    for id, val in zip(df.index, values):
        df.at[id, id] = val
    return df



drop_matrix = get_drop_data(Region.CN)

stages = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/stage_table.json")
            .json()
            ["stages"]
            .values()
)

sanity_costs = (
    pd.DataFrame(data=stages,
                 columns=["stageId", "apCost"])
      .set_index("stageId")
      .reindex(drop_matrix.index)
      .pipe(patch_stage_costs)
      .to_numpy()
      .flatten()
)

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
      .reset_index(1)
      .rename(columns={"goldCost": "4001"})
      .pipe(lambda df: -df)
      .pipe(fill_diagonal, recipe_data.index.get_level_values("count"))
      #.to_numpy(na_value=0)
)

print(recipe_matrix)



'''
def finalize_drops(df):
    matrix = df.to_numpy(na_value=0)
    return matrix, -matrix.sum(axis=0)

stage_drops, sanity_profit = finalize_drops(drop_matrix)
item_equiv_matrix = recipe_matrix + recipe_data.to_numpy(na_value=0)

sln = linprog(sanity_profit, stage_drops, sanity_costs, item_equiv_matrix, <something with np.zeros>).x
'''