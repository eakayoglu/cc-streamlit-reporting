# source venv/bin/activate
# streamlit run app.py  

# This script creates a Streamlit dashboard for Coffee Shop Reporting. It allows users to upload an Excel file, filter the data, and visualize various sales metrics through different tabs.
# Modules:
#     - pandas: For data manipulation and analysis.
#     - streamlit: For creating the web application.
#     - PIL: For image processing.
#     - plotly.express: For creating interactive plots.
# Functions:
#     - show_tab1(): Displays the main table with sales metrics and bar charts.
#     - show_tab2(): Displays a sunburst chart based on sales amount.
#     - show_tab3(): Displays a sunburst chart based on sales quantity.
#     - show_tab4(): Displays top 25 and bottom 25 products based on sales quantity with pie and bar charts.
#     - filter_dataframe(df: pd.DataFrame) -> pd.DataFrame: Adds a UI for filtering the dataframe.
#     - get_data_from_excel(): Reads data from the uploaded Excel file.
# Main Page:
#     - Displays the company logo.
#     - Allows users to upload an Excel file.
#     - Provides radio buttons to select different tabs for data visualization.
#     - Hides the Streamlit footer for a cleaner UI.

# Import necessary libraries
import pandas as pd
import streamlit as st 
from PIL import Image
import plotly.express as px

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(
    page_title="CC Reports - Dashboard", 
    page_icon=":bar_chart:", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def show_tab1(): 
    """
    Displays various sales reports in a Streamlit app.
    This function creates a Streamlit tab that shows different sales metrics and visualizations
    based on a filtered DataFrame (`filtered_df`). The visualizations include total sales amount,
    total items sold, and bar charts for sales by sub-category, category, and month.
    The function performs the following tasks:
    - Displays a loading spinner while the data is being processed.
    - Splits the layout into two columns to show a DataFrame and total sales metrics.
    - Creates and displays bar charts for sales amount by sub-category, category, and month.
    - Creates and displays bar charts for sales quantity by sub-category, category, and month.
    - Uses Plotly for creating the bar charts and Streamlit for displaying them.
    Note:
        The function assumes that `filtered_df` is a pre-defined DataFrame with the necessary columns:
        "TUTAR" (sales amount), "MIKTAR" (sales quantity), "TIPI" (sub-category), "TURU" (category), and "AY" (month).
    """
    with st.spinner("Loading..."):
        left_column, right_column = st.columns(2)

        with left_column:
            st.dataframe(filtered_df)
            
        with right_column:
            total_sales = float(filtered_df["TUTAR"].sum())
            st.subheader("Toplam Satış Tutarı:")
            st.info(f"{total_sales:,} TL")

            total_sales_item = float(filtered_df["MIKTAR"].sum())
            st.subheader("Toplam Satılan Ürün:")
            st.info(f"{total_sales_item:,} Adet")

        st.subheader("Reports - Tutar")
        tsales_by_sub_category = filtered_df.groupby(by=["TIPI"]).sum()[["TUTAR"]].sort_values(by="TUTAR")
        tfig_product_sales_sc = px.bar(
            tsales_by_sub_category,
            x="TUTAR",
            y=tsales_by_sub_category.index,
            orientation="h",
            title="<b>Alt Kategoriye Göre</b>",
            color_discrete_sequence=["#0083B8"] * len(tsales_by_sub_category),
            template="plotly_white",
        )
        tfig_product_sales_sc.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        tsales_by_category = (
            filtered_df.groupby(by=["TURU"]).sum()[["TUTAR"]].sort_values(by="TUTAR")
        )
        tfig_product_sales = px.bar(
            tsales_by_category,
            x="TUTAR",
            y=tsales_by_category.index,
            orientation="h",
            title="<b>Kategoriye Göre</b>",
            color_discrete_sequence=["#0083B8"] * len(tsales_by_category),
            template="plotly_white",
        )
        tfig_product_sales.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        # SALES BY Month [BAR CHART]
        tsales_by_month = filtered_df.groupby(by=["AY"]).sum()[["TUTAR"]]
        tfig_monthly_sales = px.bar(
            tsales_by_month,
            x=tsales_by_month.index,
            y="TUTAR",
            title="<b>Aylık Tutara Göre</b>",
            color_discrete_sequence=["#0083B8"] * len(tsales_by_month),
            template="plotly_white",
        )
        tfig_monthly_sales.update_layout(
            xaxis=dict(tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )


        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(tfig_monthly_sales, use_container_width=True)
        middle_column.plotly_chart(tfig_product_sales, use_container_width=True)
        right_column.plotly_chart(tfig_product_sales_sc, use_container_width=True)

        st.markdown("""---""")

        # SALES BY Category [BAR CHART] 2
        st.subheader("Reports - Miktar")
        ysales_by_category_s = (
            filtered_df.groupby(by=["TURU"]).sum()[["MIKTAR"]].sort_values(by="MIKTAR")
        )
        yfig_product_sales_s = px.bar(
            ysales_by_category_s,
            x="MIKTAR",
            y=ysales_by_category_s.index,
            orientation="h",
            title="<b>Kategoriye Göre</b>",
            color_discrete_sequence=["#0083B8"] * len(ysales_by_category_s),
            template="plotly_white",
        )
        yfig_product_sales_s.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        ysales_by_category_sd = (
            filtered_df.groupby(by=["TIPI"]).sum()[["MIKTAR"]].sort_values(by="MIKTAR")
        )
        yfig_product_sales_sd = px.bar(
            ysales_by_category_sd,
            x="MIKTAR",
            y=ysales_by_category_sd.index,
            orientation="h",
            title="<b>Alt Kategoriye Göre</b>",
            color_discrete_sequence=["#0083B8"] * len(ysales_by_category_sd),
            template="plotly_white",
        )
        yfig_product_sales_sd.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        # SALES BY Month [BAR CHART]
        ysales_by_month_t = filtered_df.groupby(by=["AY"]).sum()[["MIKTAR"]]
        yfig_monthly_sales_s = px.bar(
            ysales_by_month_t,
            x=ysales_by_month_t.index,
            y="MIKTAR",
            title="<b>Aylık Miktara Göre</b>",
            color_discrete_sequence=["#0083B8"] * len(ysales_by_month_t),
            template="plotly_white",
        )
        yfig_monthly_sales_s.update_layout(
            xaxis=dict(tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )


        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(yfig_monthly_sales_s, use_container_width=True)
        middle_column.plotly_chart(yfig_product_sales_s, use_container_width=True)
        right_column.plotly_chart(yfig_product_sales_sd, use_container_width=True)

def show_tab2():
    """
    Displays a sunburst chart in a Streamlit app.

    This function creates a sunburst chart using Plotly Express based on the 
    provided DataFrame `filtered_df`. The chart is displayed in a Streamlit 
    app with a loading spinner while the chart is being generated.

    The sunburst chart is structured with the following hierarchy:
    - 'AY' (Month)
    - 'TURU' (Type)
    - 'TIPI' (Subtype)

    The size of each segment in the sunburst chart is determined by the 'TUTAR' (Amount) column.

    Note:
        This function assumes that `st` (Streamlit) and `px` (Plotly Express) 
        have been imported and that `filtered_df` is a predefined DataFrame.

    Returns:
        None
    """
    with st.spinner("Loading..."):
        fig2 = px.sunburst(filtered_df, path=['AY', 'TURU', 'TIPI'], values='TUTAR', title="Tutara Göre")
        st.plotly_chart(fig2)

def show_tab3():
    """
    Displays a sunburst chart in Streamlit using Plotly.

    This function creates a sunburst chart based on the filtered DataFrame `filtered_df`.
    The chart is structured with the hierarchical path ['AY', 'TURU', 'TIPI'] and uses 'MIKTAR' 
    as the values. The chart is displayed with a title "Miktara Göre" and is shown within a 
    Streamlit spinner indicating a loading state.

    Returns:
        None
    """
    with st.spinner("Loading..."):
        fig = px.sunburst(filtered_df, path=['AY', 'TURU', 'TIPI'], values='MIKTAR', title="Miktara Göre")
        st.plotly_chart(fig)

def show_tab4():
    """
    Displays the fourth tab of the Streamlit application, which includes visualizations and data tables
    for the top 25 and bottom 25 products based on the 'MIKTAR' column.
    The function performs the following tasks:
    1. Displays a loading spinner while processing.
    2. Filters the top 25 and bottom 25 products by 'MIKTAR'.
    3. Displays a title and a dataframe for the top 25 products.
    4. Creates and displays pie charts for the top 25 products by 'TURU' and 'TIPI'.
    5. Creates and displays bar charts for the top 25 products by 'TURU' and 'TIPI'.
    6. Adds a horizontal rule to separate sections.
    7. Displays a title and a dataframe for the bottom 25 products.
    8. Creates and displays pie charts for the bottom 25 products by 'TURU' and 'TIPI'.
    9. Creates and displays bar charts for the bottom 25 products by 'TURU' and 'TIPI'.
    Note:
        This function assumes that `filtered_df`, `st`, and `px` are already defined and imported.
    """
    with st.spinner("Loading..."):
        dfx = filtered_df.nlargest(25, 'MIKTAR')
        dfy = filtered_df.nsmallest(25, 'MIKTAR')

        st.title("TOP 25")
        st.markdown("**En çok satan 25 ürün _(miktara göre)_**")
        st.dataframe(dfx)

        left_column, right_column = st.columns(2)
        with left_column:
            fig = px.pie(dfx, values='MIKTAR', names='TURU')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)
        with right_column:
            fig2 = px.pie(dfx, values='MIKTAR', names='TIPI')
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2)

        left_column, right_column = st.columns(2)
        with left_column:
            sales_by_category_s = dfx.groupby(by=["TURU"]).sum()[["MIKTAR"]].sort_values(by="MIKTAR")
            fig_product_sales_s = px.bar(
                sales_by_category_s,
                x="MIKTAR",
                y=sales_by_category_s.index,
                orientation="h",
                title="<b>Kategoriye Göre</b>",
                color_discrete_sequence=["#0083B8"] * len(sales_by_category_s),
                template="plotly_white",
            )
            fig_product_sales_s.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )
            st.plotly_chart(fig_product_sales_s)
        with right_column:
            sales_by_category_sd = dfx.groupby(by=["TIPI"]).sum()[["MIKTAR"]].sort_values(by="MIKTAR")

            fig_product_sales_sd = px.bar(
                sales_by_category_sd,
                x="MIKTAR",
                y=sales_by_category_sd.index,
                orientation="h",
                title="<b>Alt Kategoriye Göre</b>",
                color_discrete_sequence=["#0083B8"] * len(sales_by_category_sd),
                template="plotly_white",
            )
            fig_product_sales_sd.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )
            st.plotly_chart(fig_product_sales_sd)

        st.markdown("""---""")

        st.markdown("**En az satan 25 ürün _(miktara göre)_**")
        st.dataframe(dfy)
        left_column, right_column = st.columns(2)
        with left_column:
            figa = px.pie(dfy, values='MIKTAR', names='TURU')
            figa.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(figa)
        with right_column:
            figb = px.pie(dfy, values='MIKTAR', names='TIPI')
            figb.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(figb)
        
        left_column, right_column = st.columns(2)
        with left_column:
            sales_by_category_s1 = dfy.groupby(by=["TURU"]).sum()[["MIKTAR"]].sort_values(by="MIKTAR")
            fig_product_sales_s1 = px.bar(
                sales_by_category_s1,
                x="MIKTAR",
                y=sales_by_category_s1.index,
                orientation="h",
                title="<b>Kategoriye Göre</b>",
                color_discrete_sequence=["#0083B8"] * len(sales_by_category_s1),
                template="plotly_white",
            )
            fig_product_sales_s1.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )
            st.plotly_chart(fig_product_sales_s1)
        with right_column:
                sales_by_category_sd1 = dfy.groupby(by=["TIPI"]).sum()[["MIKTAR"]].sort_values(by="MIKTAR")

                fig_product_sales_sd1 = px.bar(
                    sales_by_category_sd1,
                    x="MIKTAR",
                    y=sales_by_category_sd1.index,
                    orientation="h",
                    title="<b>Alt Kategoriye Göre</b>",
                    color_discrete_sequence=["#0083B8"] * len(sales_by_category_sd1),
                    template="plotly_white",
                )
                fig_product_sales_sd1.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=(dict(showgrid=False))
                )
                st.plotly_chart(fig_product_sales_sd1)
   
# FILTERING THE LIST 
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 20:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df

@st.cache_data
def get_data_from_excel():
    """
    Fetches data from an uploaded Excel file.

    This function reads data from an Excel file using the `openpyxl` engine and 
    retrieves data from the sheet named "Monthly". The result is cached to 
    optimize performance for repeated calls with the same input.

    Returns:
        pandas.DataFrame: DataFrame containing the data from the "Monthly" sheet of the Excel file.
    """
    df =pd.read_excel(
            io=uploaded_file,
            engine="openpyxl",
            sheet_name="Monthly",
            )
    return df

# MAIN PAGE
image = Image.open('logo.jpg')
st.image(image)

st.title("Coffee Shop Reporting Dashboard")
st.success("** Note ** -> The sheet, named Monthly, will be import")

uploaded_file = st.file_uploader("Choose a excel file", type=["xlsx"])
if uploaded_file is not None:
    chsn = st.radio(
    "Tablo Seç:",
    ('Ana Tablo', 'Sunburst - Tutara Göre', 'Sunburst - Miktara Göre', 'Top 25'))

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    excel_df = get_data_from_excel()
    filtered_df = filter_dataframe(excel_df)

    if chsn == 'Ana Tablo':
        show_tab1()
    elif chsn == 'Sunburst - Tutara Göre':
        show_tab2()
    elif chsn == 'Sunburst - Miktara Göre':
        show_tab3()
    elif chsn == 'Top 25':
        show_tab4()



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)