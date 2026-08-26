import streamlit as st

st.set_page_config(page_title="Trainer Agorà", layout="wide")

# -------------------------
# DATI TRAINER DEMO
# -------------------------

trainers = [
    {
        "name": "Luca Bianchi",
        "gym": "GreenTheory Milano Centrale",
        "goals": ["Aumento massa muscolare", "Forza"],
        "levels": ["Intermedio", "Avanzato"],
        "experience": "7 anni di esperienza",
        "specialties": "Ipertrofia · Forza · Bodybuilding",
    },
    {
        "name": "Giulia Rossi",
        "gym": "GreenTheory Monza",
        "goals": ["Dimagrimento", "Benessere generale"],
        "levels": ["Principiante", "Intermedio"],
        "experience": "5 anni di esperienza",
        "specialties": "Dimagrimento · Ricomposizione corporea",
    },
    {
        "name": "Andrea Conti",
        "gym": "GreenTheory Monza",
        "goals": ["Forza", "Aumento massa muscolare"],
        "levels": ["Intermedio", "Avanzato"],
        "experience": "8 anni di esperienza",
        "specialties": "Forza · Ipertrofia · Preparazione atletica",
    },
    {
        "name": "Martina Ferri",
        "gym": "GreenTheory Milano Porta Romana",
        "goals": ["Benessere generale", "Mobilità e postura"],
        "levels": ["Principiante", "Intermedio"],
        "experience": "6 anni di esperienza",
        "specialties": "Mobilità · Postura · Benessere",
    },
    {
        "name": "Federico Sala",
        "gym": "GreenTheory Milano Centrale",
        "goals": ["Forza", "Aumento massa muscolare"],
        "levels": ["Intermedio", "Avanzato"],
        "experience": "9 anni di esperienza",
        "specialties": "Strength training · Ipertrofia",
    },
    {
        "name": "Sara Romano",
        "gym": "GreenTheory Monza",
        "goals": ["Mobilità e postura", "Benessere generale"],
        "levels": ["Principiante", "Intermedio"],
        "experience": "4 anni di esperienza",
        "specialties": "Mobilità · Postura · Functional training",
    },
]


# -------------------------
# NAVIGAZIONE
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"


def go_to(page):
    st.session_state.page = page
    st.rerun()


# -------------------------
# MATCHING
# -------------------------

def calculate_match(trainer, goal, level, gym):
    score = 0
    reasons = []

    if goal in trainer["goals"]:
        score += 45
        reasons.append("è specializzato nel tuo obiettivo")

    if trainer["gym"] == gym:
        score += 35
        reasons.append("opera nella palestra che frequenti")

    if level in trainer["levels"]:
        score += 20
        reasons.append("segue utenti con il tuo livello")

    return score, reasons


# -------------------------
# HOME
# -------------------------

if st.session_state.page == "home":

    st.title("Trainer Agorà")
    st.subheader("Trova il trainer giusto, nella palestra giusta.")

    st.write(
        "Scopri i professionisti disponibili nella tua palestra "
        "e trova quello più adatto ai tuoi obiettivi."
    )

    st.divider()

    if st.button(
        "Trova il mio trainer",
        type="primary",
        use_container_width=True
    ):
        go_to("questionario")

    if st.button(
        "Esplora le palestre",
        use_container_width=True
    ):
        go_to("palestre")

# -------------------------
# QUESTIONARIO
# -------------------------

elif st.session_state.page == "questionario":

    if st.button("← Torna alla Home"):
        go_to("home")

    st.title("Trova il trainer più adatto a te")

    st.write(
        "Rispondi a poche domande e scopri i professionisti "
        "più compatibili con quello che stai cercando."
    )

    with st.form("questionario"):

        goal = st.radio(
            "Qual è il tuo obiettivo principale?",
            [
                "Aumento massa muscolare",
                "Dimagrimento",
                "Forza",
                "Benessere generale",
                "Mobilità e postura",
            ],
        )

        level = st.radio(
            "Qual è il tuo livello?",
            [
                "Principiante",
                "Intermedio",
                "Avanzato",
            ],
        )

        gym = st.selectbox(
            "Quale GreenTheory frequenti?",
            [
                "GreenTheory Milano Centrale",
                "GreenTheory Milano Porta Romana",
                "GreenTheory Monza",
            ],
        )

        submitted = st.form_submit_button(
            "Trova i trainer per me",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        st.session_state.answers = {
            "goal": goal,
            "level": level,
            "gym": gym,
        }

        go_to("risultati")

# -------------------------
# RISULTATI
# -------------------------

elif st.session_state.page == "risultati":

    if "answers" not in st.session_state:
        go_to("questionario")

    answers = st.session_state.answers

    if st.button("← Modifica le risposte"):
        go_to("questionario")

    st.title("I trainer più adatti a te")

    st.write(
        f"Abbiamo confrontato il tuo obiettivo **{answers['goal']}**, "
        f"il tuo livello **{answers['level']}** e la palestra "
        f"**{answers['gym']}**."
    )

    results = []

    for trainer in trainers:

        score, reasons = calculate_match(
            trainer,
            answers["goal"],
            answers["level"],
            answers["gym"],
        )

        results.append(
            {
                "trainer": trainer,
                "score": score,
                "reasons": reasons,
            }
        )

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    st.divider()

    for position, result in enumerate(results[:3], start=1):

        trainer = result["trainer"]
        score = result["score"]
        reasons = result["reasons"]

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"### {position}. {trainer['name']}"
                )

                st.write(trainer["specialties"])

                st.caption(trainer["gym"])

                st.write(trainer["experience"])

            with col2:

                st.metric(
                    "Compatibilità",
                    f"{score}%"
                )

            st.markdown("**Perché te lo consigliamo**")

            if reasons:

                st.write(
                    trainer["name"]
                    + " "
                    + ", ".join(reasons)
                    + "."
                )

            else:

                st.write(
                    "Potrebbe comunque essere interessante "
                    "per ampliare la tua ricerca."
                )

            if st.button(
                "Visualizza profilo",
                key=trainer["name"],
                use_container_width=True,
            ):
                st.session_state.selected_trainer = trainer["name"]
                st.session_state.profile_origin = "risultati"
                go_to("profilo")

    st.divider()

    if st.button(
        "Torna alla Home",
        use_container_width=True
    ):
        go_to("home")


# -------------------------
# PROFILO TRAINER
# -------------------------

elif st.session_state.page == "profilo":

    trainer_name = st.session_state.get("selected_trainer")

    trainer = next(
        (t for t in trainers if t["name"] == trainer_name),
        None
    )

    if trainer is None:
        go_to("home")

    origin = st.session_state.get("profile_origin", "risultati")

    if origin == "palestre":
        if st.button("← Torna alla palestra"):
            go_to("palestre")
    else:
        if st.button("← Torna ai risultati"):
            go_to("risultati")

    st.title(trainer["name"])
    st.subheader(trainer["specialties"])

    st.caption(trainer["gym"])

    st.write(trainer["experience"])

    st.divider()

    st.subheader("Profilo professionale")

    profiles = {
        "Andrea Conti": {
            "bio": "Personal trainer specializzato nello sviluppo della forza, ipertrofia e preparazione atletica. Il suo approccio combina programmazione strutturata e progressione personalizzata.",
            "skills": [
                "Ipertrofia",
                "Strength training",
                "Preparazione atletica",
                "Tecnica degli esercizi",
            ],
            "services": [
                "Personal training 1:1",
                "Programma di allenamento personalizzato",
                "Valutazione iniziale",
                "Monitoraggio dei progressi",
            ],
        },
        "Luca Bianchi": {
            "bio": "Trainer orientato a bodybuilding, forza e sviluppo della massa muscolare.",
            "skills": [
                "Bodybuilding",
                "Ipertrofia",
                "Forza",
            ],
            "services": [
                "Personal training 1:1",
                "Schede personalizzate",
                "Programmazione mensile",
            ],
        },
        "Giulia Rossi": {
            "bio": "Personal trainer focalizzata su ricomposizione corporea, dimagrimento e costruzione di abitudini sostenibili.",
            "skills": [
                "Ricomposizione corporea",
                "Dimagrimento",
                "Allenamento principianti",
            ],
            "services": [
                "Personal training 1:1",
                "Percorsi personalizzati",
                "Programmazione allenamento",
            ],
        },
        "Sara Romano": {
            "bio": "Trainer specializzata in mobilità, postura, functional training e benessere generale.",
            "skills": [
                "Mobilità",
                "Postura",
                "Functional training",
            ],
            "services": [
                "Personal training",
                "Sessioni di mobilità",
                "Programmi personalizzati",
            ],
        },
    }

    default_profile = {
        "bio": "Professionista del fitness con esperienza nella programmazione e nell'allenamento personalizzato.",
        "skills": trainer["goals"],
        "services": [
            "Personal training 1:1",
            "Programmi personalizzati",
            "Valutazione iniziale",
        ],
    }

    profile = profiles.get(
        trainer["name"],
        default_profile
    )

    st.write(profile["bio"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Competenze")

        for skill in profile["skills"]:
            st.write("✓", skill)

    with col2:
        st.subheader("Servizi")

        for service in profile["services"]:
            st.write("✓", service)

    st.divider()

    st.subheader("Dove puoi trovarmi")

    st.write("📍", trainer["gym"])

    st.divider()

    if st.button(
        "Sono interessato a questo trainer",
        type="primary",
        use_container_width=True
    ):
        st.success(
            "Interesse registrato. Nella versione completa da qui potrai contattare il trainer."
        )


# -------------------------
# ESPLORA PALESTRE
# -------------------------

elif st.session_state.page == "palestre":

    if st.button("← Torna alla Home"):
        go_to("home")

    st.title("Esplora le palestre")

    st.write(
        "Trova la sede che frequenti e scopri subito "
        "i professionisti disponibili."
    )

    selected_gym = st.selectbox(
        "Scegli una palestra",
        [
            "GreenTheory Milano Centrale",
            "GreenTheory Milano Porta Romana",
            "GreenTheory Monza",
        ],
    )

    gym_trainers = [
        trainer
        for trainer in trainers
        if trainer["gym"] == selected_gym
    ]

    st.divider()

    st.subheader(selected_gym)

    st.write(
        f"{len(gym_trainers)} professionisti disponibili"
    )

    for trainer in gym_trainers:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {trainer['name']}")
                st.write(trainer["specialties"])
                st.caption(trainer["experience"])

            with col2:
                if st.button(
                    "Visualizza profilo",
                    key=f"gym_{trainer['name']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_trainer = trainer["name"]
                    st.session_state.profile_origin = "palestre"
                    go_to("profilo")
