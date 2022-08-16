from enum import Enum
import requests
import pandas as pd
from scipy.optimize import linprog

class Region(Enum):
    GLOBAL = "US"
    CN = "CN"

MIN_RUN_THRESHOLD = 100

def get_drop_data(region: Region) -> pd.DataFrame:
    current_stages = (
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region.value}")
                .json()
                ["matrix"]
    )
    current_stage_ids = set(stage["stageId"] for stage in current_stages)
    stages = (
        pd.DataFrame(requests.get("https://penguin-stats.io/PenguinStats/api/v2/result/matrix?show_closed_zones=true")
                             .json()
                             ["matrix"])
          .query("stageId in @current_stage_ids \
                  and times >= @MIN_RUN_THRESHOLD")
    )
    print(stages.head())

get_drop_data(Region.GLOBAL)