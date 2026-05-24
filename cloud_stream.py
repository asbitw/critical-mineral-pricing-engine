import time
import random
import requests
from datetime import datetime
# 1. Target Endpoint Details
PROJECT_ID = "project-e5083dd5-fdba-45a3-8c8"
DATASET_ID = "mineral_data"
TABLE_ID = "live_market_feed"
url = f"https://googleapis.com{PROJECT_ID}/datasets/{DATASET_ID}/tables/{TABLE_ID}/insertAll"
minerals = [
    {"name": "Lithium Carbonate", "base_price": 14500.00},
    {"name": "Cobalt Metal", "base_price": 28500.00},
    {"name": "Copper Cathodes", "base_price": 9200.00}
]
print("START: Ingesting live mineral data stream directly into BigQuery Cloud...")
print("Press Ctrl + C to stop the live market feed.\n")
try:
    for i in range(5):
        mineral = random.choice(minerals)
        global_demand_index = random.randint(70, 150)
        shipping_delay_days = random.randint(0, 14)
        geopolitical_risk = random.choice(["Low", "Medium", "High"])
        market_price = round(mineral["base_price"] * (global_demand_index / 100), 2)
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        payload = {
            "rows": [
                {
                    "json": {
                        "timestamp": current_time,
                        "mineral_name": mineral["name"],
                        "demand_index": global_demand_index,
                        "shipping_delay_days": shipping_delay_days,
                        "geopolitical_risk": geopolitical_risk,
                        "market_price": market_price
                    }
                }
            ]
        }
        # Test connection path
        response = requests.post(url, json=payload, headers={"Authorization": "Bearer SECURE_SYNC"})
        print(f"STREAM TICK {i+1}: Generated live metrics for {mineral['name']} at ${market_price:,}")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nPipeline ingestion paused cleanly by user.")
print("\nFINISH: Local ingestion processing sequence complete.")
