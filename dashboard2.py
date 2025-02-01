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
      - £12,570 – £50,270: 10%
      - Above £50,270: 2%
    """
    ni = 0
    if income <= 12570:
        return 0

    if income > 12570:
        taxable = min(income, 50270) - 12570
        ni += taxable * 0.10

    if income > 50270:
        taxable = income - 50270
        ni += taxable * 0.02

    return ni

# -------------------------------
# Main App Function
# -------------------------------
def main():
    st.title("Pension & ISA Contribution Optimization Dashboard")
    
    st.markdown("---")
    

    # -------------------------------
    # Sidebar – User Inputs
    # -------------------------------
    st.sidebar.header("Income Details")
    annual_salary = st.sidebar.number_input("Annual Salary (£)", value=50000, step=1000)
    one_off_income = st.sidebar.number_input("One-Off Income (£)", value=0, step=100)

    st.sidebar.header("Pension Details")
    current_pension = st.sidebar.number_input("Current Pension Pot (£)", value=20000, step=1000)
    annual_pension = st.sidebar.number_input("Annual Pension Contribution (£)", value=5000, step=500)

    st.sidebar.header("Retirement")
    years_to_retirement = st.sidebar.number_input("Years to Retirement", value=30, step=1)

    st.sidebar.header("Contribution Options")
    st.sidebar.subheader("Additional Pension Contribution Options (£)")
    scenario_pension_1 = st.sidebar.number_input("Option 1 - Additional Pension Contribution (£)", value=10000, key="pension1")
    scenario_pension_2 = st.sidebar.number_input("Option 2 - Additional Pension Contribution (£)", value=15000, key="pension2")
    scenario_pension_3 = st.sidebar.number_input("Option 3 - Additional Pension Contribution (£)", value=20000, key="pension3")

    st.sidebar.subheader("ISA Contribution Options (£)")
    scenario_isa_1 = st.sidebar.number_input("Option 1 - ISA Contribution (£)", value=5000, key="isa1")
    scenario_isa_2 = st.sidebar.number_input("Option 2 - ISA Contribution (£)", value=10000, key="isa2")
    scenario_isa_3 = st.sidebar.number_input("Option 3 - ISA Contribution (£)", value=15000, key="isa3")

    st.sidebar.header("Growth Assumptions")
    pension_growth_rate = st.sidebar.number_input("Pension Growth Rate (%)", value=5.0, step=0.1) / 100.0
    isa_growth_rate = st.sidebar.number_input("ISA Growth Rate (%)", value=4.0, step=0.1) / 100.0

    st.sidebar.header("Calculation Method")
    calc_method = st.sidebar.radio(
        "Choose Calculation Method",
        (
            "Total Income Calculation (Annual + One-Off)",
            "One-Off Payment Calculation (One-Off - Pension)"
        )
    )

    # 1. Sidebar Cash Available Calculation
    # Cash Available = (Income based on toggle) - (Tax + NI) - Pension Contribution
    if calc_method == "Total Income Calculation (Annual + One-Off)":
        income_based_sidebar = annual_salary + one_off_income
    else:
        income_based_sidebar = one_off_income

    taxable_sidebar = max(income_based_sidebar - annual_pension, 0)
    tax_sidebar = compute_tax(taxable_sidebar)
    ni_sidebar = compute_ni(taxable_sidebar)
    cash_available_sidebar = income_based_sidebar - annual_pension - (tax_sidebar + ni_sidebar)
    st.sidebar.markdown("#### Calculated Cash Available (before extra contributions)")
    st.sidebar.write(f"**£{cash_available_sidebar:,.2f}**")

    # Determine income based on toggle for scenario calculations
    if calc_method == "Total Income Calculation (Annual + One-Off)":
        income_based = annual_salary + one_off_income
    else:
        income_based = one_off_income

    # -------------------------------
    # Backend Calculations for Each Scenario
    # -------------------------------
    scenarios = {
        "Option 1": {"pension": scenario_pension_1, "isa": scenario_isa_1},
        "Option 2": {"pension": scenario_pension_2, "isa": scenario_isa_2},
        "Option 3": {"pension": scenario_pension_3, "isa": scenario_isa_3},
    }

    results = []  # list to store outputs for each scenario

    for option, data in scenarios.items():
        extra_pension = data["pension"]
        isa_contrib = data["isa"]

        # Total pension contribution includes the annual pension plus the extra one-off contribution
        total_pension_contrib = annual_pension + extra_pension

        # Taxable income for the scenario
        taxable_income = max(income_based - total_pension_contrib, 0)
        tax_paid = compute_tax(taxable_income)
        ni_paid = compute_ni(taxable_income)

        # Compute disposable cash available before ISA investment
        disposable_cash_before_ISA = income_based - total_pension_contrib - (tax_paid + ni_paid)
        # Cap ISA contribution to the disposable cash available
        isa_contrib_used = min(isa_contrib, disposable_cash_before_ISA)
        # Cash Available (for stacked bar & scenario results) subtracts ISA contribution as well
        cash_available = disposable_cash_before_ISA - isa_contrib_used

        # Future Pension Pot Calculation
        future_current_pot = current_pension * ((1 + pension_growth_rate) ** years_to_retirement)
        if pension_growth_rate != 0:
            future_annual_contrib = annual_pension * (((1 + pension_growth_rate) ** years_to_retirement - 1) / pension_growth_rate)
        else:
            future_annual_contrib = annual_pension * years_to_retirement
        future_extra_pension = extra_pension * ((1 + pension_growth_rate) ** years_to_retirement)
        future_pension_pot = future_current_pot + future_annual_contrib + future_extra_pension

        # Future ISA Pot Calculation (using ISA contribution capped by available cash)
        future_isa_pot = isa_contrib_used * ((1 + isa_growth_rate) ** years_to_retirement)

        # Monthly Retirement Income Calculation (Post-Tax)
        # Assumption: 4% annual withdrawal rate.
        # 25% of the pension pot is tax‑free; the remaining 75% is taxed (here we assume an effective 20% tax rate on that portion).
        monthly_pension_income = ((future_pension_pot * 0.25 * 0.04) +
                                  (future_pension_pot * 0.75 * 0.04 * 0.8)) / 12
        monthly_isa_income = (future_isa_pot * 0.04) / 12
        total_monthly_income = monthly_pension_income + monthly_isa_income

        results.append({
            "Option": option,
            "Total Pension Contribution (£)": total_pension_contrib,
            "Tax Paid (£)": tax_paid,
            "NI Paid (£)": ni_paid,
            "Cash Available (£)": cash_available,
            "Future Pension Pot (£)": future_pension_pot,
            "Future ISA Pot (£)": future_isa_pot,
            "Monthly Retirement Income (Post-Tax) (£)": total_monthly_income
        })

    # Create a DataFrame from the results
    df = pd.DataFrame(results)


    st.subheader("Breakdown of Each Contribution Option")
    
    # Format only numeric columns for display
    numeric_cols = df.select_dtypes(include=['number']).columns
    df_styled = df.style.format({col: "{:,.2f}" for col in numeric_cols})
    st.dataframe(df_styled)

    # -------------------------------
    # Recommended Option Calculation
    # -------------------------------
    # We balance Cash Available and Monthly Retirement Income (Post-Tax) using equal weights.
    cash_values = df["Cash Available (£)"]
    income_values = df["Monthly Retirement Income (Post-Tax) (£)"]
    cash_min, cash_max = cash_values.min(), cash_values.max()
    income_min, income_max = income_values.min(), income_values.max()

    scores = []
    for idx, row in df.iterrows():
        # Normalize Cash Available
        if cash_max - cash_min > 0:
            norm_cash = (row["Cash Available (£)"] - cash_min) / (cash_max - cash_min)
        else:
            norm_cash = 1
        # Normalize Monthly Income
        if income_max - income_min > 0:
            norm_income = (row["Monthly Retirement Income (Post-Tax) (£)"] - income_min) / (income_max - income_min)
        else:
            norm_income = 1

        # Equal weighting: 50% for each metric
        score = 0.5 * norm_cash + 0.5 * norm_income
        scores.append(score)

    df["Score"] = scores
    best_idx = df["Score"].idxmax()
    recommended_option = df.loc[best_idx, "Option"]
    st.subheader(f"🏆 Recommended Option: **{recommended_option}** (Best balance of Cash and Post-Tax Income)")

    # -------------------------------
    # Stacked Bar Chart Visualization
    # -------------------------------
    st.header("3️⃣ Stacked Bar Graph Comparing Scenarios")
    labels = df["Option"].tolist()
    pension_values = df["Total Pension Contribution (£)"].tolist()
    tax_values = df["Tax Paid (£)"].tolist()
    ni_values = df["NI Paid (£)"].tolist()
    cash_values = df["Cash Available (£)"].tolist()

    x = np.arange(len(labels))
    width = 0.5

    fig, ax = plt.subplots(figsize=(8, 6))
    
    bar1 = ax.bar(x, pension_values, width, label="Pension Contribution")
    bar2 = ax.bar(x, tax_values, width, bottom=pension_values, label="Tax Paid")
    bottom_stack = np.array(pension_values) + np.array(tax_values)
    bar3 = ax.bar(x, ni_values, width, bottom=bottom_stack, label="NI Paid")
    bottom_stack += np.array(ni_values)
    bar4 = ax.bar(x, cash_values, width, bottom=bottom_stack, label="Cash Available")

    ax.set_ylabel("Amount (£)")
    ax.set_title("Breakdown of Each Contribution Option")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)

    st.pyplot(fig)



if __name__ == '__main__':
    main()
