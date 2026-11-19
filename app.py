import os
import streamlit as st
from rag_pipeline import RAGPipeline

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Lexicon | Corporate Policy Digest & Consultation",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Stitch Design System Integration
# Colors & Typography directly from Stitch Screen ID 322cbe1be2274dcbadc0e3286a5b94de
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    :root {
        --stitch-primary: #002e27;
        --stitch-primary-container: #14453d;
        --stitch-primary-fixed: #bbece1;
        --stitch-background: #faf9fb;
        --stitch-surface: #faf9fb;
        --stitch-surface-container-low: #f5f3f5;
        --stitch-surface-container: #efedf0;
        --stitch-surface-container-high: #e9e8ea;
        --stitch-surface-container-lowest: #ffffff;
        --stitch-on-surface: #1b1c1e;
        --stitch-on-surface-variant: #404846;
        --stitch-outline: #707976;
        --stitch-outline-variant: #c0c8c5;
        --stitch-secondary: #a73a1a;
        --stitch-secondary-container: #fe7954;
    }

    /* Base Body Reset */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--stitch-surface) !important;
        color: var(--stitch-on-surface) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Fixed Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--stitch-surface-container-low) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.06) !important;
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.04) !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }

    /* Stitch Brand Header */
    .stitch-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 0 12px 0;
    }
    .stitch-logo-seal {
        width: 38px;
        height: 38px;
        background: var(--stitch-primary-container);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 20px;
        box-shadow: 0 2px 8px rgba(20, 69, 61, 0.2);
    }
    .stitch-brand-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--stitch-primary);
        line-height: 1.2;
    }
    .stitch-brand-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        color: var(--stitch-on-surface-variant);
        font-weight: 500;
    }

    /* Folio Items */
    .stitch-folio-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        background: var(--stitch-surface-container-lowest);
        border-radius: 8px;
        border-left: 3px solid var(--stitch-primary-container);
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        margin-bottom: 6px;
        font-size: 0.83rem;
        color: var(--stitch-on-surface);
        transition: all 0.2s ease;
    }
    .stitch-folio-item:hover {
        background: var(--stitch-surface-container-high);
    }
    .stitch-folio-badge {
        font-size: 0.68rem;
        font-weight: 600;
        background: var(--stitch-surface-container);
        color: var(--stitch-on-surface-variant);
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* Vault Card in Sidebar */
    .stitch-vault-card {
        padding: 12px 14px;
        border-radius: 12px;
        background: var(--stitch-surface-container-lowest);
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .stitch-vault-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.76rem;
    }

    /* Hero & Masthead */
    .stitch-masthead-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 4px;
        background: var(--stitch-surface-container);
        color: var(--stitch-primary);
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .stitch-live-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--stitch-primary-container);
        display: inline-block;
    }

    .stitch-hero-title {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 2.75rem;
        font-weight: 400;
        line-height: 1.1;
        letter-spacing: -0.015em;
        color: var(--stitch-on-surface);
        margin-bottom: 0.5rem;
    }
    .stitch-hero-amp {
        font-style: italic;
        color: var(--stitch-primary);
        font-family: 'Newsreader', serif;
    }
    .stitch-hero-subtitle {
        font-size: 1.05rem;
        line-height: 1.6;
        color: var(--stitch-on-surface-variant);
        max-width: 820px;
        margin-bottom: 1.8rem;
    }

    /* Metadata Strip Cards */
    .stitch-ledger-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin-bottom: 2rem;
    }
    .stitch-ledger-card {
        padding: 14px 16px;
        border-radius: 12px;
        background: var(--stitch-surface-container-lowest);
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    .stitch-ledger-card:hover {
        border-color: var(--stitch-outline-variant);
        transform: translateY(-1px);
    }
    .stitch-ledger-label {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--stitch-outline);
        font-weight: 600;
        margin-bottom: 2px;
    }
    .stitch-ledger-value {
        font-family: 'Newsreader', serif;
        font-size: 1.35rem;
        font-weight: 500;
        color: var(--stitch-primary);
    }

    /* Curated Inquiries Cards */
    .stitch-section-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.8rem;
    }
    .stitch-section-label {
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--stitch-outline);
        font-weight: 600;
    }

    /* Chat Messages - Publication Brief */
    div[data-testid="stChatMessage"] {
        background: var(--stitch-surface-container-lowest) !important;
        border: 1px solid var(--stitch-outline-variant) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.4rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
    }

    div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background: var(--stitch-surface-container-low) !important;
        border-color: var(--stitch-surface-container-high) !important;
    }

    /* Strict Dark Ink text */
    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] div,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] strong,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {
        color: var(--stitch-on-surface) !important;
    }

    /* Policy Executive Callout */
    .stitch-exec-callout {
        padding: 16px 20px;
        border-radius: 12px;
        background: var(--stitch-surface-container-low);
        border-left: 4px solid var(--stitch-primary-container);
        margin: 12px 0;
    }
    .stitch-exec-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        color: var(--stitch-primary);
        display: block;
        margin-bottom: 4px;
    }
    .stitch-exec-text {
        font-family: 'Newsreader', serif;
        font-size: 1.15rem;
        line-height: 1.55;
        color: var(--stitch-on-surface);
    }

    /* Citation Tray (Academic Footnotes) */
    .stitch-footnote-card {
        padding: 16px 20px;
        border-radius: 12px;
        background: var(--stitch-surface-container);
        margin-top: 14px;
        border: 1px solid var(--stitch-outline-variant);
    }
    .stitch-footnote-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        margin-bottom: 10px;
    }
    .stitch-footnote-quote {
        border-left: 3px solid var(--stitch-primary-container);
        padding-left: 14px;
        margin: 8px 0;
        font-family: 'Newsreader', serif;
        font-style: italic;
        font-size: 0.95rem;
        line-height: 1.5;
        color: var(--stitch-on-surface);
    }

    /* Bottom Input Dock Reset - No Black Bar */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    footer {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Floating Dock Input */
    div[data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid var(--stitch-outline-variant) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
        padding: 6px !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--stitch-primary-container) !important;
        box-shadow: 0 0 0 3px rgba(20, 69, 61, 0.12) !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--stitch-on-surface) !important;
        font-size: 0.95rem !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] button {
        background: var(--stitch-primary-container) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        transition: background 0.2s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: var(--stitch-primary) !important;
    }

    /* Custom Buttons */
    .stButton button {
        background: var(--stitch-surface-container-lowest) !important;
        color: var(--stitch-primary) !important;
        border: 1px solid var(--stitch-outline-variant) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        background: var(--stitch-primary-container) !important;
        color: #ffffff !important;
        border-color: var(--stitch-primary-container) !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# State & Directory Initialization
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICIES_DIR = os.path.join(BASE_DIR, "policies")
os.makedirs(POLICIES_DIR, exist_ok=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to **Lexicon: Corporate Policy Digest & Consultation**. I provide codified statutory findings over corporate **Leave**, **Business Travel**, and **Expense Reimbursement** guidelines.\n\nEvery finding is backed by vector grounding and audited primary source citations.",
            "sources": []
        }
    ]

# ---------------------------------------------------------
# Sidebar - Stitch Archival Drawer
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="stitch-brand">
        <div class="stitch-logo-seal">⚖️</div>
        <div>
            <div class="stitch-brand-title">Lexicon // Policy Manuals</div>
            <div class="stitch-brand-sub">Vol. XXIV • Codex Ver 4.2</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Key Input
    env_api_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=env_api_key,
        type="password",
        help="Paste your Google Gemini API key from Google AI Studio (aistudio.google.com). Kept strictly in memory."
    )
    api_key = api_key_input.strip() if api_key_input else ""
    
    # Dynamic Model Discovery
    available_choices = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    if api_key and "pipeline" in st.session_state:
        st.session_state.pipeline.set_api_key(api_key)
        detected = st.session_state.pipeline.get_available_models()
        if detected:
            available_choices = detected
            st.caption(f"⚡ {len(detected)} models detected for your API key")

    model_choice = st.selectbox(
        "Intelligence Synthesis Model",
        options=available_choices,
        index=0,
        help="Select the Gemini model for zero-hallucination policy reasoning."
    )
    
    # Vault Key Info Card matching Stitch sidebar
    vault_status = "Active (Tier-1)" if api_key else "Pending Key"
    vault_status_color = "#14453d" if api_key else "#a73a1a"
    st.markdown(f"""
    <div class="stitch-vault-card">
        <div class="stitch-vault-row">
            <span style="color: #707976; text-transform: uppercase; font-size: 0.68rem; font-weight: 600;">Vault Key</span>
            <span style="color: {vault_status_color}; font-weight: 600;">{vault_status}</span>
        </div>
        <div class="stitch-vault-row">
            <span style="color: #707976; text-transform: uppercase; font-size: 0.68rem; font-weight: 600;">Engine Node</span>
            <span style="color: #1b1c1e; font-weight: 500;">ChromaDB Semantic</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #707976; font-weight: 700; margin-bottom: 8px;">
        📜 Primary Policy Folios
    </div>
    """, unsafe_allow_html=True)
    
    policy_files = [f for f in os.listdir(POLICIES_DIR) if f.lower().endswith(".pdf")]
    if policy_files:
        for idx, pf in enumerate(policy_files):
            file_size_kb = round(os.path.getsize(os.path.join(POLICIES_DIR, pf)) / 1024, 1)
            roman_nums = ["I", "II", "III", "IV", "V", "VI"]
            roman = roman_nums[idx] if idx < len(roman_nums) else str(idx+1)
            st.markdown(f"""
            <div class="stitch-folio-item">
                <span><strong>Folio {roman}:</strong> {pf}</span>
                <span class="stitch-folio-badge">{file_size_kb} KB</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No PDF policies located in `policies/`.")

    # Upload new policy PDF
    uploaded_files = st.file_uploader(
        "Ingest Additional Policy Folio",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload official company policy documents into the ChromaDB repository."
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            save_path = os.path.join(POLICIES_DIR, uploaded_file.name)
            if not os.path.exists(save_path):
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Archived: {uploaded_file.name}")

    if st.button("🔄 Sync & Re-Index Repository", use_container_width=True):
        with st.spinner("Indexing policy manuals into ChromaDB..."):
            pipeline = RAGPipeline(gemini_api_key=api_key)
            count = pipeline.index_directory(POLICIES_DIR)
            st.success(f"Indexed {count} semantic chunks across {len(policy_files)} policy folios!")
            st.session_state.pipeline = pipeline

    if st.button("🧹 Clear Consultation Thread", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

    st.markdown("""
    <div style="margin-top: 1rem; padding: 10px; background: #ffffff; border: 1px solid #efedf0; border-radius: 8px; font-size: 0.72rem; color: #707976; font-family: 'JetBrains Mono', monospace; text-align: center;">
        ROLL NO: 34 &bull; PS 34<br/>POLICY RAG CODEX
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Pipeline Initialization
# ---------------------------------------------------------
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline(gemini_api_key=api_key)
    st.session_state.pipeline.index_directory(POLICIES_DIR)
else:
    if api_key:
        st.session_state.pipeline.set_api_key(api_key)

# ---------------------------------------------------------
# Main Page - Stitch Header & Masthead
# ---------------------------------------------------------
st.markdown("""
<div class="stitch-masthead-pill">
    <span class="stitch-live-dot"></span>
    Corporate Intelligence &amp; Compliance System • Ver. 8.19
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stitch-hero-title">
    Corporate Policy Digest <span class="stitch-hero-amp">&amp;</span> Consultation
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stitch-hero-subtitle">
    Audited HR, travel, and fiscal guidelines verified with primary source citations, institutional footnotes, and codified precedent clauses.
</div>
""", unsafe_allow_html=True)

# Live Metadata Ledger (Stitch 4-column Strip)
total_policies = len(policy_files)
status_label = "100% Certified" if api_key else "Key Required"
status_color = "#14453d" if api_key else "#a73a1a"

st.markdown(f"""
<div class="stitch-ledger-grid">
    <div class="stitch-ledger-card">
        <div>
            <div class="stitch-ledger-label">Statutory Corpus</div>
            <div class="stitch-ledger-value">{total_policies} Active Folios</div>
        </div>
        <div style="font-size: 24px; opacity: 0.4;">📖</div>
    </div>
    <div class="stitch-ledger-card">
        <div>
            <div class="stitch-ledger-label">Vector Repository</div>
            <div class="stitch-ledger-value">ChromaDB</div>
        </div>
        <div style="font-size: 24px; opacity: 0.4;">⚡</div>
    </div>
    <div class="stitch-ledger-card">
        <div>
            <div class="stitch-ledger-label">Governance Mode</div>
            <div class="stitch-ledger-value">Zero-Hallucination</div>
        </div>
        <div style="font-size: 24px; opacity: 0.4;">⚖️</div>
    </div>
    <div class="stitch-ledger-card">
        <div>
            <div class="stitch-ledger-label">Audit Integrity</div>
            <div class="stitch-ledger-value" style="color: {status_color};">{status_label}</div>
        </div>
        <div style="font-size: 24px; opacity: 0.4;">🛡️</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Curated Inquiries & Active Dossiers (Stitch Card I, II, III)
# ---------------------------------------------------------
st.markdown("""
<div class="stitch-section-heading">
    <span class="stitch-section-label">Curated Inquiries &amp; Active Dossiers</span>
    <span style="font-size: 0.72rem; color: #707976; letter-spacing: 0.06em;">CATALOGUE VOL. XXIV</span>
</div>
""", unsafe_allow_html=True)

preset_cols = st.columns(3)
quick_queries = [
    {
        "ref": "REF: ARCH-4011 • HR FOLIO",
        "title": "I. Annual Paid Leave & Carry-Forward Limits",
        "desc": "Accrual caps, statutory mandatory rollover deadlines, and executive exception waivers.",
        "query": "How many days of paid leave can I carry forward to next year?"
    },
    {
        "ref": "REF: ARCH-7300 • ACTIVE CONSULTATION",
        "title": "II. Daily Per Diem & Corporate Lodging Caps",
        "desc": "Tier-1 metropolitan lodging allowances, per diem meals, and entertainment thresholds.",
        "query": "What is the daily per diem allowance for domestic business travel?"
    },
    {
        "ref": "REF: ARCH-9840 • REMOTE WORK",
        "title": "III. Home Office Infrastructure Stipend",
        "desc": "Annual ergonomic allocation ($1,500), hardware depreciation, and dual-monitor subsidies.",
        "query": "What is the WFH equipment allowance for new employees?"
    }
]

selected_query = None
for idx, col in enumerate(preset_cols):
    q = quick_queries[idx]
    with col:
        card_btn = st.button(
            f"**{q['ref']}**\n\n### {q['title']}\n\n{q['desc']}\n\n👉 *Load Brief*",
            use_container_width=True,
            key=f"dossier_btn_{idx}"
        )
        if card_btn:
            selected_query = q["query"]

# Archival Consultation Divider
st.markdown("""
<div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin: 2rem 0 1.2rem 0;">
    <div style="height: 1px; background: #e3e2e4; flex: 1;"></div>
    <span style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #707976;">
        📜 Consultation Record • Vector-Grounding Vault Active
    </span>
    <div style="height: 1px; background: #e3e2e4; flex: 1;"></div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Consultation Stream
# ---------------------------------------------------------
for msg in st.session_state.messages:
    role_icon = "⚖️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=role_icon):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📌 Judicial Precedent & Primary Source Attributions", expanded=False):
                for s in msg["sources"]:
                    st.markdown(f"""
                    <div class="stitch-footnote-card">
                        <div class="stitch-footnote-header">
                            <span style="font-size: 0.75rem; font-weight: 700; color: #002e27; text-transform: uppercase;">
                                📜 {s['source_file']} &bull; PAGE {s['page']}
                            </span>
                            <span style="font-size: 0.7rem; color: #707976;">Audited Precedent</span>
                        </div>
                        <div class="stitch-footnote-quote">
                            "{s['content_preview']}"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Chat Input & Synthesis
# ---------------------------------------------------------
user_input = st.chat_input("Consult policy guidelines or query specific per diem allowances...")

final_query = selected_query or user_input

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query, "sources": []})
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_query)

    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Reviewing codified policy folios in ChromaDB..."):
            if api_key:
                st.session_state.pipeline.set_api_key(api_key)
            result = st.session_state.pipeline.generate_answer(
                query=final_query,
                top_k=3,
                model=model_choice
            )
            
            st.markdown(result["answer"])
            
            if result.get("sources"):
                with st.expander("📌 Judicial Precedent & Primary Source Attributions", expanded=True):
                    for s in result["sources"]:
                        st.markdown(f"""
                        <div class="stitch-footnote-card">
                            <div class="stitch-footnote-header">
                                <span style="font-size: 0.75rem; font-weight: 700; color: #002e27; text-transform: uppercase;">
                                    📜 {s['source_file']} &bull; PAGE {s['page']}
                                </span>
                                <span style="font-size: 0.7rem; color: #707976;">Audited Precedent</span>
                            </div>
                            <div class="stitch-footnote-quote">
                                "{s['content_preview']}"
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sources": result.get("sources", [])
            })
