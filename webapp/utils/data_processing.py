import numpy as np
import babel.numbers
from sqlalchemy import create_engine
import polars as pl
import pandas as pd
import streamlit as st
import re
from datetime import timedelta
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
from io import BytesIO


@st.cache_data(show_spinner="Indlæser data")  # , ttl=timedelta(hours=10)
def get_data():
    engine = create_engine(
        "sqlite:///data/investerings_database_encrypted_new.db"
    )  # Ret efter udgivelse

    query = """
        SELECT [Kommune] AS [Område], [ISIN kode], [Værdipapirets navn], 
        [Udsteder], [Markedsværdi (DKK)], [Type], 
        [Problematisk ifølge:], 
        [Årsag til eksklusion] AS [Eksklusion (Af hvem og hvorfor)], 
        [Sortlistet],
        [Problemkategori],
        [Priority],
        CASE 
            WHEN [OBS_Type] = 'red' THEN '🟥(1)'
            WHEN [OBS_Type] = 'orange' THEN '🟧(2)'
            WHEN [OBS_Type] = 'yellow' THEN '🟨(3)'
            ELSE ''
        END AS OBS
        FROM kommunale_regioner_investeringer;
    """

    # Execute the query and load the result into a Polars DataFrame
    with engine.connect() as conn:
        df_polars = pl.read_database(query, conn)

    df_pandas = df_polars.to_pandas()

    return df_pandas


# Decrypt data using AES-CBC mode
def aes_decrypt(encrypted_data, key):
    if encrypted_data is None:
        return None  # Handle None values gracefully

    # Proceed with decryption if the data is not None
    encrypted_data = base64.b64decode(encrypted_data.encode())  # Decode Base64 to bytes
    iv = encrypted_data[:16]  # Extract the first 16 bytes as the IV
    ciphertext = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode()


# Function to decrypt specified columns of the DataFrame using AES-CBC
@st.cache_data(show_spinner="Dekrypterer data", ttl=timedelta(hours=10))
def decrypt_dataframe(df, key, col_list):
    df_decrypted = df.copy()  # Create a copy of the DataFrame

    for col in col_list:
        if pd.api.types.is_string_dtype(df_decrypted[col]):
            # Decrypt string columns
            df_decrypted[col] = df_decrypted[col].apply(lambda x: aes_decrypt(x, key))
        else:
            # Convert to the original data type after decryption
            df_decrypted[col] = df_decrypted[col].apply(lambda x: aes_decrypt(str(x), key))

    df_decrypted = pl.from_pandas(df_decrypted)

    return df_decrypted


def get_ai_text(area):
    engine = create_engine(
        "sqlite:///data/investerings_database_encrypted_new.db"
    )  # Ret efter udgivelse
    with engine.connect() as conn:
        query = f"SELECT [Resumé] FROM kommunale_regioner_ai_tekster WHERE `Kommune` = '{area}';"  # Example query

        # Execute the query and load the result into a Polars DataFrame
        result_df = pd.read_sql(query, conn)
    return result_df["Resumé"][0]


# Define a function to format numbers with European conventions
def format_number_european(value, digits=0):
    value = round(value, digits)
    return babel.numbers.format_decimal(value, locale="da_DK")

def round_to_million_or_billion(value, digits=2):
    value = int(value)

    # Check the length of the number
    value_length = len(str(abs(value)))  # Using abs() to ignore negative signs in length check
    if value_length >= 10:
        # If the number has 10 or more characters, round to "milliard"
        in_billions = round(value / 1000000000, digits)
        in_billions = format_number_european(in_billions, digits)
        return f"({in_billions} mia.)"
    elif value_length >= 7:
        # If the number has 7 or more characters, round to "million"
        in_millions = round(value / 1000000, digits)
        in_millions = format_number_european(in_millions, digits)
        return f"({in_millions} mio.)"
    else:
        return ""


def get_unique_kommuner(df_pl):
    """
    Extract unique 'Kommune' values from the dataframe and sort them alphabetically.
    """
    unique_kommuner = sorted(df_pl["Område"].unique().to_list())
    # Define custom categories
    all_values = "Hele landet"
    municipalities = "Alle kommuner"
    regions = "Alle regioner"
    samsø = "Samsø"
    læsø = "Læsø"

    # Combine Samsø, Læsø with unique_kommuner and sort alphabetically
    sorted_kommuner = sorted(unique_kommuner + [samsø, læsø])

    # Create dropdown options
    dropdown_options = [all_values, municipalities, regions] + sorted_kommuner
    return dropdown_options


def get_unique_categories(df_pl):
    # Create dropdown for 'Problemkategori'
    unique_categories = df_pl.select(
        pl.col("Problemkategori")
        .drop_nulls()  # Drop null values
        .str.split("; ")  # Split the categories
        .explode()  # Explode the list into separate rows
        .unique()  # Get unique values
    )

    # Convert to a sorted list for a better dropdown experience
    unique_categories_list = sorted(
        pl.Series(unique_categories.select("Problemkategori")).to_list()
    )

    return unique_categories_list


def filter_dataframe_by_choice(
    df_pl, choice, all_values="Hele landet", municipalities="Alle kommuner", regions="Alle regioner"
):
    """
    Filter the dataframe based on the user's selection (all_values, municipalities, regions, or a specific kommune).
    """
    if choice == all_values:
        return df_pl
    elif choice == municipalities:
        return df_pl.filter(~df_pl["Område"].str.starts_with("Region"))
    elif choice == regions:
        return df_pl.filter(df_pl["Område"].str.starts_with("Region"))
    else:
        return df_pl.filter(df_pl["Område"] == choice)


def filter_dataframe_by_category(df, selected_categories):
    if selected_categories:
        # Filter rows where any of the selected categories are in 'Problemkategori'
        df_filtered = df.filter(
            pl.col("Problemkategori").map_elements(
                lambda x: any(cat in x for cat in selected_categories), return_dtype=pl.Boolean
            )
        )
    else:
        df_filtered = df
    return df_filtered


def normalize_text(text):
    # Replace special characters with a single space, collapse multiple spaces, and normalize to lowercase
    text = re.sub(r"[^\w\s]", " ", text).lower()  # Replace non-alphanumeric characters with space
    text = re.sub(r"\s+", " ", text).strip()  # Collapse multiple spaces into one and trim
    return text


def filter_df_by_search(df, search_query):
    # Use case-insensitive search if query is provided
    if search_query:
        # Normalize the search query by removing special characters but keeping spaces normalized
        normalized_search_query = normalize_text(search_query)

        # Replace NA values with empty strings and cast columns to string
        df = df.with_columns([pl.col(col).fill_null("").cast(str) for col in df.columns])

        # Combine conditions across all columns using logical OR (|) operator
        filter_expr = None
        for col in df.columns:
            # Normalize the text in each column for comparison
            normalized_col = (
                pl.col(col)
                .str.replace_all(r"[^\w\s]", " ")  # Replace non-alphanumeric chars with space
                .str.to_lowercase()  # Convert to lowercase
                .str.replace_all(r"\s+", " ")  # Collapse multiple spaces
                .str.strip_chars()  # Trim leading and trailing spaces
            )

            # Check if the normalized column contains the normalized search query
            condition = normalized_col.str.contains(normalized_search_query)
            filter_expr = condition if filter_expr is None else filter_expr | condition

        # Apply the filter
        filtered_df = df.filter(filter_expr)

    else:
        filtered_df = df

    return filtered_df


# Function to check if a value can be converted to float
def to_float_safe(val):
    try:
        return float(val)
    except ValueError:
        return None


def fix_column_types_and_sort(df):
    # Cast 'Markedsværdi (DKK)' back to float
    df = df.with_columns([pl.col("Markedsværdi (DKK)").cast(pl.Float64)])

    # Cast 'Sortlistet' to integer
    df = df.with_columns([pl.col("Sortlistet").cast(pl.Int32)])

    # Apply the function - to_float_safe -to the column
    df = df.with_columns(pl.col("Priority").map_elements(to_float_safe, return_dtype=pl.Float64))

    # Sort first by 'Sortlistet', then by 'Priority', followed by 'Kommune' and 'ISIN kode'
    filtered_df = df.sort(
        ["Sortlistet", "Priority", "Område", "ISIN kode"], nulls_last=True, descending=[True, True, False, False]
    )

    filtered_df = filtered_df.with_row_index("Index", offset=1)

    # filtered_df = filtered_df.rename({"Årsag til eksklusion": "Eksklusion (Af hvem og hvorfor)"})

    return filtered_df


# Function to generate a single line with links
def generate_organization_links(df, column_name):
    org_links = {
        "Akademiker Pension": "https://akademikerpension.dk/ansvarlighed/frasalg-og-eksklusion/",
        "AP Pension": "https://appension.dk/globalassets/content_mz/filer-pdf/investering/eksklusionsliste.pdf",
        "ATP": "https://www.atp.dk/dokument/eksklusionsliste-sept-2023",
        "BankInvest": "https://bankinvest.dk/media/l4vmr5sh/eksklusionsliste.pdf",
        "Danske Bank": "https://danskebank.com/-/media/danske-bank-com/file-cloud/2019/3/list-of-excluded-companies-and-issuers.pdf?rev=c48a5c91d8124298b91daf26361481d8",
        "FN": "https://www.ohchr.org/sites/default/files/documents/hrbodies/hrcouncil/sessions-regular/session31/database-hrc3136/23-06-30-Update-israeli-settlement-opt-database-hrc3136.pdf",
        "Industriens Pension": "https://www.industrienspension.dk/da/ForMedlemmer/Investeringer-medlem/AnsvarligeInvesteringer/TalOgFakta#accordion=%7B88B4276E-3431-46C7-B291-9071056A3737%7D",
        "Jyske Bank": "https://www.jyskebank.dk/wps/wcm/connect/jfo/ca08eb49-3a38-4e18-9ec1-d0c6dcef1371/2023-11-29+-+Eksklusionsliste_DK.pdf?MOD=AJPERES&CVID=oMBbB8q",
        "LD Fonde": "https://www.ld.dk/media/bj4bqxwz/ld-fondes-eksklusionsliste-juni-2024.pdf",
        "Lægernes Pension": "https://www.lpb.dk/Om-os/baeredygtighed/Negativliste",
        "Lærernes Pension": "https://lppension.dk/globalassets/50---om-larernes-pension/50-20---sadan-investerer-vi/arbejdet-medansvarlige-investeringer/eksklusionslisten.pdf",
        "Nordea": "https://www.nordea.com/en/doc/the-nordea-exclusion-list-2024-0.pdf",
        "Nykredit": "https://www.nykredit.com/samfundsansvar/investeringer/ekskluderede-selskaber/",
        "PenSam": "https://www.pensam.dk/-/media/pdf-filer/om-pensam/investering/2---eksklusionsliste-selskaber-juli-2024.pdf",
        "PensionDanmark": "https://www.pensiondanmark.com/investeringer/udelukkelsesliste/?AspxAutoDetectCookieSupport=1",
        "PFA": "https://www.pfa.dk/om-pfa/samfundsansvar/eksklusion/",
        "PKA": "https://pka.dk/nyheder/pka-stopper-investeringer-i-25-selskaber-pa-grund-af-manglende-klimaambitioner",
        "Sydinvest": "https://www.sydinvest.dk/investeringsforening/ansvarlighed/eksklusionsliste-selskaber",
        "PBU": "https://pbu.dk/globalassets/_d-investeringer/c.-ansvarlighed/eksklusionsliste-pr._20-11-2023.pdf",
        "Sampension": "https://www.sampension.dk/om-sampension/finansiel-information/ansvarlige-investeringer/aabenhed-og-dokumentation---data-om-sampensions-esg-indsats/Ekskluderede-selskaber",
        "Spar Nord": "https://media.sparnord.dk/dk/omsparnord/csr/eksklusionsliste.pdf",
        "Sydinvenst": "https://www.sydinvest.dk/investeringsforening/ansvarlighed/eksklusionsliste-selskaber",
        "Velliv": "https://www.velliv.dk/dk/privat/om-os/samfundsansvar/ansvarlige-investeringer/vores-holdninger",  # "https://www.velliv.dk/media/5102/eksklusionslisten-31012024.pdf",
    }
    # Extract all unique organizations from the dataframe column
    unique_orgs = set()

    for org_list in df[column_name]:
        if org_list is not None:
            orgs = org_list.split("; ")
            for org in orgs:
                unique_orgs.add(org.strip())

    # Generate the links as one line
    links = "; ".join([f"[{org}]({org_links[org]})" for org in unique_orgs if org in org_links])

    # Display the bold title and links
    st.markdown(f"**Links til seneste relevante eksklusionslister:** {links}")


# Function to convert dataframe to Excel and create a downloadable file
def to_excel_function(filtered_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data


# Function to load and inject CSS into the Streamlit app
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def write_markdown_sidebar(how_we_did=False):
    st.header("Ved publicering:")
    st.markdown(
        """
        Hvis der anvendes data fra denne database i et journalistisk produkt eller i en anden sammenhæng, 
        skal [Gravercentret](https://www.gravercentret.dk) og [Danwatch](https://danwatch.dk/) nævnes som kilde. 
        F.eks.: ”Det viser data, som er indsamlet og bearbejdet af Gravercentret, 
        Danmarks Center for Undersøgende Journalistik, i samarbejde med Danwatch."\n
        """
    )
    st.markdown(
        f"Klik for at komme til [forsiden.](/Forside)"
        if how_we_did
        else "Læs mere om, [hvordan vi har gjort.](/Sådan_har_vi_gjort)"
    )
