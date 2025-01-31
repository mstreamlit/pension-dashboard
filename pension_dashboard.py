import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="📊 Pension & ISA Simulator", layout="wide")

# --- USER INPUTS ---
st.sidebar.header("📊 Input Your Assumptions")

# --- Income & Contributions ---
annual_income = st.sidebar.number_input("Annual Income (£)", min_value=0, max_value=500000, value=85000, step=500)
one_off_income = st.sidebar.number_input("One-Off Income (£)", min_value=0, max_value=500000, value=58000, step=500)

# --- Pension Inputs ---
current_pension_pot = st.sidebar.number_input("Current Pension Pot (£)", min_value=0, value=28000, step=500)
annual_pension_contrib = st.sidebar.number_input("Annual Pension Contribution (£)", min_value=0, value=3133, step=100)
one_off_pension_contrib = st.sidebar.number_input("One-Off Pension Contribution (£)", min_value=0, value=20000, step=500)

# --- ISA Contributions ---
one_off_isa_year1 = st.sidebar.number_input("ISA One-Off Contribution (Year 1) (£)", min_value=0, value=20000, step=500)
one_off_isa_year2 = st.sidebar.number_input("ISA One-Off Contribution (Year 2) (£)", min_value=0, value=20000, step=500)
annual_isa_contrib = st.sidebar.number_input("Annual ISA Contribution (Years 3-25) (£)", min_value=0, value=5000, step=500)

# --- Investment Growth Rates ---
pension_growth = st.sidebar.number_input("Pension Growth Rate (%)", min_value=0.0, max_value=10.0, value=5.7, step=0.1) / 100
isa_growth = st.sidebar.number_input("ISA Growth Rate (%)", min_value=0.0, max_value=10.0, value=7.0, step=0.1) / 100

# --- Retirement Age ---
retirement_age = st.sidebar.number_input("Retirement Age", min_value=50, max_value=75, value=65, step=1)
years = retirement_age - 40  # Assume working from age 40

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
total_income = annual_income + one_off_income
tax_paid = calculate_tax(total_income - one_off_pension_contrib)
ni_paid = calculate_ni(total_income - one_off_pension_contrib)
balance_after_tax = total_income - one_off_pension_contrib - tax_paid - ni_paid

# --- ISA Contributions ---
isa_year_1 = min(balance_after_tax, one_off_isa_year1)
isa_year_2 = min(balance_after_tax - isa_year_1, one_off_isa_year2)
isa_annual_years_3_25 = np.array([annual_isa_contrib] * (years - 2))

# --- FUTURE VALUE CALCULATIONS ---
isa_value = isa_year_1 * ((1 + isa_growth) ** years) + isa_year_2 * ((1 + isa_growth) ** (years - 1))
isa_value += sum([isa_annual_years_3_25[i] * ((1 + isa_growth) ** (years - (i + 3))) for i in range(len(isa_annual_years_3_25))])

pension_value = (current_pension_pot + one_off_pension_contrib) * ((1 + pension_growth) ** years)
pension_value += annual_pension_contrib * sum([(1 + pension_growth) ** (years - i) for i in range(1, years + 1)])

# --- RETIREMENT INCOME CALCULATION ---
annual_isa_income = isa_value * 0.04
annual_pension_income = (pension_value * 0.25 * 0.04) + (pension_value * 0.75 * 0.04 * 0.80)
annual_post_tax_income = annual_isa_income + annual_pension_income
monthly_post_tax_income = annual_post_tax_income / 12

# --- DISPLAY RESULTS ---
st.title("📈 Pension & ISA Simulator")
st.markdown("### 🔎 Key Results")
col1, col2, col3 = st.columns(3)

col1.metric("💰 Future Pension Value", f"£{pension_value:,.0f}")
col2.metric("📈 Future ISA Value", f"£{isa_value:,.0f}")
col3.metric("🏡 Annual Post-Tax Income", f"£{annual_post_tax_income:,.0f} / Year")

st.markdown("---")

# --- GRAPHS ---
st.subheader("📊 Pension & ISA Growth Over Time")
years_range = np.arange(0, years + 1)
pension_growth_over_time = [(current_pension_pot + one_off_pension_contrib) * ((1 + pension_growth) ** i) for i in years_range]
isa_growth_over_time = [isa_value * ((1 + isa_growth) ** i) for i in years_range]

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

st.sidebar.success("✅ Adjust inputs & simulate different retirement scenarios!")
