import streamlit as st
from config import set_pandas_options, set_streamlit_options
from utils.data_processing import load_css, write_markdown_sidebar, create_user_session_log

create_user_session_log("Sådan har vi gjort")

# Apply the settings
set_pandas_options()
set_streamlit_options()

st.logo("webapp/images/GC_png_oneline_lockup_Outline_Blaa_RGB.png")

load_css("webapp/style.css")

with st.sidebar:
    write_markdown_sidebar(how_we_did=True)

# Streamlit page for 'Sådan gjorde vi'
st.header("Sådan har vi gjort")

st.markdown(
    """
[Gravercentret](https://www.gravercentret.dk), Danmarks Center for Undersøgende Journalistik, har i samarbejde med [Danwatch](https://danwatch.dk/) indhentet oplysninger om værdipapirbeholdningen hos alle 98 kommuner og fem regioner.\n
Formålet er en landsdækkende journalistisk kortlægning af de kommunale investeringer på de finansielle markeder.\n
Vi har via en aktindsigtsanmodning bedt om en komplet liste over, hvilke værdipapirer (aktier, obligationer, m.v.) kommunen eller regionen 
            ejer og hvilken værdi, papirerne udgør. Vi har også i enkelte tilfælde hentet informationerne fra de kommunale hjemmesider. Vi har undersøgt både direkte investeringer og indirekte investeringer, som forvaltes af investeringsforvaltere og fonde. \n
Landets kommuner og regioner må ikke investere direkte i aktier, men de må godt selv investere i obligationer 
            såsom statsobligationer og realkreditobligationer.\n
Kommuner og regioner har derfor typisk investeret deres midler gennem investeringsforeninger og fonde, 
            der ejer et udvalg af aktier og/eller obligationer. Her har vi bedt om at få oplyst værdien 
            af kommunens eller regionens ejerandel af disse underliggende værdipapirer.\n
##### Hvad har vi bedt om?
Vi har anmodet om de senest opgjorte beholdningslister og markedsværdier, og der kan derfor 
            i sagens natur være variation i, hvornår tallene er opgjort. Hovedparten af kommunerne har dog valgt at trække nye opgørelser til brug for besvarelsen af vores anmodning, der blev fremsat ultimo juni 2024.\n
Tallene fra flere af de største kommuner er opgjort noget tidligere. Esbjerg Kommunes investeringer er opgjort 01.09.2023, Aarhus Kommune 31.03.2024, Odense Kommune 31.03.2024 og Aalborg Kommune 30.04.2024.\n
For hvert værdipapir har vi søgt at indhente:
- ISIN-kode
- Værdipapirets navn
- Virksomhed/udsteder
- Den aktuelle markedsværdi (DKK)
- Type (aktie/obligation) \n
Da opgørelsesdatoerne som nævnt kan variere og er øjebliksbilleder, er det en god idé at få bekræftet hos kommunen 
            eller regionen, at de stadig ejer det pågældende papir enten direkte eller gennem en investeringsforening eller lignende. \n
Men selv hvis de skulle have afhændet værdipapiret, så har de altså haft investeret i papiret eller selskabet.\n
Det kan også være en idé at få en opdateret markedsværdi oplyst, hvis det synes relevant eller man mistænker, 
            at markedsværdien kan have ændret sig væsentligt. Det er dog værd at bemærke, at markedsværdierne 
            og valutakurserne svinger hele tiden, så man kan aldrig få en stabil værdi her.\n
##### Fejl og mangler
Nogle værdipapirers markedsværdi kan synes utrolig lav – helt ned til nogle få kroner. Disse lave værdier skyldes, 
            at kommuner og regioner ejer andele af aktier gennem investeringsforeninger eller fonde. Disse andele kan 
            være meget små og giver derfor i nogle tilfælde nogle meget lave markedsværdier.\n
Som udgangspunkt har vi fjernet værdipapirpositioner, der har en værdi på mindre end ti kroner for overskuelighedens skyld.\n
Ikke alle besvarelser fra kommuner og regioner har været komplette, og i disse tilfælde har vi søgt at skaffe de 
            manglende data gennem dialog. Enkelte gange er det ikke lykkedes, og derfor kan der nogle steder mangle data.\n
Vi har dog søgt at rekonstruere manglende data ved at sammenligne data om det samme værdipapir hos andre kommuner og regioner, 
            der har givet mere fyldestgørende svar om f.eks. navn, udsteder og type.\n
Manglende oplysninger som disse bør dog ikke have den store betydning andet end for detaljegraden af søgbarheden. 
            Alle værdipapirerne har et ISIN-nummer tilknyttet, som kan give yderligere oplysninger om investeringen, hvis man ønsker det.\n
Data er renset for fejlposter – f.eks. er rettigheder, kontantbeholdninger i forskellige valutaer og 
            ugyldige værdipapirer ikke medtaget i det omfang, at vi har kunnet identificere dem.\n
##### Sortlistede værdipapirer
For at berige data har vi indhentet såkaldte eksklusionslister fra de største banker og pensionskasser, 
            i det omfang det har været muligt. Eksklusionslisterne viser, hvilke værdipapirer de pågældende banker og pensionskasser ikke ønsker at investere i, og hvorfor. Det er værd at bemærke, at nogle værdipapirer kan være ekskluderet i nogle investeringsfonde, men accepteret i andre – også inden for samme bank eller pensionsselskab.\n
Vi har også medtaget FN’s liste over selskaber, der har aktiviteter i besatte områder på Vestbredden.\n
Vi har markeret problematiske værdipapirer med rødt i datasættet, men listen er langt fra komplet. 
            Der vil være flere eksklusionslister at finde fra andre banker, pensionsselskaber og NGO’er i ind-og udland.\n
Herudover har Gravercentret i datasættet markeret en række værdipapirer, der kan opfattes som kontroversielle, 
            men som ikke optræder på nogen af de eksklusionslister, vi har medtaget. Disse er markeret med gult.\n
En række eksklusionslister indeholder ikke kun selskaber, men også lande. Det betyder som minimum, 
            at statsobligationer fra det pågældende land er udelukket. Disse statsobligationer 
            har vi markeret med orange i det omfang, vi har kunnet identificere dem.\n
En eksklusion af et land kan dog også betyde en eksklusion af selskaber ejet eller kontrolleret af 
            staten og i nogle tilfælde alle selskaber hjemmehørende i det pågældende land. 
            Men da alle banker og pensionsselskaber lægger snittet forskelligt med hensyn til eksklusion af lande, 
            har vi valgt kun at markere statsobligationerne som problematiske.\n
Optræder et værdipapir i flere farvekategorier, vil den blive farvet efter den højeste kategori i rækkefølgen rød, 
            orange og gul. Så hvis et papir f.eks. både figurerer på en orange og en rød liste, bliver den farvet rød.\n
Det er endelig værd at bemærke, at der er mere end 140.000 værdipapirer i datasættet og omkring 840.000 
            felter – og med så store mængder data vil der altid være en risiko for fejl og fejlmatches.\n\n
**Spørgsmål kan rettes til data@gravercentret.dk**
            """
)


# with st.expander("Databehandling"):
#     st.write(
#         """
#     Vi har renset og struktureret dataene, så de kunne analyseres. Dette inkluderede fjernelse af irrelevante oplysninger,
#     håndtering af manglende værdier og kodning af variabler.
#     """
#     )

# with st.expander("Analysemetoder"):
#     st.write(
#         """
#     De analyserede data er blevet bearbejdet ved hjælp af statistiske værktøjer, hvor vi har fokuseret på
#     at identificere tendenser og mønstre, der kunne belyse de problemstillinger, vi ønskede at undersøge.
#     """
#     )

# # Liste med links til hjemmesider
# st.header("Kilder og yderligere information")
# st.write("Her er nogle af de kilder, vi har brugt i projektet:")

# links = {
#     "Danmarks Statistik": "https://www.dst.dk/",
#     "Sundhedsdatastyrelsen": "https://www.sundhedsdatastyrelsen.dk/",
#     "Regionernes hjemmesider": "https://www.regioner.dk/",
# }

# for name, url in links.items():
#     st.write(f"[{name}]({url})")

# # Footer
# st.write("Har du spørgsmål til metoden, er du velkommen til at kontakte os.")
