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
st.title("Kommunernes og regionernes investeringer")

st.markdown(
    """ 
    **Hvis der anvendes data fra dette site i et journalistisk produkt eller i en anden sammenhæng, skal Gravercentret og Danwatch nævnes som kilde.** 
    **F.eks.: ”Det viser data, som er indsamlet og bearbejdet af Gravercentret, Danmarks Center for Undersøgende Journalistik, i samarbejde med Danwatch."**
            """
)
st.markdown(
    """
            Gravercentret, Danmarks Center for Undersøgende Journalistik, har sammen med Danwatch undersøgt, hvilke værdipapirer de danske kommuner og regioner har valgt at investere i. \n
            Vi har kortlagt, hvilke værdipapirer der ligger nede i de investeringsfonde og investeringsforeninger, som kommunerne og regionerne har sat deres penge i.
            Disse oplysninger har vi sammenholdt med lister over hvilke værdipapirer, der er sortlistet af danske banker og pensionsselskaber samt FN. \n
            Herunder kan du se oplysninger fra alle kommuner og regioner – og du kan downloade oplysningerne i Excel-format.
            I den lyseblå kolonne til venstre kan du søge i data.\n
            *OBS: D. 24/10 er data opdateret, da vi har fundet flere statsobligationer, der ikke var markeret fra start, og d. 07/11 er data opdateret, da markedsværdierne for nogle af Odense Kommunes værdipapirer er tilrettet.*

            """
)

with st.expander("🟥🟧🟨 - Læs mere: Hvordan skal tallene forstås?"):
    st.markdown(
        """
                I tabellen nedenfor finder du informationer om samtlige værdipapirer danske kommuner og regioner har oplyst at de havde investeret i i sommeren 2024. \n
                For hvert værdipapir er det angivet, hvilken kommune eller region, der er ejeren, hvad værdipapirets navn er, og hvor meget værdipapiret er værd.\n
                Værdipapirer, der er udpeget som problematiske, har vi markeret med enten en rød, en orange eller en gul firkant.\n
                Altså viser farverne om værdipapiret optræder på en eksklusionsliste over papirer danske banker, pensionsselskaber eller FN **ikke** vil investere i af forskellige etiske årsager.\n
                Vi har opdelt de problematiske værdipapirer i tre kategorier:\n
                - 🟥(1) - **Rød**: Disse værdipapirer er udstedt af problematiske selskaber.
                - 🟧(2) - **Orange**: Disse værdipapirer er udstedet af problematiske lande.
                - 🟨(3) - **Gul**: Disse værdipapirer er potentielt kontroversielle.\n
                For hvert værdipapir, der er markeret som problematisk, er der i tabellens kollonne "Eksklusion (Af hvem og hvorfor)" en forklaring på, hvem der har udpeget det som problematisk, og hvad årsagen er.\n
                Ved at scrolle til højre i skemaet kan man se en anden kolonne, der hedder ”sortlistet”. Her kan man se, hvor mange sorte lister fra danske banker, pensionsselskaber og FN det pågældende værdipapir er på. Står der eksempelvis 5, så er værdipapiret altså sortlistet af fem forskellige parter.\n
                Som tommelfingerregel kan man sige, at jo flere sorte lister et bestemt værdipapir er på, jo mere problematisk er det.\n
                I tabellen kan du også se, hvilken type værdipapiret er (f.eks. aktie eller obligation), værdipapirets ISIN-nummer (et unikt nummer ligesom et CPR-nummer), samt hvem der har udstedt papiret.\n
                Data kan downloades til Excel neden under tabellen.
                """
    )
    st.markdown(
        'Læs mere om vores metode i <a href="/Sådan_har_vi_gjort" target="_self">her</a>.',
        unsafe_allow_html=True,
    )


with st.expander("Sådan kommer du i gang.", icon="❔"):
    st.markdown(
        """
    Hvis du vil se oplysninger om en bestemt kommune eller regions investeringer, så kan du vælge et område i menuen ude til venstre her på forsiden.\n
    Data bliver så automatisk sorteret, så du kun ser oplysninger fra den ønskede kommune her på siden.\n
    Læs hvordan du kan forstå data i afsnittet "Hvordan skal tallene forstås?" ovenfor. \n
    Fokuserer du på bestemte værdipapirer, er det god ide at få bekræftet af kommunen eller regionen, at de fortsat ejer værdipapiret (gennem deres investeringsforening eller fond). Gravercentrets site giver nemlig kun et øjebliksbillede af, hvilke værdipapirer kommunerne oplyste at de ejede i sommeren 2024. \n
    Selv hvis kommunen ikke længere skulle eje et bestemt problematisk værdipapir, så kan der fortsat være en historie i, at de faktisk har ejet det. \n 
    Vil du vide mere om, hvorfor et værdipapir er problematisk, kan du i tabellen nedenfor se, hvilken bank eller pensionsselskab, der har beskrevet det som problematisk samt hvorfor. \n
    Herefter kan du kontakte de konkrete banker eller pensionsselskaber og bede dem uddybe, hvorfor de har sortlistet værdipapiret.\n

    """
    )

# Get unique municipalities and sort alphabetically
dropdown_options = get_unique_kommuner(df_pl)

# Get list of categories/reasons
unique_categories_list = get_unique_categories(df_pl)

# Costum choice for dropdown
all_values = "Hele landet"
municipalities = "Alle kommuner"
regions = "Alle regioner"
samsø = "Samsø"
læsø = "Læsø"

# Sidebar with selection options
with st.sidebar:
    user_choice = st.selectbox(
        "Vælg område:",
        dropdown_options,
        help="Skriv i boksen for at søge efter bestemt kommune/region.",
        placeholder="Vælg en kommune/region.",
    )

    selected_categories = st.multiselect(
        "Vælg problemkategori:",
        unique_categories_list,  # Options
        help="Vi har grupperet de mange årsager til eksklusion i hovedkategorier. Vælg én eller flere.",
        placeholder="",
    )

    search_query = st.text_input(
        "Fritekst søgning i tabellen:",
        "",
        help="Søg f.eks. efter et selskabs navn eller et ISIN-nummer.",
    )

    st.markdown(
        'Klik her for mere <a href="/Avanceret_søgning" target="_self">avanceret søgning</a>.',
        unsafe_allow_html=True,
    )

    # Filter dataframe based on user's selection
    filtered_df = filter_dataframe_by_choice(df_pl, user_choice)

    filtered_df = filter_df_by_search(filtered_df, search_query)

    filtered_df = filter_dataframe_by_category(filtered_df, selected_categories)

    filtered_df = fix_column_types_and_sort(filtered_df)

    if user_choice in [all_values, municipalities, regions] and search_query or selected_categories:
        if search_query:
            st.markdown(
                f"Antal kommuner/regioner, hvor '{search_query}' indgår: \n **{filtered_df.select(pl.col("Område").n_unique()).to_numpy()[0][0]}**"
            )
        else:
            st.markdown(
                f"Antal kommuner/regioner, der fremgår efter filtrering: \n **{filtered_df.select(pl.col("Område").n_unique()).to_numpy()[0][0]}**"
            )

    write_markdown_sidebar()

# Conditionally display the header based on whether a search query is provided
if selected_categories:
    select_string = ", ".join(selected_categories)
if search_query and not selected_categories:
    st.markdown(f'Data for "{user_choice}" og "{search_query}":')
if selected_categories and not search_query:
    st.subheader(f'Data for "{user_choice}" og "{select_string}":')
if selected_categories and search_query:
    st.subheader(f'Data for "{user_choice}", "{select_string}" og "{search_query}":')
if not selected_categories and not search_query:
    if user_choice == "Hele landet":
        st.markdown(
            f"### Data for alle kommuner og regioner: \n ##### (Vælg en enkelt kommune eller region i panelet til venstre)"
        )
    else:
        st.subheader(f'Data for "{user_choice}":')

# Create three columns
col1, col2 = st.columns([0.4, 0.6])

# Column 1: Pie chart for "Type" based on "Markedsværdi (DKK)"
with col1:
    if filtered_df.shape[0] == 0:
        st.subheader(f"**Der er ingen værdipapirer/investeringer.**")
    else:
        create_pie_chart(filtered_df)

# Column 2: Number of problematic investments
with col2:
    with st.container(border=True):
        header_numbers = "Antal investeringer udpeget som problematiske:"
        st.markdown(
            f'<h4 style="text-align:center;">{header_numbers}</h4>',
            unsafe_allow_html=True,
        )

        # Count the rows where 'Problematisk ifølge:' is not empty
        problematic_count = filtered_df.filter(filtered_df["Priority"].is_in([2, 3])).shape[0]
        problematic_count = format_number_european(problematic_count)
        st.markdown(
            f'<h2 style="text-align:center;">{problematic_count}</h2>',
            unsafe_allow_html=True,
        )

        problematic_count_red = filtered_df.filter(filtered_df["Priority"] == 3).shape[0]
        problematic_count_red = format_number_european(problematic_count_red)

        problematic_count_orange = filtered_df.filter(filtered_df["Priority"] == 2).shape[0]
        problematic_count_orange = format_number_european(problematic_count_orange)

        # Using HTML to style text with color
        st.markdown(
            f"<div style='text-align:center;'> Heraf <span style='color:red; font-size:25px;'><b>{problematic_count_red}</b></span> sortlistede værdipapirer fra selskaber, "
            f"og <span style='color:#FE6E34; font-size:25px;'><b>{problematic_count_orange}</b></span> statsobligationer fra sortlistede lande.</div>",
            unsafe_allow_html=True,
        )

        problematic_count_yellow = filtered_df.filter(filtered_df["Priority"] == 1).shape[0]
        problematic_count_yellow = format_number_european(problematic_count_yellow)

        # Using HTML to style text with color
        st.markdown(" ")
        st.markdown(
            f"<div style='text-align:center;'> Derudover er der <span style='color:#FEB342; font-size:20px;'><b>{problematic_count_yellow}</b></span> potentielt problematiske værdipapirer. </div>",
            unsafe_allow_html=True,
        )

    # Nøgletal
    with st.container(border=True):
        st.subheader("Nøgletal")

        # Calculate the total number of investments
        antal_inv = format_number_european(len(filtered_df))

        st.write(f"**Antal investeringer:** {antal_inv}")

        # Calculate the total sum of 'Markedsværdi (DKK)' and display it in both DKK and millions
        total_markedsvaerdi = (
            filtered_df.select(pl.sum("Markedsværdi (DKK)")).to_pandas().iloc[0, 0]
        ).astype(int)

        markedsvaerdi_euro = format_number_european(total_markedsvaerdi)
        markedsvaerdi_euro_short = round_to_million_or_billion(total_markedsvaerdi, 1)
        st.write(f"**Total markedsværdi (DKK):** {markedsvaerdi_euro} {markedsvaerdi_euro_short}")

        # Filter for problematic investments and calculate the total sum of their 'Markedsværdi (DKK)'
        prob_df = filtered_df.filter(filtered_df["Priority"].is_in([2, 3]))
        prob_markedsvaerdi = (
            prob_df.select(pl.sum("Markedsværdi (DKK)")).to_pandas().iloc[0, 0]
        ).astype(int)

        prob_markedsvaerdi_euro = format_number_european(prob_markedsvaerdi)
        prob_markedsvaerdi_euro_short = round_to_million_or_billion(prob_markedsvaerdi, 1)
        st.write(
            f"**Markedsværdi af problematiske investeringer (DKK):** {prob_markedsvaerdi_euro} {prob_markedsvaerdi_euro_short}"
        )

with st.spinner("Henter data.."):
    if user_choice == "Hele landet" and selected_categories == [] and search_query == "":
        # Cache the data for "Hele landet"
        hele_landet_data = cache_data_for_hele_landet(filtered_df)
        display_dataframe(hele_landet_data)
    else:
        # No caching for other cases
        display_df = format_and_display_data(filtered_df)
        display_dataframe(display_df)


st.markdown(
    "\\* *Markedsværdien (DKK) er et øjebliksbillede. Tallene er oplyst af kommunerne og regionerne selv ud fra deres senest opgjorte opgørelser.*"
)

generate_organization_links(filtered_df, "Problematisk ifølge:")
st.markdown(
    '**Mere om værdipapirer udpeget af Gravercentret:** <a href="/Mulige_historier" target="_self">Mulige historier</a>',
    unsafe_allow_html=True,
)

filtered_df = filtered_df.to_pandas()
filtered_df.drop("Priority", axis=1, inplace=True)


with st.spinner("Klargør download til Excel.."):
    if user_choice == "Hele landet" and selected_categories == [] and search_query == "":
        # Cache and create the Excel file for "Hele landet"
        hele_landet_excel = cache_excel_for_hele_landet(filtered_df)

        # Create a download button for the Excel file
        st.download_button(
            label="Download til Excel",
            data=hele_landet_excel,
            file_name=f"Investeringer for {user_choice}{search_query}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        excel_data = to_excel_function(filtered_df)

        # Create a download button
        st.download_button(
            label="Download til Excel",
            data=excel_data,
            file_name=f"Investeringer for {user_choice}{search_query}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

with st.spinner("Henter AI-tekster.."):
    if user_choice not in [all_values, municipalities, regions, samsø, læsø]:
        st.subheader(f"Eksklusionsårsager for investeringer foretaget af {user_choice}: ")

        st.info(
            """Listen nedenfor er genereret med kunstig intelligens, og der tages derfor forbehold for fejl.
            Nedenstående liste er muligvis ikke udtømmende.""",
            icon="ℹ️",
        )

        ai_text = get_ai_text(user_choice)

        st.markdown(ai_text)
