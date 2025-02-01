import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # (kept if needed for any other purpose)

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
        # Assumption: 4% annual withdrawal rate; 25% of pension pot is tax‑free; 75% is taxable at 20% (80% received)
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
    # Prepare Data for Graphs
    # -------------------------------
    options_list = df["Option"].tolist()
    # Graph 1: Current Financial Breakdown (6 components)
    pension_vals = df["Total Pension Contribution (£)"].tolist()
    tax_ni_vals = (df["Tax Paid (£)"] + df["NI Paid (£)"]).tolist()
    isa_contrib_vals = df["ISA Contribution (£)"].tolist()
    cash_avail_vals = df["Cash Available (£)"].tolist()
    pension_pot_vals = df["Future Pension Pot (£)"].tolist()
    isa_pot_vals = df["Future ISA Pot (£)"].tolist()

    # Graph 2: Retirement Income Breakdown (Grouped bars)
    # Calculate gross monthly income, tax (from pension), and net (post-tax) monthly income.
    gross_income = ((df["Future Pension Pot (£)"] * 0.04) + (df["Future ISA Pot (£)"] * 0.04)) / 12
    tax_on_pension = (df["Future Pension Pot (£)"] * 0.75 * 0.04 * 0.2) / 12
    net_income = gross_income - tax_on_pension
    gross_income_vals = gross_income.tolist()
    tax_vals = tax_on_pension.tolist()
    net_income_vals = net_income.tolist()

    # -------------------------------
    # Create Graphs with Plotly and Show Side by Side
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        # Graph 1: Stacked Bar Chart for Current Financial Breakdown
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=options_list,
            y=pension_vals,
            name="Pension Contribution",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=options_list,
            y=tax_ni_vals,
            name="Tax + NI Paid",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=options_list,
            y=isa_contrib_vals,
            name="ISA Contribution",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=options_list,
            y=cash_avail_vals,
            name="Cash Available",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=options_list,
            y=pension_pot_vals,
            name="Pension Pot",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=options_list,
            y=isa_pot_vals,
            name="ISA Pot",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.update_layout(
            barmode='stack',
            title="Current Financial Breakdown",
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
            margin=dict(b=100)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Graph 2: Grouped Bar Chart for Retirement Income Breakdown
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=options_list,
            y=gross_income_vals,
            name="Gross Monthly Income",
            hovertemplate="£%{y:,.2f}"
        ))
        fig2.add_trace(go.Bar(
            x=options_list,
            y=tax_vals,
            name="Tax",
            hovertemplate="£%{y:,.2f}"
        ))
        fig2.add_trace(go.Bar(
            x=options_list,
            y=net_income_vals,
            name="Post Tax Income",
            hovertemplate="£%{y:,.2f}"
        ))
        fig2.update_layout(
            barmode='group',
            title="Retirement Income Breakdown",
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
            margin=dict(b=100)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.write("### Summary")
    st.write(
        """
✅ Interactive graphs display detailed amounts on hover  
✅ Two side-by-side graphs: one for current financial breakdown and one for retirement income breakdown  
✅ Clear legends placed outside the chart areas  
✅ Automatic recommendation based on balanced cash liquidity and post-tax retirement income  
        """
    )
    st.write("🚀 Next Steps: Test various input levels, gather user feedback, and iterate further.")

if __name__ == '__main__':
    main()
