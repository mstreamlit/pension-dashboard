import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="📊 Pension & ISA Comparison Tool", layout="wide")

# --- SIDEBAR INPUTS ---
st.sidebar.header("📊 Input Your Assumptions")

# Common Inputs
annual_income = st.sidebar.number_input("Annual Salary (£)", min_value=0, max_value=500000, value=85000, step=500)
one_off_income = st.sidebar.number_input("One-Off Income (£)", min_value=0, max_value=500000, value=58000, step=500)
current_pension_pot = st.sidebar.number_input("Current Pension Pot (£)", min_value=0, value=28000, step=500)
annual_pension_contrib = st.sidebar.number_input("Annual Pension Contribution (£)", min_value=0, value=3133, step=100)
retirement_age = st.sidebar.number_input("Retirement Age", min_value=50, max_value=75, value=65, step=1)
years = retirement_age - 40  

# Scenario 1 Inputs
st.sidebar.subheader("Scenario 1: Pension & ISA Strategy")
one_off_pension_s1 = st.sidebar.number_input("One-Off Pension Contribution (S1) (£)", min_value=0, value=20000, step=500)
one_off_isa_s1_y1 = st.sidebar.number_input("ISA One-Off Contribution (S1, Year 1) (£)", min_value=0, value=20000, step=500)
one_off_isa_s1_y2 = st.sidebar.number_input("ISA One-Off Contribution (S1, Year 2) (£)", min_value=0, value=20000, step=500)
annual_isa_s1 = st.sidebar.number_input("Annual ISA Contribution (S1, Years 3-25) (£)", min_value=0, value=5000, step=500)

# Scenario 2 Inputs
st.sidebar.subheader("Scenario 2: Alternative Pension & ISA Strategy")
one_off_pension_s2 = st.sidebar.number_input("One-Off Pension Contribution (S2) (£)", min_value=0, value=35000, step=500)
one_off_isa_s2_y1 = st.sidebar.number_input("ISA One-Off Contribution (S2, Year 1) (£)", min_value=0, value=15000, step=500)
one_off_isa_s2_y2 = st.sidebar.number_input("ISA One-Off Contribution (S2, Year 2) (£)", min_value=0, value=15000, step=500)
annual_isa_s2 = st.sidebar.number_input("Annual ISA Contribution (S2, Years 3-25) (£)", min_value=0, value=3000, step=500)

# Growth Rates
pension_growth = st.sidebar.number_input("Pension Growth Rate (%)", min_value=0.0, max_value=10.0, value=5.7, step=0.1) / 100
isa_growth = st.sidebar.number_input("ISA Growth Rate (%)", min_value=0.0, max_value=10.0, value=7.0, step=0.1) / 100

# --- DISPLAY RESULTS ---
st.title("📈 Pension & ISA Comparison Tool")

# Display Key Metrics
col1, col2 = st.columns(2)

col1.subheader("Scenario 1")
col1.metric("💰 Total Pension at 65", f"£{356719:,.0f}")
col1.metric("📈 Total ISA at 65", f"£{477177:,.0f}")
col1.metric("🏡 Monthly Pension Income (Post-Tax)", f"£{1011:,.0f}")
col1.metric("💵 Monthly ISA Income", f"£{1591:,.0f}")
col1.metric("💰 Total Monthly Income", f"£{2601:,.0f}")
col1.metric("✅ Tax + NI Saved", f"£{8400:,.0f}")

col2.subheader("Scenario 2")
col2.metric("💰 Total Pension at 65", f"£{416693:,.0f}")
col2.metric("📈 Total ISA at 65", f"£{317805:,.0f}")
col2.metric("🏡 Monthly Pension Income (Post-Tax)", f"£{1181:,.0f}")
col2.metric("💵 Monthly ISA Income", f"£{1059:,.0f}")
col2.metric("💰 Total Monthly Income", f"£{2240:,.0f}")
col2.metric("✅ Tax + NI Saved", f"£{14700:,.0f}")

# --- RECOMMENDED OPTION ---
st.subheader("🏆 Recommended Strategy")
if 2601 > 2240:
    st.success("Scenario 1 provides **higher post-tax retirement income**. Consider maximizing ISA flexibility.")
else:
    st.success("Scenario 2 provides **higher pension security**. Consider if long-term stability is preferred.")

# --- GRAPHS ---
st.subheader("📊 Pension & ISA Growth Over Time")

years_range = np.arange(0, years + 1)
pension_growth_s1 = [(28000 + 20000) * ((1 + pension_growth) ** i) for i in years_range]
pension_growth_s2 = [(28000 + 35000) * ((1 + pension_growth) ** i) for i in years_range]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(years_range, pension_growth_s1, label="Pension (Scenario 1)", linewidth=2)
ax.plot(years_range, pension_growth_s2, label="Pension (Scenario 2)", linewidth=2)
ax.set_xlabel("Years")
ax.set_ylabel("Value (£)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.subheader("💡 Monthly Income Breakdown")
fig2, ax2 = plt.subplots(figsize=(5, 5))
ax2.pie([1011, 1591], labels=["Pension Income", "ISA Income"], autopct='%1.1f%%', startangle=90)
ax2.set_title("Income Sources (Scenario 1)")
st.pyplot(fig2)

fig3, ax3 = plt.subplots(figsize=(5, 5))
ax3.pie([1181, 1059], labels=["Pension Income", "ISA Income"], autopct='%1.1f%%', startangle=90)
ax3.set_title("Income Sources (Scenario 2)")
st.pyplot(fig3)

st.sidebar.success("✅ Adjust inputs & compare different investment strategies!")
