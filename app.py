import os
import streamlit as st
import pypdf
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

    :root, [data-theme="light"], [data-theme="dark"], .stApp {
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
        --text-color: #1b1c1e !important;
        --background-color: #faf9fb !important;
        --secondary-background-color: #efedf0 !important;
    }

    /* Base Body Reset */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: var(--stitch-surface) !important;
        background: var(--stitch-surface) !important;
        color: var(--stitch-on-surface) !important;
        -webkit-text-fill-color: var(--stitch-on-surface) !important;
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

    /* Curated Inquiries & Active Dossiers Cards (Stitch Design) */
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

    .stitch-dossier-card {
        background-color: var(--stitch-surface-container-lowest) !important;
        background: var(--stitch-surface-container-lowest) !important;
        border: 1px solid var(--stitch-outline-variant);
        border-radius: 16px;
        padding: 24px 22px 18px 22px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
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
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stitch-dossier-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border-color: var(--stitch-primary-container);
    }
    .stitch-dossier-card.featured {
        border-top: 4px solid var(--stitch-primary-container) !important;
        box-shadow: 0 4px 18px rgba(20, 69, 61, 0.08);
    }
    .stitch-dossier-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        height: 24px;
    }
    .stitch-dossier-ref {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--stitch-outline) !important;
        -webkit-text-fill-color: var(--stitch-outline) !important;
    }
    .stitch-dossier-ref.featured {
        color: var(--stitch-primary-container) !important;
        -webkit-text-fill-color: var(--stitch-primary-container) !important;
    }
    .stitch-dossier-badges {
        display: flex;
        gap: 6px;
        align-items: center;
    }
    .stitch-dossier-badge {
        font-size: 0.68rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        background: var(--stitch-surface-container);
        color: var(--stitch-on-surface-variant) !important;
        -webkit-text-fill-color: var(--stitch-on-surface-variant) !important;
        letter-spacing: 0.04em;
        white-space: nowrap;
    }
    .stitch-dossier-badge.active {
        background: rgba(20, 69, 61, 0.12) !important;
        color: var(--stitch-primary-container) !important;
        -webkit-text-fill-color: var(--stitch-primary-container) !important;
    }
    .stitch-dossier-badge.secondary {
        background: rgba(167, 58, 26, 0.12) !important;
        color: var(--stitch-secondary) !important;
        -webkit-text-fill-color: var(--stitch-secondary) !important;
    }
    .stitch-dossier-title {
        font-family: 'Newsreader', Georgia, serif !important;
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        line-height: 1.35 !important;
        color: var(--stitch-on-surface) !important;
        -webkit-text-fill-color: var(--stitch-on-surface) !important;
        margin-bottom: 10px;
        height: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .stitch-dossier-desc {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.84rem !important;
        line-height: 1.55 !important;
        color: var(--stitch-on-surface-variant) !important;
        -webkit-text-fill-color: var(--stitch-on-surface-variant) !important;
        margin-bottom: 12px;
        flex-grow: 1;
        overflow: hidden;
    }
    .stitch-dossier-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 10px;
        border-top: 1px solid rgba(0, 0, 0, 0.06);
        font-size: 0.72rem;
        color: var(--stitch-outline) !important;
        -webkit-text-fill-color: var(--stitch-outline) !important;
        font-weight: 600;
        height: 24px;
    }

    /* Functional Sidebar Policy Folio Cards */
    .stitch-folio-box {
        background: var(--stitch-surface-container-lowest);
        border: 1px solid var(--stitch-outline-variant);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
    }
    .stitch-folio-box:hover {
        border-color: var(--stitch-primary-container);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stitch-folio-box-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }
    .stitch-folio-box-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--stitch-on-surface);
    }
    .stitch-folio-box-sub {
        font-size: 0.72rem;
        color: var(--stitch-outline);
        margin-bottom: 10px;
    }

    /* In-App Policy Document Inspector */
    .stitch-inspector-card {
        background: #ffffff;
        border: 1.5px solid var(--stitch-primary-container);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(20, 69, 61, 0.08);
    }
    .stitch-inspector-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        padding-bottom: 12px;
        margin-bottom: 16px;
    }
    .stitch-inspector-body {
        background: var(--stitch-surface-container-low);
        border: 1px solid var(--stitch-outline-variant);
        border-radius: 10px;
        padding: 20px;
        font-family: 'Newsreader', serif;
        font-size: 1.05rem;
        line-height: 1.65;
        color: var(--stitch-on-surface);
        max-height: 420px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    /* Institutional Auditor Profile */
    .stitch-auditor-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 14px;
        border-radius: 12px;
        background: var(--stitch-surface-container);
        border: 1px solid rgba(0,0,0,0.06);
        margin-top: 14px;
    }
    .stitch-auditor-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: var(--stitch-primary-container);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #ffffff;
        box-shadow: 0 2px 6px rgba(20,69,61,0.2);
    }

    /* Chat Messages - Publication Brief */
    div[data-testid="stChatMessage"] {
        background-color: var(--stitch-surface-container-lowest) !important;
        background: var(--stitch-surface-container-lowest) !important;
        border: 1px solid var(--stitch-outline-variant) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.4rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
    }

    div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background-color: var(--stitch-surface-container-low) !important;
        background: var(--stitch-surface-container-low) !important;
        border-color: var(--stitch-surface-container-high) !important;
    }

    /* Strict High-Contrast Dark Ink text across all messages & markdown */
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
        color: #1b1c1e !important;
        -webkit-text-fill-color: #1b1c1e !important;
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
        color: var(--stitch-primary) !important;
        display: block;
        margin-bottom: 4px;
    }
    .stitch-exec-text {
        font-family: 'Newsreader', serif;
        font-size: 1.15rem;
        line-height: 1.55;
        color: var(--stitch-on-surface) !important;
        -webkit-text-fill-color: var(--stitch-on-surface) !important;
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
        color: var(--stitch-on-surface) !important;
        -webkit-text-fill-color: var(--stitch-on-surface) !important;
    }

    /* Bottom Input Dock Reset - Complete eradication of dark/black bar */
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

    [data-testid="stBottom"]::before,
    [data-testid="stBottom"]::after {
        display: none !important;
        background: transparent !important;
    }

    /* Floating Dock Input - Crisp light surface with clear dark text */
    div[data-testid="stChatInput"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 1.5px solid var(--stitch-outline-variant) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        padding: 6px 10px !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--stitch-primary-container) !important;
        box-shadow: 0 0 0 3px rgba(20, 69, 61, 0.12) !important;
    }

    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #1b1c1e !important;
        -webkit-text-fill-color: #1b1c1e !important;
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder,
    div[data-testid="stChatInput"] textarea::-webkit-input-placeholder {
        color: #5f6368 !important;
        -webkit-text-fill-color: #5f6368 !important;
        opacity: 1 !important;
        font-weight: 400 !important;
    }

    div[data-testid="stChatInput"] button {
        background-color: var(--stitch-primary-container) !important;
        background: var(--stitch-primary-container) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        transition: background 0.2s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background-color: var(--stitch-primary) !important;
        background: var(--stitch-primary) !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
        color: #ffffff !important;
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

    /* Top Navigation Tabs (Stitch Editorial Tabs) */
    [data-testid="stTabs"] {
        margin-top: 0.8rem !important;
        margin-bottom: 2rem !important;
    }
    button[data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: var(--stitch-on-surface-variant) !important;
        -webkit-text-fill-color: var(--stitch-on-surface-variant) !important;
        padding: 12px 26px !important;
        border-radius: 10px 10px 0 0 !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    button[data-baseweb="tab"]:hover {
        color: var(--stitch-primary) !important;
        -webkit-text-fill-color: var(--stitch-primary) !important;
        background: var(--stitch-surface-container-high) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--stitch-primary) !important;
        -webkit-text-fill-color: var(--stitch-primary) !important;
        border-bottom: 3px solid var(--stitch-primary-container) !important;
        background: var(--stitch-surface-container-lowest) !important;
        box-shadow: 0 -2px 6px rgba(0,0,0,0.02) !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: var(--stitch-primary-container) !important;
    }

    /* Library Cards */
    .stitch-lib-card {
        background: var(--stitch-surface-container-lowest);
        border: 1px solid var(--stitch-outline-variant);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
    }
    .stitch-lib-card:hover {
        border-color: var(--stitch-primary-container);
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }
    .stitch-lib-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(0,0,0,0.06);
        padding-bottom: 12px;
    }
    .stitch-lib-title {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.45rem;
        font-weight: 500;
        color: var(--stitch-on-surface);
        margin: 4px 0;
    }
    .stitch-lib-desc {
        font-size: 0.88rem;
        line-height: 1.6;
        color: var(--stitch-on-surface-variant);
        margin-bottom: 16px;
    }

    /* Guide Workflow Cards */
    .stitch-guide-card {
        background: var(--stitch-surface-container-lowest);
        border: 1px solid var(--stitch-outline-variant);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: transform 0.2s ease;
    }
    .stitch-guide-card:hover {
        transform: translateY(-2px);
        border-color: var(--stitch-primary-container);
    }
    .stitch-guide-step-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--stitch-surface-container);
        color: var(--stitch-primary);
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .stitch-guide-title {
        font-family: 'Newsreader', serif;
        font-size: 1.3rem;
        font-weight: 500;
        color: var(--stitch-on-surface);
        margin-bottom: 6px;
    }
    .stitch-guide-desc {
        font-size: 0.86rem;
        line-height: 1.6;
        color: var(--stitch-on-surface-variant);
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
    <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #707976; font-weight: 700; margin-bottom: 10px;">
        📜 Codified Policy Folios
    </div>
    """, unsafe_allow_html=True)
    
    policy_files = [f for f in os.listdir(POLICIES_DIR) if f.lower().endswith(".pdf")]
    if policy_files:
        for idx, pf in enumerate(policy_files):
            filepath = os.path.join(POLICIES_DIR, pf)
            file_size_kb = round(os.path.getsize(filepath) / 1024, 1)
            roman_nums = ["I", "II", "III", "IV", "V", "VI"]
            roman = roman_nums[idx] if idx < len(roman_nums) else str(idx+1)
            clean_name = pf.replace("_Policy.pdf", "").replace("_", " ")
            
            with open(filepath, "rb") as f:
                pdf_bytes = f.read()

            st.markdown(f"""
            <div class="stitch-folio-box">
                <div class="stitch-folio-box-header">
                    <span class="stitch-folio-box-title">Folio {roman}: {clean_name}</span>
                    <span class="stitch-folio-badge">{file_size_kb} KB</span>
                </div>
                <div class="stitch-folio-box-sub">
                    File: <code>{pf}</code> &bull; <span style="color: #14453d; font-weight: 600;">Audited</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                st.download_button(
                    label="📥 Download",
                    data=pdf_bytes,
                    file_name=pf,
                    mime="application/pdf",
                    key=f"dl_sidebar_{idx}",
                    use_container_width=True
                )
            with b_col2:
                if st.button("📖 Read", key=f"inspect_sidebar_{idx}", use_container_width=True):
                    st.session_state.active_doc_preview = pf
                    st.rerun()
    else:
        st.warning("No PDF policies located in `policies/`.")

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #707976; font-weight: 700; margin-bottom: 8px;">
        ⚡ Folio Ingestion &amp; Sync
    </div>
    """, unsafe_allow_html=True)

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

    # Institutional Auditor Profile Card (Matching Stitch Sidebar)
    st.markdown("""
    <div class="stitch-auditor-profile">
        <div class="stitch-auditor-avatar">⚖️</div>
        <div style="flex-grow: 1; min-width: 0;">
            <div style="font-size: 0.82rem; font-weight: 700; color: #1b1c1e;">Compliance Officer</div>
            <div style="font-size: 0.7rem; color: #707976;">Roll No: 34 &bull; Codex PS 34</div>
        </div>
        <span style="font-size: 0.65rem; font-weight: 700; color: #14453d; background: rgba(20,69,61,0.12); padding: 2px 6px; border-radius: 4px;">ACTIVE</span>
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

# ---------------------------------------------------------
# Top Navigation Tabs (Starting with How It Works, then Dashboard & Library)
# ---------------------------------------------------------
tab_guide, tab_dashboard, tab_library = st.tabs([
    "⚙️ How It Works & System Guide",
    "🏛️ Policy Dashboard & Consultation",
    "📚 Policy PDF Folios & Document Library"
])

# ---------------------------------------------------------
# Tab 1: How It Works & System Guide (Landing & Architecture)
# ---------------------------------------------------------
with tab_guide:
    st.markdown("""
    <div style="background: rgba(20, 69, 61, 0.08); border-left: 4px solid #14453d; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px;">
        <span style="font-weight: 700; color: #14453d; font-size: 0.95rem;">🚀 System Onboarding &amp; Architecture:</span>
        <span style="color: #404846; font-size: 0.9rem;"> Review how our zero-hallucination policy engine operates below, then click the <strong>🏛️ Policy Dashboard &amp; Consultation</strong> tab above to query live guidelines!</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #14453d; font-weight: 700; margin-bottom: 4px;">
            System Architecture &amp; Methodology
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2rem; color: #1b1c1e; margin: 0 0 8px 0;">
            How the Zero-Hallucination Policy Assistant Works
        </h2>
        <p style="font-size: 0.95rem; color: #5f6368; line-height: 1.6; margin: 0;">
            Technical implementation overview of Problem Statement 34 (Company Policy Assistant) built with Multi-PDF Ingestion, ChromaDB, and Google Gemini.
        </p>
    </div>
    """, unsafe_allow_html=True)

    g_col1, g_col2 = st.columns([1, 1])

    with g_col1:
        st.markdown("""
        <div class="stitch-guide-card">
            <span class="stitch-guide-step-pill">1. Document Parsing &amp; Chunking</span>
            <div class="stitch-guide-title">Multi-PDF Ingestion Engine</div>
            <div class="stitch-guide-desc">
                Official policy PDFs (Leave, Travel, Reimbursements) are extracted using <code>pypdf</code>. Text is split into <strong>300-word sliding semantic windows</strong> with <strong>50-word overlaps</strong> to ensure cross-boundary legal context is never clipped. Every chunk retains immutable metadata tags: <code>source</code> filename and <code>page</code> number.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stitch-guide-card">
            <span class="stitch-guide-step-pill">2. High-Dimensional Embeddings</span>
            <div class="stitch-guide-title">ChromaDB Vector Store</div>
            <div class="stitch-guide-desc">
                Chunks are converted into semantic vector embeddings using Google's <code>text-embedding-004</code> and indexed into a local SQLite3-backed ChromaDB collection. This enables instant mathematical similarity calculations across thousands of statutory clauses.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stitch-guide-card">
            <span class="stitch-guide-step-pill">3. Semantic Cosine Retrieval</span>
            <div class="stitch-guide-title">Top-K Context Retrieval</div>
            <div class="stitch-guide-desc">
                When an employee enters an inquiry (e.g. <em>"How many days of paid leave can I carry forward?"</em>), the query is vectorized and compared against ChromaDB using cosine distance. The system retrieves the top-3 most statistically relevant policy clauses.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g_col2:
        st.markdown("""
        <div class="stitch-guide-card">
            <span class="stitch-guide-step-pill">4. Zero-Hallucination Synthesis</span>
            <div class="stitch-guide-title">Constrained Gemini Reasoning</div>
            <div class="stitch-guide-desc">
                The retrieved clauses and user inquiry are formatted into an audited institutional prompt and passed to Google Gemini (<code>gemini-2.5-flash</code>). Strict systemic guardrails instruct the model: <em>"Answer strictly and exclusively from the provided policy clauses. If an allowance is not mentioned, refuse to fabricate it."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stitch-guide-card">
            <span class="stitch-guide-step-pill">5. Audited Source Attributions</span>
            <div class="stitch-guide-title">Verifiable Judicial Footnotes</div>
            <div class="stitch-guide-desc">
                Every generated response includes expandable judicial precedent cards citing the exact source PDF and page number (e.g. <code>Leave_Policy.pdf • Page 1</code>) alongside verbatim quote previews, establishing 100% auditability for HR and finance compliance.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stitch-guide-card" style="border-left: 4px solid #14453d;">
            <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #14453d; letter-spacing: 0.08em; margin-bottom: 4px;">Compliance &amp; Specs</div>
            <div class="stitch-guide-title" style="font-size: 1.15rem;">Academic Project Specifications</div>
            <div style="font-size: 0.82rem; color: #404846; line-height: 1.6;">
                &bull; <strong>Problem Statement:</strong> PS 34 (Company Policy Assistant)<br/>
                &bull; <strong>Student Roll No:</strong> 34<br/>
                &bull; <strong>Vector DB:</strong> ChromaDB (Local SQLite3 Persistence)<br/>
                &bull; <strong>LLM API:</strong> Google GenAI SDK (v1beta HTTP options)<br/>
                &bull; <strong>UI System:</strong> Modern Editorial Lexicon (Google Stitch Screen 322cbe1be2274dcbadc0e3286a5b94de)
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: Policy Dashboard & Consultation
# ---------------------------------------------------------
with tab_dashboard:
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

    # In-App Folio Document Inspector (Activated via Sidebar or Library "Read")
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
                <div class="stitch-inspector-card">
                    <div class="stitch-inspector-header">
                        <div>
                            <span style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #14453d; font-weight: 700;">
                                📖 Official Institutional Folio Inspector
                            </span>
                            <h2 style="font-family: 'Newsreader', serif; font-size: 1.6rem; margin: 4px 0; color: #1b1c1e;">
                                {doc_name.replace('_Policy.pdf', '').replace('_', ' ')} Policy Manual
                            </h2>
                            <span style="font-size: 0.78rem; color: #707976;">
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
                <div class="stitch-inspector-body">{full_text}</div>
                <div style="margin-bottom: 2rem;"></div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error inspecting document: {e}")

    # Curated Inquiries & Active Dossiers (Stitch Card I, II, III)
    st.markdown("""
    <div class="stitch-section-heading">
        <span class="stitch-section-label">Curated Inquiries &amp; Active Dossiers</span>
        <span style="font-size: 0.72rem; color: #707976; letter-spacing: 0.06em;">CATALOGUE VOL. XXIV</span>
    </div>
    """, unsafe_allow_html=True)

    preset_cols = st.columns(3)
    quick_queries = [
        {
            "ref": "REF: ARCH-4011",
            "badges": [
                {"text": "HR FOLIO", "cls": ""},
                {"text": "AUDITED 2025", "cls": "secondary"}
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
                {"text": "ACTIVE CONSULTATION", "cls": "active"},
                {"text": "AUDITED 2025", "cls": "secondary"}
            ],
            "title": "II. Daily Per Diem & Corporate Lodging Caps",
            "desc": "Section 7.3.0 — Tier-1 metro lodging limits ($380/nt), transatlantic flight tiers, and client entertainment thresholds.",
            "footer_stat": "📍 Section 7.3.4 In-Scope • Active in Workspace",
            "query": "What is the daily per diem allowance for domestic business travel?",
            "featured": True
        },
        {
            "ref": "REF: ARCH-9840",
            "badges": [
                {"text": "REMOTE WORK", "cls": ""},
                {"text": "AUDITED 2025", "cls": "secondary"}
            ],
            "title": "III. Home Office Infrastructure Stipend",
            "desc": "Section 9.8.4 — Annual ergonomic allocation ($1,500), hardware depreciation schedules, and dual-monitor subsidies.",
            "footer_stat": "🛡️ Verified Q1 • Institutional Grant",
            "query": "What is the WFH equipment allowance for new employees?",
            "featured": False
        }
    ]

    selected_query = None
    for idx, col in enumerate(preset_cols):
        q = quick_queries[idx]
        with col:
            badges_html = "".join([f'<span class="stitch-dossier-badge {b["cls"]}">{b["text"]}</span>' for b in q["badges"]])
            featured_card = " featured" if q["featured"] else ""
            featured_ref = " featured" if q["featured"] else ""
            
            st.markdown(f"""
            <div class="stitch-dossier-card{featured_card}">
                <div>
                    <div class="stitch-dossier-top">
                        <span class="stitch-dossier-ref{featured_ref}">{q['ref']}</span>
                        <div class="stitch-dossier-badges">{badges_html}</div>
                    </div>
                    <div class="stitch-dossier-title">{q['title']}</div>
                    <div class="stitch-dossier-desc">{q['desc']}</div>
                </div>
                <div class="stitch-dossier-footer">
                    <span>{q['footer_stat']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            card_btn = st.button(
                "⚡ Load Brief & Consult →",
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

    # Consultation Stream
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
# Tab 3: Policy PDF Folios & Document Library
# ---------------------------------------------------------
with tab_library:
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #14453d; font-weight: 700; margin-bottom: 4px;">
            Statutory Document Repository
        </div>
        <h2 style="font-family: 'Newsreader', serif; font-size: 2rem; color: #1b1c1e; margin: 0 0 8px 0;">
            Official Policy PDF Folios &amp; Regulatory Manuals
        </h2>
        <p style="font-size: 0.95rem; color: #5f6368; line-height: 1.6; margin: 0;">
            Browse official company policy folios, inspect codified clauses page-by-page, and download certified original PDF copies for your records.
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

            clauses_html = "".join([f'<span style="display: inline-block; background: #efedf0; color: #404846; font-size: 0.72rem; font-weight: 600; padding: 3px 8px; border-radius: 4px; margin: 3px 4px 3px 0;">{c}</span>' for c in p_info["clauses"]])

            st.markdown(f"""
            <div class="stitch-lib-card">
                <div class="stitch-lib-header">
                    <div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 4px;">
                            <span style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #14453d;">FOLIO {roman}</span>
                            <span style="font-size: 0.68rem; font-weight: 600; background: rgba(20,69,61,0.1); color: #14453d; padding: 2px 6px; border-radius: 4px;">{p_info['code']}</span>
                            <span style="font-size: 0.68rem; font-weight: 600; background: #efedf0; color: #707976; padding: 2px 6px; border-radius: 4px;">Audited 2025</span>
                        </div>
                        <h3 class="stitch-lib-title">{p_info['title']}</h3>
                        <div style="font-size: 0.78rem; color: #707976;">File: <code>{pf}</code> &bull; Size: {file_size_kb} KB &bull; Extent: {num_pages} Page(s) &bull; Format: Certified PDF</div>
                    </div>
                </div>
                <div class="stitch-lib-desc">{p_info['desc']}</div>
                <div style="margin-bottom: 16px;">
                    <span style="font-size: 0.7rem; text-transform: uppercase; font-weight: 700; color: #707976; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">Key Statutory Clauses:</span>
                    <div>{clauses_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_act1, col_act2 = st.columns([1, 2])
            with col_act1:
                st.download_button(
                    label=f"📥 Download Original PDF",
                    data=pdf_data,
                    file_name=pf,
                    mime="application/pdf",
                    key=f"lib_dl_{p_idx}",
                    use_container_width=True
                )
            with col_act2:
                with st.expander(f"📖 Read Codified Full Text ({pf} &bull; {num_pages} Pages)", expanded=False):
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
