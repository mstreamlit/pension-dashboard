import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -------------------------------
# Updated Tax Calculation Function for Full Income (2024/2025)
# -------------------------------
def compute_tax(full_income):
    """
    Compute UK Income Tax for full_income (after pension contributions) using 2024/2025 bands:
    
    - Personal Allowance (PA):
       • If full_income ≤ £100,000, PA = £12,570.
       • If full_income ≥ £125,140, PA = 0.
       • Otherwise, PA = 12,570 - ((full_income - 100,000) / 2).
       
    Tax bands (applied on income above PA):
       • 20% on income from effective PA up to £50,270.
       • 40% on income from £50,271 to £125,140.
       • 45% on any income above £125,140.
    """
    if full_income <= 100000:
        PA = 12570
    elif full_income >= 125140:
        PA = 0
    else:
        PA = 12570 - ((full_income - 100000) / 2)
    
    if full_income <= PA:
        return 0
    
    taxable_income = full_income - PA
    basic_band_limit = 50270
    higher_band_limit = 125140
    
    if full_income <= basic_band_limit:
        tax = taxable_income * 0.20
    elif full_income <= higher_band_limit:
        tax = (basic_band_limit - PA) * 0.20 + (full_income - basic_band_limit) * 0.40
    else:
        tax = (basic_band_limit - PA) * 0.20 + (higher_band_limit - basic_band_limit) * 0.40 + (full_income - higher_band_limit) * 0.45
    return tax

# -------------------------------
# Updated NI Calculation Function for Full Income (2024/2025)
# -------------------------------
def compute_ni(full_income):
    """
    Compute UK National Insurance (NI) for full_income using the 2024/2025 rates:
      - 0% on earnings up to £12,570
      - 8% on earnings between £12,570 and £50,270
      - 2% on earnings above £50,270
    """
    if full_income <= 12570:
        return 0
    ni = (min(full_income, 50270) - 12570) * 0.08
    if full_income > 50270:
        ni += (full_income - 50270) * 0.02
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
    
    # Determine income base (for threshold purposes, use full income)
    income_base = annual_salary + one_off_income  # always needed to determine thresholds
    
    # -------------------------------
    # One-Off Payment Calculation Adjustments
    # -------------------------------
    if calc_method == "One-Off Payment Calculation (One-Off - Pension)":
        # For bonus tax/NI calculations, we subtract only one month's pension.
        monthly_pension_deduction = 333.17  # constant given
        # Bonus taxable amount:
        taxable_bonus = one_off_income - monthly_pension_deduction
        
        # Determine bonus tax rate using income_base thresholds:
        if income_base >= 125140:
            bonus_tax_rate = 0.45
        elif income_base >= 50271:
            bonus_tax_rate = 0.40
        elif income_base >= 12571:
            bonus_tax_rate = 0.20
        else:
            bonus_tax_rate = 0
        bonus_tax = taxable_bonus * bonus_tax_rate
        
        # Determine bonus NI rate using NI bands for full income:
        if income_base >= 50270:
            bonus_ni_rate = 0.02
        elif income_base >= 12571:
            bonus_ni_rate = 0.08
        else:
            bonus_ni_rate = 0
        bonus_ni = taxable_bonus * bonus_ni_rate
        
        bonus_cash_available = one_off_income - (bonus_tax + bonus_ni)
    
    # -------------------------------
    # Sidebar – Scenario Options & Cash Available Calculations
    # -------------------------------
    st.sidebar.header("Scenario Options")
    
    # For each option, the only variation in bonus calculation (if one-off mode)
    # is the ISA contribution.
    
    # Option 1
    st.sidebar.markdown("##### Option 1")
    option1_extra_pension = st.sidebar.number_input("Additional Pension Contribution (£)", value=0, key="option1_pension")
    option1_isa = st.sidebar.number_input("ISA Contribution (£)", value=20000, key="option1_isa")
    option1_total_pension = annual_pension + option1_extra_pension
    if calc_method == "One-Off Payment Calculation (One-Off - Pension)":
        option1_cash_available = bonus_cash_available - option1_isa
    else:
        # For Total Income Calculation, deduct the full annual pension contribution (base+extra).
        income_after_pension_1 = max(income_base - option1_total_pension, 0)
        tax_option1 = compute_tax(income_after_pension_1)
        ni_option1 = compute_ni(income_after_pension_1)
        disposable_option1 = income_after_pension_1 - (tax_option1 + ni_option1)
        option1_cash_available = disposable_option1 - option1_isa
    st.sidebar.markdown("**Cash Available for Option 1:**")
    st.sidebar.write(f"£{option1_cash_available:,.2f}")
    
    # Option 2
    st.sidebar.markdown("##### Option 2")
    option2_extra_pension = st.sidebar.number_input("Additional Pension Contribution (£)", value=10554, key="option2_pension")
    option2_isa = st.sidebar.number_input("ISA Contribution (£)", value=20000, key="option2_isa")
    option2_total_pension = annual_pension + option2_extra_pension
    if calc_method == "One-Off Payment Calculation (One-Off - Pension)":
        option2_cash_available = bonus_cash_available - option2_isa
    else:
        income_after_pension_2 = max(income_base - option2_total_pension, 0)
        tax_option2 = compute_tax(income_after_pension_2)
        ni_option2 = compute_ni(income_after_pension_2)
        disposable_option2 = income_after_pension_2 - (tax_option2 + ni_option2)
        option2_cash_available = disposable_option2 - option2_isa
    st.sidebar.markdown("**Cash Available for Option 2:**")
    st.sidebar.write(f"£{option2_cash_available:,.2f}")
    
    # Option 3
    st.sidebar.markdown("##### Option 3")
    option3_extra_pension = st.sidebar.number_input("Additional Pension Contribution (£)", value=20000, key="option3_pension")
    option3_isa = st.sidebar.number_input("ISA Contribution (£)", value=0, key="option3_isa")
    option3_total_pension = annual_pension + option3_extra_pension
    if calc_method == "One-Off Payment Calculation (One-Off - Pension)":
        option3_cash_available = bonus_cash_available - option3_isa
    else:
        income_after_pension_3 = max(income_base - option3_total_pension, 0)
        tax_option3 = compute_tax(income_after_pension_3)
        ni_option3 = compute_ni(income_after_pension_3)
        disposable_option3 = income_after_pension_3 - (tax_option3 + ni_option3)
        option3_cash_available = disposable_option3 - option3_isa
    st.sidebar.markdown("**Cash Available for Option 3:**")
    st.sidebar.write(f"£{option3_cash_available:,.2f}")
    
    # -------------------------------
    # Main Calculations for Each Scenario (For Future Projections and Retirement)
    # -------------------------------
    # For future projections we always use the full annual pension (3300 + extra) for ongoing contributions.
    scenarios = {
        "Option 1": {"pension": option1_extra_pension, "isa": option1_isa},
        "Option 2": {"pension": option2_extra_pension, "isa": option2_isa},
        "Option 3": {"pension": option3_extra_pension, "isa": option3_isa},
    }
    
    results = []  # to store outputs for each scenario
    
    for option, data in scenarios.items():
        extra_pension = data["pension"]
        isa_contrib = data["isa"]
    
        total_pension_contrib = annual_pension + extra_pension
        if calc_method == "One-Off Payment Calculation (One-Off - Pension)":
            # For bonus tax, we already computed bonus_tax and bonus_ni once.
            tax_paid_value = bonus_tax
            ni_paid_value = bonus_ni
            cash_available_value = bonus_cash_available - isa_contrib
        else:
            income_after_pension = max(income_base - total_pension_contrib, 0)
            tax_paid_value = compute_tax(income_after_pension)
            ni_paid_value = compute_ni(income_after_pension)
            disposable_cash = income_after_pension - (tax_paid_value + ni_paid_value)
            cash_available_value = disposable_cash - isa_contrib
    
        # Future Investment Projections (common to both methods)
        future_current_pot = current_pension * ((1 + pension_growth_rate) ** years_to_retirement)
        if pension_growth_rate != 0:
            future_annual_contrib = annual_pension * (((1 + pension_growth_rate) ** years_to_retirement - 1) / pension_growth_rate)
        else:
            future_annual_contrib = annual_pension * years_to_retirement
        future_extra_pension = extra_pension * ((1 + pension_growth_rate) ** years_to_retirement)
        future_pension_pot = future_current_pot + future_annual_contrib + future_extra_pension
        future_isa_pot = isa_contrib * ((1 + isa_growth_rate) ** years_to_retirement)
    
        # Monthly Retirement Income Calculation (Post-Tax)
        monthly_pension_income = ((future_pension_pot * 0.25 * 0.04) +
                                  (future_pension_pot * 0.75 * 0.04 * 0.8)) / 12
        monthly_isa_income = (future_isa_pot * 0.04) / 12
        total_monthly_income = monthly_pension_income + monthly_isa_income
        # Gross Monthly Income (Before tax on pension)
        gross_monthly_income = ((future_pension_pot * 0.04) + (future_isa_pot * 0.04)) / 12
    
        results.append({
            "Option": option,
            "Total Pension Contribution (£)": total_pension_contrib,
            "Tax Paid (£)": tax_paid_value,
            "NI Paid (£)": ni_paid_value,
            "ISA Contribution (£)": isa_contrib,
            "Cash Available (£)": cash_available_value,
            "Future Pension Pot (£)": future_pension_pot,
            "Future ISA Pot (£)": future_isa_pot,
            "Monthly Retirement Income (Post-Tax) (£)": total_monthly_income,
            "Gross Monthly Income (£)": gross_monthly_income
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
    # Create x-axis labels as two rows: "Option X" on the first row and the additional pension contribution on the second.
    option_labels = [
        f"{row['Option']}<br>{row['Total Pension Contribution (£)'] - annual_pension:,.0f}"
        for idx, row in df.iterrows()
    ]
    
    # Graph 1: Current Financial Breakdown (6 components)
    pension_vals = df["Total Pension Contribution (£)"].tolist()
    tax_ni_vals = (df["Tax Paid (£)"] + df["NI Paid (£)"]).tolist()
    isa_contrib_vals = df["ISA Contribution (£)"].tolist()
    cash_avail_vals = df["Cash Available (£)"].tolist()
    pension_pot_vals = df["Future Pension Pot (£)"].tolist()
    isa_pot_vals = df["Future ISA Pot (£)"].tolist()
    
    # Graph 2: Retirement Income Breakdown (Stacked)
    # Split the retirement income into three stacks:
    # - Pension Tax = Future Pension Pot * 0.75 * 0.04 * 0.2 / 12
    # - ISA Income = Future ISA Pot * 0.04 / 12
    # - Net Pension Income = (Monthly Retirement Income (Post-Tax) - ISA Income)
    pension_tax_vals = (df["Future Pension Pot (£)"] * 0.75 * 0.04 * 0.2 / 12).tolist()
    isa_income_vals = (df["Future ISA Pot (£)"] * 0.04 / 12).tolist()
    net_pension_income_vals = (
        df["Monthly Retirement Income (Post-Tax) (£)"] - (df["Future ISA Pot (£)"] * 0.04 / 12)
    ).tolist()
    
    # -------------------------------
    # Create Graphs with Plotly and Show Side by Side
    # -------------------------------
    graph_height = 500
    common_margin = dict(l=50, r=50, t=50, b=150)
    
    col1, col_gap, col2 = st.columns([1, 0.1, 1])
    
    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=option_labels,
            y=pension_vals,
            name="Pension Contribution",
            marker_color="#2E8B57",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=option_labels,
            y=tax_ni_vals,
            name="Tax + NI Paid",
            marker_color="#B22222",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=option_labels,
            y=isa_contrib_vals,
            name="ISA Contribution",
            marker_color="#66CDAA",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=option_labels,
            y=cash_avail_vals,
            name="Cash Available",
            marker_color="#32CD32",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=option_labels,
            y=pension_pot_vals,
            name="Pension Pot",
            marker_color="#1E90FF",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.add_trace(go.Bar(
            x=option_labels,
            y=isa_pot_vals,
            name="ISA Pot",
            marker_color="#87CEFA",
            hovertemplate="£%{y:,.2f}"
        ))
        fig1.update_layout(
            barmode='stack',
            title="Current Financial Breakdown",
            xaxis_title="Options",
            yaxis_title="Amount (£)",
            xaxis=dict(tickangle=0),
            legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center"),
            margin=common_margin,
            height=graph_height,
            width=800
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=option_labels,
            y=pension_tax_vals,
            name="Pension Tax",
            marker_color="#DC143C",
            hovertemplate="£%{y:,.2f}"
        ))
        fig2.add_trace(go.Bar(
            x=option_labels,
            y=net_pension_income_vals,
            name="Net Pension Income",
            marker_color="#228B22",
            hovertemplate="£%{y:,.2f}"
        ))
        fig2.add_trace(go.Bar(
            x=option_labels,
            y=isa_income_vals,
            name="ISA Income",
            marker_color="#FF8C00",
            hovertemplate="£%{y:,.2f}"
        ))
        fig2.update_layout(
            barmode='stack',
            title="Retirement Income Breakdown",
            xaxis_title="Options",
            yaxis_title="Monthly Income (£)",
            xaxis=dict(tickangle=0),
            legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center"),
            margin=common_margin,
            height=graph_height,
            width=800
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    st.write("### Summary")
    st.write(
        """
✅ Both graphs now have consistent height, width, and margins with legends split into multiple rows.
✅ X-axis labels are displayed on two lines (option number and additional pension contribution).
✅ Graph 1 (stacked): Shows current contributions & liquidity.
✅ Graph 2 (stacked): Breaks down retirement income into Pension Tax, Net Pension Income, and ISA Income.
✅ Automatic recommendation is provided based on balanced cash liquidity and post-tax retirement income.
        """
    )
    st.write("🚀 Next Steps: Test various input levels, gather user feedback, and iterate further.")
    
if __name__ == '__main__':
    main()
