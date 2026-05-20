import sqlite3
import random
import time
from datetime import datetime

# Initialize local SQL Database file
conn = sqlite3.connect('mineral_market.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS live_market_feed (
        timestamp TEXT, mineral_name TEXT, demand_index INTEGER,
        shipping_delay_days INTEGER, geopolitical_risk TEXT, market_price REAL
    )
''')
conn.commit()

minerals = [
    {"name": "Lithium Carbonate", "base_price": 14500.00},
    {"name": "Cobalt Metal", "base_price": 28500.00},
    {"name": "Copper Cathodes", "base_price": 9200.00}
]

print("START: Ingesting live mineral data stream directly into SQL Database...")

for i in range(10):
    mineral = random.choice(minerals)
    global_demand_index = random.randint(70, 150)
    shipping_delay_days = random.randint(0, 14)
    geopolitical_risk = random.choice(["Low", "Medium", "High"])
    
    market_price = round(mineral["base_price"] * (global_demand_index / 100), 2)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO live_market_feed VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_time, mineral['name'], global_demand_index, shipping_delay_days, geopolitical_risk, market_price))
    conn.commit()
    print(f"SUCCESS: Row {i+1} saved to SQL: {mineral['name']} at ${market_price:,}")
    time.sleep(1)

conn.close()
print("FINISH: Stream finished! 'mineral_market.db' generated successfully.")
