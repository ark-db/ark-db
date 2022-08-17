import utils
from enum import Enum
import requests
import pandas as pd
from scipy.optimize import linprog

EXP_DEVALUE_FACTOR = 0.8
MIN_RUN_THRESHOLD = 100
ALLOWED_ITEMS = utils.VALID_ITEMS["material"] + utils.VALID_ITEMS["misc"]
PURE_GOLD_TO_EXP = 1000/(3/1.2) # value of pure gold = value of exp produced in factory for the same duration as 1 pure gold

class Region(Enum):
    GLOBAL = "US"
    CN = "CN"

def is_valid_stage(stage: dict) -> bool:
    stage_id = stage["stageId"]
    return stage_id.startswith(("main", "sub", "wk")) or stage_id.endswith("perm")

def trim_stage_ids(stages: pd.DataFrame) -> pd.DataFrame:
    stages["stageId"] = stages["stageId"].str.removesuffix("_perm")
    return stages

def get_drop_data(region: Region) -> pd.DataFrame:
    current_stages = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )
    current_stage_ids = set(stage["stageId"] for stage in filter(is_valid_stage, current_stages))
    drop_data = (
        pd.DataFrame(data=requests.get("https://penguin-stats.io/PenguinStats/api/v2/result/matrix?show_closed_zones=true")
                                  .json()
                                  ["matrix"],
                     columns=["stageId", "itemId", "times", "quantity"])
          .query("stageId in @current_stage_ids \
                  and times >= @MIN_RUN_THRESHOLD \
                  and itemId in @ALLOWED_ITEMS")
          .pipe(trim_stage_ids)
          .assign(drop_rate = lambda df: df["quantity"] / df["times"])
          .pivot(index="stageId",
                 columns="itemId",
                 values="drop_rate")
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