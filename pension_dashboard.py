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

# --- TOGGLE FOR CALCULATION TYPE ---
calculation_type = st.radio(
    "Select Calculation Method:",
    ("Total Income Calculation (Annual + One-Off)", "One-Off Payment Calculation (Tax Rate Based on Annual)")
)

# --- TAX & NI FUNCTIONS ---
def calculate_tax(income):
    if income <= 12570:
        return 0  # Personal Allowance
    elif income <= 50270:
        return (income - 12570) * 0.20
    elif income <= 125140:
        return (50270 - 12570) * 0.20 + (income - 50270) * 0.40
    else:
        return (50270 - 12570) * 0.20 + (125140 - 50270) * 0.40 + (income - 125140) * 0.45

def calculate_ni(income):
    if income <= 12570:
        return 0  # No NI below threshold
    elif income <= 50270:
        return (income - 12570) * 0.12  # 12% for income between 12570 and 50270
    else:
        return (50270 - 12570) * 0.12 + (income - 50270) * 0.02  # 2% above 50270

# --- CALCULATE SCENARIOS ---
def calculate_scenario(pension_contribution):
    # Ensure total income for tax calculation is always defined
    total_income_for_tax = annual_income + one_off_income  # Used for tax rate determination

    if calculation_type == "Total Income Calculation (Annual + One-Off)":
        taxable_income = total_income_for_tax - pension_contribution  # Uses full income
    else:  # One-Off Payment Calculation (taxable income is just one-off, tax based on full income)
        taxable_income = one_off_income - pension_contribution  

    # Calculate tax using total income but applying it to taxable income only
    tax_paid = calculate_tax(total_income_for_tax) - calculate_tax(total_income_for_tax - taxable_income)
    ni_paid = calculate_ni(taxable_income)
    
    # Cash Available Calculation
    cash_available = taxable_income - tax_paid - ni_paid
    
    return {
        "Pension Contribution": pension_contribution,
        "Taxable Income": taxable_income,
        "Tax Paid": tax_paid,
        "NI Paid": ni_paid,
        "Cash Available": cash_available
    }


# Compute all three options
scenario_1 = calculate_scenario(pension_opt1)
scenario_2 = calculate_scenario(pension_opt2)
scenario_3 = calculate_scenario(pension_opt3)

# --- DISPLAY RESULTS ---
st.subheader("💰 Cash Available After Pension & Tax Based on Selected Calculation Method")
st.write(f"**Option 1:** £{scenario_1['Cash Available']:,.0f}")
st.write(f"**Option 2:** £{scenario_2['Cash Available']:,.0f}")
st.write(f"**Option 3:** £{scenario_3['Cash Available']:,.0f}")

# --- RECOMMENDED OPTION ---
st.subheader("🏆 Recommended Option")
best_option = max([scenario_1, scenario_2, scenario_3], key=lambda x: x["Cash Available"])
st.success(f"Based on cash available, **Option {['1', '2', '3'][[scenario_1, scenario_2, scenario_3].index(best_option)]} is recommended.**")

