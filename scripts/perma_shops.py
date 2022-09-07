from collections import defaultdict
import json
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

all_shop_effics = defaultdict(list)







with open("./scripts/msv.json", "r") as f1, open("./scripts/foo.json", "w") as f2:
    sanity_values = json.load(f1)
    json.dump(all_shop_effics, f2)