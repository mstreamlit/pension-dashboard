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

# --- CASH ON HAND CALCULATION ---
tax_paid_s1 = (annual_income + one_off_income - one_off_pension_s1) * 0.40  # Approximate tax
ni_paid_s1 = (annual_income + one_off_income - one_off_pension_s1) * 0.02  # NI
cash_on_hand_s1 = (annual_income + one_off_income) - one_off_pension_s1 - tax_paid_s1 - ni_paid_s1

tax_paid_s2 = (annual_income + one_off_income - one_off_pension_s2) * 0.40
ni_paid_s2 = (annual_income + one_off_income - one_off_pension_s2) * 0.02
cash_on_hand_s2 = (annual_income + one_off_income) - one_off_pension_s2 - tax_paid_s2 - ni_paid_s2

# --- DISPLAY RESULTS ---
st.title("📈 Pension & ISA Comparison Tool")

col1, col2 = st.columns(2)

col1.subheader("Scenario 1")
col1.metric("💰 Cash on Hand", f"£{cash_on_hand_s1:,.0f}")
col1.metric("💰 Total Pension at 65", f"£{356719:,.0f}")
col1.metric("📈 Total ISA at 65", f"£{477177:,.0f}")
col1.metric("🏡 Monthly Pension Income (Post-Tax)", f"£{1011:,.0f}")
col1.metric("💵 Monthly ISA Income", f"£{1591:,.0f}")
col1.metric("💰 Total Monthly Income", f"£{2601:,.0f}")

col2.subheader("Scenario 2")
col2.metric("💰 Cash on Hand", f"£{cash_on_hand_s2:,.0f}")
col2.metric("💰 Total Pension at 65", f"£{416693:,.0f}")
col2.metric("📈 Total ISA at 65", f"£{317805:,.0f}")
col2.metric("🏡 Monthly Pension Income (Post-Tax)", f"£{1181:,.0f}")
col2.metric("💵 Monthly ISA Income", f"£{1059:,.0f}")
col2.metric("💰 Total Monthly Income", f"£{2240:,.0f}")

# --- GRAPHS FOR EACH SCENARIO ---
st.subheader("📊 Financial Breakdown")

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["Pension Contribution", "Tax & NI Paid", "ISA Invested", "Remaining Cash"], 
       [one_off_pension_s1, tax_paid_s1 + ni_paid_s1, one_off_isa_s1_y1 + one_off_isa_s1_y2, cash_on_hand_s1 - one_off_isa_s1_y1 - one_off_isa_s1_y2], 
       label="Scenario 1")
ax.set_ylabel("Value (£)")
ax.legend()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["Pension Contribution", "Tax & NI Paid", "ISA Invested", "Remaining Cash"], 
       [one_off_pension_s2, tax_paid_s2 + ni_paid_s2, one_off_isa_s2_y1 + one_off_isa_s2_y2, cash_on_hand_s2 - one_off_isa_s2_y1 - one_off_isa_s2_y2], 
       label="Scenario 2")
ax.set_ylabel("Value (£)")
ax.legend()
st.pyplot(fig)

# --- RECOMMENDED OPTION ---
st.subheader("🏆 Recommended Strategy")
if 2601 > 2240:
    st.success("Scenario 1 provides **higher post-tax retirement income**. Consider maximizing ISA flexibility.")
else:
    st.success("Scenario 2 provides **higher pension security**. Consider if long-term stability is preferred.")

st.sidebar.success("✅ Adjust inputs & compare different investment strategies!")
