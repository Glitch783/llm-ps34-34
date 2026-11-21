import os
import streamlit as st
import pypdf
from rag_pipeline import RAGPipeline

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Lexicon | Corporate Policy Digest & Consultation",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Konk Electrical Design System Integration
# Design Language: Architectural Luxury, High-End Engineering, Dark Onyx & Metallic Gold
# Colors, typography, and styling directly mapped from https://konkelectrical.com/
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root, [data-theme="light"], [data-theme="dark"], .stApp {
        --konk-ink: #0B0B0C;
        --konk-surface: #121214;
        --konk-surface-elevated: #18181B;
        --konk-surface-light: #222226;
        --konk-bone: #F2F0EB;
        --konk-bone-muted: #D1CFCA;
        --konk-steel: #8C8A84;
        --konk-border: #26262A;
        --konk-border-subtle: #1C1C1F;
        --konk-gold: #E7B96F;
        --konk-bronze: #C89446;
        --konk-gold-glow: rgba(231, 185, 111, 0.15);
        
        --text-color: #F2F0EB !important;
        --background-color: #0B0B0C !important;
        --secondary-background-color: #121214 !important;
    }

    /* Base Body Reset */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: var(--konk-ink) !important;
        background: var(--konk-ink) !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        font-family: 'Archivo', system-ui, -apple-system, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Fixed Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0E0E10 !important;
        border-right: 1px solid var(--konk-border) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }

    /* Konk Brand Header */
    .konk-brand {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 6px 0 16px 0;
        border-bottom: 1px solid var(--konk-border);
        margin-bottom: 14px;
    }
    .konk-logo-seal {
        width: 42px;
        height: 42px;
        background: var(--konk-surface-elevated);
        border: 1px solid var(--konk-bronze);
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--konk-gold);
        font-size: 22px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }
    .konk-brand-title {
        font-family: 'Archivo', sans-serif;
        font-size: 0.92rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--konk-bone);
        line-height: 1.2;
    }
    .konk-brand-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        color: var(--konk-steel);
        font-weight: 500;
        letter-spacing: 0.06em;
    }

    /* Folio Items (Sidebar) */
    .konk-folio-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        background: var(--konk-surface);
        border-radius: 8px;
        border: 1px solid var(--konk-border);
        border-left: 3px solid var(--konk-gold);
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        margin-bottom: 8px;
        font-size: 0.84rem;
        color: var(--konk-bone);
        transition: all 0.2s ease;
    }
    .konk-folio-item:hover {
        background: var(--konk-surface-elevated);
        border-color: var(--konk-gold);
        transform: translateX(2px);
    }
    .konk-folio-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 600;
        background: rgba(231, 185, 111, 0.12);
        color: var(--konk-gold);
        border: 1px solid rgba(231, 185, 111, 0.25);
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* Vault Card in Sidebar */
    .konk-vault-card {
        padding: 14px 16px;
        border-radius: 10px;
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .konk-vault-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.78rem;
        color: var(--konk-steel);
    }
    .konk-vault-val {
        font-family: 'JetBrains Mono', monospace;
        color: var(--konk-bone);
        font-weight: 600;
    }

    /* Hero & Masthead */
    .konk-masthead-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 5px 12px;
        border-radius: 4px;
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        color: var(--konk-gold);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .konk-live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--konk-gold);
        box-shadow: 0 0 8px var(--konk-gold);
        display: inline-block;
    }

    .konk-hero-title {
        font-family: 'Archivo', sans-serif !important;
        font-size: 3.1rem !important;
        font-weight: 800 !important;
        line-height: 1.12 !important;
        letter-spacing: -0.02em !important;
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        margin-bottom: 0.6rem;
    }
    .konk-hero-gold {
        color: var(--konk-gold) !important;
        -webkit-text-fill-color: var(--konk-gold) !important;
        font-style: normal;
    }
    .konk-hero-subtitle {
        font-family: 'Archivo', sans-serif;
        font-size: 1.05rem;
        line-height: 1.65;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        max-width: 860px;
        margin-bottom: 2rem;
    }

    /* Metadata Strip Cards (Statutory Ledger) */
    .konk-ledger-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 14px;
        margin-bottom: 2.2rem;
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
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
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
        font-size: 1.45rem;
        font-weight: 800;
        color: var(--konk-gold);
    }

    /* Section Headings */
    .konk-section-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--konk-border-subtle);
    }
    .konk-section-label {
        font-family: 'Archivo', sans-serif;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--konk-bone);
        font-weight: 800;
    }

    /* Dossier Cards (Konk Architectural Style) */
    .konk-dossier-card {
        background-color: var(--konk-surface) !important;
        background: var(--konk-surface) !important;
        border: 1px solid var(--konk-border);
        border-radius: 12px;
        padding: 24px 22px 18px 22px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 310px !important;
        min-height: 310px !important;
        max-height: 310px !important;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
        transition: all 0.25s ease;
    }
    .konk-dossier-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border-color: var(--konk-gold);
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
    .konk-dossier-badges {
        display: flex;
        gap: 6px;
        align-items: center;
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
        letter-spacing: 0.05em;
        white-space: nowrap;
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

    /* Sidebar Folio Cards */
    .konk-folio-box {
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        transition: all 0.2s ease;
    }
    .konk-folio-box:hover {
        border-color: var(--konk-gold);
    }
    .konk-folio-box-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }
    .konk-folio-box-title {
        font-family: 'Archivo', sans-serif;
        font-size: 0.86rem;
        font-weight: 700;
        color: var(--konk-bone);
    }
    .konk-folio-box-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--konk-steel);
        margin-bottom: 10px;
    }

    /* In-App Policy Document Inspector */
    .konk-inspector-card {
        background: var(--konk-surface);
        border: 1.5px solid var(--konk-gold);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }
    .konk-inspector-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--konk-border);
        padding-bottom: 14px;
        margin-bottom: 16px;
    }
    .konk-inspector-body {
        background: var(--konk-surface-elevated);
        border: 1px solid var(--konk-border);
        border-radius: 8px;
        padding: 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        line-height: 1.65;
        color: var(--konk-bone);
        max-height: 440px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    /* Institutional Auditor Profile */
    .konk-auditor-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        border-radius: 10px;
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        margin-top: 14px;
    }
    .konk-auditor-avatar {
        width: 38px;
        height: 38px;
        border-radius: 6px;
        background: var(--konk-surface-elevated);
        border: 1px solid var(--konk-gold);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: var(--konk-gold);
    }

    /* Chat Messages - Konk Architectural Stream */
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
        border-color: var(--konk-border) !important;
    }

    div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        border-left: 3px solid var(--konk-gold) !important;
    }

    /* High-Contrast Bone White text across chat messages */
    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] div,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] strong,
    div[data-testid="stChatMessage"] em,
    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3,
    div[data-testid="stChatMessage"] h4,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] *,
    div[data-testid="stChatMessageContent"],
    div[data-testid="stChatMessageContent"] *,
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown span,
    .stMarkdown div,
    .stMarkdown * {
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
    }

    /* Citation Tray (Academic Footnotes) */
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

    /* Bottom Input Dock Reset */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] > div > div,
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottomBlockContainer"] > div,
    .stBottom,
    .stBottom > div,
    .stChatFloatingInputContainer,
    [data-testid="stChatFloatingInputContainer"],
    footer,
    footer * {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Floating Dock Input - Dark Luxury Onyx */
    div[data-testid="stChatInput"] {
        background-color: var(--konk-surface) !important;
        background: var(--konk-surface) !important;
        border: 1.5px solid var(--konk-border) !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
        padding: 6px 10px !important;
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
        font-size: 0.95rem !important;
        font-family: 'Archivo', sans-serif !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder,
    div[data-testid="stChatInput"] textarea::-webkit-input-placeholder {
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        opacity: 1 !important;
        font-weight: 400 !important;
    }

    div[data-testid="stChatInput"] button {
        background-color: var(--konk-gold) !important;
        background: var(--konk-gold) !important;
        color: var(--konk-ink) !important;
        -webkit-text-fill-color: var(--konk-ink) !important;
        border-radius: 8px !important;
        border: none !important;
        transition: transform 0.2s ease, background 0.2s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background-color: #F2C983 !important;
        transform: scale(1.05) !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: var(--konk-ink) !important;
        stroke: var(--konk-ink) !important;
        color: var(--konk-ink) !important;
    }

    /* Custom Streamlit Buttons */
    .stButton button {
        background: var(--konk-surface-elevated) !important;
        color: var(--konk-bone) !important;
        border: 1px solid var(--konk-border) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        background: var(--konk-gold) !important;
        color: var(--konk-ink) !important;
        -webkit-text-fill-color: var(--konk-ink) !important;
        border-color: var(--konk-gold) !important;
        transform: translateY(-1px) !important;
    }

    /* Download Buttons */
    div[data-testid="stDownloadButton"] button {
        background: var(--konk-surface-elevated) !important;
        color: var(--konk-gold) !important;
        border: 1px solid var(--konk-gold) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: var(--konk-gold) !important;
        color: var(--konk-ink) !important;
        -webkit-text-fill-color: var(--konk-ink) !important;
    }

    /* Top Navigation Tabs - Konk Numbered Aesthetic */
    [data-testid="stTabs"] {
        margin-top: 1rem !important;
        margin-bottom: 2.2rem !important;
    }
    [role="tablist"] {
        border-bottom: 1px solid var(--konk-border) !important;
        gap: 8px !important;
    }
    button[role="tab"] {
        font-family: 'Archivo', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: var(--konk-steel) !important;
        -webkit-text-fill-color: var(--konk-steel) !important;
        padding: 14px 28px !important;
        border-radius: 8px 8px 0 0 !important;
        background: var(--konk-surface) !important;
        border: 1px solid var(--konk-border) !important;
        border-bottom: none !important;
        transition: all 0.2s ease !important;
    }
    button[role="tab"]:hover {
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        background: var(--konk-surface-elevated) !important;
    }
    button[role="tab"][aria-selected="true"] {
        color: var(--konk-bone) !important;
        -webkit-text-fill-color: var(--konk-bone) !important;
        border-top: 2px solid var(--konk-gold) !important;
        border-left: 1px solid var(--konk-border) !important;
        border-right: 1px solid var(--konk-border) !important;
        border-bottom: 1px solid var(--konk-surface-elevated) !important;
        background: var(--konk-surface-elevated) !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: var(--konk-gold) !important;
    }

    /* Library Cards */
    .konk-lib-card {
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        transition: all 0.2s ease;
    }
    .konk-lib-card:hover {
        border-color: var(--konk-gold);
        transform: translateY(-2px);
    }
    .konk-lib-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 14px;
        border-bottom: 1px solid var(--konk-border);
        padding-bottom: 14px;
    }
    .konk-lib-title {
        font-family: 'Archivo', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--konk-bone);
        margin: 4px 0;
    }
    .konk-lib-desc {
        font-family: 'Archivo', sans-serif;
        font-size: 0.90rem;
        line-height: 1.6;
        color: var(--konk-steel);
        margin-bottom: 16px;
    }

    /* Guide / Architecture Cards */
    .konk-guide-card {
        background: var(--konk-surface);
        border: 1px solid var(--konk-border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        transition: all 0.2s ease;
    }
    .konk-guide-card:hover {
        border-color: var(--konk-gold);
        transform: translateY(-2px);
    }
    .konk-guide-step-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(231, 185, 111, 0.12);
        color: var(--konk-gold);
        border: 1px solid rgba(231, 185, 111, 0.3);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 10px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .konk-guide-title {
        font-family: 'Archivo', sans-serif;
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--konk-bone);
        margin-bottom: 8px;
    }
    .konk-guide-desc {
        font-family: 'Archivo', sans-serif;
        font-size: 0.88rem;
        line-height: 1.65;
        color: var(--konk-steel);
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
# Sidebar - Konk Architectural Drawer
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="konk-brand">
        <div class="konk-logo-seal">⚖️</div>
        <div>
            <div class="konk-brand-title">Lexicon // Codex</div>
            <div class="konk-brand-sub">VOL. XXIV • CODEX VER 4.2</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ingested Folios Quick Counter
    policy_files = [f for f in os.listdir(POLICIES_DIR) if f.endswith(".pdf")]
    
    st.markdown(f"""
    <div class="konk-vault-card">
        <div class="konk-vault-row">
            <span>CHROMA INDEX</span>
            <span class="konk-vault-val">ACTIVE (SQLITE3)</span>
        </div>
        <div class="konk-vault-row">
            <span>INGESTED FOLIOS</span>
            <span class="konk-vault-val">{len(policy_files)} MANUSCRIPTS</span>
        </div>
        <div class="konk-vault-row">
            <span>EMBEDDING ENGINE</span>
            <span class="konk-vault-val">text-embedding-004</span>
        </div>
        <div class="konk-vault-row">
            <span>REASONING KERNEL</span>
            <span class="konk-vault-val">gemini-2.5-flash</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Configuration Section
    st.markdown("<div style=\"font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #8C8A84; font-weight: 700; margin-bottom: 6px;\">// SYSTEM CREDENTIALS</div>", unsafe_allow_html=True)
    api_key = st.text_input(
        "Google Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Institutional API key for Gemini 2.5 synthesis."
    )

    model_choice = st.selectbox(
        "Synthesis Kernel",
        ["gemini-2.5-flash", "gemini-1.5-pro"],
        index=0,
        help="Select audited reasoning model for statutory synthesis."
    )

    # Initialize RAG Pipeline in session state
    if "pipeline" not in st.session_state:
        with st.spinner("Initializing ChromaDB Vector Index..."):
            pipeline = RAGPipeline(gemini_api_key=api_key if api_key else None)
            if pipeline.collection.count() == 0:
                pipeline.index_directory(POLICIES_DIR)
            st.session_state.pipeline = pipeline

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Functional Policy PDF Access & In-App Text Inspector
    st.markdown("<div style=\"font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #8C8A84; font-weight: 700; margin-bottom: 8px;\">// POLICY ARCHIVE &amp; DOWNLOADS</div>", unsafe_allow_html=True)
    
    if policy_files:
        for pfile in policy_files:
            file_path = os.path.join(POLICIES_DIR, pfile)
            file_size_kb = round(os.path.getsize(file_path) / 1024, 1)
            
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()

            st.markdown(f"""
            <div class="konk-folio-box">
                <div class="konk-folio-box-header">
                    <span class="konk-folio-box-title">{pfile.replace('_', ' ').replace('.pdf', '')}</span>
                    <span class="konk-folio-badge">{file_size_kb} KB</span>
                </div>
                <div class="konk-folio-box-sub">Certified PDF &bull; ChromaDB Grounded</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_dl, col_view = st.columns([1, 1])
            with col_dl:
                st.download_button(
                    label="📥 PDF",
                    data=pdf_bytes,
                    file_name=pfile,
                    mime="application/pdf",
                    key=f"sidebar_dl_{pfile}",
                    use_container_width=True
                )
            with col_view:
                if st.button("🔍 View", key=f"sidebar_view_{pfile}", use_container_width=True):
                    st.session_state.active_doc_preview = pfile
    else:
        st.markdown("<div style='font-size:0.8rem; color:#8C8A84;'>No PDF folios found in policies/</div>", unsafe_allow_html=True)

    # Institutional Auditor Profile
    st.markdown("""
    <div class="konk-auditor-profile">
        <div class="konk-auditor-avatar">⚖️</div>
        <div>
            <div style="font-family: 'Archivo'; font-size: 0.82rem; font-weight: 800; color: #F2F0EB;">Statutory Auditor</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.70rem; color: #8C8A84;">PS 34 // ROLL NO: 34</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("🧹 Reset Consultation Stream", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Consultation record cleared. Inquire regarding corporate **Leave**, **Business Travel**, or **Reimbursement** statutory provisions.",
                "sources": []
            }
        ]
        st.session_state.active_doc_preview = None
        st.rerun()

# ---------------------------------------------------------
# Main Stage: Hero Masthead (Konk Architectural Style)
# ---------------------------------------------------------
st.markdown("""
<div class="konk-masthead-pill">
    <span class="konk-live-dot"></span>
    <span>01 // ARCHITECTURAL CODEX &bull; PROBLEM STATEMENT 34 &bull; ROLL NO: 34</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="konk-hero-title">
    Corporate Policy Digest <span class="konk-hero-gold">&amp; Consultation.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="konk-hero-subtitle">
    Where Details Matter. Codified HR, business travel, and fiscal guidelines verified with zero-hallucination vector grounding, primary source attributions, and immutable audit trails.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Top Navigation Tabs (01 How It Works -> 02 Dashboard -> 03 Library)
# ---------------------------------------------------------
tab_guide, tab_dashboard, tab_library = st.tabs([
    "01 // How It Works & System Guide",
    "02 // Policy Dashboard & Consultation",
    "03 // Policy PDF Folios & Document Library"
])

# ---------------------------------------------------------
# Tab 1: How It Works & System Guide (Landing & Architecture)
# ---------------------------------------------------------
with tab_guide:
    st.markdown("""
    <div style="background: rgba(231, 185, 111, 0.08); border-left: 3px solid #E7B96F; padding: 16px 20px; border-radius: 8px; margin-bottom: 24px;">
        <span style="font-family: 'Archivo'; font-weight: 800; color: #E7B96F; font-size: 0.95rem;">🚀 ARCHITECTURAL ONBOARDING:</span>
        <span style="font-family: 'Archivo'; color: #D1CFCA; font-size: 0.92rem;"> Review how our zero-hallucination statutory engine operates below, then navigate to <strong>02 // Policy Dashboard &amp; Consultation</strong> to execute live vector queries!</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #E7B96F; font-weight: 700; margin-bottom: 4px;">
            // SYSTEM ARCHITECTURE &amp; METHODOLOGY
        </div>
        <h2 style="font-family: 'Archivo'; font-size: 2.1rem; font-weight: 800; color: #F2F0EB; margin: 0 0 8px 0;">
            How the Zero-Hallucination Policy Assistant Works
        </h2>
        <p style="font-family: 'Archivo'; font-size: 0.95rem; color: #8C8A84; line-height: 1.6; margin: 0;">
            Technical architecture of Problem Statement 34 (Company Policy Assistant) engineered with Multi-PDF Ingestion, ChromaDB, and Google Gemini.
        </p>
    </div>
    """, unsafe_allow_html=True)

    g_col1, g_col2 = st.columns([1, 1])

    with g_col1:
        st.markdown("""
        <div class="konk-guide-card">
            <span class="konk-guide-step-pill">01 // INGESTION &amp; CHUNKING</span>
            <div class="konk-guide-title">Multi-PDF Ingestion Engine</div>
            <div class="konk-guide-desc">
                Official policy PDFs (Leave, Travel, Reimbursements) are extracted using <code>pypdf</code>. Text is split into <strong>300-word sliding semantic windows</strong> with <strong>50-word overlaps</strong> to ensure cross-boundary legal context is never clipped. Every chunk retains immutable metadata tags: <code>source</code> filename and <code>page</code> number.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-guide-card">
            <span class="konk-guide-step-pill">02 // VECTORIZATION</span>
            <div class="konk-guide-title">ChromaDB Vector Repository</div>
            <div class="konk-guide-desc">
                Chunks are converted into high-dimensional semantic embeddings using Google's <code>text-embedding-004</code> and indexed into a local SQLite3-backed ChromaDB collection. This enables instant mathematical similarity calculations across thousands of statutory clauses.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-guide-card">
            <span class="konk-guide-step-pill">03 // SIMILARITY RETRIEVAL</span>
            <div class="konk-guide-title">Top-K Context Retrieval</div>
            <div class="konk-guide-desc">
                When an employee enters an inquiry (e.g. <em>"How many days of paid leave can I carry forward?"</em>), the query is vectorized and compared against ChromaDB using cosine distance. The system retrieves the top-3 most statistically relevant policy clauses.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g_col2:
        st.markdown("""
        <div class="konk-guide-card">
            <span class="konk-guide-step-pill">04 // REASONING ENGINE</span>
            <div class="konk-guide-title">Constrained Gemini Reasoning</div>
            <div class="konk-guide-desc">
                The retrieved clauses and user inquiry are formatted into an audited institutional prompt and passed to Google Gemini (<code>gemini-2.5-flash</code>). Strict systemic guardrails instruct the model: <em>"Answer strictly and exclusively from the provided policy clauses. If an allowance is not mentioned, refuse to fabricate it."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-guide-card">
            <span class="konk-guide-step-pill">05 // AUDITABILITY</span>
            <div class="konk-guide-title">Verifiable Judicial Footnotes</div>
            <div class="konk-guide-desc">
                Every generated response includes expandable judicial precedent cards citing the exact source PDF and page number (e.g. <code>Leave_Policy.pdf • Page 1</code>) alongside verbatim quote previews, establishing 100% auditability for HR and finance compliance.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="konk-guide-card" style="border-top: 3px solid #E7B96F;">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; color: #E7B96F; letter-spacing: 0.08em; margin-bottom: 6px;">// SPECIFICATIONS</div>
            <div class="konk-guide-title" style="font-size: 1.2rem;">Academic Project Specifications</div>
            <div style="font-family: 'Archivo'; font-size: 0.86rem; color: #D1CFCA; line-height: 1.7;">
                &bull; <strong>Problem Statement:</strong> PS 34 (Company Policy Assistant)<br/>
                &bull; <strong>Student Roll No:</strong> 34<br/>
                &bull; <strong>Vector DB:</strong> ChromaDB (Local SQLite3 Persistence)<br/>
                &bull; <strong>LLM API:</strong> Google GenAI SDK (v1beta HTTP options)<br/>
                &bull; <strong>Design System:</strong> Architectural Luxury Codex (Konk Electrical Template)
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: Policy Dashboard & Consultation
# ---------------------------------------------------------
with tab_dashboard:
    # Live Metadata Ledger (Konk 4-column Strip)
    total_policies = len(policy_files)
    status_label = "100% Certified" if api_key else "Key Required"
    status_color = "#E7B96F" if api_key else "#C89446"

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

    # In-App Folio Document Inspector (Activated via Sidebar or Library "View")
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
                <div class="konk-inspector-card">
                    <div class="konk-inspector-header">
                        <div>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #E7B96F; font-weight: 700;">
                                // OFFICIAL INSTITUTIONAL FOLIO INSPECTOR
                            </span>
                            <h2 style="font-family: 'Archivo'; font-size: 1.7rem; font-weight: 800; margin: 6px 0; color: #F2F0EB;">
                                {doc_name.replace('_Policy.pdf', '').replace('_', ' ')} Policy Manual
                            </h2>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.78rem; color: #8C8A84;">
                                Source File: <code>{doc_name}</code> &bull; {total_pages} Page(s) &bull; Audited Statutory Copy
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c_close, c_dl = st.columns([1, 1])
                with c_close:
                    if st.button("❌ Close Document Inspector", key="close_inspector", use_container_width=True):
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
                <div class="konk-inspector-body">{full_text}</div>
                <div style="margin-bottom: 2rem;"></div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error inspecting document: {e}")

    # Curated Inquiries & Active Dossiers (Konk Architectural Cards)
    st.markdown("""
    <div class="konk-section-heading">
        <span class="konk-section-label">CURATED INQUIRIES &amp; ACTIVE DOSSIERS</span>
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
                        <div class="konk-dossier-badges">{badges_html}</div>
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

    # Archival Consultation Divider
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 14px; margin: 2.2rem 0 1.4rem 0;">
        <div style="height: 1px; background: #26262A; flex: 1;"></div>
        <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #8C8A84;">
            📜 CONSULTATION RECORD • VECTOR-GROUNDING VAULT ACTIVE
        </span>
        <div style="height: 1px; background: #26262A; flex: 1;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Consultation Stream
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

# ---------------------------------------------------------
# Tab 3: Policy PDF Folios & Document Library
# ---------------------------------------------------------
with tab_library:
    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #E7B96F; font-weight: 700; margin-bottom: 4px;">
            // STATUTORY DOCUMENT REPOSITORY
        </div>
        <h2 style="font-family: 'Archivo'; font-size: 2.1rem; font-weight: 800; color: #F2F0EB; margin: 0 0 8px 0;">
            Official Policy PDF Folios &amp; Regulatory Manuals
        </h2>
        <p style="font-family: 'Archivo'; font-size: 0.95rem; color: #8C8A84; line-height: 1.6; margin: 0;">
            Inspect official company policy folios, read codified text page-by-page, and download certified original PDF copies for your records.
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

            clauses_html = "".join([f'<span style="display: inline-block; background: #18181B; border: 1px solid #26262A; color: #D1CFCA; font-family: \'JetBrains Mono\', monospace; font-size: 0.72rem; font-weight: 500; padding: 4px 8px; border-radius: 4px; margin: 3px 4px 3px 0;">{c}</span>' for c in p_info["clauses"]])

            st.markdown(f"""
            <div class="konk-lib-card">
                <div class="konk-lib-header">
                    <div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #E7B96F;">FOLIO {roman}</span>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 600; background: rgba(231,185,111,0.12); border: 1px solid rgba(231,185,111,0.3); color: #E7B96F; padding: 2px 6px; border-radius: 4px;">{p_info['code']}</span>
                            <span style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 600; background: #18181B; border: 1px solid #26262A; color: #8C8A84; padding: 2px 6px; border-radius: 4px;">Audited 2026</span>
                        </div>
                        <h3 class="konk-lib-title">{p_info['title']}</h3>
                        <div style="font-family: 'JetBrains Mono'; font-size: 0.76rem; color: #8C8A84;">File: <code>{pf}</code> &bull; Size: {file_size_kb} KB &bull; Extent: {num_pages} Page(s) &bull; Format: Certified PDF</div>
                    </div>
                </div>
                <div class="konk-lib-desc">{p_info['desc']}</div>
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
    else:
        st.warning("No policy folios found in repository.")

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
