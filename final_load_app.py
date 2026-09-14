import streamlit as st
import pandas as pd
import os

# load history
if "load_history" not in st.session_state:
    st.session_state.load_history = []



st.set_page_config(
    page_title="Load Profit Analyzer",
    page_icon="🚛",
    layout="wide"
)

st.markdown(
    """
    <style>

    /* Main page background */
    .stApp {
        background-color: #e0f2fe;
    }

    /* Bordered Streamlit container - Load Information only */
    .st-key-load_info,
    .st-key-load_info > div,
    .st-key-load_info div[data-testid="stVerticalBlock"] {
       background-color: #1e3a8a  !important;
       border-radius: 12px !important;
    }

    /* Text inside the container */
    .st-key-load_info h3,
    .st-key-load_info label,
    .st-key-load_info p {
        color: white !important;
    }

    /* Number input box inside the container */
    .st-key-load_info div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: white !important;
    }

    /* Actual typing area inside the container */
    .st-key-load_info div[data-testid="stNumberInput"] input {
        background-color: white !important;
        color: black !important;
    }

    /* NEW: Load Analysis container background */
    .st-key-load_analysis,
    .st-key-load_analysis > div,
    .st-key-load_analysis div[data-testid="stVerticalBlock"] {
        background-color: #f8fafc !important;
        border-radius: 12px !important;
    }

    /* NEW: Turn each metric into a card */
    .st-key-load_analysis div[data-testid="stMetric"] {
        background-color: white !important;
        border-radius: 10px !important;
        padding: 14px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15) !important;
        border-left: 4px solid #1e3a8a !important;
        max-width: 220px !important;
    }

    /* NEW: Metric label styling */
    .st-key-load_analysis div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
    }

    /* NEW: Metric value styling */
    .st-key-load_analysis div[data-testid="stMetricValue"] {
        color: #1e3a8a !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Get the folder this script lives in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "file_logo.png")

logo_col, title_col = st.columns([1, 10],  gap="small")
with logo_col:
    st.image(logo_path, width=100)
with title_col:
    st.title("UBOX Solutions")


st.subheader("Load Tracker & Profit Analysis")
st.write("Analyze load profitability, operating costs, and deadhead efficiency before accepting a load.")

with st.container(border=True, key="load_info"):
    st.subheader("Load Information")

    with st.form("load_form", clear_on_submit=True):
        
        col_loc1, col_loc2 = st.columns(2)
        with col_loc1:
            pickup_location = st.text_input("Pick-up Location")
        with col_loc2:
            delivery_location = st.text_input("Delivery Destination")
            
        col_dt1, col_dt2, col_dt3, col_dt4 = st.columns(4)
        with col_dt1:
           pickup_date = st.date_input("Pick-up Date")
        with col_dt2:
           pickup_time = st.time_input("Pick-up Time")
        with col_dt3:
           dropoff_date = st.date_input("Drop-off Date")
        with col_dt4:
           dropoff_time = st.time_input("Drop-off Time")
            
        col1, col2, col3, col4,= st.columns(4)
        with col1:
            load_pay = st.number_input("Load Pay ($)", min_value=0.01)
        with col2:
            loaded_miles = st.number_input("Loaded miles ", min_value=0.01)
        with col3:
            deadhead_miles = st.number_input("Deadhead miles ", min_value=0.0)
        with col4:
            mpg = st.number_input("Truck MPG ", min_value=0.01)

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            diesel = st.number_input("Diesel price per gallon ($) ", min_value=0.01)
        with col6:
            driver_pay = st.number_input("Driver pay ($) ", min_value=0.0)
        with col7:
            tolls = st.number_input("Tolls ($) ", min_value=0.0)
        with col8:
            maint_cost_permile = st.number_input("Maintenance cost per mile ($) ", min_value=0.0)

        submitted = st.form_submit_button("Analyse Load", type="primary")

if submitted:
        total_miles = loaded_miles + deadhead_miles
        gallon_needed = total_miles / mpg
        fuel_cost = gallon_needed * diesel
        revenue_per_mile = load_pay / total_miles
        profit_after_fuel = load_pay - fuel_cost
        profit_per_mile = profit_after_fuel / total_miles
        maintenance_cost = total_miles * maint_cost_permile
        total_expenses = fuel_cost + driver_pay + tolls + maintenance_cost
        net_profit = load_pay - total_expenses
        net_profit_per_mile = net_profit / total_miles
        operating_margin = net_profit / load_pay * 100
        deadhead_pourcentage = (deadhead_miles / total_miles) * 100
        
        #save this load results into list
        new_entry = ({
            "pickup_location": pickup_location,
            "delivery_location": delivery_location,
            "pickup_datetime": f"{pickup_date} {pickup_time.strftime('%H:%M')}",
            "dropoff_datetime": f"{dropoff_date} {dropoff_time.strftime('%H:%M')}",
            "load_pay_$": load_pay,
            "total_miles": total_miles,
            "gallon_needed": gallon_needed,
            "fuel_cost_$": fuel_cost,
            "driver_pay_$" : driver_pay,
            "tolls_$" : tolls,
            "revenue_per_mile_$": revenue_per_mile,
            "profit_after_fuel_$": profit_after_fuel,
            "profit_per_mile_$": profit_per_mile,
            "maintenance_cost_$": maintenance_cost,
            "total_expenses_$": total_expenses,
            "net_profit_$": net_profit,
            "net_profit_per_mile_$": net_profit_per_mile,
            "operating_margin_%": operating_margin,
            "deadhead_pourcentage_%": deadhead_pourcentage
        })
        
        is_valid_input = load_pay > 0.01 and loaded_miles > 0.01 and mpg > 0.01 and diesel > 0.01 and pickup_location.strip() != "" and delivery_location.strip() != ""
        if is_valid_input:
            if not st.session_state.load_history or st.session_state.load_history[-1] != new_entry:
               st.session_state.load_history.append(new_entry)
            st.session_state.last_result = new_entry
        else:
            st.warning("Please fill in the load details before analyzing.")
            
if "last_result" in st.session_state:
    r = st.session_state.last_result
    with st.container(border=True, key="load_analysis"):
        st.subheader("Load Analysis")
        result1, result2, result3, result4, result5, result6 = st.columns(6)
        with result1:
            st.metric("Total Miles", f"{r['total_miles']:.2f}")
        with result2:
            st.metric("Net Profit $", f"${r['net_profit_$']:.2f}")
        with result3:
            st.metric("Net Profit per Mile $", f"${r['net_profit_per_mile_$']:.2f}")
        with result4:
            st.metric("Total Expenses $", f"${r['total_expenses_$']:.2f}")
        with result5:
            st.metric("Operating Margin %", f"{r['operating_margin_%']:.2f}%")
        with result6:
            st.metric("Deadhead Miles %", f"{r['deadhead_pourcentage_%']:.2f}%")

        st.divider()

        st.subheader("Revenue & Performance")
        rp1, rp2, rp3, rp4, rp5 = st.columns(5)
        with rp1:
            st.metric("Load pay $", f"{r['load_pay_$']:.2f}")
        with rp2:
            st.metric("Gallons needed", f"{r['gallon_needed']:.2f}")
        with rp3:
            st.metric("Revenue per mile $", f"${r['revenue_per_mile_$']:.2f}")
        with rp4:
            st.metric("Profit after fuel $", f"${r['profit_after_fuel_$']:.2f}")
        with rp5:
            st.metric("Profit per mile $", f"${r['profit_per_mile_$']:.2f}")

        st.subheader("Expenses")
        ex1, ex2, ex3, ex4 = st.columns(4)
        with ex1:
            st.metric("Fuel cost $", f"${r['fuel_cost_$']:.2f}")
        with ex2:
            st.metric("Maintenance cost $", f"${r['maintenance_cost_$']:.2f}")
        with ex3:
            st.metric("Driver pay $", f"${r['driver_pay_$']:.2f}")
        with ex4:
            st.metric("Tolls $", f"${r['tolls_$']:.2f}")

        st.divider()

        if r['net_profit_per_mile_$'] >= 1.50:
            st.success("GREAT LOAD")
        elif r['net_profit_per_mile_$'] >= 1.00:
            st.info("ACCEPTABLE LOAD")
        elif r['net_profit_per_mile_$'] >= 0.50:
            st.warning("LOW PROFIT LOAD")
        else:
            st.error("POOR LOAD")

        if r['deadhead_pourcentage_%'] <= 10:
            st.success(f"{r['deadhead_pourcentage_%']:.2f}% --> Deadhead - Excellent")
        elif r['deadhead_pourcentage_%'] <= 20:
            st.info(f"{r['deadhead_pourcentage_%']:.2f}% --> Deadhead - Good")
        elif r['deadhead_pourcentage_%'] <= 30:
            st.warning(f"{r['deadhead_pourcentage_%']:.2f}% --> Deadhead - High")
        else:
            st.error(f"{r['deadhead_pourcentage_%']:.2f}% --> Deadhead Miles - Very High")
                
if st.session_state.load_history:
    df = pd.DataFrame(st.session_state.load_history)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Total Loads Analyzed", len(df))
    with col_b:
        st.metric("Avg Profit per Mile", f"${df['net_profit_per_mile_$'].mean():.2f}")
    
    # NEW: define the styling function
    def highlight_columns(df):
        styles = pd.DataFrame('', index=df.index, columns=df.columns)
        styles['net_profit_per_mile_$'] = 'background-color: #bbf7d0'
        styles['total_expenses_$'] = 'background-color: #fecaca'
        return styles

    # CHANGED: was st.dataframe(df) — now applies the styling
    
    styled_df = df.style.apply(highlight_columns, axis=None)

    # NEW: convert to HTML and add header CSS
    html_table = styled_df.to_html()

    st.markdown(
        """
        <style>
        .load-history-table thead th {
            background-color: #1e3a8a !important;
            color: white !important;
            padding: 6px 10px !important;
            font-size: 13px !important;
            white-space: nowrap;
        }
        .load-history-table td {
            padding: 4px 10px !important;
            font-size: 13px !important;
            white-space: nowrap;
        }
        .load-history-table-wrapper {
            overflow-x: auto;
            width: 100%;
            border: 1px solid #999;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    f'<div class="load-history-table-wrapper"><div class="load-history-table">{html_table}</div></div>',
    unsafe_allow_html=True
    )
    
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
            "Download History as CSV",
            data=csv,
            file_name="load_history.csv",
            mime="text/csv"
        )
    
if st.button("Clear History"):
    st.session_state.load_history = []
    
    
    
        