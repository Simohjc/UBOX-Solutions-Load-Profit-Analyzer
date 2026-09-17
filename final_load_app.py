import streamlit as st
import pandas as pd
import os
import psycopg2


# connectiong python with database and saving all data in the databaase as table
conn = psycopg2.connect(
    host = "localhost",
    dbname = "ubox_loads",
    user = "postgres",
    password = "123love"
)
cursor = conn.cursor()

#create table for saving data in the database ubox_loads
cursor.execute("""
      create table if not exists tracking_loads(
          id serial primary key,
          pickup_location text not null,
          delivery_location text not null,
          pickup_datetime timestamp not null,         
          dropoff_datetime timestamp not null,      
          load_pay_dollar numeric not null,         
          total_miles numeric not null,      
          gallon_needed numeric not null,           
          fuel_cost_dollar numeric not  null,          
          driver_pay_dollar numeric not null,          
          tolls_dollar  numeric not null,      
          revenue_per_mile_dollar numeric not null,         
          profit_after_fuel_dollar numeric not null,      
          profit_per_mile_dollar numeric not null,       
          maintenance_cost_dollar numeric not null,            
          total_expenses_dollar numeric not null,           
          net_profit_dollar numeric not null,         
          net_profit_per_mile_dollar numeric not null,         
          operating_margin_percent numeric not null,          
          deadhead_pourcentage_percent numeric not null          
      )         
""")
conn.commit()

class Load:
    def __init__(self,pickup_location,delivery_location,pickup_datetime,
                 dropoff_datetime,load_pay_dollar,total_miles,gallon_needed,
                 fuel_cost_dollar,driver_pay_dollar,tolls_dollar,revenue_per_mile_dollar,profit_after_fuel_dollar,
                 profit_per_mile_dollar,maintenance_cost_dollar,total_expenses_dollar,net_profit_dollar,
                 net_profit_per_mile_dollar,operating_margin_percent,deadhead_pourcentage_percent):
        
                  self.pickup_location = pickup_location
                  self.delivery_location = delivery_location
                  self.pickup_datetime = pickup_datetime    
                  self.dropoff_datetime =  dropoff_datetime   
                  self.load_pay_dollar = load_pay_dollar      
                  self.total_miles = total_miles    
                  self.gallon_needed =  gallon_needed       
                  self.fuel_cost_dollar =  fuel_cost_dollar       
                  self.driver_pay_dollar =   driver_pay_dollar     
                  self.tolls_dollar  = tolls_dollar    
                  self.revenue_per_mile_dollar =   revenue_per_mile_dollar    
                  self.profit_after_fuel_dollar =  profit_after_fuel_dollar    
                  self.profit_per_mile_dollar =  profit_per_mile_dollar    
                  self.maintenance_cost_dollar =   maintenance_cost_dollar        
                  self.total_expenses_dollar = total_expenses_dollar         
                  self.net_profit_dollar =  net_profit_dollar      
                  self.net_profit_per_mile_dollar =   net_profit_per_mile_dollar     
                  self.operating_margin_percent =   operating_margin_percent      
                  self.deadhead_pourcentage_percent = deadhead_pourcentage_percent
                  
    def describe(self):
      return (f"Load: {self.pickup_location} -> {self.delivery_location} | "
             f"Pay: ${self.load_pay_dollar} | Miles: {self.total_miles} | "
             f"Net Profit: ${self.net_profit_dollar} | Profit/Mile: ${self.net_profit_per_mile_dollar}")
      
def add_load(cursor, conn, load):
    cursor.execute(
        """
          insert into tracking_loads(
           pickup_location, delivery_location, pickup_datetime, dropoff_datetime,
            load_pay_dollar, total_miles, gallon_needed, fuel_cost_dollar, driver_pay_dollar,
            tolls_dollar, revenue_per_mile_dollar, profit_after_fuel_dollar, profit_per_mile_dollar,
            maintenance_cost_dollar, total_expenses_dollar, net_profit_dollar,
            net_profit_per_mile_dollar, operating_margin_percent, deadhead_pourcentage_percent  
          ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        
        """,
        (
            load.pickup_location, load.delivery_location, load.pickup_datetime, load.dropoff_datetime,
            load.load_pay_dollar, load.total_miles, load.gallon_needed, load.fuel_cost_dollar,
            load.driver_pay_dollar, load.tolls_dollar, load.revenue_per_mile_dollar,
            load.profit_after_fuel_dollar, load.profit_per_mile_dollar, load.maintenance_cost_dollar,
            load.total_expenses_dollar, load.net_profit_dollar, load.net_profit_per_mile_dollar,
            load.operating_margin_percent, load.deadhead_pourcentage_percent   
        )
    )
    conn.commit()






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
            "load_pay_dollar": load_pay,
            "total_miles": total_miles,
            "gallon_needed": gallon_needed,
            "fuel_cost_dollar": fuel_cost,
            "driver_pay_dollar" : driver_pay,
            "tolls_dollar" : tolls,
            "revenue_per_mile_dollar": revenue_per_mile,
            "profit_after_fuel_dollar": profit_after_fuel,
            "profit_per_mile_dollar": profit_per_mile,
            "maintenance_cost_dollar": maintenance_cost,
            "total_expenses_dollar": total_expenses,
            "net_profit_dollar": net_profit,
            "net_profit_per_mile_dollar": net_profit_per_mile,
            "operating_margin_percent": operating_margin,
            "deadhead_pourcentage_percent": deadhead_pourcentage
        })
        
        is_valid_input = load_pay > 0.01 and loaded_miles > 0.01 and mpg > 0.01 and diesel > 0.01 and pickup_location.strip() != "" and delivery_location.strip() != ""
        if is_valid_input:
            if not st.session_state.load_history or st.session_state.load_history[-1] != new_entry:
               st.session_state.load_history.append(new_entry)
            st.session_state.last_result = new_entry
            #new: also save to the database
            db_load = Load(**new_entry)
            add_load(cursor, conn, db_load)
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
            st.metric("Net Profit $", f"${r['net_profit_dollar']:.2f}")
        with result3:
            st.metric("Net Profit per Mile $", f"${r['net_profit_per_mile_dollar']:.2f}")
        with result4:
            st.metric("Total Expenses $", f"${r['total_expenses_dollar']:.2f}")
        with result5:
            st.metric("Operating Margin %", f"{r['operating_margin_percent']:.2f}%")
        with result6:
            st.metric("Deadhead Miles %", f"{r['deadhead_pourcentage_percent']:.2f}%")

        st.divider()

        st.subheader("Revenue & Performance")
        rp1, rp2, rp3, rp4, rp5 = st.columns(5)
        with rp1:
            st.metric("Load pay $", f"{r['load_pay_dollar']:.2f}")
        with rp2:
            st.metric("Gallons needed", f"{r['gallon_needed']:.2f}")
        with rp3:
            st.metric("Revenue per mile $", f"${r['revenue_per_mile_dollar']:.2f}")
        with rp4:
            st.metric("Profit after fuel $", f"${r['profit_after_fuel_dollar']:.2f}")
        with rp5:
            st.metric("Profit per mile $", f"${r['profit_per_mile_dollar']:.2f}")

        st.subheader("Expenses")
        ex1, ex2, ex3, ex4 = st.columns(4)
        with ex1:
            st.metric("Fuel cost $", f"${r['fuel_cost_dollar']:.2f}")
        with ex2:
            st.metric("Maintenance cost $", f"${r['maintenance_cost_dollar']:.2f}")
        with ex3:
            st.metric("Driver pay $", f"${r['driver_pay_dollar']:.2f}")
        with ex4:
            st.metric("Tolls $", f"${r['tolls_dollar']:.2f}")

        st.divider()

        if r['net_profit_per_mile_dollar'] >= 1.50:
            st.success("GREAT LOAD")
        elif r['net_profit_per_mile_dollar'] >= 1.00:
            st.info("ACCEPTABLE LOAD")
        elif r['net_profit_per_mile_dollar'] >= 0.50:
            st.warning("LOW PROFIT LOAD")
        else:
            st.error("POOR LOAD")

        if r['deadhead_pourcentage_percent'] <= 10:
            st.success(f"{r['deadhead_pourcentage_percent']:.2f}% --> Deadhead - Excellent")
        elif r['deadhead_pourcentage_percent'] <= 20:
            st.info(f"{r['deadhead_pourcentage_percent']:.2f}% --> Deadhead - Good")
        elif r['deadhead_pourcentage_percent'] <= 30:
            st.warning(f"{r['deadhead_pourcentage_percent']:.2f}% --> Deadhead - High")
        else:
            st.error(f"{r['deadhead_pourcentage_percent']:.2f}% --> Deadhead Miles - Very High")
                
if st.session_state.load_history:
    df = pd.DataFrame(st.session_state.load_history)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Total Loads Analyzed", len(df))
    with col_b:
        st.metric("Avg Profit per Mile", f"${df['net_profit_per_mile_dollar'].mean():.2f}")
    
    # NEW: define the styling function
    def highlight_columns(df):
        styles = pd.DataFrame('', index=df.index, columns=df.columns)
        styles['net_profit_per_mile_dollar'] = 'background-color: #bbf7d0'
        styles['total_expenses_dollar'] = 'background-color: #fecaca'
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
    
    
    
        
