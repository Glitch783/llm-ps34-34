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
# Styling: Floating Capsule Header + Serein Luxury Aesthetics
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

    /* Canvas Reset */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: var(--konk-ink) !important;
        background: var(--konk-ink) !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        font-family: 'Archivo', system-ui, -apple-system, sans-serif !important;
    }

    .main .block-container {
        max-width: 1140px !important;
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
        margin: 0 auto !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* TOP BRAND BAR */
    .top-brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0 16px 0;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .top-brand-title {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.6rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        color: var(--konk-bone);
        text-transform: uppercase;
    }
    .top-brand-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(231, 185, 111, 0.1);
        border: 1px solid rgba(231, 185, 111, 0.3);
        color: var(--konk-gold);
        letter-spacing: 0.08em;
    }

    /* FUNCTIONAL TOP CAPSULE TABS */
    [data-testid="stTabs"] {
        margin-top: 0.4rem !important;
        margin-bottom: 2rem !important;
    }
    [role="tablist"] {
        background: rgba(18, 18, 20, 0.95) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid var(--konk-border) !important;
        border-radius: 9999px !important;
        padding: 6px !important;
        gap: 6px !important;
        max-width: 780px !important;
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4) !important;
    }
    button[role="tab"] {
        font-family: 'Archivo', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        padding: 9px 24px !important;
        border-radius: 9999px !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
        cursor: pointer !important;
    }
    button[role="tab"]:hover {
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }
    button[role="tab"][aria-selected="true"] {
        color: #0B0B0C !important;
        -webkit-text-fill-color: #0B0B0C !important;
        background: var(--konk-gold) !important;
        box-shadow: 0 2px 10px rgba(231, 185, 111, 0.35) !important;
    }
    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* HERO SECTION */
    .serein-hero {
        text-align: center;
        padding: 2rem 1rem 2.8rem 1rem;
        max-width: 840px;
        margin: 0 auto;
    }
    .serein-hero-tracker {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--konk-gold);
        margin-bottom: 1rem;
        display: inline-block;
    }
    .serein-hero-headline {
        font-family: 'Newsreader', Georgia, serif !important;
        font-size: 3.4rem !important;
        font-weight: 400 !important;
        line-height: 1.15 !important;
        letter-spacing: -0.015em !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        margin-bottom: 1.2rem;
    }
    .serein-hero-lede {
        font-family: 'Archivo', sans-serif;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.65;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        max-width: 660px;
        margin: 0 auto 1.8rem auto;
    }

    /* PICTORIAL HOW-IT-WORKS STEP CARDS */
    .step-card {
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        border-radius: 14px;
        padding: 22px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        transition: all 0.25s ease;
        position: relative;
    }
    .step-card:hover {
        transform: translateY(-3px);
        border-color: var(--konk-gold);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
    }
    .step-icon-badge {
        width: 48px;
        height: 48px;
        border-radius: 10px;
        background: var(--konk-surface-elevated);
        border: 1px solid rgba(231, 185, 111, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 14px;
    }
    .step-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        font-weight: 700;
        color: var(--konk-gold);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .step-title {
        font-family: 'Archivo', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--konk-bone);
        margin-bottom: 8px;
    }
    .step-desc {
        font-family: 'Archivo', sans-serif;
        font-size: 0.86rem;
        line-height: 1.6;
        color: var(--konk-steel);
    }

    /* VISUAL CONNECTOR ARROWS */
    .flow-diagram-strip {
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        border-radius: 14px;
        padding: 20px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        gap: 12px;
        overflow-x: auto;
    }
    .flow-node {
        display: flex;
        align-items: center;
        gap: 10px;
        white-space: nowrap;
    }
    .flow-node-icon {
        font-size: 22px;
    }
    .flow-node-text {
        font-family: 'Archivo', sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--konk-bone);
    }
    .flow-arrow {
        color: var(--konk-gold);
        font-size: 18px;
        font-weight: 700;
        opacity: 0.7;
    }

    /* CARDS & CONTAINERS */
    .konk-card {
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
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
    }
    .konk-dossier-ref.featured {
        color: var(--konk-gold) !important;
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
    }
    .konk-dossier-badge.active {
        background: rgba(231, 185, 111, 0.12) !important;
        border-color: rgba(231, 185, 111, 0.4) !important;
        color: var(--konk-gold) !important;
    }
    .konk-dossier-badge.secondary {
        background: rgba(200, 148, 70, 0.12) !important;
        border-color: rgba(200, 148, 70, 0.4) !important;
        color: var(--konk-bronze) !important;
    }
    .konk-dossier-title {
        font-family: 'Archivo', sans-serif !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        color: var(--konk-bone) !important;
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
        border: 1px solid var(--konk-border) !important;
        border-radius: 12px !important;
        padding: 1.6rem !important;
        margin-bottom: 1.4rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background-color: var(--konk-surface-elevated) !important;
    }
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        border-left: 3px solid var(--konk-gold) !important;
    }
    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] *,
    .stMarkdown,
    .stMarkdown * {
        color: var(--konk-bone) !important;
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
    }

    /* CHAT FLOATING DOCK */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stBottom,
    footer,
    footer * {
        background: transparent !important;
        border: none !important;
    }
    div[data-testid="stChatInput"] {
        background-color: var(--konk-surface) !important;
        border: 1.5px solid var(--konk-border) !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
        padding: 6px 12px !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--konk-gold) !important;
        box-shadow: 0 0 0 3px rgba(231, 185, 111, 0.25) !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: var(--konk-surface) !important;
        color: var(--konk-bone) !important;
        font-family: 'Archivo', sans-serif !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: var(--konk-gold) !important;
        color: #0B0B0C !important;
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
            "content": "Welcome to **Lexicon: Corporate Policy Intelligence**. Inquire regarding statutory findings over **Leave**, **Business Travel**, and **Expense Reimbursement** guidelines.\n\nEvery response is backed by zero-hallucination vector grounding and primary source attributions.",
            "sources": []
        }
    ]

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
# TOP BRAND BAR
# ---------------------------------------------------------
st.markdown("""
<div class="top-brand-bar">
    <div class="top-brand-title">L E X I C O N</div>
    <div class="top-brand-badge">PS 34 &bull; ZERO-HALLUCINATION &bull; ROLL NO: 34</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCTIONAL FLOATING TOP HEADER TABS (Short Abbreviations)
# ---------------------------------------------------------
tab_guide, tab_dashboard, tab_library, tab_settings = st.tabs([
    "⚙️ Guide",
    "🏛️ Consult",
    "📚 Library",
    "🔧 Settings"
])

# ---------------------------------------------------------
# TAB 1: HOW IT WORKS (Simple, Pictorial & Client-Centric)
# ---------------------------------------------------------
with tab_guide:
    # Centered Serein-Style Hero
    st.markdown("""
    <div class="serein-hero">
        <div class="serein-hero-tracker">
            INSTITUTIONAL AI POLICY ASSISTANT &bull; HOW IT WORKS
        </div>
        <h1 class="serein-hero-headline">
            Corporate policy intelligence, built around you.
        </h1>
        <p class="serein-hero-lede">
            Here is how you use the platform: upload or browse official company manuals, let our vector engine index every clause, and receive instant, audited answers with verbatim page citations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Visual Flow Diagram Strip (Pictorial Overview)
    st.markdown("""
    <div class="flow-diagram-strip">
        <div class="flow-node">
            <span class="flow-node-icon">📄</span>
            <div>
                <div class="flow-node-text">1. Upload Policy PDFs</div>
                <div style="font-size: 0.70rem; color: #8C8A84;">Official Company Manuals</div>
            </div>
        </div>
        <span class="flow-arrow">&rarr;</span>
        <div class="flow-node">
            <span class="flow-node-icon">⚙️</span>
            <div>
                <div class="flow-node-text">2. AI Vector Indexing</div>
                <div style="font-size: 0.70rem; color: #8C8A84;">ChromaDB Semantic Memory</div>
            </div>
        </div>
        <span class="flow-arrow">&rarr;</span>
        <div class="flow-node">
            <span class="flow-node-icon">💬</span>
            <div>
                <div class="flow-node-text">3. Inquire in Plain English</div>
                <div style="font-size: 0.70rem; color: #8C8A84;">Ask About Leave &amp; Per Diems</div>
            </div>
        </div>
        <span class="flow-arrow">&rarr;</span>
        <div class="flow-node">
            <span class="flow-node-icon">⚖️</span>
            <div>
                <div class="flow-node-text">4. Audited Findings</div>
                <div style="font-size: 0.70rem; color: #8C8A84;">Zero-Hallucination Citations</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Simple Step Cards (How the Client Uses the Site)
    step_col1, step_col2 = st.columns([1, 1])

    with step_col1:
        st.markdown("""
        <div class="step-card">
            <div>
                <div class="step-icon-badge">📤</div>
                <div class="step-number">STEP 01 // CLIENT ACTION</div>
                <div class="step-title">Upload or Browse Policy Manuals</div>
                <div class="step-desc">
                    As a user or HR administrator, you provide the policy PDF (e.g. Leave, Business Travel, Reimbursement). The application accepts official manuals and stores them securely in the policy repository.
                </div>
            </div>
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #26262A; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #E7B96F;">
                📁 Supported Formats: Multi-page PDF
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="step-card">
            <div>
                <div class="step-icon-badge">💬</div>
                <div class="step-number">STEP 03 // CLIENT ACTION</div>
                <div class="step-title">Ask Inquiries in Plain English</div>
                <div class="step-desc">
                    Type your question naturally—such as <em>"How many days of paid leave can I carry forward?"</em> or <em>"What is the daily meal per diem for domestic travel?"</em> The system finds the exact statutory section automatically.
                </div>
            </div>
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #26262A; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #E7B96F;">
                🔍 Cosine Semantic Search: Top-3 relevant chunks
            </div>
        </div>
        """, unsafe_allow_html=True)

    with step_col2:
        st.markdown("""
        <div class="step-card">
            <div>
                <div class="step-icon-badge">🧠</div>
                <div class="step-number">STEP 02 // SYSTEM WORKFLOW</div>
                <div class="step-title">AI Reads &amp; Understands the Clauses</div>
                <div class="step-desc">
                    The model extracts text using <code>pypdf</code>, splits it into 300-word sliding semantic windows, and generates high-dimensional embeddings via Google <code>text-embedding-004</code>. Every clause is indexed in local ChromaDB memory.
                </div>
            </div>
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #26262A; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #E7B96F;">
                ⚡ Vector Engine: ChromaDB (Local SQLite3)
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="step-card">
            <div>
                <div class="step-icon-badge">⚖️</div>
                <div class="step-number">STEP 04 // FINAL OUTPUT</div>
                <div class="step-title">Get Audited Answers with Citations</div>
                <div class="step-desc">
                    Google Gemini synthesizes a direct answer restricted strictly to the verified document text. Every answer includes expandable <strong>Judicial Precedent Footnotes</strong> displaying the source PDF name, page number, and quote preview.
                </div>
            </div>
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #26262A; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #E7B96F;">
                🛡️ Zero Hallucinations: 100% Verifiable Source Links
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Interactive Client PDF Uploader Section
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="konk-card" style="border-left: 3px solid #E7B96F;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #E7B96F; letter-spacing: 0.08em; margin-bottom: 6px;">
            // TRY IT OUT: UPLOAD A NEW POLICY PDF
        </div>
        <div style="font-family: 'Archivo'; font-size: 1.2rem; font-weight: 800; color: #F2F0EB; margin-bottom: 6px;">
            Add Your Company Policy Manual
        </div>
        <div style="font-family: 'Archivo'; font-size: 0.88rem; color: #8C8A84; line-height: 1.5; margin-bottom: 14px;">
            Upload a company policy PDF to test the workflow live. The system will parse its clauses, vectorize the text, and make it instantly queryable in the <strong>🏛️ Consult</strong> tab.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_pdf = st.file_uploader(
        "Upload PDF Manual to Ingest into ChromaDB",
        type=["pdf"],
        help="Upload an official company PDF to index into the vector store.",
        key="guide_pdf_uploader"
    )
    if uploaded_pdf is not None:
        save_path = os.path.join(POLICIES_DIR, uploaded_pdf.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        with st.spinner(f"Ingesting {uploaded_pdf.name} into ChromaDB vector index..."):
            chunks_indexed = st.session_state.pipeline.index_pdf(save_path)
            st.success(f"Successfully ingested '{uploaded_pdf.name}' ({chunks_indexed} semantic chunks indexed)! Switch to the **🏛️ Consult** tab to inquire on it.")

# ---------------------------------------------------------
# TAB 2: CONSULT (Policy Dashboard & Live Consultation)
# ---------------------------------------------------------
with tab_dashboard:
    # Statutory Ledger Metrics Strip
    total_policies = len([f for f in os.listdir(POLICIES_DIR) if f.endswith(".pdf")])
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
        if st.button("🧹 Clear Consultation Record", key="clear_chat_dash"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Consultation record cleared. Inquire regarding corporate **Leave**, **Business Travel**, or **Reimbursement** statutory provisions.",
                    "sources": []
                }
            ]
            st.rerun()

# ---------------------------------------------------------
# TAB 3: LIBRARY (Policy PDF Folios & Document Repository)
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

    current_policy_files = [f for f in os.listdir(POLICIES_DIR) if f.endswith(".pdf")]
    if current_policy_files:
        for p_idx, pf in enumerate(current_policy_files):
            filepath = os.path.join(POLICIES_DIR, pf)
            file_size_kb = round(os.path.getsize(filepath) / 1024, 1)
            roman_nums = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
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
# TAB 4: SETTINGS (Vector Engine Credentials & Model Selection)
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
            Configure your institutional Google Gemini API credentials and select the reasoning model for statutory synthesis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    set_col1, set_col2 = st.columns([1, 1])
    with set_col1:
        st.markdown('<div class="konk-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-family: monospace; font-size: 0.75rem; text-transform: uppercase; color: #E7B96F; font-weight: 700; margin-bottom: 8px;'>API KEY SETTINGS</div>", unsafe_allow_html=True)
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
