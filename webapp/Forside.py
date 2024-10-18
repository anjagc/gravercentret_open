import streamlit as st
import polars as pl
import os
import sys
from utils.data_processing import (
    get_data,
    get_unique_kommuner,
    get_unique_categories,
    filter_dataframe_by_choice,
    filter_dataframe_by_category,
    generate_organization_links,
    filter_df_by_search,
    fix_column_types_and_sort,
    format_number_european,
    round_to_million_or_billion,
    get_ai_text,
    to_excel_function,
    load_css,
    write_markdown_sidebar,
    format_and_display_data,
    display_dataframe,
    create_user_session_log,
    cache_data_for_hele_landet,
    cache_excel_for_hele_landet,
)
from utils.plots import create_pie_chart
from config import set_pandas_options, set_streamlit_options

# Apply the settings
set_pandas_options()
set_streamlit_options()
load_css("webapp/style.css")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

create_user_session_log("Forside")

df_pl = get_data()

st.logo("webapp/images/GC_png_oneline_lockup_Outline_Blaa_RGB.png")

# Title of the app
st.title("Test af Streamlit")
