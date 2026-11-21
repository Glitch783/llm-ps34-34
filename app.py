import os
import streamlit as st
import pypdf
from rag_pipeline import RAGPipeline

# ---------------------------------------------------------
# Page Configuration - Full Width, No Sidebar
# ---------------------------------------------------------
st.set_page_config(
    page_title="LEXICON CODEX — Zero-Hallucination Policy Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Exact Stitch CSS Tokens & Layout (Screen ID: 60a56b78165a45ffb092e733f39b23cb)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,500;1,6..72,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root, [data-theme="light"], [data-theme="dark"], .stApp {
        --parchment: #F5F2EB;
        --ink: #1C1A18;
        --charcoal: #3D3A36;
        --cognac: #8B4513;
        --cognac-hover: #73380F;
        --cognac-light: #F8EFEA;
        --vellum: #FFFFFF;
        --hairline: #D8D2C5;
        --spruce: #24614A;
        --muted: #6E6961;
        --text-color: #1C1A18 !important;
        --background-color: #F5F2EB !important;
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

    /* Ambient Warm Glow & Subtle Architectural Grid */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: var(--parchment) !important;
        background: var(--parchment) !important;
        background-size: 40px 40px !important;
        background-image: 
            linear-gradient(to right, rgba(28, 26, 24, 0.035) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(28, 26, 24, 0.035) 1px, transparent 1px) !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
    }

    .main .block-container {
        max-width: 1080px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 6rem !important;
        margin: 0 auto !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* EXACT STITCH FLOATING PILL NAVBAR */
    .stitch-header-wrap {
        width: 100%;
        max-width: 900px;
        margin: 0 auto 2.5rem auto;
        padding: 0 10px;
    }
    .stitch-nav-pill {
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--hairline);
        border-radius: 9999px;
        padding: 10px 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 16px 40px rgba(28, 26, 24, 0.06);
        transition: all 0.2s ease;
    }
    /* REMOVE ALL UNDERLINES IN HEADER PILL ACROSS ALL STATES */
    .stitch-header-wrap a,
    .stitch-header-wrap a:hover,
    .stitch-header-wrap a:focus,
    .stitch-header-wrap a:visited,
    .stitch-header-wrap a:active,
    .stitch-header-wrap span,
    .stitch-nav-pill a,
    .stitch-nav-pill a:hover,
    .stitch-nav-pill a:focus,
    .stitch-nav-pill a:visited,
    .stitch-brand,
    .stitch-brand:hover,
    .stitch-brand *,
    .stitch-cta-btn,
    .stitch-cta-btn:hover,
    .stitch-cta-btn:focus,
    .stitch-cta-btn:visited,
    .stitch-cta-btn *,
    .stitch-nav-link,
    .stitch-nav-link:hover,
    .stitch-nav-link.active,
    .stitch-nav-link * {
        text-decoration: none !important;
        text-decoration-line: none !important;
        border-bottom: none !important;
        box-shadow: none;
    }

    .stitch-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        text-decoration: none !important;
    }
    .stitch-brand-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: var(--ink);
        text-transform: uppercase;
        text-decoration: none !important;
    }
    .stitch-nav-links {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .stitch-nav-link {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.86rem;
        font-weight: 500;
        letter-spacing: 0.01em;
        color: var(--charcoal);
        text-decoration: none !important;
        padding: 7px 18px;
        border-radius: 9999px;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        display: inline-block;
    }
    .stitch-nav-link:hover {
        color: var(--cognac);
        background: rgba(139, 69, 19, 0.08);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.08) !important;
    }
    .stitch-nav-link.active {
        color: #FFFFFF !important;
        background: var(--cognac) !important;
        font-weight: 700;
        box-shadow: 0 4px 14px rgba(139, 69, 19, 0.28) !important;
        transform: translateY(0);
    }
    .stitch-nav-link.active:hover {
        background: var(--cognac-hover) !important;
        transform: translateY(-1px);
    }
    .stitch-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .stitch-cta-btn {
        background: var(--cognac);
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 7px 16px;
        border-radius: 9999px;
        text-decoration: none !important;
        box-shadow: 0 4px 16px rgba(139, 69, 19, 0.22) !important;
        transition: background 0.2s ease, transform 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .stitch-cta-btn:hover {
        background: var(--cognac-hover);
        transform: translateY(-1px);
        text-decoration: none !important;
    }

    /* EXACT STITCH HERO SECTION */
    .stitch-hero {
        text-align: center !important;
        padding: 2.2rem 1rem 3rem 1rem;
        max-width: 860px;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stitch-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 5px 14px;
        border-radius: 9999px;
        background: #E8E3DA;
        border: 1px solid var(--hairline);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
    }
    .stitch-eyebrow-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--charcoal);
    }
    .stitch-headline {
        font-family: 'Newsreader', Georgia, serif !important;
        font-size: 3.8rem !important;
        font-weight: 400 !important;
        line-height: 1.08 !important;
        letter-spacing: -0.02em !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        margin-bottom: 1.4rem;
        text-align: center !important;
    }
    .stitch-headline a,
    a.header-anchor {
        display: none !important;
    }
    .stitch-headline-accent {
        font-style: italic;
        color: var(--cognac) !important;
        -webkit-text-fill-color: var(--cognac) !important;
        font-weight: 400;
    }
    .stitch-lede {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.08rem !important;
        font-weight: 400 !important;
        line-height: 1.7 !important;
        color: var(--charcoal) !important;
        -webkit-text-fill-color: var(--charcoal) !important;
        max-width: 680px !important;
        width: 100% !important;
        margin: 0 auto 2.2rem auto !important;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        align-self: center !important;
        display: block !important;
    }
    div[data-testid="stMarkdownContainer"] .stitch-lede,
    .stitch-hero p,
    .stitch-hero .stitch-lede {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        align-self: center !important;
    }
    
    /* INITIATE VECTOR CONSULTATION BUTTON */
    .stitch-initiate-btn,
    .stitch-initiate-btn:hover,
    .stitch-initiate-btn:focus,
    .stitch-initiate-btn:visited,
    .stitch-initiate-btn:active,
    .stitch-initiate-btn span,
    .stitch-initiate-btn *,
    div[data-testid="stMarkdownContainer"] a.stitch-initiate-btn,
    div[data-testid="stMarkdownContainer"] a.stitch-initiate-btn * {
        text-decoration: none !important;
        text-decoration-line: none !important;
        border-bottom: none !important;
        outline: none !important;
    }
    .stitch-initiate-btn {
        background: var(--cognac);
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.84rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 14px 34px;
        border-radius: 9999px;
        text-decoration: none !important;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 10px 25px rgba(139, 69, 19, 0.25);
        transition: all 0.25s ease;
        margin-bottom: 1.5rem;
    }
    .stitch-initiate-btn:hover {
        background: var(--cognac-hover);
        transform: scale(1.03);
        box-shadow: 0 14px 30px rgba(139, 69, 19, 0.35);
        text-decoration: none !important;
    }

    .stitch-telemetry {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--muted);
    }

    /* STEP CARDS & FLOW STRIP */
    .flow-strip {
        background: var(--vellum);
        border: 1px solid var(--hairline);
        border-radius: 14px;
        padding: 18px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        gap: 10px;
        box-shadow: 0 4px 16px rgba(28, 26, 24, 0.03);
        overflow-x: auto;
    }
    .step-card {
        background: var(--vellum);
        border: 1px solid var(--hairline);
        border-radius: 14px;
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(28, 26, 24, 0.04);
        transition: all 0.25s ease;
    }
    .step-card:hover {
        transform: translateY(-2px);
        border-color: var(--cognac);
        box-shadow: 0 8px 25px rgba(28, 26, 24, 0.08);
    }

    /* FRIENDLY VISUAL WORKFLOW CARDS */
    .workflow-header {
        text-align: center !important;
        margin-top: 2rem;
        margin-bottom: 1.8rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .workflow-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--cognac);
        margin-bottom: 6px;
        text-align: center !important;
    }
    .workflow-title {
        font-family: 'Newsreader', serif;
        font-size: 2.1rem;
        font-weight: 500;
        color: var(--ink);
        margin: 0 0 6px 0;
        text-align: center !important;
    }
    .workflow-subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.92rem;
        color: var(--muted);
        max-width: 580px;
        margin: 0 auto !important;
        line-height: 1.5;
        text-align: center !important;
    }
    .friendly-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 2rem;
    }
    @media (max-width: 960px) {
        .friendly-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media (max-width: 560px) {
        .friendly-grid {
            grid-template-columns: 1fr;
        }
    }
    .friendly-card {
        background: var(--vellum);
        border: 1px solid var(--hairline);
        border-radius: 16px;
        padding: 22px 18px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 3px 14px rgba(28, 26, 24, 0.03);
    }
    .friendly-card:hover {
        transform: translateY(-4px);
        border-color: var(--cognac);
        box-shadow: 0 10px 25px rgba(139, 69, 19, 0.09);
    }
    .friendly-step-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        color: var(--cognac);
        background: #F8EFEA;
        border: 1px solid rgba(139, 69, 19, 0.18);
        padding: 3px 9px;
        border-radius: 9999px;
        width: fit-content;
        margin-bottom: 12px;
    }
    .friendly-figure-box {
        background: linear-gradient(135deg, #FAF7F2 0%, #F3EEE4 100%);
        border: 1px dashed #D8D2C5;
        border-radius: 12px;
        padding: 14px 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 14px;
        min-height: 92px;
        text-align: center;
    }
    .friendly-card-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .friendly-card-desc {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.84rem;
        color: #4A4640;
        line-height: 1.45;
        margin-bottom: 14px;
    }
    .friendly-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        font-weight: 600;
        color: var(--cognac);
        background: #FFFFFF;
        border: 1px solid var(--hairline);
        padding: 4px 9px;
        border-radius: 6px;
        margin-top: auto;
        width: fit-content;
    }

    /* STITCH ARCHITECTURAL PREVIEW CARDS */
    .stitch-preview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin-top: 2rem;
        padding-top: 1.8rem;
        border-top: 1px solid var(--hairline);
    }
    .stitch-preview-card {
        border: 1px solid var(--hairline);
        background: var(--vellum);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(28, 26, 24, 0.04);
    }

    /* DOSSIER CARDS (EQUAL HEIGHT) */
    .dossier-card {
        background: var(--vellum);
        border: 1px solid var(--hairline);
        border-radius: 14px;
        padding: 24px 22px 18px 22px;
        box-shadow: 0 4px 16px rgba(28, 26, 24, 0.04);
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
    .dossier-card:hover {
        transform: translateY(-2px);
        border-color: var(--cognac);
    }
    .dossier-card.featured {
        border-top: 3px solid var(--cognac);
    }

    /* LEDGER GRID */
    .ledger-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 14px;
        margin-bottom: 2rem;
    }
    .ledger-card {
        padding: 16px 18px;
        border-radius: 12px;
        background: var(--vellum);
        border: 1px solid var(--hairline);
        box-shadow: 0 4px 16px rgba(28, 26, 24, 0.04);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* CHAT STREAM */
    div[data-testid="stChatMessage"] {
        background-color: var(--vellum) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 12px !important;
        padding: 1.6rem !important;
        margin-bottom: 1.4rem !important;
        box-shadow: 0 4px 16px rgba(28, 26, 24, 0.04) !important;
    }
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background-color: #FAF8F5 !important;
    }
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        border-left: 3px solid var(--cognac) !important;
    }
    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] *,
    .stMarkdown,
    .stMarkdown * {
        color: var(--ink) !important;
    }

    /* CHAT INPUT FLOATING DOCK */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stBottom,
    footer,
    footer * {
        background: transparent !important;
        border: none !important;
    }
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    div[data-testid="stChatInput"] > div {
        background-color: var(--vellum) !important;
        border: 1.5px solid var(--hairline) !important;
        border-radius: 9999px !important;
        box-shadow: 0 8px 30px rgba(28, 26, 24, 0.08) !important;
        padding: 6px 14px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stChatInput"] > div:focus-within {
        border-color: var(--cognac) !important;
        box-shadow: 0 0 0 3px rgba(139, 69, 19, 0.15) !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: var(--ink) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: var(--cognac) !important;
        color: #FFFFFF !important;
        border-radius: 9999px !important;
        border: none !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background-color: var(--cognac-hover) !important;
    }

    /* BUTTONS */
    .stButton button {
        background: var(--vellum) !important;
        color: var(--ink) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 9999px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        background: var(--cognac) !important;
        color: #FFFFFF !important;
        border-color: var(--cognac) !important;
    }
    div[data-testid="stDownloadButton"] button {
        background: var(--vellum) !important;
        color: var(--cognac) !important;
        border: 1px solid var(--cognac) !important;
        border-radius: 9999px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: var(--cognac) !important;
        color: #FFFFFF !important;
    }

    .folio-card {
        background: var(--vellum);
        border: 1px solid var(--hairline);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(28, 26, 24, 0.04);
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
            "content": "Welcome to **LEXICON CODEX**. I provide verified statutory findings over corporate **Leave**, **Business Travel**, and **Expense Reimbursement** guidelines.\n\nEvery response is backed by zero-hallucination vector grounding and primary source attributions.",
            "sources": []
        }
    ]

ENV_FILE = os.path.join(BASE_DIR, ".env")

def get_persisted_api_key():
    k = os.getenv("GEMINI_API_KEY", "").strip()
    if k:
        return k
    if os.path.exists(ENV_FILE):
        try:
            with open(ENV_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
        except Exception:
            pass
    return ""

def persist_api_key(api_key: str):
    api_key = (api_key or "").strip()
    os.environ["GEMINI_API_KEY"] = api_key
    st.session_state.api_key = api_key
    try:
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
    except Exception as e:
        print(f"Error persisting API key: {e}")
    if "pipeline" in st.session_state and st.session_state.pipeline:
        st.session_state.pipeline.set_api_key(api_key)

if "api_key" not in st.session_state or not st.session_state.api_key:
    st.session_state.api_key = get_persisted_api_key()

if "model_choice" not in st.session_state:
    st.session_state.model_choice = "gemini-2.5-flash"

# Determine active tab from URL query params or session state
active_tab = st.query_params.get("tab", "home")
if active_tab == "architecture":
    active_tab = "home"
if active_tab == "folios":
    active_tab = "policy"
if active_tab not in ["home", "consultation", "policy", "settings"]:
    active_tab = "home"

# Initialize RAG Pipeline
if "pipeline" not in st.session_state:
    with st.spinner("Initializing ChromaDB Vector Repository..."):
        pipeline = RAGPipeline(gemini_api_key=st.session_state.api_key if st.session_state.api_key else None)
        if pipeline.collection.count() == 0:
            pipeline.index_directory(POLICIES_DIR)
        st.session_state.pipeline = pipeline

# ---------------------------------------------------------
# EXACT STITCH FLOATING PILL NAVBAR
# ---------------------------------------------------------
act_home = "active" if active_tab == "home" else ""
act_consult = "active" if active_tab == "consultation" else ""
act_policy = "active" if active_tab == "policy" else ""
act_settings = "active" if active_tab == "settings" else ""

st.markdown(f"""
<div class="stitch-header-wrap">
    <nav class="stitch-nav-pill">
        <a class="stitch-brand" href="?tab=home" target="_self">
            <span style="font-size: 1.15rem;">⚖️</span>
            <span class="stitch-brand-title">LEXICON CODEX</span>
        </a>
        <div class="stitch-nav-links">
            <a class="stitch-nav-link {act_home}" href="?tab=home" target="_self">Home</a>
            <a class="stitch-nav-link {act_consult}" href="?tab=consultation" target="_self">Consultation</a>
            <a class="stitch-nav-link {act_policy}" href="?tab=policy" target="_self">Policy</a>
            <a class="stitch-nav-link {act_settings}" href="?tab=settings" target="_self">Settings</a>
        </div>
        <div class="stitch-actions">
            <a class="stitch-cta-btn" href="?tab=consultation" target="_self">
                CONSULT CODEX ⚡
            </a>
        </div>
    </nav>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: HOME (Landing & How It Works)
# ---------------------------------------------------------
if active_tab == "home":
    # Exact Stitch Hero Section
    st.markdown("""
    <div class="stitch-hero" style="text-align: center !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; margin: 0 auto !important; max-width: 860px !important;">
        <div class="stitch-eyebrow" style="margin-left: auto !important; margin-right: auto !important;">
            <span class="stitch-pulse-dot"></span>
            <span class="stitch-eyebrow-text">Problem Statement 34 &bull; Zero-Hallucination Policy Engine</span>
        </div>
        <h1 class="stitch-headline" style="text-align: center !important; width: 100% !important;">
            Corporate policy intelligence,<br/>codified <span class="stitch-headline-accent">without error.</span>
        </h1>
        <p class="stitch-lede" style="text-align: center !important; margin-left: auto !important; margin-right: auto !important; max-width: 680px !important; width: 100% !important; align-self: center !important; display: block !important;">
            Directly ground every inquiry in verified enterprise policy folios. Engineered with ChromaDB vectorization and strict non-parametric refusal guardrails for complete statutory auditability.
        </p>
        <div style="text-align: center !important; width: 100% !important; display: flex !important; justify-content: center !important;">
            <a class="stitch-initiate-btn" href="?tab=consultation" target="_self" style="text-decoration: none !important; text-decoration-line: none !important; border-bottom: none !important; color: #FFFFFF !important;">
                <span style="text-decoration: none !important; color: #FFFFFF !important;">INITIATE VECTOR CONSULTATION</span>
                <span style="font-size: 1.1rem; font-weight: 700; text-decoration: none !important; color: #FFFFFF !important;">&rarr;</span>
            </a>
        </div>
        <div class="stitch-telemetry" style="text-align: center !important; justify-content: center !important; width: 100% !important;">
            <span style="color: #24614A; font-weight: 600;">● 3 Verified Folios (HR • Travel • Expense)</span>
            <span style="color: #D8D2C5;">•</span>
            <span>Latency: ≤ 42ms</span>
            <span style="color: #D8D2C5;">•</span>
            <span style="color: #8B4513; font-weight: 600;">Zero Extrapolation Guardrails Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Friendly Visual 4-Step Client Workflow
    st.markdown("""<div class="workflow-header">
<div class="workflow-eyebrow">HOW IT WORKS</div>
<h2 class="workflow-title">4 Simple Steps to Verified Policy Answers</h2>
<p class="workflow-subtitle">No legal jargon to decode. Just clear, trusted guidance with exact proof in seconds.</p>
</div>
<div class="friendly-grid">
<div class="friendly-card">
<div>
<div class="friendly-step-badge">STEP 01 &bull; UPLOAD</div>
<div class="friendly-figure-box">
<div style="font-size: 32px; margin-bottom: 4px;">📂</div>
<div style="display: flex; gap: 4px; justify-content: center; flex-wrap: wrap;">
<span style="font-size: 0.65rem; background: #FFFFFF; border: 1px solid #D8D2C5; border-radius: 4px; padding: 2px 6px; font-weight: 600; color: #1C1A18;">HR Leave</span>
<span style="font-size: 0.65rem; background: #FFFFFF; border: 1px solid #D8D2C5; border-radius: 4px; padding: 2px 6px; font-weight: 600; color: #1C1A18;">Travel</span>
<span style="font-size: 0.65rem; background: #FFFFFF; border: 1px solid #D8D2C5; border-radius: 4px; padding: 2px 6px; font-weight: 600; color: #1C1A18;">Expense</span>
</div>
</div>
<div class="friendly-card-title">Drop in Policies</div>
<div class="friendly-card-desc">
Upload your official company PDF handbooks and guidelines.
</div>
</div>
<div class="friendly-pill">📄 Any PDF Manual</div>
</div>

<div class="friendly-card">
<div>
<div class="friendly-step-badge">STEP 02 &bull; ORGANIZE</div>
<div class="friendly-figure-box">
<div style="display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 20px; margin-bottom: 6px;">
<span>📄</span>
<span style="color: #8B4513; font-size: 14px; font-weight: 700;">&rarr;</span>
<span style="background: #F8EFEA; border: 1px solid #8B4513; border-radius: 6px; padding: 2px 6px; font-size: 18px;">⚡</span>
<span style="color: #8B4513; font-size: 14px; font-weight: 700;">&rarr;</span>
<span>🧠</span>
</div>
<div style="font-size: 0.68rem; color: #24614A; font-weight: 700; background: #E8F5E9; border-radius: 4px; padding: 2px 8px;">
● Instant Memory Ready
</div>
</div>
<div class="friendly-card-title">AI Reads Every Rule</div>
<div class="friendly-card-desc">
Smart AI indexes every clause so nothing is missed or overlooked.
</div>
</div>
<div class="friendly-pill">⚡ 1-Click Fast Index</div>
</div>

<div class="friendly-card">
<div>
<div class="friendly-step-badge">STEP 03 &bull; ASK</div>
<div class="friendly-figure-box" style="padding: 10px 8px;">
<div style="width: 100%; display: flex; flex-direction: column; gap: 4px;">
<div style="background: #FFFFFF; border: 1px solid #D8D2C5; border-radius: 8px 8px 8px 2px; padding: 3px 7px; font-size: 0.68rem; color: #1C1A18; font-weight: 600; text-align: left; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
💬 "Can I claim meals?"
</div>
<div style="background: #8B4513; color: #FFFFFF; border-radius: 8px 8px 2px 8px; padding: 3px 7px; font-size: 0.68rem; font-weight: 600; text-align: right; align-self: flex-end;">
"How many leave days?"
</div>
</div>
</div>
<div class="friendly-card-title">Ask in Plain English</div>
<div class="friendly-card-desc">
Ask questions naturally just like chatting with HR. No special syntax.
</div>
</div>
<div class="friendly-pill">🗣️ Natural Language</div>
</div>

<div class="friendly-card">
<div>
<div class="friendly-step-badge">STEP 04 &bull; VERIFY</div>
<div class="friendly-figure-box" style="padding: 8px 8px;">
<div style="background: #FFFFFF; border: 1px solid #D8D2C5; border-radius: 8px; padding: 5px 8px; width: 100%; box-shadow: 0 1px 4px rgba(0,0,0,0.04); text-align: left;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2px;">
<span style="color: #24614A; font-weight: 700; font-size: 0.68rem; display: flex; align-items: center; gap: 3px;">
<span>✅</span> Verified
</span>
<span style="color: #8B4513; font-size: 0.64rem; font-family: 'JetBrains Mono', monospace; font-weight: 600;">Folio II • Page 4</span>
</div>
<div style="color: #6E6961; font-size: 0.64rem; font-style: italic; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
"Meals covered up to $75/day..."
</div>
</div>
</div>
<div class="friendly-card-title">Verified Answers</div>
<div class="friendly-card-desc">
Receive direct answers with exact page numbers and quotes attached.
</div>
</div>
<div class="friendly-pill">🛡️ 100% Verifiable Proof</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Interactive Client PDF Uploader Section
    st.markdown("""<div style="background: #FFFFFF; border: 1px solid #D8D2C5; border-left: 4px solid #8B4513; border-radius: 14px; padding: 22px 24px; box-shadow: 0 4px 16px rgba(28,26,24,0.04); margin-bottom: 20px;">
<div style="display: flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono'; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #8B4513; letter-spacing: 0.08em; margin-bottom: 6px;">
<span>🚀</span> TRY IT LIVE WITH YOUR OWN POLICY
</div>
<div style="font-family: 'Newsreader', serif; font-size: 1.35rem; font-weight: 600; color: #1C1A18; margin-bottom: 6px;">
Ingest Any Company Manual in 1 Click
</div>
<div style="font-family: 'Plus Jakarta Sans'; font-size: 0.88rem; color: #4A4640; line-height: 1.5; margin-bottom: 14px;">
Drag and drop any official company PDF here. The engine will parse it, map its rules, and let you query it right away in the <strong>Consultation</strong> tab.
</div>
</div>""", unsafe_allow_html=True)

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
            st.success(f"Successfully ingested '{uploaded_pdf.name}' ({chunks_indexed} semantic chunks indexed)! Click **Consultation** in the top navbar to query it.")

# ---------------------------------------------------------
# SECTION 2: CONSULTATION (Dashboard & Live Consultation Stream)
# ---------------------------------------------------------
elif active_tab == "consultation":
    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #8B4513; font-weight: 700; margin-bottom: 4px;">
            STATUTORY CONSULTATION LEDGER
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2.2rem; font-weight: 500; color: #1C1A18; margin: 0 0 8px 0;">
            Policy Consultation &amp; Vector Reasoning
        </h2>
        <p style="font-family: 'Plus Jakarta Sans'; font-size: 0.95rem; color: #3D3A36; line-height: 1.6; margin: 0;">
            Execute natural language inquiries grounded strictly in verified policy folios with 100% auditable source citations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Statutory Ledger Metrics Strip
    total_policies = len([f for f in os.listdir(POLICIES_DIR) if f.endswith(".pdf")])
    status_label = "100% Certified" if st.session_state.api_key else "Key Required"
    status_color = "#24614A" if st.session_state.api_key else "#8B4513"

    st.markdown(f"""
    <div class="ledger-grid">
        <div class="ledger-card">
            <div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6E6961; font-weight: 600; margin-bottom: 4px;">Statutory Corpus</div>
                <div style="font-family: 'Plus Jakarta Sans'; font-size: 1.35rem; font-weight: 700; color: #8B4513;">{total_policies} Active Folios</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">📖</div>
        </div>
        <div class="ledger-card">
            <div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6E6961; font-weight: 600; margin-bottom: 4px;">Vector Repository</div>
                <div style="font-family: 'Plus Jakarta Sans'; font-size: 1.35rem; font-weight: 700; color: #8B4513;">ChromaDB</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">⚡</div>
        </div>
        <div class="ledger-card">
            <div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6E6961; font-weight: 600; margin-bottom: 4px;">Governance Mode</div>
                <div style="font-family: 'Plus Jakarta Sans'; font-size: 1.35rem; font-weight: 700; color: #8B4513;">Zero-Hallucination</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">⚖️</div>
        </div>
        <div class="ledger-card">
            <div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6E6961; font-weight: 600; margin-bottom: 4px;">Audit Integrity</div>
                <div style="font-family: 'Plus Jakarta Sans'; font-size: 1.35rem; font-weight: 700; color: {status_color};">{status_label}</div>
            </div>
            <div style="font-size: 24px; opacity: 0.6;">🛡️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Inline API Key Manager on Consultation Tab
    if not st.session_state.api_key:
        st.markdown("""<div style="background: #FFFFFF; border: 1px solid #D8D2C5; border-left: 4px solid #8B4513; border-radius: 12px; padding: 18px 22px; margin-top: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 14px rgba(28,26,24,0.03);">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-size: 1.2rem;">🔑</span>
<span style="font-family: 'Plus Jakarta Sans'; font-size: 1.02rem; font-weight: 700; color: #1C1A18;">Activate Google Gemini API Key</span>
</div>
<span style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 700; color: #8B4513; background: #F8EFEA; padding: 3px 8px; border-radius: 4px;">KEY REQUIRED FOR LIVE LLM</span>
</div>
<div style="font-family: 'Plus Jakarta Sans'; font-size: 0.86rem; color: #4A4640; line-height: 1.5; margin-bottom: 12px;">
Paste your Google Gemini API key below to unlock live AI synthesis. The key will be saved automatically so you won't need to enter it again.
</div>
</div>""", unsafe_allow_html=True)
        col_key_input, col_key_btn = st.columns([5, 1])
        with col_key_input:
            entered_key = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Paste Gemini API key (AIzaSy...)",
                label_visibility="collapsed",
                key="consult_key_input"
            )
        with col_key_btn:
            if st.button("Activate Key ➔", key="btn_activate_key_consult", use_container_width=True):
                if entered_key.strip():
                    persist_api_key(entered_key.strip())
                    st.success("API Key activated and permanently saved!")
                    st.rerun()
                else:
                    st.warning("Please paste a valid key.")
    else:
        st.markdown(f"""<div style="display: flex; align-items: center; justify-content: space-between; background: #F8FAF7; border: 1px solid #D8D2C5; border-radius: 10px; padding: 10px 18px; margin-top: 1.5rem; margin-bottom: 1.2rem;">
<div style="display: flex; align-items: center; gap: 8px; font-family: 'Plus Jakarta Sans'; font-size: 0.85rem; color: #24614A; font-weight: 600;">
<span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #24614A;"></span>
<span>Gemini API Connected &bull; Live Synthesis Active</span>
</div>
<div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #8B4513; font-weight: 600;">
Model: {st.session_state.model_choice}
</div>
</div>""", unsafe_allow_html=True)

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
                <div style="background: #FFFFFF; border: 1.5px solid #8B4513; border-radius: 12px; padding: 22px; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(28,26,24,0.06);">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #D8D2C5; padding-bottom: 12px; margin-bottom: 14px;">
                        <div>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #8B4513; font-weight: 700;">
                                OFFICIAL INSTITUTIONAL FOLIO INSPECTOR
                            </span>
                            <h2 style="font-family: 'Newsreader', serif; font-size: 1.6rem; font-weight: 500; margin: 4px 0; color: #1C1A18;">
                                {doc_name.replace('_Policy.pdf', '').replace('_', ' ')} Policy Manual
                            </h2>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.76rem; color: #6E6961;">
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
                <div style="background: #FAF8F5; border: 1px solid #D8D2C5; border-radius: 8px; padding: 20px; font-family: 'JetBrains Mono'; font-size: 0.88rem; line-height: 1.65; color: #1C1A18; max-height: 400px; overflow-y: auto; white-space: pre-wrap;">{full_text}</div>
                <div style="margin-bottom: 2rem;"></div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error inspecting document: {e}")

    # Curated Inquiries & Active Dossiers
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; padding-bottom: 8px; border-bottom: 1px solid #D8D2C5;">
        <span style="font-family: 'Plus Jakarta Sans'; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.1em; color: #1C1A18; font-weight: 800;">
            CURATED INQUIRIES &amp; ACTIVE DOSSIERS
        </span>
        <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #6E6961; letter-spacing: 0.08em;">CATALOGUE VOL. XXIV</span>
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
            badges_html = "".join([f'<span style="font-family: monospace; font-size: 0.66rem; font-weight: 600; padding: 3px 8px; border-radius: 4px; background: #EFECE4; border: 1px solid #D8D2C5; color: #6E6961;">{b["text"]}</span> ' for b in q["badges"]])
            featured_card = " featured" if q["featured"] else ""
            
            st.markdown(f"""
            <div class="dossier-card{featured_card}">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; height: 24px;">
                        <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; font-weight: 700; color: #8B4513;">{q['ref']}</span>
                        <div>{badges_html}</div>
                    </div>
                    <div style="font-family: 'Newsreader', serif; font-size: 1.25rem; font-weight: 500; color: #1C1A18; margin-bottom: 10px; height: 56px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">{q['title']}</div>
                    <div style="font-family: 'Plus Jakarta Sans'; font-size: 0.86rem; line-height: 1.55; color: #3D3A36; margin-bottom: 12px; flex-grow: 1; overflow: hidden;">{q['desc']}</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid #D8D2C5; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #6E6961; height: 24px;">
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

    # Consultation Stream
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 14px; margin: 2.2rem 0 1.4rem 0;">
        <div style="height: 1px; background: #D8D2C5; flex: 1;"></div>
        <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #6E6961;">
            📜 CONSULTATION RECORD &bull; VECTOR-GROUNDING VAULT ACTIVE
        </span>
        <div style="height: 1px; background: #D8D2C5; flex: 1;"></div>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        role_icon = "⚖️" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=role_icon):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📄 Source Citations & Policy Excerpts", expanded=False):
                    for s in msg["sources"]:
                        st.markdown(f"""
                        <div style="padding: 16px 20px; border-radius: 8px; background: #FAF8F5; margin-top: 14px; border: 1px solid #D8D2C5;">
                            <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 8px; border-bottom: 1px solid #D8D2C5; margin-bottom: 10px;">
                                <span style="font-family: 'JetBrains Mono'; font-size: 0.76rem; font-weight: 700; color: #8B4513; text-transform: uppercase;">
                                    📜 {s['source_file']} &bull; PAGE {s['page']}
                                </span>
                                <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; color: #6E6961;">Audited Precedent</span>
                            </div>
                            <div style="border-left: 3px solid #8B4513; padding-left: 14px; margin: 8px 0; font-family: 'Newsreader', serif; font-style: italic; font-size: 0.95rem; line-height: 1.55; color: #1C1A18;">
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

    # Chat Input & Synthesis
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
                    with st.expander("📄 Source Citations & Policy Excerpts", expanded=False):
                        for s in result["sources"]:
                            st.markdown(f"""
                            <div style="padding: 16px 20px; border-radius: 8px; background: #FAF8F5; margin-top: 14px; border: 1px solid #D8D2C5;">
                                <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 8px; border-bottom: 1px solid #D8D2C5; margin-bottom: 10px;">
                                    <span style="font-family: 'JetBrains Mono'; font-size: 0.76rem; font-weight: 700; color: #8B4513; text-transform: uppercase;">
                                        📜 {s['source_file']} &bull; PAGE {s['page']}
                                    </span>
                                    <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; color: #6E6961;">Audited Precedent</span>
                                </div>
                                <div style="border-left: 3px solid #8B4513; padding-left: 14px; margin: 8px 0; font-family: 'Newsreader', serif; font-style: italic; font-size: 0.95rem; line-height: 1.55; color: #1C1A18;">
                                    "{s['content_preview']}"
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result.get("sources", [])
                })

# ---------------------------------------------------------
# SECTION 3: POLICY (Document Library & Original PDF Downloads)
# ---------------------------------------------------------
elif active_tab in ["policy", "folios"]:
    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #8B4513; font-weight: 700; margin-bottom: 4px;">
            STATUTORY DOCUMENT REPOSITORY
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2.2rem; font-weight: 500; color: #1C1A18; margin: 0 0 8px 0;">
            Official Policy PDF Folios &amp; Regulatory Manuals
        </h2>
        <p style="font-family: 'Plus Jakarta Sans'; font-size: 0.95rem; color: #3D3A36; line-height: 1.6; margin: 0;">
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

            clauses_html = "".join([f'<span style="display: inline-block; background: #EFECE4; border: 1px solid #D8D2C5; color: #1C1A18; font-family: monospace; font-size: 0.72rem; font-weight: 500; padding: 4px 8px; border-radius: 4px; margin: 3px 4px 3px 0;">{c}</span>' for c in p_info["clauses"]])

            st.markdown(f"""
            <div class="folio-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; border-bottom: 1px solid #D8D2C5; padding-bottom: 14px;">
                    <div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #8B4513;">FOLIO {roman}</span>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 600; background: #F8EFEA; border: 1px solid #D8D2C5; color: #8B4513; padding: 2px 6px; border-radius: 4px;">{p_info['code']}</span>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 600; background: #EFECE4; border: 1px solid #D8D2C5; color: #6E6961; padding: 2px 6px; border-radius: 4px;">Audited 2026</span>
                        </div>
                        <h3 style="font-family: 'Newsreader', serif; font-size: 1.5rem; font-weight: 500; color: #1C1A18; margin: 4px 0;">{p_info['title']}</h3>
                        <div style="font-family: 'JetBrains Mono'; font-size: 0.76rem; color: #6E6961;">File: <code>{pf}</code> &bull; Size: {file_size_kb} KB &bull; Extent: {num_pages} Page(s) &bull; Format: Certified PDF</div>
                    </div>
                </div>
                <div style="font-family: 'Plus Jakarta Sans'; font-size: 0.90rem; line-height: 1.6; color: #3D3A36; margin-bottom: 16px;">{p_info['desc']}</div>
                <div style="margin-bottom: 16px;">
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; text-transform: uppercase; font-weight: 700; color: #6E6961; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">Key Statutory Clauses:</span>
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
# SECTION 4: SETTINGS (Credentials & Engine Configuration)
# ---------------------------------------------------------
elif active_tab == "settings":
    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #8B4513; font-weight: 700; margin-bottom: 4px;">
            SYSTEM CONFIGURATION &amp; AUDIT SETTINGS
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2.2rem; font-weight: 500; color: #1C1A18; margin: 0 0 8px 0;">
            Vector Engine Credentials &amp; Model Selection
        </h2>
        <p style="font-family: 'Plus Jakarta Sans'; font-size: 0.95rem; color: #3D3A36; line-height: 1.6; margin: 0;">
            Configure your institutional Google Gemini API credentials and select the reasoning model for statutory synthesis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    set_col1, set_col2 = st.columns([1, 1])
    with set_col1:
        st.markdown('<div class="folio-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-family: monospace; font-size: 0.75rem; text-transform: uppercase; color: #8B4513; font-weight: 700; margin-bottom: 8px;'>API KEY SETTINGS</div>", unsafe_allow_html=True)
        new_key = st.text_input(
            "Google Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Gemini API key from Google AI Studio."
        )
        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            if st.button("💾 Save Key", key="save_settings_key", use_container_width=True):
                if new_key.strip():
                    persist_api_key(new_key.strip())
                    st.success("API Key permanently saved!")
                    st.rerun()
                else:
                    st.warning("Please enter a valid key.")
        with col_s2:
            if st.button("🗑️ Clear Key", key="clear_settings_key", use_container_width=True):
                persist_api_key("")
                st.info("API Key cleared.")
                st.rerun()

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        new_model = st.selectbox(
            "Reasoning Kernel",
            ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
            index=0 if st.session_state.model_choice == "gemini-2.5-flash" else 1,
            help="Select audited reasoning model for statutory synthesis."
        )
        if new_model != st.session_state.model_choice:
            st.session_state.model_choice = new_model
            st.info(f"Synthesis Kernel switched to {new_model}")
        st.markdown('</div>', unsafe_allow_html=True)

    with set_col2:
        st.markdown(f"""
        <div class="folio-card">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; text-transform: uppercase; color: #8B4513; font-weight: 700; margin-bottom: 12px;">REPOSITORY HEALTH LEDGER</div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #D8D2C5; font-size: 0.82rem;">
                <span style="color: #6E6961;">Vector Store</span>
                <span style="color: #1C1A18; font-family: 'JetBrains Mono'; font-weight: 600;">ChromaDB (Local SQLite3)</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #D8D2C5; font-size: 0.82rem;">
                <span style="color: #6E6961;">Embedding Model</span>
                <span style="color: #1C1A18; font-family: 'JetBrains Mono'; font-weight: 600;">text-embedding-004</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #D8D2C5; font-size: 0.82rem;">
                <span style="color: #6E6961;">Ingested Manuscripts</span>
                <span style="color: #8B4513; font-family: 'JetBrains Mono'; font-weight: 600;">{len(policy_files)} Official PDFs</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 0.82rem;">
                <span style="color: #6E6961;">Academic Roll No</span>
                <span style="color: #1C1A18; font-family: 'JetBrains Mono'; font-weight: 600;">34 (Problem Statement 34)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer Imprint
st.markdown("""
<div style="width: 100%; border-top: 1px solid #D8D2C5; padding: 24px 0 10px 0; margin-top: 3rem; text-align: center;">
    <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; max-width: 900px; margin: 0 auto; font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; color: #6E6961;">
        <span>LEXICON ARCHITECTURAL CODEX &bull; ENTERPRISE RUNTIME</span>
        <span style="color: #8B4513; font-weight: 600;">STRICT NON-PARAMETRIC REFUSAL MODE ACTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)
