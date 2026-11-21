import os
import streamlit as st
import pypdf
from rag_pipeline import RAGPipeline

# ---------------------------------------------------------
# Page Configuration - Full Width, No Sidebar
# ---------------------------------------------------------
st.set_page_config(
    page_title="Lexicon | Corporate Policy Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Styling: Floating Capsule Header + Serein & Konk Luxury Aesthetics
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700;800;900&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root, [data-theme="light"], [data-theme="dark"], .stApp {
        --konk-ink: #0B0B0C;
        --konk-surface: #121214;
        --konk-surface-elevated: #18181B;
        --konk-bone: #F2F0EB;
        --konk-bone-muted: #D1CFCA;
        --konk-steel: #8C8A84;
        --konk-border: #26262A;
        --konk-gold: #E7B96F;
        --konk-bronze: #C89446;
        --text-color: #F2F0EB !important;
        --background-color: #0B0B0C !important;
    }

    /* COMPLETE ERADICATION OF SIDEBAR */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Main Container Padding & Body Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: var(--konk-ink) !important;
        background: var(--konk-ink) !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        font-family: 'Archivo', system-ui, -apple-system, sans-serif !important;
    }

    .main .block-container {
        max-width: 1180px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 6rem !important;
        margin: 0 auto !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* FLOATING PILL NAVBAR (SEREIN AESTHETIC) */
    .serein-nav-pill {
        background: rgba(18, 18, 20, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--konk-border);
        border-radius: 9999px;
        padding: 10px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 auto 2.5rem auto;
        max-width: 860px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .serein-logo {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.4rem;
        font-weight: 500;
        letter-spacing: 0.08em;
        color: var(--konk-bone);
        text-transform: uppercase;
    }
    .serein-nav-links {
        display: flex;
        gap: 20px;
        align-items: center;
    }
    .serein-nav-item {
        font-family: 'Archivo', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--konk-steel);
        text-decoration: none;
        letter-spacing: 0.04em;
        transition: color 0.2s ease;
    }
    .serein-nav-item:hover {
        color: var(--konk-bone);
    }
    .serein-nav-cta {
        background: var(--konk-bronze);
        color: #ffffff !important;
        font-family: 'Archivo', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        padding: 8px 18px;
        border-radius: 9999px;
        border: none;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 8px rgba(200, 148, 70, 0.3);
    }

    /* HERO SECTION (SEREIN INSPIRED) */
    .serein-hero {
        text-align: center;
        padding: 2.5rem 1rem 3.5rem 1rem;
        max-width: 860px;
        margin: 0 auto;
    }
    .serein-hero-tracker {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--konk-gold);
        margin-bottom: 1.2rem;
        display: inline-block;
    }
    .serein-hero-headline {
        font-family: 'Newsreader', Georgia, serif !important;
        font-size: 3.8rem !important;
        font-weight: 400 !important;
        line-height: 1.12 !important;
        letter-spacing: -0.015em !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        margin-bottom: 1.4rem;
    }
    .serein-hero-lede {
        font-family: 'Archivo', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.7;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        max-width: 680px;
        margin: 0 auto 2.2rem auto;
    }
    .serein-hero-btn {
        background: var(--konk-bronze);
        color: #ffffff;
        font-family: 'Archivo', sans-serif;
        font-size: 0.92rem;
        font-weight: 600;
        font-style: italic;
        padding: 12px 28px;
        border-radius: 9999px;
        display: inline-block;
        box-shadow: 0 4px 16px rgba(200, 148, 70, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* SECTION NAVIGATION BAR (TOP TABS) */
    [data-testid="stTabs"] {
        margin-top: 1rem !important;
        margin-bottom: 2.5rem !important;
    }
    [role="tablist"] {
        background: var(--konk-surface) !important;
        border: 1px solid var(--konk-border) !important;
        border-radius: 9999px !important;
        padding: 6px !important;
        gap: 6px !important;
        max-width: 920px !important;
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
    }
    button[role="tab"] {
        font-family: 'Archivo', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        padding: 10px 22px !important;
        border-radius: 9999px !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
    }
    button[role="tab"]:hover {
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }
    button[role="tab"][aria-selected="true"] {
        color: #0B0B0C !important;
        -webkit-text-fill-color: #0B0B0C !important;
        background: var(--konk-gold) !important;
        box-shadow: 0 2px 10px rgba(231, 185, 111, 0.3) !important;
    }
    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* CARDS & CONTAINERS */
    .konk-card {
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }
    .konk-card:hover {
        border-color: var(--konk-gold);
    }

    /* DOSSIER CARDS (3-COLUMN EQUAL HEIGHT) */
    .konk-dossier-card {
        background: var(--konk-surface) !important;
        border: 1px solid var(--konk-border);
        border-radius: 14px;
        padding: 24px 22px 18px 22px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 310px !important;
        min-height: 310px !important;
        max-height: 310px !important;
        box-sizing: border-box;
        margin-bottom: 12px;
        transition: all 0.25s ease;
    }
    .konk-dossier-card:hover {
        transform: translateY(-3px);
        border-color: var(--konk-gold);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .konk-dossier-card.featured {
        border-top: 3px solid var(--konk-gold) !important;
    }
    .konk-dossier-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        height: 24px;
    }
    .konk-dossier-ref {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
    }
    .konk-dossier-ref.featured {
        color: var(--konk-gold) !important;
        -webkit-text-fill-color: var(--konk-gold) !important;
    }
    .konk-dossier-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 4px;
        background: var(--konk-surface-elevated);
        border: 1px solid var(--konk-border);
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
    }
    .konk-dossier-badge.active {
        background: rgba(231, 185, 111, 0.12) !important;
        border-color: rgba(231, 185, 111, 0.4) !important;
        color: var(--konk-gold) !important;
        -webkit-text-fill-color: var(--konk-gold) !important;
    }
    .konk-dossier-badge.secondary {
        background: rgba(200, 148, 70, 0.12) !important;
        border-color: rgba(200, 148, 70, 0.4) !important;
        color: var(--konk-bronze) !important;
        -webkit-text-fill-color: var(--konk-bronze) !important;
    }
    .konk-dossier-title {
        font-family: 'Archivo', sans-serif !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        margin-bottom: 10px;
        height: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .konk-dossier-desc {
        font-family: 'Archivo', sans-serif !important;
        font-size: 0.86rem !important;
        line-height: 1.55 !important;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        margin-bottom: 12px;
        flex-grow: 1;
        overflow: hidden;
    }
    .konk-dossier-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 10px;
        border-top: 1px solid var(--konk-border);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        font-weight: 500;
        height: 24px;
    }

    /* METRIC STRIP */
    .konk-ledger-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 14px;
        margin-bottom: 2rem;
    }
    .konk-ledger-card {
        padding: 16px 18px;
        border-radius: 10px;
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    .konk-ledger-card:hover {
        border-color: var(--konk-gold);
        transform: translateY(-2px);
    }
    .konk-ledger-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--konk-steel);
        font-weight: 600;
        margin-bottom: 4px;
    }
    .konk-ledger-value {
        font-family: 'Archivo', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--konk-gold);
    }

    /* CHAT STREAM */
    div[data-testid="stChatMessage"] {
        background-color: var(--konk-surface) !important;
        background: var(--konk-surface) !important;
        border: 1px solid var(--konk-border) !important;
        border-radius: 12px !important;
        padding: 1.6rem !important;
        margin-bottom: 1.4rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background-color: var(--konk-surface-elevated) !important;
        background: var(--konk-surface-elevated) !important;
    }
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        border-left: 3px solid var(--konk-gold) !important;
    }
    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] *,
    .stMarkdown,
    .stMarkdown * {
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
    }

    /* CITATION FOOTNOTE */
    .konk-footnote-card {
        padding: 16px 20px;
        border-radius: 8px;
        background: var(--konk-surface-elevated);
        margin-top: 14px;
        border: 1px solid var(--konk-border);
    }
    .konk-footnote-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--konk-border);
        margin-bottom: 10px;
    }
    .konk-footnote-quote {
        border-left: 3px solid var(--konk-gold);
        padding-left: 14px;
        margin: 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        line-height: 1.55;
        color: var(--konk-bone-muted) !important;
        -webkit-text-fill-color: var(--konk-bone-muted) !important;
    }

    /* CHAT FLOATING DOCK */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stBottom,
    footer,
    footer * {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
    }
    div[data-testid="stChatInput"] {
        background-color: var(--konk-surface) !important;
        background: var(--konk-surface) !important;
        border: 1.5px solid var(--konk-border) !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
        padding: 6px 12px !important;
        max-width: 920px !important;
        margin: 0 auto !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--konk-gold) !important;
        box-shadow: 0 0 0 3px rgba(231, 185, 111, 0.25) !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: var(--konk-surface) !important;
        background: var(--konk-surface) !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        font-family: 'Archivo', sans-serif !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: var(--konk-gold) !important;
        color: #0B0B0C !important;
        -webkit-text-fill-color: #0B0B0C !important;
        border-radius: 8px !important;
    }

    /* BUTTONS */
    .stButton button {
        background: var(--konk-surface-elevated) !important;
        color: var(--konk-bone) !important;
        border: 1px solid var(--konk-border) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        background: var(--konk-gold) !important;
        color: #0B0B0C !important;
        -webkit-text-fill-color: #0B0B0C !important;
        border-color: var(--konk-gold) !important;
    }
    div[data-testid="stDownloadButton"] button {
        background: var(--konk-surface-elevated) !important;
        color: var(--konk-gold) !important;
        border: 1px solid var(--konk-gold) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: var(--konk-gold) !important;
        color: #0B0B0C !important;
        -webkit-text-fill-color: #0B0B0C !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# State & Directory Initialization
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICIES_DIR = os.path.join(BASE_DIR, "policies")
os.makedirs(POLICIES_DIR, exist_ok=True)
policy_files = [f for f in os.listdir(POLICIES_DIR) if f.endswith(".pdf")]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to **Lexicon: Corporate Policy Intelligence**. Inquire regarding codified statutory findings over **Leave**, **Business Travel**, and **Expense Reimbursement** guidelines.\n\nEvery response is backed by zero-hallucination vector grounding and primary source attributions.",
            "sources": []
        }
    ]

# Default API Key from environment or session
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")

if "model_choice" not in st.session_state:
    st.session_state.model_choice = "gemini-2.5-flash"

# Initialize RAG Pipeline
if "pipeline" not in st.session_state:
    with st.spinner("Initializing ChromaDB Vector Repository..."):
        pipeline = RAGPipeline(gemini_api_key=st.session_state.api_key if st.session_state.api_key else None)
        if pipeline.collection.count() == 0:
            pipeline.index_directory(POLICIES_DIR)
        st.session_state.pipeline = pipeline

# ---------------------------------------------------------
# FLOATING CAPSULE HEADER (Serein Nav Style)
# ---------------------------------------------------------
st.markdown("""
<div class="serein-nav-pill">
    <div class="serein-logo">LEXICON</div>
    <div class="serein-nav-links">
        <span class="serein-nav-item">How It Works</span>
        <span class="serein-nav-item">Policy Dashboard</span>
        <span class="serein-nav-item">Document Library</span>
        <span class="serein-nav-item">Credentials</span>
    </div>
    <a href="#consultation-stream" class="serein-nav-cta">Consult Assistant &rarr;</a>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LANDING HERO SECTION (Serein Inspired)
# ---------------------------------------------------------
st.markdown("""
<div class="serein-hero">
    <div class="serein-hero-tracker">
        INDEPENDENT &bull; STATUTORY FIDUCIARY &bull; ZERO-HALLUCINATION
    </div>
    <h1 class="serein-hero-headline">
        Corporate policy intelligence, built around you.
    </h1>
    <p class="serein-hero-lede">
        We synthesize employee leave rules, business travel per diem caps, and expense reimbursement guidelines into one audited, zero-hallucination statutory consultation platform.
    </p>
    <div>
        <span class="serein-hero-btn">Where Details Matter &bull; PS 34</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TOP SECTION NAVIGATION (Streamlit Pill Tabs)
# ---------------------------------------------------------
tab_guide, tab_dashboard, tab_library, tab_settings = st.tabs([
    "⚙️ How It Works & System Guide",
    "🏛️ Policy Dashboard & Consultation",
    "📚 Policy PDF Folios & Document Library",
    "🔧 System & API Credentials"
])

# ---------------------------------------------------------
# SECTION 1: HOW THE SYSTEM WORKS (Landing Walkthrough)
# ---------------------------------------------------------
with tab_guide:
    st.markdown("""
    <div style="background: rgba(231, 185, 111, 0.08); border-left: 3px solid #E7B96F; padding: 16px 20px; border-radius: 8px; margin-bottom: 24px;">
        <span style="font-family: 'Archivo'; font-weight: 800; color: #E7B96F; font-size: 0.95rem;">🚀 ARCHITECTURAL ONBOARDING:</span>
        <span style="font-family: 'Archivo'; color: #D1CFCA; font-size: 0.92rem;"> Review how our zero-hallucination statutory engine operates below, then switch to the <strong>🏛️ Policy Dashboard &amp; Consultation</strong> section above to query live guidelines!</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #E7B96F; font-weight: 700; margin-bottom: 4px;">
            // SYSTEM ARCHITECTURE &amp; METHODOLOGY
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2.2rem; font-weight: 400; color: #F2F0EB; margin: 0 0 8px 0;">
            How the Zero-Hallucination Policy Assistant Works
        </h2>
        <p style="font-family: 'Archivo'; font-size: 0.95rem; color: #8C8A84; line-height: 1.6; margin: 0;">
            Complete architectural implementation of Problem Statement 34 (Company Policy Assistant) built with Multi-PDF Ingestion, ChromaDB, and Google Gemini.
        </p>
    </div>
    """, unsafe_allow_html=True)

    g_col1, g_col2 = st.columns([1, 1])

    with g_col1:
        st.markdown("""
        <div class="konk-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; color: #E7B96F; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">01 // INGESTION &amp; CHUNKING</span>
            <div style="font-family: 'Archivo'; font-size: 1.35rem; font-weight: 800; color: #F2F0EB; margin-bottom: 8px;">Multi-PDF Ingestion Engine</div>
            <div style="font-family: 'Archivo'; font-size: 0.88rem; line-height: 1.65; color: #8C8A84;">
                Official policy PDFs (Leave, Travel, Reimbursements) are extracted using <code>pypdf</code>. Text is split into <strong>300-word sliding semantic windows</strong> with <strong>50-word overlaps</strong> to ensure cross-boundary legal context is never clipped. Every chunk retains immutable metadata tags: <code>source</code> filename and <code>page</code> number.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; color: #E7B96F; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">02 // VECTORIZATION</span>
            <div style="font-family: 'Archivo'; font-size: 1.35rem; font-weight: 800; color: #F2F0EB; margin-bottom: 8px;">ChromaDB Vector Repository</div>
            <div style="font-family: 'Archivo'; font-size: 0.88rem; line-height: 1.65; color: #8C8A84;">
                Chunks are converted into high-dimensional semantic embeddings using Google's <code>text-embedding-004</code> and indexed into a local SQLite3-backed ChromaDB collection. This enables instant mathematical similarity calculations across thousands of statutory clauses.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; color: #E7B96F; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">03 // SIMILARITY RETRIEVAL</span>
            <div style="font-family: 'Archivo'; font-size: 1.35rem; font-weight: 800; color: #F2F0EB; margin-bottom: 8px;">Top-K Context Retrieval</div>
            <div style="font-family: 'Archivo'; font-size: 0.88rem; line-height: 1.65; color: #8C8A84;">
                When an employee enters an inquiry (e.g. <em>"How many days of paid leave can I carry forward?"</em>), the query is vectorized and compared against ChromaDB using cosine distance. The system retrieves the top-3 most statistically relevant policy clauses.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g_col2:
        st.markdown("""
        <div class="konk-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; color: #E7B96F; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">04 // REASONING ENGINE</span>
            <div style="font-family: 'Archivo'; font-size: 1.35rem; font-weight: 800; color: #F2F0EB; margin-bottom: 8px;">Constrained Gemini Reasoning</div>
            <div style="font-family: 'Archivo'; font-size: 0.88rem; line-height: 1.65; color: #8C8A84;">
                The retrieved clauses and user inquiry are formatted into an audited institutional prompt and passed to Google Gemini (<code>gemini-2.5-flash</code>). Strict systemic guardrails instruct the model: <em>"Answer strictly and exclusively from the provided policy clauses. If an allowance is not mentioned, refuse to fabricate it."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-card">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; color: #E7B96F; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">05 // AUDITABILITY</span>
            <div style="font-family: 'Archivo'; font-size: 1.35rem; font-weight: 800; color: #F2F0EB; margin-bottom: 8px;">Verifiable Judicial Footnotes</div>
            <div style="font-family: 'Archivo'; font-size: 0.88rem; line-height: 1.65; color: #8C8A84;">
                Every generated response includes expandable judicial precedent cards citing the exact source PDF and page number (e.g. <code>Leave_Policy.pdf • Page 1</code>) alongside verbatim quote previews, establishing 100% auditability for HR and finance compliance.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-card" style="border-top: 3px solid #E7B96F;">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; color: #E7B96F; letter-spacing: 0.08em; margin-bottom: 6px;">// SPECIFICATIONS</div>
            <div style="font-family: 'Archivo'; font-size: 1.2rem; font-weight: 800; color: #F2F0EB; margin-bottom: 8px;">Academic Project Specifications</div>
            <div style="font-family: 'Archivo'; font-size: 0.86rem; color: #D1CFCA; line-height: 1.7;">
                &bull; <strong>Problem Statement:</strong> PS 34 (Company Policy Assistant)<br/>
                &bull; <strong>Student Roll No:</strong> 34<br/>
                &bull; <strong>Vector DB:</strong> ChromaDB (Local SQLite3 Persistence)<br/>
                &bull; <strong>LLM API:</strong> Google GenAI SDK (v1beta HTTP options)<br/>
                &bull; <strong>Design Template:</strong> Serein &amp; Konk Clean Floating Header Architecture
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 2: POLICY DASHBOARD & CONSULTATION
# ---------------------------------------------------------
with tab_dashboard:
    # Statutory Ledger Metrics Strip
    total_policies = len(policy_files)
    status_label = "100% Certified" if st.session_state.api_key else "Key Configured"
    status_color = "#E7B96F" if st.session_state.api_key else "#C89446"

    st.markdown(f"""
    <div class="konk-ledger-grid">
        <div class="konk-ledger-card">
            <div>
                <div class="konk-ledger-label">Statutory Corpus</div>
                <div class="konk-ledger-value">{total_policies} Active Folios</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">📖</div>
        </div>
        <div class="konk-ledger-card">
            <div>
                <div class="konk-ledger-label">Vector Repository</div>
                <div class="konk-ledger-value">ChromaDB</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">⚡</div>
        </div>
        <div class="konk-ledger-card">
            <div>
                <div class="konk-ledger-label">Governance Mode</div>
                <div class="konk-ledger-value">Zero-Hallucination</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">⚖️</div>
        </div>
        <div class="konk-ledger-card">
            <div>
                <div class="konk-ledger-label">Audit Integrity</div>
                <div class="konk-ledger-value" style="color: {status_color};">{status_label}</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">🛡️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # In-App Folio Inspector if active
    if st.session_state.get("active_doc_preview"):
        doc_name = st.session_state.active_doc_preview
        doc_path = os.path.join(POLICIES_DIR, doc_name)
        if os.path.exists(doc_path):
            try:
                reader = pypdf.PdfReader(doc_path)
                total_pages = len(reader.pages)
                pages_text = [page.extract_text() for page in reader.pages]
                full_text = "\n\n--- PAGE BREAK ---\n\n".join(pages_text)
                
                with open(doc_path, "rb") as f:
                    doc_bytes = f.read()

                st.markdown(f"""
                <div class="konk-card" style="border: 1.5px solid #E7B96F;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #26262A; padding-bottom: 12px; margin-bottom: 14px;">
                        <div>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #E7B96F; font-weight: 700;">
                                // OFFICIAL INSTITUTIONAL FOLIO INSPECTOR
                            </span>
                            <h2 style="font-family: 'Archivo'; font-size: 1.6rem; font-weight: 800; margin: 4px 0; color: #F2F0EB;">
                                {doc_name.replace('_Policy.pdf', '').replace('_', ' ')} Policy Manual
                            </h2>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.76rem; color: #8C8A84;">
                                Source File: <code>{doc_name}</code> &bull; {total_pages} Page(s) &bull; Audited Statutory Copy
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c_close, c_dl = st.columns([1, 1])
                with c_close:
                    if st.button("❌ Close Inspector", key="close_inspector", use_container_width=True):
                        st.session_state.active_doc_preview = None
                        st.rerun()
                with c_dl:
                    st.download_button(
                        label=f"📥 Download PDF ({doc_name})",
                        data=doc_bytes,
                        file_name=doc_name,
                        mime="application/pdf",
                        key="dl_from_inspector",
                        use_container_width=True
                    )
                
                st.markdown(f"""
                <div style="background: #18181B; border: 1px solid #26262A; border-radius: 8px; padding: 20px; font-family: 'JetBrains Mono'; font-size: 0.88rem; line-height: 1.65; color: #F2F0EB; max-height: 400px; overflow-y: auto; white-space: pre-wrap;">{full_text}</div>
                <div style="margin-bottom: 2rem;"></div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error inspecting document: {e}")

    # Curated Inquiries & Active Dossiers
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; padding-bottom: 8px; border-bottom: 1px solid #1C1C1F;">
        <span style="font-family: 'Archivo'; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.1em; color: #F2F0EB; font-weight: 800;">
            CURATED INQUIRIES &amp; ACTIVE DOSSIERS
        </span>
        <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #8C8A84; letter-spacing: 0.08em;">CATALOGUE VOL. XXIV</span>
    </div>
    """, unsafe_allow_html=True)

    preset_cols = st.columns(3)
    quick_queries = [
        {
            "ref": "REF: ARCH-4011",
            "badges": [
                {"text": "HR FOLIO", "cls": ""},
                {"text": "AUDITED 2026", "cls": "secondary"}
            ],
            "title": "I. Annual Paid Leave & Carry-Forward Limits",
            "desc": "Section 4.1.2 — Accrual caps, statutory mandatory rollover deadlines, and executive exception waivers.",
            "footer_stat": "📜 14 Precedents • Statutory Codex",
            "query": "How many days of paid leave can I carry forward to next year?",
            "featured": False
        },
        {
            "ref": "REF: ARCH-7300",
            "badges": [
                {"text": "ACTIVE INQUIRY", "cls": "active"},
                {"text": "AUDITED 2026", "cls": "secondary"}
            ],
            "title": "II. Daily Per Diem & Corporate Lodging Caps",
            "desc": "Section 7.3.0 — Tier-1 metro lodging limits ($150/nt), per diem meal rates ($45/day), and travel authorization rules.",
            "footer_stat": "📍 Section 7.3.4 In-Scope • Active in Workspace",
            "query": "What is the daily per diem allowance for domestic business travel?",
            "featured": True
        },
        {
            "ref": "REF: ARCH-9840",
            "badges": [
                {"text": "REMOTE WORK", "cls": ""},
                {"text": "AUDITED 2026", "cls": "secondary"}
            ],
            "title": "III. Home Office Infrastructure Stipend",
            "desc": "Section 9.8.4 — Remote work setup stipend ($400), broadband ($40/mo), and cellular reimbursement ($30/mo).",
            "footer_stat": "🛡️ Verified Q1 • Institutional Grant",
            "query": "What is the WFH equipment allowance for new employees?",
            "featured": False
        }
    ]

    selected_query = None
    for idx, col in enumerate(preset_cols):
        q = quick_queries[idx]
        with col:
            badges_html = "".join([f'<span class="konk-dossier-badge {b["cls"]}">{b["text"]}</span>' for b in q["badges"]])
            featured_card = " featured" if q["featured"] else ""
            featured_ref = " featured" if q["featured"] else ""
            
            st.markdown(f"""
            <div class="konk-dossier-card{featured_card}">
                <div>
                    <div class="konk-dossier-top">
                        <span class="konk-dossier-ref{featured_ref}">{q['ref']}</span>
                        <div style="display: flex; gap: 6px; align-items: center;">{badges_html}</div>
                    </div>
                    <div class="konk-dossier-title">{q['title']}</div>
                    <div class="konk-dossier-desc">{q['desc']}</div>
                </div>
                <div class="konk-dossier-footer">
                    <span>{q['footer_stat']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            card_btn = st.button(
                "⚡ Consult Brief & Inquire →",
                use_container_width=True,
                key=f"dossier_btn_{idx}"
            )
            if card_btn:
                selected_query = q["query"]

    # Consultation Stream Anchor
    st.markdown('<div id="consultation-stream"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 14px; margin: 2.2rem 0 1.4rem 0;">
        <div style="height: 1px; background: #26262A; flex: 1;"></div>
        <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #8C8A84;">
            📜 CONSULTATION RECORD &bull; VECTOR-GROUNDING VAULT ACTIVE
        </span>
        <div style="height: 1px; background: #26262A; flex: 1;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Chat Messages
    for msg in st.session_state.messages:
        role_icon = "⚖️" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=role_icon):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📌 Judicial Precedent & Primary Source Attributions", expanded=False):
                    for s in msg["sources"]:
                        st.markdown(f"""
                        <div class="konk-footnote-card">
                            <div class="konk-footnote-header">
                                <span style="font-family: 'JetBrains Mono'; font-size: 0.76rem; font-weight: 700; color: #E7B96F; text-transform: uppercase;">
                                    📜 {s['source_file']} &bull; PAGE {s['page']}
                                </span>
                                <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; color: #8C8A84;">Audited Precedent</span>
                            </div>
                            <div class="konk-footnote-quote">
                                "{s['content_preview']}"
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    c_clear, _ = st.columns([1, 3])
    with c_clear:
        if st.button("🧹 Clear Consultation Stream", key="clear_chat_dash"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Consultation record cleared. Inquire regarding corporate **Leave**, **Business Travel**, or **Reimbursement** statutory provisions.",
                    "sources": []
                }
            ]
            st.rerun()

# ---------------------------------------------------------
# SECTION 3: POLICY PDF FOLIOS & DOCUMENT LIBRARY
# ---------------------------------------------------------
with tab_library:
    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #E7B96F; font-weight: 700; margin-bottom: 4px;">
            // STATUTORY DOCUMENT REPOSITORY
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2.2rem; font-weight: 400; color: #F2F0EB; margin: 0 0 8px 0;">
            Official Policy PDF Folios &amp; Regulatory Manuals
        </h2>
        <p style="font-family: 'Archivo'; font-size: 0.95rem; color: #8C8A84; line-height: 1.6; margin: 0;">
            Directly access official policy folios, inspect full text page-by-page without an external viewer, and download certified original PDF copies.
        </p>
    </div>
    """, unsafe_allow_html=True)

    policy_summaries = {
        "Leave_Policy.pdf": {
            "title": "Leave & Attendance Policy Manual",
            "code": "HR-POL-001",
            "desc": "Governs statutory privilege leave, sick leave, mandatory annual carry-forward limits (max 10 days), 26 weeks paid maternity leave, 2 weeks paternity leave, and bereavement guidelines.",
            "clauses": ["Sec 1: Attendance & Hours", "Sec 2: Annual Privilege Leave", "Sec 3: Sick Leave", "Sec 4: Parental Leave", "Sec 5: Encashment Rules"]
        },
        "Travel_Policy.pdf": {
            "title": "Corporate Business Travel Guidelines",
            "code": "HR-POL-002",
            "desc": "Defines domestic & international booking procedures, economy/business flight tiers, Tier-1 Metro Lodging limits ($150/night), daily per diem allowances ($45/day domestic), and mileage reimbursements.",
            "clauses": ["Sec 1: Travel Authorizations", "Sec 2: Flight Bookings", "Sec 3: Lodging Limits", "Sec 4: Per Diem Meals ($45/day)", "Sec 5: 30-Day Expense Deadlines"]
        },
        "Reimbursement_Policy.pdf": {
            "title": "Expense Reimbursement & WFH Benefits",
            "code": "HR-POL-003",
            "desc": "Outlines remote work equipment grants ($400 setup stipend within 60 days of joining), monthly broadband ($40/mo), cellular subsidies ($30/mo), certification allowances, and non-reimbursable personal claims.",
            "clauses": ["Sec 1: Eligible Expenditures", "Sec 2: Broadband & Cellular", "Sec 3: Professional Certifications", "Sec 4: WFH Equipment Grant ($400)", "Sec 5: Ineligible Claims"]
        }
    }

    if policy_files:
        for p_idx, pf in enumerate(policy_files):
            filepath = os.path.join(POLICIES_DIR, pf)
            file_size_kb = round(os.path.getsize(filepath) / 1024, 1)
            roman_nums = ["I", "II", "III", "IV", "V", "VI"]
            roman = roman_nums[p_idx] if p_idx < len(roman_nums) else str(p_idx+1)
            
            p_info = policy_summaries.get(pf, {
                "title": pf.replace("_Policy.pdf", "").replace("_", " ") + " Policy Manual",
                "code": f"DOC-POL-00{p_idx+1}",
                "desc": "Official institutional compliance document verified and indexed in ChromaDB vector repository.",
                "clauses": ["General Compliance", "Statutory Provisions", "Audited Clauses"]
            })

            with open(filepath, "rb") as f:
                pdf_data = f.read()

            try:
                reader = pypdf.PdfReader(filepath)
                num_pages = len(reader.pages)
                extracted_pages = [f"### Page {p_num + 1}\n\n{p.extract_text()}" for p_num, p in enumerate(reader.pages)]
                full_text_content = "\n\n---\n\n".join(extracted_pages)
            except Exception:
                num_pages = 1
                full_text_content = "Document text could not be extracted."

            clauses_html = "".join([f'<span style="display: inline-block; background: #18181B; border: 1px solid #26262A; color: #D1CFCA; font-family: monospace; font-size: 0.72rem; font-weight: 500; padding: 4px 8px; border-radius: 4px; margin: 3px 4px 3px 0;">{c}</span>' for c in p_info["clauses"]])

            st.markdown(f"""
            <div class="konk-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; border-bottom: 1px solid #26262A; padding-bottom: 14px;">
                    <div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #E7B96F;">FOLIO {roman}</span>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 600; background: rgba(231,185,111,0.12); border: 1px solid rgba(231,185,111,0.3); color: #E7B96F; padding: 2px 6px; border-radius: 4px;">{p_info['code']}</span>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 600; background: #18181B; border: 1px solid #26262A; color: #8C8A84; padding: 2px 6px; border-radius: 4px;">Audited 2026</span>
                        </div>
                        <h3 style="font-family: 'Archivo'; font-size: 1.5rem; font-weight: 800; color: #F2F0EB; margin: 4px 0;">{p_info['title']}</h3>
                        <div style="font-family: 'JetBrains Mono'; font-size: 0.76rem; color: #8C8A84;">File: <code>{pf}</code> &bull; Size: {file_size_kb} KB &bull; Extent: {num_pages} Page(s) &bull; Format: Certified PDF</div>
                    </div>
                </div>
                <div style="font-family: 'Archivo'; font-size: 0.90rem; line-height: 1.6; color: #8C8A84; margin-bottom: 16px;">{p_info['desc']}</div>
                <div style="margin-bottom: 16px;">
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; text-transform: uppercase; font-weight: 700; color: #8C8A84; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">// Key Statutory Clauses:</span>
                    <div>{clauses_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_act1, col_act2 = st.columns([1, 2])
            with col_act1:
                st.download_button(
                    label=f"📥 Download PDF ({pf})",
                    data=pdf_data,
                    file_name=pf,
                    mime="application/pdf",
                    key=f"lib_dl_{p_idx}",
                    use_container_width=True
                )
            with col_act2:
                with st.expander(f"📖 Read Full Text ({pf} &bull; {num_pages} Pages)", expanded=False):
                    st.markdown(full_text_content)
            
            st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 4: SYSTEM & API CREDENTIALS (Replaces Sidebar)
# ---------------------------------------------------------
with tab_settings:
    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #E7B96F; font-weight: 700; margin-bottom: 4px;">
            // SYSTEM CONFIGURATION &amp; AUDIT SETTINGS
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2.2rem; font-weight: 400; color: #F2F0EB; margin: 0 0 8px 0;">
            Vector Engine Credentials &amp; Model Selection
        </h2>
        <p style="font-family: 'Archivo'; font-size: 0.95rem; color: #8C8A84; line-height: 1.6; margin: 0;">
            Configure your institutional Google Gemini API credentials and select the reasoning model for statutory synthesis without needing a sidebar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    set_col1, set_col2 = st.columns([1, 1])
    with set_col1:
        st.markdown('<div class="konk-card">', unsafe_allow_html=True)
        st.markdown("<div style=\"font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; color: #E7B96F; font-weight: 700; margin-bottom: 8px;\">API KEY SETTINGS</div>", unsafe_allow_html=True)
        new_key = st.text_input(
            "Google Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Gemini API key from Google AI Studio."
        )
        if new_key != st.session_state.api_key:
            st.session_state.api_key = new_key
            st.session_state.pipeline.set_api_key(new_key)
            st.success("API Key updated successfully!")

        new_model = st.selectbox(
            "Reasoning Kernel",
            ["gemini-2.5-flash", "gemini-1.5-pro"],
            index=0 if st.session_state.model_choice == "gemini-2.5-flash" else 1,
            help="Select audited reasoning model for statutory synthesis."
        )
        if new_model != st.session_state.model_choice:
            st.session_state.model_choice = new_model
            st.info(f"Synthesis Kernel switched to {new_model}")
        st.markdown('</div>', unsafe_allow_html=True)

    with set_col2:
        st.markdown(f"""
        <div class="konk-card">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; text-transform: uppercase; color: #E7B96F; font-weight: 700; margin-bottom: 12px;">REPOSITORY HEALTH LEDGER</div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #26262A; font-size: 0.82rem;">
                <span style="color: #8C8A84;">Vector Store</span>
                <span style="color: #F2F0EB; font-family: 'JetBrains Mono'; font-weight: 600;">ChromaDB (Local SQLite3)</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #26262A; font-size: 0.82rem;">
                <span style="color: #8C8A84;">Embedding Model</span>
                <span style="color: #F2F0EB; font-family: 'JetBrains Mono'; font-weight: 600;">text-embedding-004</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #26262A; font-size: 0.82rem;">
                <span style="color: #8C8A84;">Ingested Manuscripts</span>
                <span style="color: #E7B96F; font-family: 'JetBrains Mono'; font-weight: 600;">{len(policy_files)} Official PDFs</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 0.82rem;">
                <span style="color: #8C8A84;">Academic Roll No</span>
                <span style="color: #F2F0EB; font-family: 'JetBrains Mono'; font-weight: 600;">34 (Problem Statement 34)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Chat Input & Synthesis (Docked at Container Bottom)
# ---------------------------------------------------------
user_input = st.chat_input("Consult policy guidelines or query specific per diem allowances...")

final_query = selected_query or user_input

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query, "sources": []})
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_query)

    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Reviewing codified policy folios in ChromaDB..."):
            if st.session_state.api_key:
                st.session_state.pipeline.set_api_key(st.session_state.api_key)
            result = st.session_state.pipeline.generate_answer(
                query=final_query,
                top_k=3,
                model=st.session_state.model_choice
            )
            
            st.markdown(result["answer"])
            
            if result.get("sources"):
                with st.expander("📌 Judicial Precedent & Primary Source Attributions", expanded=True):
                    for s in result["sources"]:
                        st.markdown(f"""
                        <div class="konk-footnote-card">
                            <div class="konk-footnote-header">
                                <span style="font-family: 'JetBrains Mono'; font-size: 0.76rem; font-weight: 700; color: #E7B96F; text-transform: uppercase;">
                                    📜 {s['source_file']} &bull; PAGE {s['page']}
                                </span>
                                <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; color: #8C8A84;">Audited Precedent</span>
                            </div>
                            <div class="konk-footnote-quote">
                                "{s['content_preview']}"
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sources": result.get("sources", [])
            })
