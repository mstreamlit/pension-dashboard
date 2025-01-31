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
total_income = annual_income + one_off_income
current_pension_pot = st.sidebar.number_input("Current Pension Pot (£)", min_value=0, value=28000, step=500)
annual_pension_contrib = st.sidebar.number_input("Annual Pension Contribution (£)", min_value=0, value=3133, step=100)
retirement_age = st.sidebar.number_input("Retirement Age", min_value=50, max_value=75, value=65, step=1)
years = retirement_age - 40  

# Pension Contribution Options
st.sidebar.subheader("Pension Contribution Options")
pension_opt1 = st.sidebar.number_input("Pension Contribution (Option 1) (£)", min_value=0, value=10554, step=500)
pension_opt2 = st.sidebar.number_input("Pension Contribution (Option 2) (£)", min_value=0, value=20000, step=500)
pension_opt3 = st.sidebar.number_input("Pension Contribution (Option 3) (£)", min_value=0, value=58000, step=500)

# ISA Contribution Options
st.sidebar.subheader("ISA Contribution Options")
isa_opt1 = st.sidebar.number_input("ISA Contribution (Option 1) (£)", min_value=0, value=20000, step=500)
isa_opt2 = st.sidebar.number_input("ISA Contribution (Option 2) (£)", min_value=0, value=20000, step=500)
isa_opt3 = st.sidebar.number_input("ISA Contribution (Option 3) (£)", min_value=0, value=20000, step=500)

# Growth Rates
pension_growth = st.sidebar.number_input("Pension Growth Rate (%)", min_value=0.0, max_value=10.0, value=5.7, step=0.1) / 100
isa_growth = st.sidebar.number_input("ISA Growth Rate (%)", min_value=0.0, max_value=10.0, value=7.0, step=0.1) / 100

# --- TAX & NI FUNCTIONS ---
def calculate_corrected_tax(income):
    if income <= 12570:
        return 0  # Personal Allowance (tax-free)
    elif income <= 50270:
        return (income - 12570) * 0.20
    elif income <= 125140:
        return (50270 - 12570) * 0.20 + (income - 50270) * 0.40
    else:
        return (50270 - 12570) * 0.20 + (125140 - 50270) * 0.40 + (income - 125140) * 0.45

def calculate_corrected_ni(income):
    if income <= 12570:
        return 0
    elif income <= 50270:
        return (income - 12570) * 0.12
    else:
        return (50270 - 12570) * 0.12 + (income - 50270) * 0.02

# --- CALCULATE SCENARIOS ---
def calculate_scenario(pension_contribution, isa_contribution):
    taxable_income = total_income - pension_contribution
    tax_paid = calculate_corrected_tax(taxable_income)
    ni_paid = calculate_corrected_ni(taxable_income)
    cash_on_hand = total_income - pension_contribution - tax_paid - ni_paid
    isa_actual = min(isa_contribution, cash_on_hand)  

    # Future values of pension & ISA
    pension_pot = (current_pension_pot + pension_contribution) * ((1 + pension_growth) ** years)
    pension_pot += annual_pension_contrib * sum([(1 + pension_growth) ** (years - i) for i in range(1, years + 1)])

    isa_pot = isa_actual * ((1 + isa_growth) ** years)

    # Monthly retirement income
    monthly_pension_income = ((pension_pot * 0.25 * 0.04) + ((pension_pot * 0.75 * 0.04) * 0.80)) / 12
    monthly_isa_income = (isa_pot * 0.04) / 12
    total_monthly_income = monthly_pension_income + monthly_isa_income

    return {
        "Pension Contribution": pension_contribution,
        "Tax Paid": tax_paid,
        "NI Paid": ni_paid,
        "Cash on Hand": cash_on_hand,
        "ISA Contribution": isa_actual,
        "Pension Pot at Retirement": pension_pot,
        "ISA Pot at Retirement": isa_pot,
        "Total Monthly Income Post-Tax": total_monthly_income
    }

# Compute all three options
scenario_1 = calculate_scenario(pension_opt1, isa_opt1)
scenario_2 = calculate_scenario(pension_opt2, isa_opt2)
scenario_3 = calculate_scenario(pension_opt3, isa_opt3)

# --- STACKED BAR CHART ---
st.subheader("📊 Comparison of All Pension & ISA Options")

options = ["Option 1", "Option 2", "Option 3"]
pension_contributions = [scenario_1["Pension Contribution"], scenario_2["Pension Contribution"], scenario_3["Pension Contribution"]]
tax_paid = [scenario_1["Tax Paid"], scenario_2["Tax Paid"], scenario_3["Tax Paid"]]
ni_paid = [scenario_1["NI Paid"], scenario_2["NI Paid"], scenario_3["NI Paid"]]
isa_invested = [scenario_1["ISA Contribution"], scenario_2["ISA Contribution"], scenario_3["ISA Contribution"]]
pension_pot = [scenario_1["Pension Pot at Retirement"], scenario_2["Pension Pot at Retirement"], scenario_3["Pension Pot at Retirement"]]
isa_pot = [scenario_1["ISA Pot at Retirement"], scenario_2["ISA Pot at Retirement"], scenario_3["ISA Pot at Retirement"]]
monthly_income = [scenario_1["Total Monthly Income Post-Tax"] * 12, scenario_2["Total Monthly Income Post-Tax"] * 12, scenario_3["Total Monthly Income Post-Tax"] * 12]

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(options, pension_contributions, label="Pension Contribution")
ax.bar(options, tax_paid, bottom=pension_contributions, label="Tax Paid")
ax.bar(options, ni_paid, bottom=np.array(pension_contributions) + np.array(tax_paid), label="NI Paid")
ax.bar(options, isa_invested, bottom=np.array(pension_contributions) + np.array(tax_paid) + np.array(ni_paid), label="ISA Invested")
ax.bar(options, pension_pot, bottom=np.array(pension_contributions) + np.array(tax_paid) + np.array(ni_paid) + np.array(isa_invested), label="Pension Pot at Retirement")
ax.bar(options, isa_pot, bottom=np.array(pension_contributions) + np.array(tax_paid) + np.array(ni_paid) + np.array(isa_invested) + np.array(pension_pot), label="ISA Pot at Retirement")
ax.legend()
st.pyplot(fig)
