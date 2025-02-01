import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Helper Functions for Tax & NI Calculations
# -------------------------------
def compute_tax(income):
    """
    Compute UK Income Tax based on taxable income.
    
    Tax brackets:
      - £0 – £12,570: 0%
      - £12,570 – £50,270: 20%
      - £50,270 – £125,140: 40%
      - Above £125,140: 45%
    """
    tax = 0
    if income <= 12570:
        return 0

    if income > 12570:
        taxable = min(income, 50270) - 12570
        tax += taxable * 0.20

    if income > 50270:
        taxable = min(income, 125140) - 50270
        tax += taxable * 0.40

    if income > 125140:
        taxable = income - 125140
        tax += taxable * 0.45

    return tax

def compute_ni(income):
    """
    Compute UK National Insurance (NI) on the given income.
    
    NI brackets:
      - Below £12,570: 0%
      - £12,570 – £50,270: 12%
      - Above £50,270: 2%
    """
    ni = 0
    if income <= 12570:
        return 0

    if income > 12570:
        taxable = min(income, 50270) - 12570
        ni += taxable * 0.12

    if income > 50270:
        taxable = income - 50270
        ni += taxable * 0.02

    return ni

# -------------------------------
# Main App Function
# -------------------------------
def main():
    st.title("Pension & ISA Contribution Optimization Dashboard")
    st.write("📅 **Date:** January 2025")
    st.write("👤 **Owner:** [Your Name]")
    st.write("💼 **Purpose:** Helps users determine the optimal pension and ISA contributions by evaluating tax implications, NI, cash availability, and long‐term retirement income.")

    st.markdown("---")
    st.header("1️⃣ Overview")
    st.write(
        """
The dashboard allows you to:
- Compare three different pension contribution scenarios.
- Assess cash available for ISA investments.
- See the impact of contributions on tax, NI, and net take-home.
- View projected retirement pots for pension & ISA investments.
- Get a dynamic recommendation for the best contribution strategy.
        """
    )

    # -------------------------------
    # Sidebar – General Inputs
    # -------------------------------
    st.sidebar.header("Income Details")
    annual_salary = st.sidebar.number_input("Annual Salary (£)", value=135000, step=1000)
    one_off_income = st.sidebar.number_input("One-Off Income (£)", value=58000, step=100)

    st.sidebar.header("Pension Details")
    current_pension = st.sidebar.number_input("Current Pension Pot (£)", value=20000, step=1000)
    annual_pension = st.sidebar.number_input("Annual Pension Contribution (£)", value=3300, step=100)

    st.sidebar.header("Retirement")
    years_to_retirement = st.sidebar.number_input("Years to Retirement", value=25, step=1)

    st.sidebar.header("Growth Assumptions")
    pension_growth_rate = st.sidebar.number_input("Pension Growth Rate (%)", value=5.7, step=0.1) / 100.0
    isa_growth_rate = st.sidebar.number_input("ISA Growth Rate (%)", value=7.0, step=0.1) / 100.0

    st.sidebar.header("Calculation Method")
    calc_method = st.sidebar.radio(
        "Choose Calculation Method",
        (
            "Total Income Calculation (Annual + One-Off)",
            "One-Off Payment Calculation (One-Off - Pension)"
        )
    )

    # Determine the income base based on the toggle
    if calc_method == "Total Income Calculation (Annual + One-Off)":
        income_based = annual_salary + one_off_income
    else:
        income_based = one_off_income

    # -------------------------------
    # Sidebar – Scenario Options & Cash Available Calculations
    # -------------------------------
    st.sidebar.header("Scenario Options")

    # ---- Option 1 ----
    st.sidebar.markdown("##### Option 1")
    option1_extra_pension = st.sidebar.number_input("Additional Pension Contribution (£)", value=0, key="option1_pension")
    option1_isa = st.sidebar.number_input("ISA Contribution (£)", value=20000, key="option1_isa")
    option1_total_pension = annual_pension + option1_extra_pension
    taxable_income_option1 = max(income_based - option1_total_pension, 0)
    tax_option1 = compute_tax(taxable_income_option1)
    ni_option1 = compute_ni(taxable_income_option1)
    disposable_option1 = income_based - option1_total_pension - (tax_option1 + ni_option1)
    option1_cash_available = disposable_option1 - option1_isa
    st.sidebar.markdown("**Cash Available for Option 1:**")
    st.sidebar.write(f"£{option1_cash_available:,.2f}")

    # ---- Option 2 ----
    st.sidebar.markdown("##### Option 2")
    option2_extra_pension = st.sidebar.number_input("Additional Pension Contribution (£)", value=10554, key="option2_pension")
    option2_isa = st.sidebar.number_input("ISA Contribution (£)", value=20000, key="option2_isa")
    option2_total_pension = annual_pension + option2_extra_pension
    taxable_income_option2 = max(income_based - option2_total_pension, 0)
    tax_option2 = compute_tax(taxable_income_option2)
    ni_option2 = compute_ni(taxable_income_option2)
    disposable_option2 = income_based - option2_total_pension - (tax_option2 + ni_option2)
    option2_cash_available = disposable_option2 - option2_isa
    st.sidebar.markdown("**Cash Available for Option 2:**")
    st.sidebar.write(f"£{option2_cash_available:,.2f}")

    # ---- Option 3 ----
    st.sidebar.markdown("##### Option 3")
    option3_extra_pension = st.sidebar.number_input("Additional Pension Contribution (£)", value=20000, key="option3_pension")
    option3_isa = st.sidebar.number_input("ISA Contribution (£)", value=0, key="option3_isa")
    option3_total_pension = annual_pension + option3_extra_pension
    taxable_income_option3 = max(income_based - option3_total_pension, 0)
    tax_option3 = compute_tax(taxable_income_option3)
    ni_option3 = compute_ni(taxable_income_option3)
    disposable_option3 = income_based - option3_total_pension - (tax_option3 + ni_option3)
    option3_cash_available = disposable_option3 - option3_isa
    st.sidebar.markdown("**Cash Available for Option 3:**")
    st.sidebar.write(f"£{option3_cash_available:,.2f}")

    # -------------------------------
    # Main Calculations for Each Scenario
    # -------------------------------
    # Also include ISA Contribution as a field for graphing.
    scenarios = {
        "Option 1": {"pension": option1_extra_pension, "isa": option1_isa},
        "Option 2": {"pension": option2_extra_pension, "isa": option2_isa},
        "Option 3": {"pension": option3_extra_pension, "isa": option3_isa},
    }

    results = []  # list to store outputs for each scenario

    for option, data in scenarios.items():
        extra_pension = data["pension"]
        isa_contrib = data["isa"]

        total_pension_contrib = annual_pension + extra_pension
        taxable_income = max(income_based - total_pension_contrib, 0)
        tax_paid = compute_tax(taxable_income)
        ni_paid = compute_ni(taxable_income)
        disposable_cash = income_based - total_pension_contrib - (tax_paid + ni_paid)
        cash_available = disposable_cash - isa_contrib

        # -------------------------------
        # Future Investment Projections
        # -------------------------------
        future_current_pot = current_pension * ((1 + pension_growth_rate) ** years_to_retirement)
        if pension_growth_rate != 0:
            future_annual_contrib = annual_pension * (((1 + pension_growth_rate) ** years_to_retirement - 1) / pension_growth_rate)
        else:
            future_annual_contrib = annual_pension * years_to_retirement
        future_extra_pension = extra_pension * ((1 + pension_growth_rate) ** years_to_retirement)
        future_pension_pot = future_current_pot + future_annual_contrib + future_extra_pension

        future_isa_pot = isa_contrib * ((1 + isa_growth_rate) ** years_to_retirement)

        # -------------------------------
        # Monthly Retirement Income Calculation (Post-Tax)
        # Assumption: 4% annual withdrawal rate; first 25% is tax‑free and remaining 75% is taxed (80% received)
        # -------------------------------
        monthly_pension_income = ((future_pension_pot * 0.25 * 0.04) +
                                  (future_pension_pot * 0.75 * 0.04 * 0.8)) / 12
        monthly_isa_income = (future_isa_pot * 0.04) / 12
        total_monthly_income = monthly_pension_income + monthly_isa_income

        results.append({
            "Option": option,
            "Total Pension Contribution (£)": total_pension_contrib,
            "Tax Paid (£)": tax_paid,
            "NI Paid (£)": ni_paid,
            "ISA Contribution (£)": isa_contrib,
            "Cash Available (£)": cash_available,
            "Future Pension Pot (£)": future_pension_pot,
            "Future ISA Pot (£)": future_isa_pot,
            "Monthly Retirement Income (Post-Tax) (£)": total_monthly_income
        })

    df = pd.DataFrame(results)
    st.markdown("---")
    st.header("2️⃣ Results Displayed")
    st.subheader("Breakdown of Each Contribution Option")
    numeric_cols = df.select_dtypes(include=['number']).columns
    df_styled = df.style.format({col: "{:,.2f}" for col in numeric_cols})
    st.dataframe(df_styled)

    # -------------------------------
    # Recommended Option Calculation
    # -------------------------------
    cash_values = df["Cash Available (£)"]
    income_values = df["Monthly Retirement Income (Post-Tax) (£)"]
    cash_min, cash_max = cash_values.min(), cash_values.max()
    income_min, income_max = income_values.min(), income_values.max()

    scores = []
    for idx, row in df.iterrows():
        norm_cash = (row["Cash Available (£)"] - cash_min) / (cash_max - cash_min) if cash_max - cash_min > 0 else 1
        norm_income = (row["Monthly Retirement Income (Post-Tax) (£)"] - income_min) / (income_max - income_min) if income_max - income_min > 0 else 1
        score = 0.5 * norm_cash + 0.5 * norm_income
        scores.append(score)

    df["Score"] = scores
    best_idx = df["Score"].idxmax()
    recommended_option = df.loc[best_idx, "Option"]
    st.subheader(f"🏆 Recommended Option: **{recommended_option}** (Best balance of Cash & Post-Tax Income)")

    # -------------------------------
    # Graph 1: Current Financial Breakdown
    # -------------------------------
    st.header("3️⃣ Current Financial Breakdown")
    labels = df["Option"].tolist()
    x = np.arange(len(labels))
    width = 0.5

    pension = df["Total Pension Contribution (£)"].tolist()
    tax_ni = (df["Tax Paid (£)"] + df["NI Paid (£)"]).tolist()
    isa_contrib = df["ISA Contribution (£)"].tolist()
    cash_avail = df["Cash Available (£)"].tolist()

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(labels))
    bar1 = ax1.bar(x, pension, width, label="Pension Contribution")
    bottom += np.array(pension)
    bar2 = ax1.bar(x, tax_ni, width, bottom=bottom, label="Tax + NI Paid")
    bottom += np.array(tax_ni)
    bar3 = ax1.bar(x, isa_contrib, width, bottom=bottom, label="ISA Contribution")
    bottom += np.array(isa_contrib)
    bar4 = ax1.bar(x, cash_avail, width, bottom=bottom, label="Cash Available")
    ax1.set_ylabel("Amount (£)")
    ax1.set_title("Current Financial Breakdown")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend(loc="upper left")
    st.pyplot(fig1)

    # -------------------------------
    # Graph 2: Retirement Projection Breakdown
    # -------------------------------
    st.header("4️⃣ Retirement Projection Breakdown")
    # For annual income, we multiply monthly retirement income by 12.
    pension_pot = df["Future Pension Pot (£)"].tolist()
    isa_pot = df["Future ISA Pot (£)"].tolist()
    annual_income = (df["Monthly Retirement Income (Post-Tax) (£)"] * 12).tolist()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(labels))
    bar1 = ax2.bar(x, pension_pot, width, label="Pension Pot")
    bottom += np.array(pension_pot)
    bar2 = ax2.bar(x, isa_pot, width, bottom=bottom, label="ISA Pot")
    bottom += np.array(isa_pot)
    bar3 = ax2.bar(x, annual_income, width, bottom=bottom, label="Annual Income (Post-Tax)")
    ax2.set_ylabel("Amount (£)")
    ax2.set_title("Retirement Projection Breakdown")
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend(loc="upper left")
    st.pyplot(fig2)

    st.markdown("---")
    st.write("### Summary")
    st.write(
        """
✅ Dynamic tax & NI calculations based on UK rates  
✅ Separate, real-time cash available calculations for each scenario displayed in the sidebar  
✅ Two separate graphs: one for current contributions & liquidity and another for retirement projections  
✅ Automatic recommendation based on balanced cash liquidity and post-tax retirement income  
        """
    )
    st.write("🚀 Next Steps: Run testing with various contribution levels, gather user feedback, and iterate.")

if __name__ == '__main__':
    main()
