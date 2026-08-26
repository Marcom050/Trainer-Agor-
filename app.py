import unicodedata

import streamlit as st


st.set_page_config(
    page_title="Trainer Agorà | GreenTheory",
    page_icon="TA",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# All demo content lives here so every screen renders the same trainer information.
TRAINERS = [
    {
        "name": "Luca Bianchi",
        "gym": "GreenTheory Milano Centrale",
        "experience_years": 7,
        "bio": "Aiuto chi vuole costruire massa e forza con una programmazione progressiva, precisa e sostenibile.",
        "skills": ["Ipertrofia", "Forza", "Bodybuilding", "Tecnica dei fondamentali"],
        "goals": ["Aumento massa muscolare", "Forza"],
        "levels": ["Intermedio", "Avanzato"],
        "services": ["Personal training 1:1", "Scheda personalizzata", "Check mensile"],
        "support": ["Programmazione strutturata", "Motivazione e costanza"],
        "availability": ["Prima delle 9", "18–21"],
        "modalities": ["In presenza", "Online"],
    },
    {
        "name": "Giulia Rossi",
        "gym": "GreenTheory Monza",
        "experience_years": 5,
        "bio": "Creo percorsi accessibili per dimagrire, ritrovare energia e trasformare l'allenamento in un'abitudine duratura.",
        "skills": ["Ricomposizione corporea", "Dimagrimento", "Allenamento principianti"],
        "goals": ["Dimagrimento", "Benessere generale"],
        "levels": ["Principiante", "Intermedio"],
        "services": ["Personal training 1:1", "Percorso introduttivo", "Monitoraggio progressi"],
        "support": ["Motivazione e costanza", "Guida tecnica continua"],
        "availability": ["9–13", "18–21"],
        "modalities": ["In presenza", "Online"],
    },
    {
        "name": "Andrea Conti",
        "gym": "GreenTheory Monza",
        "experience_years": 8,
        "bio": "Unisco preparazione atletica e strength training per rendere ogni progresso misurabile, dal gesto tecnico alla performance.",
        "skills": ["Forza", "Ipertrofia", "Preparazione atletica", "Tecnica degli esercizi"],
        "goals": ["Forza", "Aumento massa muscolare"],
        "levels": ["Intermedio", "Avanzato"],
        "services": ["Personal training 1:1", "Test di performance", "Programmazione periodizzata"],
        "support": ["Programmazione strutturata", "Guida tecnica continua"],
        "availability": ["Prima delle 9", "13–18"],
        "modalities": ["In presenza"],
    },
    {
        "name": "Martina Ferri",
        "gym": "GreenTheory Milano Porta Romana",
        "experience_years": 6,
        "bio": "Accompagno le persone verso un movimento più libero e consapevole, con attenzione a postura, mobilità e qualità della vita.",
        "skills": ["Mobilità", "Postura", "Core training", "Recupero funzionale"],
        "goals": ["Benessere generale", "Mobilità e postura"],
        "levels": ["Principiante", "Intermedio"],
        "services": ["Valutazione posturale", "Sessioni di mobilità", "Personal training 1:1"],
        "support": ["Guida tecnica continua", "Motivazione e costanza"],
        "availability": ["9–13", "13–18"],
        "modalities": ["In presenza", "Online"],
    },
    {
        "name": "Federico Sala",
        "gym": "GreenTheory Milano Centrale",
        "experience_years": 9,
        "bio": "Lavoro con atleti e appassionati esperti su forza massimale, ipertrofia e preparazione mirata agli obiettivi.",
        "skills": ["Strength training", "Powerlifting", "Ipertrofia", "Performance"],
        "goals": ["Forza", "Aumento massa muscolare"],
        "levels": ["Intermedio", "Avanzato"],
        "services": ["Coaching 1:1", "Analisi tecnica video", "Programmazione avanzata"],
        "support": ["Programmazione strutturata", "Guida tecnica continua"],
        "availability": ["13–18", "18–21"],
        "modalities": ["In presenza", "Online"],
    },
    {
        "name": "Sara Romano",
        "gym": "GreenTheory Monza",
        "experience_years": 4,
        "bio": "Rendo il movimento piacevole e concreto attraverso functional training, mobilità e percorsi costruiti sul ritmo della persona.",
        "skills": ["Functional training", "Mobilità", "Postura", "Circuit training"],
        "goals": ["Mobilità e postura", "Benessere generale", "Dimagrimento"],
        "levels": ["Principiante", "Intermedio"],
        "services": ["Personal training", "Sessioni di mobilità", "Piccoli gruppi"],
        "support": ["Motivazione e costanza", "Guida tecnica continua"],
        "availability": ["Prima delle 9", "9–13"],
        "modalities": ["In presenza"],
    },
]

GYMS = list(dict.fromkeys(trainer["gym"] for trainer in TRAINERS))
GOALS = ["Aumento massa muscolare", "Dimagrimento", "Forza", "Benessere generale", "Mobilità e postura"]
LEVELS = ["Principiante", "Intermedio", "Avanzato"]
SUPPORT_TYPES = ["Programmazione strutturata", "Motivazione e costanza", "Guida tecnica continua"]
TIME_SLOTS = ["Prima delle 9", "9–13", "13–18", "18–21"]


st.markdown(
    """
    <style>
    .stApp { background: #f5f7f4; color: #142018; }
    /* Keep page content below Streamlit's fixed Community Cloud toolbar. */
    .block-container { max-width: 1160px; padding-top: 4.5rem; padding-bottom: 4rem; }
    h1, h2, h3 { letter-spacing: -0.035em; }
    .brand { display:block; font-size: 1.05rem; line-height:1.35; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: #194f36; }
    .hero { padding: 4.5rem 3.5rem; border-radius: 28px; background: linear-gradient(125deg,#102b20 0%,#1b5940 68%,#8bbd44 145%); color: white; margin: 1.2rem 0 2rem; }
    .hero h1 { font-size: clamp(2.7rem,6vw,5.4rem); line-height: .98; max-width: 850px; color: white; margin: .4rem 0 1.4rem; }
    .hero p { font-size: 1.16rem; line-height: 1.65; max-width: 680px; color: #e4eee8; }
    .eyebrow { color: #79b947; font-weight: 750; text-transform: uppercase; letter-spacing: .13em; font-size: .78rem; }
    .trainer-card { min-height: 205px; background: white; border: 1px solid #dfe7e1; border-radius: 18px; padding: 1.4rem; margin-bottom: .65rem; box-shadow: 0 8px 26px rgba(25,50,35,.05); }
    .trainer-card h3 { margin: .3rem 0; }
    .tag { display: inline-block; background: #edf4eb; color: #28573c; padding: .28rem .62rem; border-radius: 20px; margin: .15rem .1rem; font-size: .78rem; }
    .muted { color: #66736b; font-size: .9rem; }
    .score { color: #1b6947; font-weight: 800; font-size: 1.6rem; }
    div.stButton > button { border-radius: 10px; min-height: 2.8rem; font-weight: 700; }
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background:#1b6947; border-color:#1b6947; color:#fff;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background:#145238; border-color:#145238; color:#fff;
    }
    div.stButton > button[kind="primary"]:focus,
    div.stButton > button[data-testid="stBaseButton-primary"]:focus {
        box-shadow:0 0 0 .2rem rgba(27,105,71,.25); color:#fff;
    }
    div[data-testid="stMetric"] { background:#edf4eb; border-radius:14px; padding:1rem; }
    [data-testid="stForm"] { background:white; border:1px solid #dfe7e1; border-radius:20px; padding:1.2rem 1.5rem; }
    @media(max-width:700px) { .hero { padding:2.7rem 1.5rem; } .block-container { padding-top:4rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


if "page" not in st.session_state:
    st.session_state.page = "home"
if "answers" not in st.session_state:
    st.session_state.answers = {}


def go_to(page):
    st.session_state.page = page
    st.rerun()


def open_profile(trainer_name, origin):
    st.session_state.selected_trainer = trainer_name
    st.session_state.profile_origin = origin
    go_to("profilo")


def trainer_by_name(name):
    return next((trainer for trainer in TRAINERS if trainer["name"] == name), None)


def normalize_search_text(value):
    """Normalize text so searches are case- and accent-insensitive."""
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


def search_trainers(query):
    """Find partial matches in every trainer detail useful to a visitor."""
    needle = normalize_search_text(query).strip()
    if not needle:
        return []

    searchable_fields = ("skills", "goals", "services", "modalities")
    matches = []
    for trainer in TRAINERS:
        searchable_values = [trainer["name"], trainer["gym"]]
        for field in searchable_fields:
            searchable_values.extend(trainer[field])
        haystack = normalize_search_text(" ".join(searchable_values))
        if needle in haystack:
            matches.append(trainer)
    return matches


def calculate_match(trainer, answers):
    """Return a transparent, deterministic score and only the reasons earned."""
    checks = [
        (answers["goal"] in trainer["goals"], 30, f"è specializzato in {answers['goal'].lower()}"),
        (answers["gym"] == trainer["gym"], 25, "lavora nella GreenTheory che frequenti"),
        (answers["level"] in trainer["levels"], 15, f"segue persone di livello {answers['level'].lower()}"),
        (answers["support"] in trainer["support"], 15, f"offre {answers['support'].lower()}"),
        (answers["time"] in trainer["availability"], 15, f"è disponibile nella fascia {answers['time']}"),
    ]
    return sum(weight for matched, weight, _ in checks if matched), [reason for matched, _, reason in checks if matched]


def card_markup(trainer, detailed=False):
    skills = "".join(f'<span class="tag">{skill}</span>' for skill in trainer["skills"][:3])
    bio = f"<p>{trainer['bio']}</p>" if detailed else ""
    return f"""
        <div class="trainer-card">
          <div class="muted">{trainer['gym']} · {trainer['experience_years']} anni di esperienza</div>
          <h3>{trainer['name']}</h3>{bio}<div>{skills}</div>
        </div>
    """


def render_brand():
    st.markdown('<div class="brand">Trainer Agorà</div>', unsafe_allow_html=True)


page = st.session_state.page

if page == "home":
    render_brand()
    st.markdown(
        """<section class="hero"><div class="eyebrow">Il tuo percorso comincia dalla persona giusta</div>
        <h1>Trova il trainer giusto, nella palestra giusta.</h1>
        <p>Trainer Agorà ti aiuta a conoscere i professionisti GreenTheory e a scegliere chi comprende davvero obiettivi, livello e stile di allenamento.</p></section>""",
        unsafe_allow_html=True,
    )
    cta_primary, cta_secondary, _ = st.columns([1.1, 1.1, 1.5])
    with cta_primary:
        if st.button("Trova il mio trainer", type="primary", use_container_width=True):
            go_to("questionario")
    with cta_secondary:
        if st.button("Esplora le palestre", use_container_width=True):
            go_to("palestre")

    st.markdown("### Trova un trainer")
    query = st.text_input(
        "Cerca per nome, palestra, competenza, obiettivo, servizio o modalità",
        placeholder="Es. Andrea, Monza, mobilità, ipertrofia, online…",
    )
    if query.strip():
        matches = search_trainers(query)
        st.caption(f"{len(matches)} {'risultato' if len(matches) == 1 else 'risultati'}")
        for trainer in matches:
            left, right = st.columns([4, 1])
            with left:
                st.markdown(card_markup(trainer), unsafe_allow_html=True)
            with right:
                if st.button("Visualizza profilo", key=f"search_{trainer['name']}", use_container_width=True):
                    open_profile(trainer["name"], "home")
        if not matches:
            st.info("Nessun professionista corrisponde alla ricerca. Prova con una competenza o una sede diversa.")

    st.divider()
    st.markdown('<div class="eyebrow">Professionisti GreenTheory</div>', unsafe_allow_html=True)
    st.header("Trainer in evidenza")
    cols = st.columns(3)
    for col, trainer in zip(cols, [TRAINERS[1], TRAINERS[2], TRAINERS[3]]):
        with col:
            st.markdown(card_markup(trainer, detailed=True), unsafe_allow_html=True)
            if st.button("Scopri il profilo", key=f"featured_{trainer['name']}", use_container_width=True):
                open_profile(trainer["name"], "home")

elif page == "questionario":
    render_brand()
    if st.button("← Torna alla home"):
        go_to("home")
    st.markdown('<div class="eyebrow">Matching rapido</div>', unsafe_allow_html=True)
    st.title("Cinque risposte, una selezione su misura.")
    st.write("Dicci cosa cerchi: confronteremo le tue preferenze con i profili GreenTheory.")
    answers = st.session_state.answers
    with st.form("questionario"):
        goal = st.selectbox("1. Obiettivo principale", GOALS, index=GOALS.index(answers.get("goal", GOALS[0])))
        level = st.segmented_control("2. Il tuo livello", LEVELS, default=answers.get("level", LEVELS[0]), selection_mode="single")
        gym = st.selectbox("3. GreenTheory frequentata", GYMS, index=GYMS.index(answers.get("gym", GYMS[0])))
        support = st.selectbox("4. Supporto desiderato", SUPPORT_TYPES, index=SUPPORT_TYPES.index(answers.get("support", SUPPORT_TYPES[0])))
        time = st.segmented_control("5. Fascia oraria preferita", TIME_SLOTS, default=answers.get("time", TIME_SLOTS[0]), selection_mode="single")
        submitted = st.form_submit_button("Mostrami i trainer compatibili", type="primary", use_container_width=True)
    if submitted:
        st.session_state.answers = {"goal": goal, "level": level, "gym": gym, "support": support, "time": time}
        go_to("risultati")

elif page == "risultati":
    required = {"goal", "level", "gym", "support", "time"}
    if not required.issubset(st.session_state.answers):
        go_to("questionario")
    answers = st.session_state.answers
    render_brand()
    top, home = st.columns([1, 1])
    with top:
        if st.button("← Modifica le risposte"):
            go_to("questionario")
    with home:
        if st.button("Torna alla home"):
            go_to("home")
    st.markdown('<div class="eyebrow">La tua selezione</div>', unsafe_allow_html=True)
    st.title("I trainer più compatibili con te")
    st.write(f"Obiettivo **{answers['goal']}** · {answers['gym']} · fascia **{answers['time']}**")
    ranked = []
    for index, trainer in enumerate(TRAINERS):
        score, reasons = calculate_match(trainer, answers)
        ranked.append((score, -index, trainer, reasons))
    ranked.sort(reverse=True, key=lambda item: (item[0], item[1]))
    # Below 45/100 there are fewer than two meaningful preference matches.
    suitable = [result for result in ranked if result[0] >= 45][:3]
    st.divider()
    for position, (score, _, trainer, reasons) in enumerate(suitable, 1):
        with st.container(border=True):
            info, metric = st.columns([4, 1])
            with info:
                st.caption(f"SCELTA {position} · {trainer['gym']}")
                st.subheader(trainer["name"])
                st.write(" · ".join(trainer["skills"][:3]))
                st.caption(f"{trainer['experience_years']} anni di esperienza")
            with metric:
                st.metric("Compatibilità", f"{score}/100")
            st.markdown("**Perché te lo consigliamo**")
            st.write("; ".join(reason.capitalize() for reason in reasons) + ".")
            if st.button("Visualizza profilo", key=f"result_{trainer['name']}", use_container_width=True):
                open_profile(trainer["name"], "risultati")
    if len(suitable) < 3:
        st.info(f"Ti mostriamo {len(suitable)} {'profilo' if len(suitable) == 1 else 'profili'} davvero pertinente. Preferiamo non suggerirti trainer poco adatti: modifica una preferenza per ampliare la selezione.")

elif page == "profilo":
    trainer = trainer_by_name(st.session_state.get("selected_trainer"))
    if trainer is None:
        go_to("home")
    origin = st.session_state.get("profile_origin", "home")
    back_labels = {"risultati": "← Torna ai risultati", "palestre": "← Torna alla palestra", "home": "← Torna alla home"}
    render_brand()
    if st.button(back_labels.get(origin, "← Torna alla home")):
        go_to(origin if origin in {"risultati", "palestre"} else "home")
    st.markdown(f'<div class="eyebrow">{trainer["gym"]}</div>', unsafe_allow_html=True)
    st.title(trainer["name"])
    st.subheader(" · ".join(trainer["skills"][:3]))
    st.write(f"**{trainer['experience_years']} anni di esperienza**")
    st.write(trainer["bio"])
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Competenze")
        for item in trainer["skills"]:
            st.write(f"✓ {item}")
        st.subheader("Servizi")
        for item in trainer["services"]:
            st.write(f"✓ {item}")
    with col2:
        st.subheader("Come possiamo lavorare")
        st.write("**Modalità**")
        st.write(" · ".join(trainer["modalities"]))
        st.write("**Disponibilità**")
        st.write(" · ".join(trainer["availability"]))
        st.write("**Tipo di supporto**")
        st.write(" · ".join(trainer["support"]))
        st.write("**Livelli seguiti**")
        st.write(" · ".join(trainer["levels"]))
    st.divider()
    if st.button("Sono interessato a questo trainer", type="primary", use_container_width=True):
        st.success(f"Perfetto! Abbiamo registrato il tuo interesse per {trainer['name']}. In una prossima versione potrai inviare direttamente una richiesta.")

elif page == "palestre":
    render_brand()
    if st.button("← Torna alla home"):
        go_to("home")
    st.markdown('<div class="eyebrow">La community vicino a te</div>', unsafe_allow_html=True)
    st.title("Esplora le palestre")
    st.write("Seleziona una sede GreenTheory per vedere subito tutti i professionisti che operano lì.")
    selected_gym = st.selectbox("Scegli una palestra", GYMS, key="selected_gym")
    gym_trainers = [trainer for trainer in TRAINERS if trainer["gym"] == selected_gym]
    st.subheader(f"{len(gym_trainers)} professionisti a {selected_gym.replace('GreenTheory ', '')}")
    for trainer in gym_trainers:
        left, right = st.columns([4, 1])
        with left:
            st.markdown(card_markup(trainer, detailed=True), unsafe_allow_html=True)
        with right:
            if st.button("Visualizza profilo", key=f"gym_{trainer['name']}", use_container_width=True):
                open_profile(trainer["name"], "palestre")

else:
    st.session_state.page = "home"
    st.rerun()
