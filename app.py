import copy
import html
import unicodedata
from datetime import datetime

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

# Seed content for the beta only. A deep copy is placed in session state below,
# so reviews added or edited by visitors never change these source values.
DEMO_REVIEWS = {
    "Luca Bianchi": [
        {"user_name": "Elena", "service_quality": 5, "professionalism": 5, "communication": 4, "demo": True},
        {"user_name": "Paolo", "service_quality": 4, "professionalism": 5, "communication": 4, "demo": True},
    ],
    "Giulia Rossi": [
        {"user_name": "Chiara", "service_quality": 5, "professionalism": 4, "communication": 5, "demo": True},
        {"user_name": "Davide", "service_quality": 4, "professionalism": 4, "communication": 5, "demo": True},
        {"user_name": "Marta", "service_quality": 5, "professionalism": 5, "communication": 4, "demo": True},
    ],
    "Andrea Conti": [
        {"user_name": "Simone", "service_quality": 4, "professionalism": 5, "communication": 4, "demo": True},
        {"user_name": "Alessia", "service_quality": 5, "professionalism": 5, "communication": 4, "demo": True},
    ],
}

DEMO_REQUESTS = [
    {
        "id": "demo-1", "trainer_name": "Andrea Conti", "user_name": "Marco",
        "goal": "Aumento massa muscolare", "service": "Personal training 1:1",
        "message": "Vorrei capire come impostare un percorso di forza e massa.",
        "status": "Nuova", "created_at": "2026-01-02T10:00:00", "demo": True,
    },
    {
        "id": "demo-2", "trainer_name": "Giulia Rossi", "user_name": "Elena",
        "goal": "Dimagrimento", "service": "Percorso introduttivo",
        "message": "Cerco un percorso graduale per ricominciare ad allenarmi.",
        "status": "Da ricontattare", "created_at": "2026-01-01T16:30:00", "demo": True,
    },
]
REQUEST_STATUSES = ["Nuova", "Da ricontattare", "Contattato"]

# Keep the source data immutable: trainer edits live only for the current
# Streamlit session and are automatically discarded when that session ends.
if "trainer_profiles" not in st.session_state:
    st.session_state.trainer_profiles = copy.deepcopy(TRAINERS)
TRAINERS = st.session_state.trainer_profiles
if "reviews" not in st.session_state:
    st.session_state.reviews = copy.deepcopy(DEMO_REVIEWS)
if "requests" not in st.session_state:
    st.session_state.requests = copy.deepcopy(DEMO_REQUESTS)

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
    .block-container { max-width: 1160px; padding-top: 3.5rem; padding-bottom: 3rem; }
    h1, h2, h3 { letter-spacing: -0.035em; }
    .brand { display:block; font-size: 1.05rem; line-height:1.35; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: #194f36; }
    .hero { padding: 4.5rem 3.5rem; border-radius: 28px; background: linear-gradient(125deg,#102b20 0%,#1b5940 68%,#8bbd44 145%); color: white; margin: 1.2rem 0 2rem; }
    .hero h1 { font-size: clamp(2.7rem,6vw,5.4rem); line-height: .98; max-width: 850px; color: white; margin: .4rem 0 1.4rem; }
    .hero p { font-size: 1.16rem; line-height: 1.65; max-width: 680px; color: #e4eee8; }
    .eyebrow { color: #79b947; font-weight: 750; text-transform: uppercase; letter-spacing: .13em; font-size: .78rem; }
    .trainer-card { min-height: 178px; background: white; border: 1px solid #dfe7e1; border-radius: 18px; padding: 1.25rem; margin:.25rem 0 .45rem; box-shadow: 0 8px 26px rgba(25,50,35,.05); }
    .trainer-head { display:flex; align-items:center; gap:.85rem; margin-bottom:.8rem; }
    .trainer-card h3 { margin:0 0 .12rem; font-size:1.18rem; }
    .avatar { width:48px; height:48px; flex:0 0 48px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:#1b6947; color:white; font-weight:800; letter-spacing:.04em; }
    .avatar.large { width:72px; height:72px; flex-basis:72px; font-size:1.25rem; }
    .card-skills { color:#2d4939; font-weight:600; margin:.65rem 0 .5rem; }
    .card-rating { color:#1b6947; font-weight:750; }
    .tag { display: inline-block; background: #edf4eb; color: #28573c; padding: .28rem .62rem; border-radius: 20px; margin: .15rem .1rem; font-size: .78rem; }
    .muted { color: #66736b; font-size: .9rem; }
    .score { color: #1b6947; font-weight: 800; font-size: 1.6rem; }
    .verified { display:inline-block; background:#dff1e4; color:#155b3b; border:1px solid #b9ddc4; padding:.32rem .7rem; border-radius:20px; font-size:.8rem; font-weight:750; }
    .profile-hero { background:white; border:1px solid #dfe7e1; border-radius:22px; padding:1.5rem; margin:.5rem 0 1.2rem; }
    .profile-title { display:flex; gap:1rem; align-items:center; }
    .profile-title h1 { margin:.05rem 0 .35rem; font-size:clamp(2rem,5vw,3.25rem); }
    .profile-meta { color:#536158; margin:.6rem 0 0; }
    .detail-block { background:white; border:1px solid #e2e9e3; border-radius:16px; padding:1rem 1.1rem; margin:.4rem 0; }
    .detail-block h3 { font-size:1rem; margin:0 0 .55rem; }
    .admin-card { background:white; border:1px solid #dfe7e1; border-radius:16px; padding:1rem 1.15rem; margin:.45rem 0; }
    .admin-card h3 { margin:.15rem 0 .25rem; font-size:1.08rem; }
    .admin-line { color:#536158; font-size:.88rem; margin:.2rem 0; }
    .profile-ok { color:#17613f; font-weight:750; }
    .profile-todo { color:#8a5a18; font-weight:750; }
    div.stButton > button { border-radius: 10px; min-height: 2.8rem; font-weight: 700; border-color:#b8c9bd; }
    div.stButton > button:hover { border-color:#1b6947; color:#145238; }
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
    /* Native widgets inherit the brand color from config; these rules also cover focus chrome. */
    :where(input,textarea,button,[role="combobox"]):focus-visible { outline-color:#1b6947 !important; box-shadow:0 0 0 .2rem rgba(27,105,71,.18) !important; }
    [data-testid="stFeedback"] svg { color:#1b6947; }
    footer { visibility:hidden; }
    @media(max-width:700px) {
      .hero { padding:2.5rem 1.35rem; border-radius:22px; }
      .hero h1 { font-size:2.55rem; }
      .block-container { padding:3.5rem 1rem 2.5rem; }
      .profile-title { align-items:flex-start; }
      .avatar.large { width:58px; height:58px; flex-basis:58px; }
      .trainer-card { min-height:0; }
      [data-testid="stHorizontalBlock"] { flex-wrap:wrap; }
      [data-testid="column"] { min-width:min(100%, 280px); }
    }
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


def review_overall(review):
    """Calculate one review's overall score from its three dimensions."""
    return sum(review[field] for field in ("service_quality", "professionalism", "communication")) / 3


def review_summary(reviews):
    """Return calculated aggregate ratings, or None when there are no reviews."""
    if not reviews:
        return None
    count = len(reviews)
    return {
        "overall": sum(review_overall(review) for review in reviews) / count,
        "service_quality": sum(review["service_quality"] for review in reviews) / count,
        "professionalism": sum(review["professionalism"] for review in reviews) / count,
        "communication": sum(review["communication"] for review in reviews) / count,
        "count": count,
    }


def save_review(trainer_name, user_name, service_quality, professionalism, communication):
    """Create or update a review by case-insensitive reviewer name this session."""
    ratings = (service_quality, professionalism, communication)
    if any(not isinstance(rating, int) or not 1 <= rating <= 5 for rating in ratings):
        raise ValueError("Ogni valutazione deve essere compresa tra 1 e 5.")
    reviews = st.session_state.reviews.setdefault(trainer_name, [])
    normalized_name = user_name.strip().casefold()
    new_review = {
        "user_name": user_name.strip(),
        "service_quality": service_quality,
        "professionalism": professionalism,
        "communication": communication,
        "demo": False,
    }
    for index, review in enumerate(reviews):
        if review["user_name"].strip().casefold() == normalized_name:
            reviews[index] = new_review
            return True
    reviews.append(new_review)
    return False


def save_request(trainer_name, user_name, goal, service, message):
    """Save a visitor request in the current session and return its id."""
    next_number = st.session_state.get("next_request_number", 1)
    request_id = f"session-{next_number}"
    st.session_state.next_request_number = next_number + 1
    st.session_state.requests.append({
        "id": request_id, "trainer_name": trainer_name, "user_name": user_name.strip(),
        "goal": goal, "service": service, "message": message.strip(), "status": "Nuova",
        "created_at": datetime.now().isoformat(timespec="microseconds"), "demo": False,
    })
    return request_id


def requests_for(trainer_name):
    """Return only one trainer's requests, newest first."""
    return sorted(
        (request for request in st.session_state.requests if request["trainer_name"] == trainer_name),
        key=lambda request: request["created_at"], reverse=True,
    )


def profile_is_complete(trainer):
    """Use only the six essential public fields for a simple completeness state."""
    required_fields = ("bio", "gym", "skills", "services", "availability", "modalities")
    return all(bool(trainer.get(field)) for field in required_fields)


def admin_summary(trainers):
    """Calculate the demo dashboard metrics from current session data."""
    trainer_names = {trainer["name"] for trainer in trainers}
    reviews = [
        review
        for trainer_name in trainer_names
        for review in st.session_state.reviews.get(trainer_name, [])
    ]
    requests = [
        request for request in st.session_state.requests
        if request.get("trainer_name") in trainer_names
    ]
    return {
        "professionals": len(trainers),
        "gyms": len({trainer["gym"] for trainer in trainers}),
        "requests": len(requests),
        "rating": (sum(review_overall(review) for review in reviews) / len(reviews)) if reviews else None,
    }


def admin_trainer_markup(trainer):
    """Render aggregate professional data without exposing request contents."""
    reviews = st.session_state.reviews.get(trainer["name"], [])
    summary = review_summary(reviews)
    request_count = len(requests_for(trainer["name"]))
    rating = f'{summary["overall"]:.1f} / 5' if summary else "Nessuna valutazione"
    review_count = summary["count"] if summary else 0
    complete = profile_is_complete(trainer)
    profile_label = "Profilo completo" if complete else "Profilo da completare"
    profile_class = "profile-ok" if complete else "profile-todo"
    skills = " · ".join(html.escape(skill) for skill in trainer.get("skills", [])[:3]) or "Competenze da aggiungere"
    return f"""
        <div class="admin-card">
          <div class="trainer-head">{avatar_markup(trainer)}<div><h3>{html.escape(trainer['name'])}</h3>
          <div class="admin-line">{html.escape(trainer['gym'])}</div></div></div>
          <div class="admin-line">{skills}</div>
          <div class="admin-line">★ {rating} · {review_count} recensioni · {request_count} richieste</div>
          <div><span class="verified">Verificato</span> &nbsp; <span class="{profile_class}">{profile_label}</span></div>
        </div>
    """


def trainer_initials(trainer):
    """Return a compact text fallback that can later be replaced by an image."""
    return "".join(part[0] for part in trainer["name"].split()[:2]).upper()


def avatar_markup(trainer, large=False):
    """Centralized, dependency-free trainer avatar markup."""
    size_class = " large" if large else ""
    return f'<div class="avatar{size_class}" aria-hidden="true">{html.escape(trainer_initials(trainer))}</div>'


def card_markup(trainer, detailed=False):
    skills = " · ".join(html.escape(skill) for skill in trainer["skills"][:3])
    bio = f"<p>{html.escape(trainer['bio'])}</p>" if detailed else ""
    summary = review_summary(st.session_state.reviews.get(trainer["name"], []))
    rating = (
        f'★ {summary["overall"]:.1f} · {summary["count"]} '
        f'{"recensione" if summary["count"] == 1 else "recensioni"}'
        if summary else "Nuovo su Trainer Agorà"
    )
    return f"""
        <div class="trainer-card">
          <div class="trainer-head">{avatar_markup(trainer)}<div><h3>{html.escape(trainer['name'])}</h3>
          <div class="muted">{html.escape(trainer['gym'])}</div></div></div>
          {bio}<div class="card-skills">{skills}</div><div class="card-rating">{rating}</div>
        </div>
    """


def render_trainer_card(trainer, key, detailed=False, label="Visualizza profilo", origin="home"):
    """Render the shared trainer card and its full-width, visually connected CTA."""
    st.markdown(card_markup(trainer, detailed=detailed), unsafe_allow_html=True)
    if st.button(f"{label} →", key=key, use_container_width=True):
        open_profile(trainer["name"], origin)


def render_brand():
    st.markdown('<div class="brand">Trainer Agorà</div>', unsafe_allow_html=True)


def render_reviews(trainer, show_review_form=True):
    """Render the compact review summary, details, and optional visitor form."""
    reviews = st.session_state.reviews.get(trainer["name"], [])
    summary = review_summary(reviews)
    st.header("Recensioni")
    st.caption("Le valutazioni inserite restano disponibili per questa sessione.")
    if summary:
        overall, quality, professionalism, communication = st.columns(4)
        overall.metric("Valutazione media", f'{summary["overall"]:.1f} / 5')
        quality.metric("Qualità del servizio", f'{summary["service_quality"]:.1f}')
        professionalism.metric("Professionalità", f'{summary["professionalism"]:.1f}')
        communication.metric("Disponibilità e comunicazione", f'{summary["communication"]:.1f}')
        st.write(f'**{summary["count"]} {"recensione" if summary["count"] == 1 else "recensioni"}**')
        with st.expander("Leggi le singole recensioni"):
            for review in reviews:
                demo_label = " · Demo" if review.get("demo") else ""
                st.markdown(f'**{review["user_name"]}** · {review_overall(review):.1f}/5{demo_label}')
                st.caption(
                    f'Qualità del servizio: {review["service_quality"]}/5 · '
                    f'Professionalità: {review["professionalism"]}/5 · '
                    f'Disponibilità e comunicazione: {review["communication"]}/5'
                )
                st.divider()
    else:
        st.info("Nessuna recensione ancora.")

    if not show_review_form:
        return
    st.subheader("Lascia una recensione")
    st.write("Valuta ogni aspetto da una a cinque stelle.")
    with st.form(f'review_form_{trainer["name"]}'):
        user_name = st.text_input("Il tuo nome", placeholder="Nome")
        st.markdown("**Qualità del servizio**")
        service_quality = st.feedback("stars", key=f'quality_{trainer["name"]}')
        st.markdown("**Professionalità**")
        professionalism = st.feedback("stars", key=f'professionalism_{trainer["name"]}')
        st.markdown("**Disponibilità e comunicazione**")
        communication = st.feedback("stars", key=f'communication_{trainer["name"]}')
        submitted = st.form_submit_button("Invia recensione", type="primary", use_container_width=True)
    if submitted:
        if not user_name.strip():
            st.error("Inserisci il tuo nome per inviare la recensione.")
        elif None in (service_quality, professionalism, communication):
            st.error("Seleziona una valutazione per tutti e tre gli aspetti.")
        else:
            updated = save_review(
                trainer["name"], user_name, service_quality + 1, professionalism + 1, communication + 1
            )
            st.session_state.review_notice = (
                "Hai già recensito questo trainer. La nuova valutazione ha aggiornato quella precedente."
                if updated else "Recensione inviata. Grazie per la tua valutazione!"
            )
            st.rerun()


def render_public_profile(trainer, show_user_actions=True):
    """Render the single public-profile view used by visitors and trainers."""
    summary = review_summary(st.session_state.reviews.get(trainer["name"], []))
    rating = f'★ {summary["overall"]:.1f} · {summary["count"]} recensioni' if summary else "Nessuna recensione"
    st.markdown(
        f'''<section class="profile-hero"><div class="profile-title">{avatar_markup(trainer, large=True)}<div>
        <div class="eyebrow">Professionista verificato</div><h1>{html.escape(trainer["name"])}</h1>
        <div>{html.escape(trainer["gym"])}</div></div></div>
        <div class="profile-meta">{trainer['experience_years']} anni di esperienza · {html.escape(" · ".join(trainer["modalities"]))} &nbsp; | &nbsp; <strong>{rating}</strong></div></section>''',
        unsafe_allow_html=True,
    )
    st.subheader("Il mio approccio")
    st.write(trainer["bio"])
    if not show_user_actions:
        st.caption("Anteprima del profilo pubblico")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        for title, values in (("Competenze", trainer["skills"]), ("Obiettivi seguiti", trainer["goals"]), ("Servizi", trainer["services"])):
            tags = "".join(f'<span class="tag">{html.escape(item)}</span>' for item in values)
            st.markdown(f'<div class="detail-block"><h3>{title}</h3>{tags}</div>', unsafe_allow_html=True)
    with col2:
        for title, values in (("Modalità", trainer["modalities"]), ("Disponibilità", trainer["availability"]), ("Tipo di supporto", trainer["support"]), ("Livelli seguiti", trainer["levels"])):
            st.markdown(f'<div class="detail-block"><h3>{title}</h3>{html.escape(" · ".join(values))}</div>', unsafe_allow_html=True)
    st.divider()
    if show_user_actions:
        notice = st.session_state.pop("request_notice", None)
        if notice and notice[0] == trainer["name"]:
            recipient_preposition = "ad" if trainer["name"][0].lower() in "aeiou" else "a"
            st.success(f"Richiesta inviata {recipient_preposition} {trainer['name']}.")
            st.write("Nella versione completa il trainer potrà ricontattarti tramite Trainer Agorà.")
        form_key = f'request_form_open_{trainer["name"]}'
        if not st.session_state.get(form_key, False):
            if st.button("Sono interessato a questo trainer", type="primary", use_container_width=True):
                st.session_state[form_key] = True
                st.rerun()
        else:
            st.subheader("Invia una richiesta di contatto")
            st.caption("Racconta brevemente al trainer che tipo di supporto stai cercando.")
            with st.form(f'contact_request_{trainer["name"]}', clear_on_submit=True):
                user_name = st.text_input("Il tuo nome", placeholder="Nome")
                goal = st.selectbox("Obiettivo", GOALS)
                service = st.selectbox("Servizio di interesse", trainer["services"])
                message = st.text_area("Messaggio opzionale", placeholder="Aggiungi qualche dettaglio utile")
                submitted = st.form_submit_button("Invia richiesta", type="primary", use_container_width=True)
            if submitted:
                if not user_name.strip():
                    st.error("Inserisci il tuo nome per inviare la richiesta.")
                else:
                    save_request(trainer["name"], user_name, goal, service, message)
                    st.session_state[form_key] = False
                    st.session_state.request_notice = (trainer["name"], True)
                    st.rerun()
    if notice := st.session_state.pop("review_notice", None):
        st.success(notice)
    render_reviews(trainer, show_review_form=show_user_actions)


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

    st.caption("Sei un professionista?")
    if st.button("Accedi all'Area Trainer", type="tertiary"):
        go_to("area_trainer")

    st.caption("Per GreenTheory")
    if st.button("Area GreenTheory", type="tertiary"):
        go_to("area_greentheory")

    st.markdown("### Trova un trainer")
    query = st.text_input(
        "Cerca per nome, palestra, competenza, obiettivo, servizio o modalità",
        placeholder="Es. Andrea, Monza, mobilità, ipertrofia, online…",
    )
    if query.strip():
        matches = search_trainers(query)
        st.caption(f"{len(matches)} {'risultato' if len(matches) == 1 else 'risultati'}")
        for trainer in matches:
            render_trainer_card(trainer, f"search_{trainer['name']}")
        if not matches:
            st.info("Nessun professionista corrisponde alla ricerca. Prova con una competenza o una sede diversa.")

    st.divider()
    st.markdown('<div class="eyebrow">Professionisti GreenTheory</div>', unsafe_allow_html=True)
    st.header("Trainer in evidenza")
    cols = st.columns(3)
    for col, trainer in zip(cols, [TRAINERS[1], TRAINERS[2], TRAINERS[3]]):
        with col:
            render_trainer_card(trainer, f"featured_{trainer['name']}", detailed=True, label="Scopri il profilo")

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
            st.caption(f"SCELTA {position} · Compatibilità {score}/100")
            st.markdown(card_markup(trainer), unsafe_allow_html=True)
            st.markdown("**Perché te lo consigliamo**")
            st.write("; ".join(reason.capitalize() for reason in reasons) + ".")
            if st.button("Visualizza profilo →", key=f"result_{trainer['name']}", use_container_width=True):
                open_profile(trainer["name"], "risultati")
    if len(suitable) < 3:
        st.info(f"Ti mostriamo {len(suitable)} {'profilo' if len(suitable) == 1 else 'profili'} davvero pertinente. Preferiamo non suggerirti trainer poco adatti: modifica una preferenza per ampliare la selezione.")

elif page == "profilo":
    trainer = trainer_by_name(st.session_state.get("selected_trainer"))
    if trainer is None:
        go_to("home")
    origin = st.session_state.get("profile_origin", "home")
    back_labels = {"risultati": "← Torna ai risultati", "palestre": "← Torna alla palestra", "home": "← Torna alla home", "dashboard_trainer": "← Torna alla dashboard"}
    render_brand()
    if st.button(back_labels.get(origin, "← Torna alla home")):
        go_to(origin if origin in {"risultati", "palestre", "dashboard_trainer"} else "home")
    render_public_profile(trainer, show_user_actions=origin != "dashboard_trainer")

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
        render_trainer_card(trainer, f"gym_{trainer['name']}", detailed=True, origin="palestre")

elif page == "area_trainer":
    render_brand()
    if st.button("← Torna alla home"):
        go_to("home")
    st.markdown('<div class="eyebrow">Spazio professionisti</div>', unsafe_allow_html=True)
    st.title("Area Trainer")
    st.subheader("Gestisci il tuo profilo professionale su Trainer Agorà.")
    with st.form("trainer_login"):
        names = [trainer["name"] for trainer in TRAINERS]
        current = st.session_state.get("logged_trainer", names[0])
        selected = st.selectbox("Accedi come", names, index=names.index(current) if current in names else 0)
        if st.form_submit_button("Entra nella dashboard", type="primary", use_container_width=True):
            st.session_state.logged_trainer = selected
            go_to("dashboard_trainer")

elif page == "area_greentheory":
    render_brand()
    if st.button("← Torna alla home"):
        go_to("home")
    st.markdown('<div class="eyebrow">Vista demo GreenTheory</div>', unsafe_allow_html=True)
    st.title("GreenTheory Network")
    st.write("Panoramica dei professionisti e delle interazioni nel network.")
    st.caption("Vista dimostrativa con dati aggregati della sessione.")

    gym_options = ["Tutte le palestre"] + list(dict.fromkeys(trainer["gym"] for trainer in TRAINERS))
    selected_gym = st.selectbox("Filtra per palestra", gym_options, key="admin_gym_filter")
    filtered_trainers = (
        TRAINERS if selected_gym == "Tutte le palestre"
        else [trainer for trainer in TRAINERS if trainer["gym"] == selected_gym]
    )
    metrics = admin_summary(filtered_trainers)
    metric_columns = st.columns(4)
    metric_columns[0].metric("Professionisti", metrics["professionals"])
    metric_columns[1].metric("Palestre", metrics["gyms"])
    metric_columns[2].metric("Richieste", metrics["requests"])
    metric_columns[3].metric(
        "Rating network",
        f'{metrics["rating"]:.1f} / 5' if metrics["rating"] is not None else "—",
    )

    st.header("Network professionisti")
    st.write("Stato sintetico dei profili e delle interazioni, senza dati personali delle richieste.")
    visible_gyms = list(dict.fromkeys(trainer["gym"] for trainer in filtered_trainers))
    for gym in visible_gyms:
        gym_trainers = [trainer for trainer in filtered_trainers if trainer["gym"] == gym]
        st.subheader(gym)
        st.caption(f'{len(gym_trainers)} {"professionista" if len(gym_trainers) == 1 else "professionisti"}')
        for trainer in gym_trainers:
            st.markdown(admin_trainer_markup(trainer), unsafe_allow_html=True)

elif page == "dashboard_trainer":
    trainer = trainer_by_name(st.session_state.get("logged_trainer"))
    if trainer is None:
        go_to("area_trainer")
    render_brand()
    if st.session_state.pop("profile_saved", False):
        st.success("Profilo aggiornato. Le modifiche sono già visibili nel profilo pubblico e nella ricerca.")
    header, home = st.columns([4, 1])
    with header:
        st.markdown('<div class="eyebrow">Dashboard trainer</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="profile-title">{avatar_markup(trainer)}<div><h1>{html.escape(trainer["name"])}</h1>'
            f'<div>{html.escape(trainer["gym"])}</div></div></div>', unsafe_allow_html=True,
        )
        completion = "Profilo completo" if profile_is_complete(trainer) else "Profilo da completare"
        st.markdown(f'<span class="verified">Professionista verificato</span> &nbsp; <strong>{completion}</strong>', unsafe_allow_html=True)
        st.caption(f'{trainer["experience_years"]} anni di esperienza · {" · ".join(trainer["modalities"])}')
    with home:
        if st.button("Torna alla Home", use_container_width=True):
            go_to("home")
    trainer_reviews = st.session_state.reviews.get(trainer["name"], [])
    ratings = review_summary(trainer_reviews)
    trainer_requests = requests_for(trainer["name"])
    new_requests = sum(request["status"] == "Nuova" for request in trainer_requests)
    kpis = st.columns(4)
    kpis[0].metric("Valutazione", f'{ratings["overall"]:.1f} / 5' if ratings else "—")
    kpis[1].metric("Recensioni", ratings["count"] if ratings else 0)
    kpis[2].metric("Richieste", len(trainer_requests))
    kpis[3].metric("Nuove", new_requests)
    st.markdown("### Recensioni ricevute")
    if ratings:
        with st.expander("Le mie recensioni"):
            for review in trainer_reviews:
                st.markdown(f'**{review["user_name"]}** · {review_overall(review):.1f}/5')
                st.caption(
                    f'Qualità: {review["service_quality"]}/5 · Professionalità: {review["professionalism"]}/5 · '
                    f'Comunicazione: {review["communication"]}/5'
                )
    else:
        st.info("Nessuna recensione ancora")
    st.markdown("### Azioni principali")
    edit, public, requests = st.columns(3)
    with edit:
        if st.button("Modifica profilo", type="primary", use_container_width=True):
            go_to("modifica_trainer")
    with public:
        if st.button("Visualizza profilo pubblico", use_container_width=True):
            open_profile(trainer["name"], "dashboard_trainer")
    with requests:
        if st.button("Richieste ricevute", use_container_width=True):
            go_to("richieste_trainer")

elif page == "modifica_trainer":
    trainer = trainer_by_name(st.session_state.get("logged_trainer"))
    if trainer is None:
        go_to("area_trainer")
    render_brand()
    if st.button("← Torna alla dashboard"):
        go_to("dashboard_trainer")
    st.markdown('<div class="eyebrow">Area Trainer</div>', unsafe_allow_html=True)
    st.title("Modifica profilo")

    def choices(field, defaults):
        return list(dict.fromkeys(defaults + [value for profile in TRAINERS for value in profile[field]]))

    with st.form("edit_trainer"):
        bio = st.text_area("Bio", value=trainer["bio"], height=130)
        gym_options = list(dict.fromkeys(GYMS + [profile["gym"] for profile in TRAINERS]))
        gym = st.selectbox("Palestra", gym_options, index=gym_options.index(trainer["gym"]))
        experience = st.number_input("Anni di esperienza", min_value=0, max_value=50, value=trainer["experience_years"], step=1)
        skills = st.multiselect("Competenze", choices("skills", []), default=trainer["skills"], accept_new_options=True)
        goals = st.multiselect("Obiettivi seguiti", choices("goals", GOALS), default=trainer["goals"])
        levels = st.multiselect("Livelli seguiti", choices("levels", LEVELS), default=trainer["levels"])
        services = st.multiselect("Servizi offerti", choices("services", []), default=trainer["services"], accept_new_options=True)
        support = st.multiselect("Tipo di supporto", choices("support", SUPPORT_TYPES), default=trainer["support"])
        availability = st.multiselect("Fasce orarie disponibili", choices("availability", TIME_SLOTS), default=trainer["availability"])
        modalities = st.multiselect("Modalità", ["In presenza", "Online"], default=trainer["modalities"])
        submitted = st.form_submit_button("Salva modifiche", type="primary", use_container_width=True)
    if submitted:
        trainer.update({"bio": bio.strip(), "gym": gym, "experience_years": int(experience), "skills": skills,
                        "goals": goals, "levels": levels, "services": services, "support": support,
                        "availability": availability, "modalities": modalities})
        st.session_state.profile_saved = True
        go_to("dashboard_trainer")

elif page == "richieste_trainer":
    trainer = trainer_by_name(st.session_state.get("logged_trainer"))
    if trainer is None:
        go_to("area_trainer")
    render_brand()
    if st.button("← Torna alla dashboard"):
        go_to("dashboard_trainer")
    st.markdown('<div class="eyebrow">Area Trainer</div>', unsafe_allow_html=True)
    st.title("Richieste ricevute")
    st.caption("Le richieste restano disponibili solo durante questa sessione. Alcuni contenuti iniziali sono dimostrativi.")
    requests = requests_for(trainer["name"])
    if not requests:
        st.info("Nessuna richiesta ricevuta al momento. Quando una persona sarà interessata ai tuoi servizi, la sua richiesta comparirà qui.")
    for request in requests:
        with st.container(border=True):
            heading, state = st.columns([3, 2])
            with heading:
                st.subheader(request["user_name"])
                st.write(f'**Obiettivo:** {request["goal"]}  \n**Servizio:** {request["service"]}')
                if request["message"]:
                    st.write(request["message"])
                if request.get("demo"):
                    st.caption("Contenuto dimostrativo beta")
            with state:
                selected_status = st.selectbox(
                    "Stato", REQUEST_STATUSES, index=REQUEST_STATUSES.index(request["status"]),
                    key=f'request_status_{request["id"]}',
                )
                if selected_status != request["status"]:
                    request["status"] = selected_status

else:
    st.session_state.page = "home"
    st.rerun()
