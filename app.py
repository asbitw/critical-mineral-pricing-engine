import streamlit as st
import pandas as pd
import io

# 1. Page Configuration for Executive View
st.set_page_config(page_title="Critical Minerals Engine", layout="wide")
st.title("🌋 Live Critical Minerals Pricing & Supply Risk Engine")
st.markdown("Real-time executive monitoring stream for high-velocity commodity metrics.")

# 2. Raw Sample Data Stream Ingestion
csv_data = """timestamp,mineral_name,demand_index,shipping_delay_days,geopolitical_risk,market_price
2026-05-21 12:00:00,Lithium Carbonate,125,4,High,18125.00
2026-05-21 12:05:00,Cobalt Metal,95,2,Medium,27075.00
2026-05-21 12:10:00,Copper Cathodes,140,9,High,12880.00
2026-05-21 12:15:00,Lithium Carbonate,85,1,Low,12325.00
2026-05-21 12:20:00,Copper Cathodes,110,5,Medium,10120.00"""

# 3. Data Processing Layer
df = pd.read_csv(io.StringIO(csv_data))
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Calculate live high-level summary KPIs
total_volume = len(df)
high_risk_events = len(df[df['geopolitical_risk'] == 'High'])
avg_market_demand = round(df['demand_index'].mean(), 1)

# 4. Executive KPI Component Layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Data Stream Ticks", value=total_volume)
with col2:
    st.metric(label="Global Demand Index Avg", value=f"{avg_market_demand}%")
with col3:
    st.metric(label="High Risk Supply Disruptions", value=high_risk_events)

st.markdown("---")

# 5. Visual Interactive Elements
st.subheader("📊 Live Spot Market Analytics")
m_col1, m_col2 = st.columns(2)

with m_col1:
    # Spot price movement tracking chart
    st.write("**Price Trend History by Commodity**")
    chart_df = df.pivot(index='timestamp', columns='mineral_name', values='market_price')
    st.line_chart(chart_df)

with m_col2:
    # High-risk supply chain overview
    st.write("**Active Logistics Bottlenecks**")
    st.dataframe(
        df[['mineral_name', 'shipping_delay_days', 'geopolitical_risk']]
        .sort_values(by='shipping_delay_days', ascending=False),
        hide_index=True
    )

# 6. Granular Ledger Audit View
st.subheader("📑 Real-Time Ingestion Ledger")
st.dataframe(df.style.format({"market_price": "${:,.2f}"}), use_container_width=True)
