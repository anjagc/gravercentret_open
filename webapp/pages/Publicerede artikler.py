import streamlit as st
from config import set_pandas_options, set_streamlit_options
from utils.data_processing import load_css, write_markdown_sidebar, create_user_session_log

# Apply the settings
set_pandas_options()
set_streamlit_options()

load_css("webapp/style.css")

create_user_session_log("Publicerede artikler")

st.logo("webapp/images/GC_png_oneline_lockup_Outline_Blaa_RGB.png")

with st.sidebar:
    write_markdown_sidebar()


def create_expander_article(media_name, headline, subheadline, pub_date, authors, link, bonus=""):
    with st.expander(f"{media_name}: **{headline}**", expanded=False):
        st.write(
            f"""
#### {headline}
##### {subheadline}

*{pub_date}*\n
*{authors}*

[Link til artikel]({link})\n
{bonus}
    """
        )


# Side-titel
st.header("Eksempler på publiceret journalistik")

# Overordnede afsnit
st.markdown(
    """
På denne side vil vi samle nogle eksempler på journalistiske historier, som er blevet til på baggrund af data her fra sitet. \n
"""
)

with st.expander(
    "Danwatch: **Kommuner investerer millioner i sortlistede virksomheder**", expanded=False
):
    st.write(
        """
#### Kommuner investerer millioner i sortlistede virksomheder
##### Atomvåben, oliegiganter, mineselskaber, besat land og gambling er blandt kommunernes investeringer, der også havner i statsobligationer fra skattelylande og regimer, der ikke lever op til menneskerettigheder.

*Udgivet d. 21. oktober 2024 kl. 00.01*\n
*Joachim Kattrup, Lasse Egeris og Charlotte Aagaard*

Trods høje ambitioner om bæredygtighed, klimaindsats og social ansvarlighed har danske kommuner investeret millioner af skatteborgernes penge i lande og virksomheder, der udvinder fossile brændstoffer, krænker menneskerettigheder, er i skattely og mange andre alvorlige problematikker. \n
Det afslører en helt ny database over kommunale investeringer i mere end 140.000 værdipapirer for i alt 66,7 milliarder kroner. \n
Danwatch har i samarbejde med Gravercentret - Danmarks Center for Undersøgende Journalistisk – undersøgt alle 98 kommuner og 5 regioners investeringer. Kortlægningen er den første af sin art nogensinde. \n
414 millioner kommunale kroner er placeret i 5.133 værdipapirer udstedt af selskaber eller lande, som danske pensionskasser ikke vil investere i af forskellige etiske årsager og derfor har sat på en sortliste over problematiske investeringer.\n
Kortlægningen afslører kommunale investeringer fordelt på mere end 20 "problem-kategorier”, som bl.a. tæller klima, våben, menneskerettigheder, Rusland, tobak, skattely, fossile brændsler, gambling og usunde fødevarer.\n
Kortlægningen afslører meget store forskelle i kommunernes etiske hensyn i deres finansielle investeringer.\n
For eksempel har København investeret i kun elleve problematiske selskaber, imens man på Kalundborgs investerings liste finder 286 værdipapirer fordelt på mere end 70 selskaber, som er ekskluderet af danske pensionskasser.\n
Danwatch har forelagt resultaterne for professor i økonomistyring, Per Nikolaj Bukh fra Aalborg Universitet.  \n
“Forskellene i hvilke af de potentielt problematiske investeringer, som kommunerne har, kan i høj grad forklares med, hvilke forvaltere kommunerne har hyret.  Forvalterne har forskellige tilbud om ESG-screenede (bæredygtighedsindsatser, red.) fonde og dermed også på hvilke selskaber, som man investerer i”, siger Per Nikolaj Bukh.\n

##### Verdens største olieselskaber
Danske kommuner har investeret betydelige beløb i nogle af verdens mest forurenende olieselskaber, herunder TotalEnergies, Shell, Chevron og Aramco. \n
Men det stopper ikke ved det. Også statskontrollerede fossile giganter som mexicanske Pemex, brasilianske Petrobras og Kasakhstanske KazMunayGas er blandt kommunernes investeringer. \n
Disse fossile selskaber er kendt for deres massive CO2-udledninger og fortsatte satsning på udvikling af fossile brændstoffer.\n

##### Investeringer i ulovlige bosættelser
Ud over olieselskaber investerer danske kommuner også i virksomheder, der er involveret i aktiviteter i de besatte palæstinensiske områder. Det kan være i strid med FN, ifølge en vurdering fra Den Internationale Domstol (ICJ).  ICJ konkluderer, at Israels fortsatte tilstedeværelse i disse områder er ulovlig ifølge international lov.\n
Eksempler inkluderer flere israelske banker og internationale rejsebureauer som TripAdvisor og Booking.com. De står på FN´s liste over virksomheder, der er involveret i aktiviteter i israelske besatte områder. Mange på listen har danske kommuner i ejerkredsen.  \n
Og selv om kommunerne hyrer forvaltere, som investerer deres penge, så har den enkelte kommune også et stort ansvar for at sikre, at borgernes penge ikke ender i problematiske aktiviteter og virksomheder. Det vurderer uafhængig ESG-rådgiver og tidligere chef for bæredygtige investeringer i Nykredit, Søren Larsen.\n
“Investor skal have afklaret, at selskabet ikke modarbejder FN's afgørelser og i øvrigt respekterer menneskerettighederne.  Det kan være svært at afgøre i de konkrete tilfælde.  Men det skal afklares, hvis investeringen skal være i overensstemmelse med FN”, siger Søren Larsen. \n
Kortlægningen viser også, at landets store kommuner har flest penge investeret i kontroversielle selskaber, fordi de også har de største økonomier. \n
Men de problematiske investeringer i de store kommuner er fordelt på færre selskaber end mange af landets mindre kommuner.  \n
"Generelt så indikerer investering i få kontroversielle selskaber, at investor har en systematisk tilgang til at undgå disse blandt de mange tusinde aktieselskaber, der handles på verdens børser”, vurderer Søren Larsen, der har rådgivet både store private og offentlige investorer.\n
København skiller sig ud ved kun at have investeret i få problematiske virksomheder.\n
"Det er ret vigtigt at formulere en ansvarlig investeringspolitik og sikre, at man har en aftale med en forvalter, som kan gennemføre politikken. Derefter skal kommunerne som alle andre investorer sikre sig, at politikken faktisk bliver ført ud i livet, siger Søren Larsen.\n
Som den eneste af landets kommuner har København etableret sin egen investeringsforening. Det sikre, at forvalterne handler ud fra de kriterier som kommunen fastsætter.\n
“Det er et politisk ønske, at midlerne bliver investeret på en ansvarlig måde. Det indebærer , at kommunen ikke ønsker at investere i selskaber, der ikke tager ansvar for miljø, menneskerettigheder og arbejdstagerrettigheder m.v. på niveau med anerkendte, internationale regler og normer”, oplyser Københavns Kommunes Økonomiforvaltning i en mail til Danwatch. \n

##### Kontroversielle stater og skattelylande
I et ministerbrev fra 2012 opfordrede økonomiminister, Margrethe Vestager, landets kommunalbestyrelser til at “drøfte etiske hensyn”, når kommunale midler investeres.\n
En række kommuner, blandt andet Herning, Kalundborg og Ringkøbing-Skjern, har investeret i investeringsforeninger indeholdende statsobligationer udstedt af Panama og Trinidad & Tobago. Begge lande er skattely ifølge EU’s officielle liste over skattelylande.\n
“En af de udfordringer, der er med investeringsforeninger, er, at sammensætningen af værdipapirer i foreningen kan ændre sig, så en investering kan gå fra at overholde vores ønsker til at overtræde dem uden, at der umiddelbart tilgår os information om dette,” siger Mads Damkjær Nielsen, Kommunikationschef i Kalundborg Kommune. \n
Kortlægningen afslører også, at flere kommuner har investeringer i Saudi Arabiske statsobligationer - et land som blandt andet Akademikerpension har ekskluderet på grund af både krænkelser af menneskerettigheder og klimaskadelige aktiviteter.   \n
De fleste kommuner har vedtaget investeringspolitikker og trods store forskelle i udfaldet af de konkrete investeringer, har blandt andet Københavns Kommune haft en betydningsfuld rolle i udviklingen af ansvarlige investeringer. Det gælder især inden for klima.\n
"Nogle af de største kommuner har faktisk sammen med flere pensionskasser været førende inden for ansvarlige investeringer. De var blandt de første til at koble klimamål til investeringer”, siger Søren Larsen.\n
Databasen over kommunernes investeringer er tilgængelig for alle pr. 21. oktober 2024. 75 af de 98 kommuner har problematiske investeringer. Fire  af fem regioner har problematiske investeringer.\n

        """
    )

create_expander_article(
    "Folketidende",
    "Mens borgerne kæmper med overvægt: Kommunen investerer i McDonald’s, Coca-Cola og Pepsi",
    "Den enes død, den andens burgerbolle. Lolland og Guldborgsund kommuner investerer i firmaer, der tjener på usunde fødevarer.",
    "Udgivet d. 22. oktober 2024 kl. 06.00",
    "David Arnholm og Michael Patrick Larsen",
    "https://folketidende.dk/lolland/mens-borgerne-kaemper-med-overvaegt-kommunen-investerer-i-mcdonald-s-coca-cola-og-pepsi",
)

create_expander_article(
    "Din Avis Aarhus Onsdag",
    "Våben, gambling og menneskerettigheder - over 21 millioner skattekroner kan være »problematisk« investeret",
    "Over 21 millioner kroner har Aarhus Kommune investeret i værdipapirer, der er 'potentielt problematiske'.",
    "Udgivet d. 21. oktober 2024 kl. 05.52",
    "Mathias Dueholm",
    "https://aarhus.lokalavisen.dk/samfund/ECE17548446/vaaben-gambling-og-menneskerettigheder-over-21-millioner-skattekroner-kan-vaere-problematisk-investeret/",
    bonus="""
På baggrund af artiklen kom der en opfølgende artikel med en reaktion fra Jesper Kjeldsen (S), formand for Økonomi- og Erhvervsudvalget:
[Link til artikel](https://aarhus.lokalavisen.dk/politik/ECE17557594/det-er-svaert-at-tro-udvalgsformand-overrasket-over-aarhus-sortlistede-investeringer/)
    """,
)

create_expander_article(
    media_name="Risbjerg & Co.",
    headline="Hvidovre har millioner investeret i våben, fed mad og fossile brændsler",
    subheadline="Hvidovre Kommune har flere millioner kroner investeret i værdipapirer, der er sortlistet af danske banker, pensionsselskaber eller FN. Borgmester Anders Wolf Andresen (SF) tager sagen op.",
    pub_date="Udgivet d. 22. oktober 2024",
    authors="Thomas Hoffmann",
    link="https://risbjergco.dk/hvidovre-har-millioner-investeret-i-vaaben-fed-mad-og-fossile-braendsler/",
)

create_expander_article(
    media_name="KøbenhavnLIV",
    headline="Kommune afsløret: Investerede millioner i selskab, der laver nogle af verdens mest frygtede våben",
    subheadline="Stik imod egen investeringspolitik blev et tocifret millionbeløb fra Københavns Kommune investeret i et sortlistet japansk selskab, der har været involveret i produktion af napalm-lignende bomber.",
    pub_date="Udgivet d. 21. oktober 2024 kl. 06.30",
    authors="Mads Klitgaard",
    link="https://kobenhavnliv.dk/kobenhavngl/kommune-afsloeret-investerede-millioner-i-selskab-der-laver-nogle-af-verdens-mest-frygtede-vaaben?teaser-referral=4744eed4-04c1-404e-8dc0-3e8491344b25-16",
)

create_expander_article(
    media_name="PingvinNyt.dk",
    headline="Favrskov Kommune har investeret 2,1 mio kr. i 17 sortlistede selskaber",
    subheadline="Selskaberne er sortlistede af danske investeringsselskaber og banker, men alligevel investerer kommunen i disse",
    pub_date="Udgivet d. 22. oktober 2024",
    authors="",
    link="https://pingvinnyt.dk/favrskov-kommune-har-investeret-21-mio-kr-i-17-sortlistede-selskaber/",
)

create_expander_article(
    media_name="Fyns Amts Avis",
    headline="Svendborg har 1,6 millioner placeret i sortlistede selskaber: Borgmester er ikke overrasket",
    subheadline="Selvom der politisk har været fokus på ansvarlige investeringer, afslører en ny kortlægning, at kommunen stadig har værdipapirer i virksomheder med tvivlsom etik og moral. Det hele gennemgås med en tættekam, siger borgmester Bo Hansen (S).",
    pub_date="Udgivet d. 21. oktober 2024 kl. 06.00",
    authors="Anton Theodor Kornum",
    link="https://faa.dk/svendborg/svendborg-har-1-6-millioner-placeret-i-sortlistede-selskaber-borgmester-er-ikke-overrasket?teaser-referral=0d6bf0ad-f402-4a8b-9b3b-24b999771a74-9",
)

create_expander_article(
    media_name="TV2 ØST",
    headline="Kalundborg sælger sortlistede investeringer efter afsløring",
    subheadline="Hvert syvende af Kalundborg Kommunes værdipapirer stemples som problematiske i ny opgørelse. Nu vil borgmesteren rydde op.",
    pub_date="Udgivet d. 22. oktober 2024 kl. 14.49",
    authors="Mads Brandsen",
    link="https://www.tv2east.dk/kalundborg/kalundborg-saelger-sortlistede-investeringer-efter-afsloering",
)
create_expander_article(
    media_name="JydskeVestkysten",
    headline="Her ender dine skattepenge: Investerer millionbeløb i kontroversielle selskaber på FN-liste",
    subheadline="Både Esbjerg og Fanø Kommuner har investeret i selskaber, som ifølge FN er med til at understøtte Israels ulovlige bosættelser.",
    pub_date="Udgivet d. 22. oktober 2024 kl. 11.18",
    authors="Anders Dehn",
    link="",
)

create_expander_article(
    media_name="Horsens Folkeblad",
    headline="Kontroversielle våben og brud på menneskerettigheder: Kommunen har millioner i sortlistede selskaber",
    subheadline="Hedensted Kommune har investeret 2,6 mio. kr. i selskaber, som banker og pensionskasser har blacklistet af moralske og etiske grunde.",
    pub_date="Udgivet d. 21. oktober 2024 kl. 10.55",
    authors="Lennart Kjær Schouborg",
    link="https://hsfo.dk/hedensted/kontroversielle-vaaben-og-brud-paa-menneskerettigheder-kommunen-har-millioner-i-sortlistede-selskaber",
)

create_expander_article(
    media_name="Dagbladet Ringkøbing-Skjern",
    headline="Olie og sortlistede lande: Kommunen ligger højt i opgørelse over problematiske investeringer",
    subheadline="Ringkøbing-Skjern Kommune har over 9 millioner kroner investeret i virksomheder og lande, der er karakteriseret som problematiske. Det er blandt andet lande, som er på EU's sortliste, og virksomheder, der  producerer fossile brændstoffer.",
    pub_date="Udgivet d. 21. oktober 2024 kl. 05.59",
    authors="Magnus Bjørn Ambye og Rasmus Holm Jacobsen",
    link="https://dbrs.dk/ringkoebing-skjern/olie-og-sortlistede-lande-kommunen-ligger-hoejt-i-opgoerelse-over-problematiske-investeringer",
)

create_expander_article(
    media_name="Sjællandske Medier",
    headline="Sjællandske kommuner har 170 millioner i kontroversielle våben, gambling, tobak og andre problematiske virksomheder",
    subheadline="En opgørelse kaster lys over, hvordan kommunerne investerer borgernes penge.",
    pub_date="Udgivet d. 21. oktober 2024 kl. 06.01",
    authors="Rane von Benzon",
    link="https://www.sn.dk/art6159221/erhverv/indblik/kommuner-har-170-millioner-i-kontroversielle-vaaben-gambling-og-tobak/",
)

create_expander_article(
    media_name="TV 2/Bornholm",
    headline="Borgmestervikar: Sortlistede værdipapirer i åbenbar strid med politik",
    subheadline="Morten Riis kalder det et stort problem, at regionskommunen investerer i aktier og obligationer fra sortlistede selskaber. Den vikarierende borgmester har derfor bedt kommunaldirektøren tage fat i Danske Invest, der står for investeringerne. Der er investeret i åbenbar strid med regionskommunens politik på området, lyder det.",
    pub_date="Udgivet d. 22. oktober 2024 kl. 16.22",
    authors="William Husted",
    link="https://tv2bornholm.dk/artikel/borgmestervikar-sortlistede-vaerdipapirer-i-aabenbar-strid-med-politik",
)


# create_expander_article(
#     media_name="",
#     headline="",
#     subheadline="",
#     pub_date="Udgivet d. 21. oktober 2024 kl. 06.00",
#     authors="",
#     link="",
# )

# create_expander_article(
#     media_name="",
#     headline="",
#     subheadline="",
#     pub_date="Udgivet d. 21. oktober 2024 kl. 06.00",
#     authors="",
#     link="",
# )
