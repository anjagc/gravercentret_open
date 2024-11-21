import streamlit as st
import polars as pl
from utils.data_processing import (
    get_data,
    filter_df_by_search,
    fix_column_types_and_sort,
    format_number_european,
    round_to_million_or_billion,
    get_unique_categories,
    get_unique_kommuner,
    filter_dataframe_by_category,
    filter_dataframe_by_multiple_choices,
    to_excel_function,
    load_css,
    write_markdown_sidebar,
    create_user_session_log,
    generate_organization_links,
    display_dataframe,
)
from config import set_pandas_options, set_streamlit_options
from datetime import datetime

create_user_session_log("Avanceret søgning")

# Apply the settings
set_pandas_options()
set_streamlit_options()

st.logo("webapp/images/GC_png_oneline_lockup_Outline_Blaa_RGB.png")

load_css("webapp/style.css")

df_pl = get_data()

with st.sidebar:
    write_markdown_sidebar()


st.header("Søg videre i databasen")

default_priorities = [2, 3]
unique_categories_list = get_unique_categories(df_pl)

dropdown_areas = get_unique_kommuner(df_pl)

to_be_removed = {"Alle kommuner", "Alle regioner", "Hele landet"}
dropdown_areas = [item for item in dropdown_areas if item not in to_be_removed]

col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Fritekst søgning i data:", "")

    selected_priorities = st.multiselect(
        "Vælg type(r):",
        placeholder="Klik for at vælge én eller flere.",
        options=[None, 1, 2, 3],
        default=default_priorities,
        format_func=lambda x: {
            None: "Øvrige værdipapirer",
            1: "Potentielt problematiske",
            2: "Problematiske statsobligationer",
            3: "Problematiske selskaber",
        }.get(x, str(x)),
    )

with col2:
    selected_areas = st.multiselect(
        "Vælg område(r):",
        dropdown_areas,
        placeholder="Vælg flere kommuner eller regioner.",
    )
    selected_categories = st.multiselect(
        "Vælg problemkategori(er):",
        unique_categories_list,  # Options
        help="Vi har grupperet de mange årsager til eksklusion i hovedkategorier. Vælg én eller flere.",
        placeholder="Vælg problemkategori.",
    )


with st.expander("Om søgeværktøjet (klik for at folde ud eller ind)", expanded=True):
    st.markdown(
        """
    #### Sådan bruger du søgeværktøjet:
    Du søger ved først at vælge, hvilke grupper af værdipapirer du vil søge i. 
                    Vi har inddelt dem i fire grupper – værdipapirer fra problematiske selskaber, 
                    statsobligationerne fra problematiske stater, potentielt problematiske papirer og øvrige. 
                    Hvis du vil søge i hele databasen, skal du vælge dem alle til. Vil du blot søge i de problematiske papirer, 
                    så er de to relevante grupper tilføjet fra start som standard.\n
    Herefter kan du fritekstsøge og/eller vælge kategorier af problematiske papirer. Vær opmærksom på:

    - **Sprogforskelle:** Søgeværktøjet skelner mellem forskellige sprog. For eksempel vil en søgning på 'Kina' ikke give resultater for 'China'. Sørg derfor for at prøve flere varianter af søgeord.
    - **Eksperimentér med søgeord:** Hvis du ikke finder det, du leder efter med det samme, så prøv forskellige formuleringer eller delord af det, du søger.
    - **Download data:** Ønsker du at downloade top 10? Brug download-ikonet, som findes øverst i tabellen. I bunden er der en download-knap for det fulde data baseret på de valg, der er taget.
            """
    )

with st.expander("Disse områder har ingen problematiske investeringer:"):
    st.write(
        """
    23 kommuner og en region har ingen problematiske investeringer, som optræder på eksklusionslister fra banker, pensionsselskaber eller FN.\n

    Der er tale om følgende kommuner: Glostrup, Odsherred, Frederikssund, Hjørring, Stevns, Gladsaxe, Vordingborg, Halsnæs, Frederikshavn, Tårnby, Odder, Dragør, Albertslund, Ishøj, Langeland, Herlev, Gentofte, Sønderborg, Allerød, Ærø, Ringsted samt Læsø og Samsø, der slet ikke har investeringer.\n
    Region Syddanmark har heller ingen problematiske investeringer.\n

    """
    )


# Filter the dataframe by selected priorities and search query
filtered_df = (
    df_pl.filter(
        (df_pl["Priority"].is_in([p for p in selected_priorities if p is not None]))
        | (df_pl["Priority"].is_null())
    )
    if None in selected_priorities
    else df_pl.filter(df_pl["Priority"].is_in(selected_priorities))
)

filtered_df = filter_dataframe_by_multiple_choices(filtered_df, selected_areas)
filtered_df = filter_df_by_search(filtered_df, search_query)
filtered_df = filter_dataframe_by_category(filtered_df, selected_categories)
filtered_df = fix_column_types_and_sort(filtered_df)


# Function to get either top 10 municipalities or the full list based on market value or count
def get_municipalities(filtered_df, sort_by_col, top_n=None):
    kommune_summary = (
        filtered_df.group_by("Område")
        .agg(
            [
                pl.len().alias("Antal investeringer"),
                pl.sum("Markedsværdi (DKK)").alias("Total Markedsværdi (DKK)"),
            ]
        )
        .sort(sort_by_col, descending=True)
        .with_row_index("Placering")  # Add index column called 'Placering'
        .with_columns((pl.col("Placering") + 1).alias("Placering"))
    )

    # Format the 'Total Markedsværdi (DKK)' column to European formatting
    kommune_summary = kommune_summary.with_columns(
        pl.col("Total Markedsværdi (DKK)").map_elements(
            format_number_european, return_dtype=pl.Utf8
        )
    )

    # If top_n is set, return only the top_n rows
    if top_n:
        return kommune_summary.head(top_n)
    else:
        return kommune_summary


st.markdown(f"### Kommuner og regioner, der har investeret mest:")

# User choice to toggle between top 10 and full list
view_option = st.radio(
    "Vælg visningsmulighed:",
    ("Top 10", "Hele listen"),
    help="Skift mellem at se top 10 og hele listen.",
)


# Display top 10 or full list based on user selection
col_sum, col_count = st.columns(2)

with col_sum:
    if view_option == "Top 10":
        top_municipalities_sum = get_municipalities(
            filtered_df, "Total Markedsværdi (DKK)", top_n=10
        )
        st.write("##### Top 10 - størst samlet markedsværdi:")
    else:
        top_municipalities_sum = get_municipalities(filtered_df, "Total Markedsværdi (DKK)")
        st.write("##### Hele listen over kommuner med den største sum:")

    st.dataframe(
        top_municipalities_sum[
            ["Placering", "Område", "Total Markedsværdi (DKK)", "Antal investeringer"]
        ]
    )

with col_count:
    if view_option == "Top 10":
        top_municipalities_count = get_municipalities(filtered_df, "Antal investeringer", top_n=10)
        st.write("##### Top 10 - antal af investeringer:")
    else:
        top_municipalities_count = get_municipalities(filtered_df, "Antal investeringer")
        st.write("##### Hele listen over kommuner med det største antal af investeringer:")

    st.dataframe(top_municipalities_count)

# Display the filtered dataframe
st.write("##### Data baseret på søgning/filtre:")

with st.container(border=True):
    # Display search results
    st.markdown(
        f"***Antallet af kommuner/regioner:*** \n **{filtered_df.select(pl.col('Område').n_unique()).to_numpy()[0][0]}**"
    )

    # Calculate the sum of all investments in the "Markedsværdi (DKK)" column
    investment_sum = filtered_df.select(pl.col("Markedsværdi (DKK)").sum()).to_numpy()[0][0]

    # Create the conditional text for the sum
    if search_query or selected_categories:
        sum_text = f"***Summen af investeringerne:*** **{format_number_european(investment_sum)} DKK** **{round_to_million_or_billion(investment_sum, 1)}** (Baseret på filtrering) "
    else:
        sum_text = f"***Summen af investeringerne:*** **{format_number_european(investment_sum)} DKK** **{round_to_million_or_billion(investment_sum, 1)}**"

    # Display the sum with markdown
    st.markdown(f"{sum_text}")


display_df = filtered_df.with_columns(
    pl.col("Markedsværdi (DKK)")
    .map_elements(format_number_european, return_dtype=pl.Utf8)
    .alias("Markedsværdi (DKK)"),
)

display_dataframe(display_df)

st.markdown(
    "\\* *Markedsværdien (DKK) er et øjebliksbillede. Tallene er oplyst af kommunerne og regionerne selv ud fra deres senest opgjorte opgørelser.*"
)

generate_organization_links(filtered_df, "Problematisk ifølge:")
st.markdown(
    '**Mere om værdipapirer udpeget af Gravercentret:** <a href="/Mulige_historier" target="_self">Mulige historier</a>',
    unsafe_allow_html=True,
)

display_df = display_df.to_pandas()
display_df.drop("Priority", axis=1, inplace=True)

# Convert dataframe to Excel
excel_data = to_excel_function(display_df)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with st.spinner("Klargør download til Excel.."):
    # Create a download button
    st.download_button(
        label="Download til Excel",
        data=excel_data,
        file_name=f"Investeringer-{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
