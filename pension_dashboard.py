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
years = retirement_age - 40  # Assume working from age 40
isa_limit = 20000  # ISA annual contribution limit

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

# --- SCENARIO CALCULATIONS ---
def calculate_scenario(one_off_pension, one_off_isa_y1, one_off_isa_y2, annual_isa):
    total_income = annual_income + one_off_income
    
    # Tax and NI calculations before pension contribution
    tax_before = calculate_tax(total_income)
    ni_before = calculate_ni(total_income)
    
    # After pension contribution
    tax_after = calculate_tax(total_income - one_off_pension)
    ni_after = calculate_ni(total_income - one_off_pension)
    
    # Tax savings
    tax_savings = tax_before - tax_after
    ni_savings = ni_before - ni_after
    total_tax_ni_savings = tax_savings + ni_savings

    # Balance after Tax & NI
    balance_after_tax = total_income - one_off_pension - tax_after - ni_after

    # ISA Contributions & Growth
    isa_year_1 = min(balance_after_tax, one_off_isa_y1)
    isa_year_2 = min(balance_after_tax - isa_year_1, one_off_isa_y2)
    isa_annual_years_3_25 = np.array([annual_isa] * (years - 2))

    isa_value = isa_year_1 * ((1 + isa_growth) ** years) + isa_year_2 * ((1 + isa_growth) ** (years - 1))
    isa_value += sum([isa_annual_years_3_25[i] * ((1 + isa_growth) ** (years - (i + 3))) for i in range(len(isa_annual_years_3_25))])

    pension_value = (current_pension_pot + one_off_pension) * ((1 + pension_growth) ** years)
    pension_value += annual_pension_contrib * sum([(1 + pension_growth) ** (years - i) for i in range(1, years + 1)])

    # Post-Retirement Income Calculation
    annual_isa_income = isa_value * 0.04
    annual_pension_income = (pension_value * 0.25 * 0.04) + (pension_value * 0.75 * 0.04 * 0.80)
    annual_post_tax_income = annual_isa_income + annual_pension_income
    monthly_post_tax_income = annual_post_tax_income / 12

    return (pension_value, isa_value, annual_post_tax_income, monthly_post_tax_income, 
            annual_pension_income, annual_isa_income, total_tax_ni_savings)

# --- COMPUTE RESULTS ---
pension_s1, isa_s1, annual_income_s1, monthly_income_s1, pension_income_s1, isa_income_s1, tax_savings_s1 = calculate_scenario(one_off_pension_s1, one_off_isa_s1_y1, one_off_isa_s1_y2, annual_isa_s1)
pension_s2, isa_s2, annual_income_s2, monthly_income_s2, pension_income_s2, isa_income_s2, tax_savings_s2 = calculate_scenario(one_off_pension_s2, one_off_isa_s2_y1, one_off_isa_s2_y2, annual_isa_s2)

# --- DISPLAY RESULTS ---
st.title("📈 Pension & ISA Comparison Tool")

col1, col2 = st.columns(2)
col1.subheader("Scenario 1")
col1.metric("💰 Future Pension", f"£{pension_s1:,.0f}")
col1.metric("📈 Future ISA", f"£{isa_s1:,.0f}")
col1.metric("🏡 Annual Income", f"£{annual_income_s1:,.0f}")
col1.metric("💰 Tax + NI Saved", f"£{tax_savings_s1:,.0f}")

col2.subheader("Scenario 2")
col2.metric("💰 Future Pension", f"£{pension_s2:,.0f}")
col2.metric("📈 Future ISA", f"£{isa_s2:,.0f}")
col2.metric("🏡 Annual Income", f"£{annual_income_s2:,.0f}")
col2.metric("💰 Tax + NI Saved", f"£{tax_savings_s2:,.0f}")

st.sidebar.success("✅ Adjust inputs & compare different investment strategies!")
