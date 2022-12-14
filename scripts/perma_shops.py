import json

with (open("./scripts/shop_data.json", "r") as f1,
      open("./scripts/msv.json", "r") as f2,
      open("./src/lib/data/perma_shops.json", "w") as f3):
    SHOPS = json.load(f1)
    SANITY_VALUES = json.load(f2)
    ALL_SHOP_DATA = {
        region: [
            {
                "currency": shop["currency"],
                "items": [
                    [
                        {
                            "id": item["id"],
                            "count": item["count"],
                            # -2 in data represents finite but unknown quantity
                            "stock": item.get("stock") or -2,
                            "cost": item["cost"],
                            # -1 in data represents unvalued item
                            "value": round(value * item["count"] / item["cost"], 3) if value != -1 else -1
                        }
                        for item in tier if (value := SANITY_VALUES[region].get(item["id"]))
                    ]
                    for tier in shop["items"]
                ]
            }
            for shop in SHOPS
        ]
        for region in ["glb", "cn"]
    }

    json.dump(ALL_SHOP_DATA, f3)

print("Successfully updated permanent shop data")