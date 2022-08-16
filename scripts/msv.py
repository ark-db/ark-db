import utils
from enum import Enum
import requests
import pandas as pd
from scipy.optimize import linprog

class Region(Enum):
    GLOBAL = "US"
    CN = "CN"

MIN_RUN_THRESHOLD = 100
ALLOWED_ITEMS = utils.VALID_ITEMS["material"]

def is_valid_stage(stage):
    stage_id = stage["stageId"]
    return stage_id.startswith(("main", "sub", "wk")) or stage_id.endswith("perm")

def trim_stage_ids(df):
    df["stageId"] = df["stageId"].str.removesuffix("_perm")
    return df

def get_drop_data(region: Region) -> pd.DataFrame:
    current_stages = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )
    current_stage_ids = set(stage["stageId"] for stage in filter(is_valid_stage, current_stages))
    stages = (
        pd.DataFrame(data=requests.get("https://penguin-stats.io/PenguinStats/api/v2/result/matrix?show_closed_zones=true")
                                  .json()
                                  ["matrix"],
                     columns=["stageId", "itemId", "times", "quantity"])
          .query("stageId in @current_stage_ids \
                  and times >= @MIN_RUN_THRESHOLD \
                  and itemId in @ALLOWED_ITEMS")
          .pipe(trim_stage_ids)
          .assign(drop_rate = lambda df: df["quantity"] / df["times"])
          .drop(["quantity", "times"], axis=1)
          .pivot(index="stageId",
                 columns="itemId",
                 values="drop_rate")
    )
    return stages

drop_matrix = get_drop_data(Region.CN)



def patch_stage_costs(df):
    MISSING_STAGE_COSTS = {
        "a003_f03": 15, # OF-F3
        "a003_f04": 18, # OF-F4
    }
    stages, sanity_costs = MISSING_STAGE_COSTS.keys(), MISSING_STAGE_COSTS.values()
    df.loc[stages, "apCost"] = sanity_costs
    return df

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
)

print(sanity_costs)