import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pension & ISA Strategy Dashboard", layout="wide")

# --- USER INPUTS ---
st.sidebar.header("📊 Input Your Assumptions")
pension_contribution = st.sidebar.number_input("One-Off Pension Contribution (£)", min_value=0, max_value=60000, value=20000, step=500)
pension_growth = st.sidebar.number_input("Pension Growth Rate (%)", min_value=0.0, max_value=10.0, value=5.7, step=0.1) / 100
isa_growth = st.sidebar.number_input("ISA Growth Rate (%)", min_value=0.0, max_value=10.0, value=7.0, step=0.1) / 100

# --- CONSTANTS ---
current_pension_pot = 28000
annual_pension_contrib = 3133
commission = 58791
years = 25
isa_limit = 20000

# --- TAX & NI CALCULATION ---
def calculate_tax(income):
    if income > 150000:
        return income * 0.45
    elif income > 50270:
        return income * 0.40
    else:
        return income * 0.20

def calculate_ni(income):
    return income * 0.02 if income > 50270 else 0

# --- CALCULATE POST-TAX BALANCE ---
tax_paid = calculate_tax(commission - pension_contribution)
ni_paid = calculate_ni(commission - pension_contribution)
balance_after_tax = commission - pension_contribution - tax_paid - ni_paid

# --- ISA CONTRIBUTION & CARRYOVER ---
isa_contribution = min(balance_after_tax, isa_limit)
isa_carryover = max(0, balance_after_tax - isa_limit)

# --- FUTURE VALUE CALCULATIONS ---
isa_value = isa_contribution * ((1 + isa_growth) ** years) + isa_carryover * ((1 + isa_growth) ** (years - 1))
pension_value = (current_pension_pot + pension_contribution) * ((1 + pension_growth) ** years)
pension_value += annual_pension_contrib * sum([(1 + pension_growth) ** (years - i) for i in range(1, years + 1)])

# --- RETIREMENT INCOME CALCULATION ---
annual_isa_income = isa_value * 0.04
annual_pension_income = (pension_value * 0.25 * 0.04) + (pension_value * 0.75 * 0.04 * 0.80)
annual_post_tax_income = annual_isa_income + annual_pension_income
monthly_post_tax_income = annual_post_tax_income / 12

# --- DISPLAY RESULTS ---
st.title("📈 Pension & ISA Strategy Dashboard")
st.markdown("### 🔎 Key Results")
col1, col2, col3 = st.columns(3)

col1.metric("💰 Future Pension Value (25Y)", f"£{pension_value:,.0f}")
col2.metric("📈 Future ISA Value (25Y)", f"£{isa_value:,.0f}")
col3.metric("🏡 Annual Post-Tax Income", f"£{annual_post_tax_income:,.0f} / Year")

st.markdown("---")

# --- GRAPHS ---
st.subheader("📊 Pension & ISA Growth Over Time")
years_range = np.arange(0, years + 1)
pension_growth_over_time = [(current_pension_pot + pension_contribution) * ((1 + pension_growth) ** i) for i in years_range]
isa_growth_over_time = [isa_contribution * ((1 + isa_growth) ** i) for i in years_range]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(years_range, pension_growth_over_time, label="Pension Value", linewidth=2)
ax.plot(years_range, isa_growth_over_time, label="ISA Value", linewidth=2)
ax.set_xlabel("Years")
ax.set_ylabel("Value (£)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.subheader("💡 Breakdown of Post-Retirement Income")
fig2, ax2 = plt.subplots(figsize=(5, 5))
ax2.pie([annual_pension_income, annual_isa_income], labels=["Pension Income", "ISA Income"], autopct='%1.1f%%', startangle=90)
ax2.set_title("Income Sources at Retirement")
st.pyplot(fig2)

st.sidebar.success("✅ Adjust the inputs and see how your retirement funds change in real-time!")
