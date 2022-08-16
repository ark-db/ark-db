from enum import Enum
import requests
import pandas as pd
from scipy.optimize import linprog

class Region(Enum):
    GLOBAL = "US"
    CN = "CN"

def get_drop_data(region: Region) -> pd.DataFrame:
    current_stages = set(map(
        lambda entry: entry["stageId"],
        requests.get(f"https://penguin-stats.io/PenguinStats/api/v2/result/matrix?server={region}")
                .json()
                ["matrix"]
    ))
    stages = (
        pd.DataFrame(requests.get("https://penguin-stats.io/PenguinStats/api/v2/result/matrix?show_closed_zones=true")
                             .json()
                             ["matrix"])
          .query("stageId in @current_stages")
    )
    print(stages.head())
    #return pd.merge(all_stages, current_stages, )

get_drop_data(Region.GLOBAL.value)