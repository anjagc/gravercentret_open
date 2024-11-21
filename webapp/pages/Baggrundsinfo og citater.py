import streamlit as st
from config import set_pandas_options, set_streamlit_options
from utils.data_processing import load_css, write_markdown_sidebar, create_user_session_log

create_user_session_log("Baggrundsinfo og citater")

st.logo("webapp/images/GC_png_oneline_lockup_Outline_Blaa_RGB.png")

# Apply the settings
set_pandas_options()
set_streamlit_options()
load_css("webapp/style.css")


with st.sidebar:
    write_markdown_sidebar()

tab1, tab2 = st.tabs(
    [
        "Citater og mulige kilder",
        "Baggrundsviden om FN's liste",
    ]
)

with tab1:
    st.header("Citater til fri afbenyttelse")

    st.markdown(
        """
        ###### Citaterne på denne side er til fri afbenyttelse i forbindelse med omtale af informationer fra dette datasæt. De kan anvendes uden, at du behøver angive, at de er fra dette site.\n
    """
    )

    with st.expander(
        "**Per Nikolaj Bukh, professor i økonomistyring fra Aalborg Universitet:**", expanded=False
    ):
        st.markdown(
            """
    “Kommunerne må investere i samme investeringsbeviser som fonde og forventes at være økonomisk ansvarlige. De bør faktisk investere deres overskydende likviditet. Men de må kun investere i bestemte typer af obligationer og investeringsforeninger”, siger professor i økonomistyring, Per Nikolaj Bukh fra Aalborg Universitet. \n

    “Forskellene i hvilke af de potentielt problematiske investeringer, som kommunerne har, kan i høj grad forklares med, hvilke forvaltere kommunerne har hyret.  Forvalterne har forskellige tilbud om ESG-screenede (bæredygtighedsindsatser red.) fonde og dermed også på hvilke selskaber, som man investerer i”, siger Per Nikolaj Bukh. 
    """
        )

    with st.expander(
        "**Søren Larsen, uafhængig ESG-rådgiver og tidligere chef for bæredygtige investeringer i Nykredit:**",
        expanded=False,
    ):
        st.markdown(
            """
    "Generelt så indikerer investering i få kontroversielle selskaber, at investor har en systematisk tilgang til at undgå disse blandt de mange tusinde aktieselskaber, der handles på verdens børser”, vurderer Søren Larsen, der rådgiver virksomheder i bæredygtig virksomhedsdrift, finansiering samt ansvarlig investering og tidligere var chef for bæredygtige investeringer i Nykredit.\n

    "Det er ret vigtigt at formulere en ansvarlig investeringspolitik og sikre, at man har en aftale med en forvalter, som kan gennemføre politikken. Derefter skal kommunerne som alle andre investorer sikre sig, at politikken faktisk bliver ført ud i livet", siger Søren Larsen, der har rådgivet både store private og offentlige investorer. \n

    """
        )

    with st.expander(
        "**Oplysninger fra Københavns Kommunes Økonomiforvaltning:**",
        expanded=False,
    ):
        st.markdown(
            """
        ***Spørgsmål: Hvorfor er det vigtigt for Københavns Kommune at tage ESG-hensyn i investeringer?***\n

        "Kommunens midler er grundlæggende øremærket til specifikke formål på skoler, plejehjem, infrastruktur, m.v., men indtil de skal anvendes, investeres de bedst muligt med forholdsvis lav risiko." \n

        "Det er et politisk ønske, at midlerne bliver investeret på en ansvarlig måde. Det indebærer, at midlerne i stigende grad placeres i grønne, bæredygtige investeringer. Det indebærer også, at kommunen ikke ønsker at investere i selskaber, der ikke tager ansvar for miljø, menneskerettigheder og arbejdstagerrettigheder m.v. på niveau med anerkendte, internationale regler og normer." \n

        "Kommunen ønsker derfor ikke at investere i selskaber inden for eks. fossil energi, tobak og atomvåben eller selskaber på FN´s liste over selskaber med tråde til israelske bosættelser."\n

        ***Spørgsmål: Københavns Kommune har sine egne investeringsforeninger.  Hvorfor har man valgt den løsning?***\n

        "Dels kan der være en administrativ lettelse ved at investere via en investeringsforening, da der så ikke skal foretages løbende køb, salg og værdi-korrektioner via kommunens eget regnskab, men i investeringsforeningen. Dels kan det - i kraft af kommunens størrelse og deraf størrelsen på de midler, der bliver investeret - give mening omkostningsmæssigt at have egen investeringsforening."\n
        "Derudover betyder det også, at kommunen har større indflydelse, særligt på hvad der ikke investeres i og kan derfor også i højere grad implementere sine egne mål bl.a. i forhold til andelen af grønne, bæredygtige investeringer."\n
        "At Københavns Kommune har egen investeringsforening, betyder nemlig, at kommunens forvaltere handler ud fra kriterier fastsat af Københavns Kommune. Det er bl.a. kommunens krav til ansvarlige investeringer, der årligt bliver forelagt kommunens økonomiudvalg."\n
        "Dermed kan der også fravælges selskaber, kommunen ikke ønsker at investere i, uafhængigt af hvilke løsninger der findes ift. de eksisterende investeringsforeninger. Københavns Kommune etablerede investeringsforeningen i 2007, og den administreres af Danske Invest."


    """
        )

    with st.expander("**KL og Danske Regioner**", expanded=False):
        st.markdown(
            """
        Hverken KL eller Danske Regioner ønsker at komme med nogle råd eller anbefalinger til deres medlemmer vedrørende investeringer.

        KL er kommet med følgende skriftlige kommentar: "KL yder ikke finansiel rådgivning til kommunerne, så vi har ikke råd og anbefalinger ift. kommunernes placering af midler. Det er op til kommunerne inden for styrelseslovens rammer."

        Og Danske Regioner svarer følgende: "Det er ikke noget Danske Regioner rådgiver om."
        """
        )

    st.header("Sådan er reglerne på området")
    st.markdown(
        """
    Det er tilladt for kommuner og regioner at investere direkte i stats- 
    eller realkreditobligationer eller obligationer, der frembyder en tilsvarende sikkerhed.\n
    Men kommuner og regioner må ikke anbringe midler direkte i aktier.\n
    Dog kan de anbringe midler i investeringsforeninger, der investerer i 
    aktier og dermed eje andele af disse aktier og få del i såvel udbytte som evt. kursstigninger.\n
    Det følger af kommunalfuldmagtsreglerne (de uskrevne regler om 
    kommunernes opgavevaretagelse), at kommuner som udgangspunkt ikke må 
    drive erhvervsvirksomhed, herunder handel, håndværk, industri og finansiel virksomhed, 
    medmindre der er lovhjemmel til det.\n
    Forbuddet mod at drive kommunal erhvervsvirksomhed er for det første begrundet i, 
    at kommunerne har til opgave at udføre opgaver, der kommer almenvellet til gode. 
    For det andet er det begrundet i et ønske om at undgå konkurrenceforvridning i 
    forhold til den private sektor.\n
    **Kilde: Indenrigs- og Sundhedsministeriet**

    """
    )

    st.header("Mulige kilder")

    st.markdown(
        """
                De oplagte kilder til historier på baggrund af data er naturligvis kommunen eller regionen selv. 
                Det vil typisk være de politiske valgte, der vil være mest interessante at tale med, 
                for der er ikke noget ulovligt i at investere i problematiske værdipapirer. Det er mere et spørgsmål om moral og etik.\n
    I kommunerne vil det være borgmesteren, der er født formand for økonomiudvalget og repræsentanter for oppositionen i kommunen, 
                der vil være interessante at få en kommentar fra.\n
    Det samme gør sig gældende for regionerne.\n
    Det kunne også være interessant at tale med presseafdelingerne for de banker og pensionskasser, 
                der havde sortlistet nogle bestemte papirer for at få en uddybning af årsagen til eksklusionen.\n
    """
    )

with tab2:
    st.subheader("Baggrundsviden om FN's liste")

    st.markdown(
        """
        **Liste fra FN’s højkommissær for menneskerettigheder**\n
        Sekretariatet for FN’s højkommissær for menneskerettigheder (OHCHR), som har til opgave at fremme, overvåge og beskytte menneskerettighederne over hele verden, har oprettet [en liste over virksomheder](https://www.ohchr.org/sites/default/files/documents/hrbodies/hrcouncil/sessions-regular/session31/database-hrc3136/23-06-30-Update-israeli-settlement-opt-database-hrc3136.pdf), der er involveret i aktiviteter relateret til israelske bosættelser i besatte palæstinensiske områder - Vestbredden, Østjerusalem og Gazastriben. \n
        Disse områder er under israelsk besættelse, og bosættelserne anses for at være i strid med international lov, særligt Genèvekonventionen. \n

        Listen er baseret på FN’s Menneskerettighedsråds undersøgelse og inkluderer virksomheder, der for eksempel leverer udstyr til bosættelser eller udnytter naturressourcer fra de besatte områder. Databasen bliver løbende opdateret for at vise, hvilke virksomheder der fortsat er involveret i disse aktiviteter.\n

    """
    )
    st.markdown(
        """
        **Den Internationale Domstols (ICJ) vurdering**\n
        Det er i den forbindelse relevant at se på [Den Internationale Domstols (ICJ) vurdering fra den 19. juli 2024.](https://www.icj-cij.org/sites/default/files/case-related/186/186-20240719-sum-01-00-en.pdf) Den omhandler de juridiske konsekvenser af Israels politikker og praksisser i de besatte palæstinensiske områder. \n

        ICJ konkluderer, at Israels fortsatte tilstedeværelse i disse områder er ulovlig ifølge international lov. Besættelsen strider imod folkeretten, herunder palæstinensernes ret til selvbestemmelse. \n

        Dette betyder, at også investeringer eller finansieringsaktiviteter, der direkte eller indirekte støtter Israels ulovlige bosættelser eller udnyttelse af ressourcer i de besatte områder, kan være i strid med international lov, da de kan opfattes som en medvirken til at opretholde den ulovlige besættelse. \n

    """
    )
