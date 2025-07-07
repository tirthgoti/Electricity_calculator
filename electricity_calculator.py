import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="⚡ Electricity Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ Electricity Consumption Calculator")
st.subheader("Calculate your home electricity consumption and get insights on energy usage")

st.header("📋 Personal Information")
col1, col2, col3, col4 = st.columns(4)
with col1:
    name = st.text_input("👤 Enter your name:", placeholder="John Doe")
with col2:
    age = st.number_input("🎂 Enter your age:", min_value=1, max_value=120, value=25)
with col3:
    city = st.text_input("🏙️ Enter your city:", placeholder="Mumbai")
with col4:
    area = st.text_input("📍 Enter your area name:", placeholder="Bandra West")

st.header("🏠 Housing Information")
col1, col2 = st.columns(2)
with col1:
    flat_tenement = st.radio("🏢 Are you living in:", ["Flat", "Tenement"], horizontal=True)
with col2:
    facility = st.radio("🏡 Housing type:", ["1BHK", "2BHK", "3BHK"], horizontal=True)

st.header("🔌 Appliances Selection")
col1, col2 = st.columns(2)
with col1:
    ac = st.radio("❄️ Are you using AC?", ["No", "Yes"], horizontal=True)
    fridge = st.radio("🧊 Are you using Fridge?", ["No", "Yes"], horizontal=True)
with col2:
    washing_machine = st.radio("👕 Washing Machine", ["No", "Yes"], horizontal=True)
    
selected_appliances = []
if ac == "Yes":
    selected_appliances.append("❄️ AC")
if fridge == "Yes":
    selected_appliances.append("🧊 Fridge")
if washing_machine == "Yes":
    selected_appliances.append("👕 Washing Machine")

if selected_appliances:
    st.success("**Selected Appliances:** " + " | ".join(selected_appliances))

st.divider()

def calculate_energy_consumption():
    cal_energy = 0
    
    if facility == "1BHK":
        cal_energy += 2 * 0.4 + 2 * 0.8
    elif facility == "2BHK":
        cal_energy += 3 * 0.4 + 3 * 0.8
    elif facility == "3BHK":
        cal_energy += 4 * 0.4 + 4 * 0.8
    
    if ac == "Yes":
        cal_energy += 3.0
    if fridge == "Yes":
        cal_energy += 3.0
    if washing_machine == "Yes":
        cal_energy += 1.2
    
    return cal_energy

daily_consumption = calculate_energy_consumption()
monthly_consumption = daily_consumption * 30
yearly_consumption = daily_consumption * 365

cost_per_unit = 5
daily_cost = daily_consumption * cost_per_unit
monthly_cost = monthly_consumption * cost_per_unit
yearly_cost = yearly_consumption * cost_per_unit

if name:
    st.header(f"👋 Hello {name}!")
    st.write(f"📍 **Location:** {area}, {city} | 🏠 **Housing:** {facility} {flat_tenement}")
    
    st.success("⚡ **Your Daily Electricity Consumption**")
    st.metric(
        label="Daily Consumption",
        value=f"{daily_consumption:.2f} kWh",
        delta=f"₹{daily_cost:.2f} per day"
    )
    
    st.header("📊 Consumption Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📅 Monthly Consumption",
            value=f"{monthly_consumption:.2f} kWh",
            delta=f"₹{monthly_cost:.2f}"
        )
    
    with col2:
        st.metric(
            label="📆 Yearly Consumption",
            value=f"{yearly_consumption:.2f} kWh",
            delta=f"₹{yearly_cost:.2f}"
        )
    
    with col3:
        if daily_consumption < 5:
            rating = "🟢 Excellent"
        elif daily_consumption < 10:
            rating = "🟡 Good"
        elif daily_consumption < 15:
            rating = "🟠 Average"
        else:
            rating = "🔴 High"
        
        st.metric(
            label="⭐ Energy Efficiency",
            value=rating.split(" ")[1],
            delta=rating.split(" ")[0]
        )
    
    with col4:
        co2_emission = yearly_consumption * 0.82
        trees_needed = co2_emission / 21.77
        
        st.metric(
            label="🌳 CO2 Emission (Yearly)",
            value=f"{co2_emission:.0f} kg",
            delta=f"{trees_needed:.1f} trees to offset"
        )
    
    st.header("📈 Visual Analysis")
    
    appliances = []
    consumption = []
    
    base_consumption = 0
    if facility == "1BHK":
        base_consumption = 2.4
    elif facility == "2BHK":
        base_consumption = 3.6
    elif facility == "3BHK":
        base_consumption = 4.8
    
    appliances.append(f"Base ({facility})")
    consumption.append(base_consumption)
    
    if ac == "Yes":
        appliances.append("❄️ Air Conditioner")
        consumption.append(3.0)
    if fridge == "Yes":
        appliances.append("🧊 Refrigerator")
        consumption.append(3.0)
    if washing_machine == "Yes":
        appliances.append("👕 Washing Machine")
        consumption.append(1.2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = px.pie(
            values=consumption,
            names=appliances,
            title="Daily Energy Consumption by Appliance",
            color_discrete_sequence=['#FFD54F', '#FFC107', '#FFB300', '#FF8F00', '#FF6F00']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_bar = px.bar(
            x=appliances,
            y=consumption,
            title="Energy Consumption by Appliance (kWh/day)",
            labels={"x": "Appliances", "y": "Consumption (kWh/day)"},
            color=consumption,
            color_continuous_scale=['#FFFDE7', '#FFF59D', '#FFD54F', '#FFC107', '#FF8F00']
        )
        fig_bar.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    days = list(range(1, 31))
    daily_costs = [daily_cost * day for day in days]
    cumulative_consumption = [daily_consumption * day for day in days]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=days,
        y=daily_costs,
        mode='lines+markers',
        name='Cumulative Cost (₹)',
        line=dict(width=3, color='#FF8F00'),
        marker=dict(size=6, color='#FFC107'),
        yaxis='y'
    ))
    fig_line.add_trace(go.Scatter(
        x=days,
        y=cumulative_consumption,
        mode='lines+markers',
        name='Cumulative Consumption (kWh)',
        line=dict(width=3, color='#FFD54F'),
        marker=dict(size=6, color='#FFEB3B'),
        yaxis='y2'
    ))
    fig_line.update_layout(
        title="Monthly Electricity Cost & Consumption Projection",
        xaxis_title="Days",
        yaxis=dict(title="Cost (₹)", side='left'),
        yaxis2=dict(title="Consumption (kWh)", side='right', overlaying='y'),
        legend=dict(x=0.02, y=0.98)
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.header("💡 Energy Saving Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🏠 Home Efficiency:**
        - 🌟 Use LED bulbs instead of incandescent
        - ❄️ Set AC temperature to 24°C or higher
        - 🌞 Use natural light during the day
        - 🏠 Improve home insulation
        """)
    
    with col2:
        st.info("""
        **🔌 Appliance Management:**
        - 🔌 Unplug devices when not in use
        - 🧊 Keep refrigerator at optimal temperature
        - ⏰ Use appliances during off-peak hours
        - 🔧 Regular maintenance of appliances
        """)
    
    st.header("📊 How You Compare")
    
    avg_consumption = {
        "1BHK": 4.5,
        "2BHK": 6.5,
        "3BHK": 8.5
    }
    
    avg_for_house = avg_consumption.get(facility, 8.0)
    difference = daily_consumption - avg_for_house
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=f"Your {facility} Consumption",
            value=f"{daily_consumption:.2f} kWh",
            delta=f"{difference:+.2f} vs average"
        )
    
    with col2:
        st.metric(
            label=f"Average {facility} Consumption",
            value=f"{avg_for_house:.2f} kWh",
            delta="India average"
        )
    
    with col3:
        if difference > 0:
            status = "⚠️ Above Average"
            advice = "Consider energy-saving measures"
        else:
            status = "✅ Below Average"
            advice = "Great! Keep it up"
        
        st.metric(
            label="Status",
            value=status,
            delta=advice
        )

else:
    st.warning("👆 Please enter your name to see your electricity consumption analysis!")

st.divider()
st.success("📈 **Want to reduce your electricity bill?**")
st.write("Consider switching to solar panels, upgrading to energy-efficient appliances, or implementing smart home automation!")