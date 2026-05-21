import sqlite3

# 1. Connect to our local mineral database
conn = sqlite3.connect('mineral_market.db')
cursor = conn.cursor()

print("--- CRITICAL MINERALS BUSINESS INTELLIGENCE REPORT ---")
print("Extracting high-value metrics for commodities traders...\n")

# 2. SQL query to calculate averages per mineral type
query = '''
    SELECT 
        mineral_name,
        COUNT(*) as total_ticks,
        ROUND(AVG(demand_index), 1) as avg_demand,
        ROUND(AVG(market_price), 2) as avg_price
    FROM live_market_feed
    GROUP BY mineral_name
'''

cursor.execute(query)
rows = cursor.fetchall()

# 3. Use individual layout index markers [0, 1, 2, 3] to isolate the columns
for row in rows:
    print(f"Mineral: {row[0]}")
    print(f"  Total Data Ticks: {row[1]}")
    print(f"  Average Demand Score: {row[2]}")
    print(f"  Average Market Price: ${row[3]:,}")
    print("-" * 40)

conn.close()
print("FINISH: Business report rendering complete.")
