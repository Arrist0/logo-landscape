import io
import re
import requests
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Logo Landscape — Visual Identity Research",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS with Click-to-Flip via <details> and Full Light/Dark Compatibility
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Space+Grotesk:wght@500;700&display=swap');

/* Dynamic Theme Variables */
:root {
  --bg: #ffffff;
  --card: #f8f9fa;
  --ink: #1a1a1a;
  --muted: #666666;
  --line: #e2e8f0;
  --accent: #6366f1;
  --card-back: #ffffff;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1117;
    --card: #171923;
    --ink: #f7fafc;
    --muted: #a0aec0;
    --line: #2d3748;
    --accent: #6366f1;
    --card-back: #1a1d29;
  }
}

* { transition: background-color 0.2s ease, border-color 0.2s ease; }

.main, .stApp { 
  background-color: var(--bg);
  color: var(--ink);
  font-family: "DM Sans", sans-serif; 
}

/* Header & Top Bar */
.topbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 25px;
}

h1.app-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 28px;
    margin: 0;
    color: var(--ink);
    font-weight: 700;
}

.top-meta {
    font-size: 13px;
    color: var(--muted);
}

.hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(28px, 3.5vw, 44px);
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 18px;
}

/* Pill Toggle Switch */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    background-color: var(--card);
    border-radius: 30px;
    padding: 4px;
    border: 1.5px solid var(--line);
    display: inline-flex;
}
div[data-testid="stRadio"] label {
    border-radius: 26px !important;
    padding: 6px 18px !important;
    background-color: transparent;
    cursor: pointer;
    margin: 0;
}
div[data-testid="stRadio"] label p { color: var(--ink) !important; }
div[data-testid="stRadio"] label[data-checked="true"] { background-color: var(--accent) !important; }
div[data-testid="stRadio"] label[data-checked="true"] p { color: #ffffff !important; font-weight: 600 !important; }
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] { margin-left: 0; }
div[data-testid="stRadio"] span[data-baseweb="radio"] { display: none; }

/* Editorial Summary Card */
.editorial-wrap {
    display: grid;
    grid-template-columns: 0.9fr 1.3fr;
    gap: 32px;
    align-items: center;
    border: 1.5px solid var(--line);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 24px;
    background: var(--card);
}

.editorial-hero {
    border-right: 1px solid var(--line);
    padding-right: 28px;
}

.editorial-eyebrow {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 6px;
}

.editorial-number {
    font-family: "Space Grotesk", sans-serif;
    font-size: 48px;
    line-height: 1.0;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.02em;
}

.editorial-desc {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.5;
    margin-top: 8px;
}

.editorial-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 8px 0;
    border-bottom: 1px solid var(--line);
}

.editorial-row:last-child { border-bottom: none; padding-bottom: 0; }
.editorial-row:first-child { padding-top: 0; }

.editorial-row-label { font-size: 13px; color: var(--ink); }
.editorial-sub { color: var(--muted); font-size: 11px; display: block; }
.editorial-row-value {
    font-family: "Space Grotesk", sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--ink);
}

/* Color Palette Bar */
.palette-bar-container {
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: 12px;
    padding: 14px 20px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.palette-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
    white-space: nowrap;
    margin-right: 20px;
}

.palette-items {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
    align-items: center;
    width: 100%;
}

.palette-item {
    display: flex;
    align-items: center;
    gap: 8px;
}

.palette-swatch {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 1px solid rgba(0, 0, 0, 0.15);
}

.palette-name { font-size: 13px; font-weight: 500; color: var(--ink); }
.palette-pct { font-size: 12px; color: var(--muted); font-weight: 600; }

/* Pure HTML Details Click-to-Flip Architecture */
details.flip-card {
    width: 100%;
    height: 350px;
    margin-bottom: 24px;
    perspective: 1000px;
    outline: none;
}

details.flip-card summary {
    list-style: none;
    cursor: pointer;
    width: 100%;
    height: 100%;
}

details.flip-card summary::-webkit-details-marker {
    display: none;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease;
    transform-style: preserve-3d;
    border-radius: 12px;
}

/* Hover Effect: Subtle Lift and Highlight ONLY */
details.flip-card:hover .flip-card-inner {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(99, 102, 241, 0.18);
}

/* Click Triggered Flip */
details.flip-card[open] .flip-card-inner {
    transform: rotateY(180deg);
}

details.flip-card[open]:hover .flip-card-inner {
    transform: rotateY(180deg) translateY(-4px);
}

.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
    border-radius: 12px;
    border: 1.5px solid var(--line);
    overflow: hidden;
}

.flip-card-front {
    background-color: var(--card);
    display: flex;
    flex-direction: column;
}

.flip-card-back {
    background-color: var(--card-back);
    color: var(--ink);
    transform: rotateY(180deg);
    padding: 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-color: var(--accent);
}

/* Card Content Elements */
.card-image-box {
    height: 170px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border-bottom: 1.5px solid var(--line);
}

.card-image-box img {
    max-height: 130px;
    max-width: 90%;
    object-fit: contain;
}

.card-front-content {
    padding: 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-grow: 1;
}

.card-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
    line-height: 1.25;
}

.card-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    font-size: 12px;
    color: var(--muted);
}

.card-meta-item strong { color: var(--ink); }

.flip-hint {
    font-size: 10.5px;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
    margin-top: 10px;
}

/* Back Card Details */
.back-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--accent);
    border-bottom: 1px solid var(--line);
    padding-bottom: 6px;
    margin-bottom: 10px;
}

.back-detail-row {
    font-size: 12px;
    margin-bottom: 6px;
    color: var(--muted);
}

.back-detail-row strong { color: var(--ink); }

.back-symbolism {
    font-size: 11.5px;
    color: var(--ink);
    line-height: 1.45;
    background: rgba(0, 0, 0, 0.03);
    padding: 8px 10px;
    border-radius: 6px;
    border: 1px solid var(--line);
    max-height: 110px;
    overflow-y: auto;
}

/* Sidebar Styling */
[data-testid="stSidebar"] { background-color: var(--bg); }
[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    height: 44px !important;
    border-radius: 8px !important;
    background-color: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    color: var(--ink) !important;
    font-weight: 600 !important;
}

/* ===== Analytics page ===== */
.swatch {
    width: 14px;
    height: 14px;
    border-radius: 4px;
    border: 1px solid rgba(0,0,0,0.08);
    display: inline-block;
    margin-right: 7px;
    vertical-align: middle;
}

.rr-kpis {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

.kpi {
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: 10px;
    padding: 14px 16px;
}

.kpi-label {
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}

.kpi-value {
    font-family: "Space Grotesk", sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--ink);
}

.kpi-sub { font-size: 12px; color: var(--muted); margin-top: 2px; }

.rr-charts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.chart-card {
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: 12px;
    padding: 18px 20px;
}

.chart-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 14px;
}

.bar-row {
    display: grid;
    grid-template-columns: 110px 1fr 40px;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 12.5px;
}

.bar-row:last-child { margin-bottom: 0; }

.bar-label {
    display: flex;
    align-items: center;
    color: var(--ink);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.bar-track {
    background: var(--bg);
    border: 1px solid var(--line);
    border-radius: 5px;
    height: 14px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 5px 0 0 5px;
    background: var(--accent);
}

.bar-pct { text-align: right; color: var(--muted); font-weight: 600; }

.full-width-card { grid-column: 1 / -1; }

.crosstab {
    display: grid;
    gap: 0;
    font-size: 12px;
}

.crosstab .ct-cell {
    padding: 8px 6px;
    border-bottom: 1px solid var(--line);
    display: flex;
    align-items: center;
    color: var(--ink);
}

.crosstab .ct-head {
    font-weight: 700;
    color: var(--muted);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border-bottom: 1.5px solid var(--ink);
}

.ct-row-label { font-weight: 600; }

.heat {
    justify-content: center;
    border-radius: 4px;
    margin: 3px;
    font-weight: 700;
    color: var(--ink);
    display: flex;
}

.rr-footnote { font-size: 11.5px; color: var(--muted); margin-top: 14px; line-height: 1.5; }

/* ===== UX overhaul additions (v8) ===== */

/* Sidebar title + toggle */
.sidebar-app-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--ink);
    margin: 4px 0 14px 0;
}

/* Toggle row: pill + sync icon on one baseline */
.st-key-toggle_row div[data-testid="stHorizontalBlock"] {
    align-items: center !important;
}

/* Gallery / Analytics segmented pill: a real sliding thumb that physically
   moves between the two options, rather than each label independently
   toggling its own background. Full-width, roomy, no leftover native
   radio-button artwork. */
.st-key-view_toggle_wrap { margin-bottom: 18px; }
.st-key-view_toggle_wrap div[data-testid="stWidgetLabel"] {
    display: none !important;
}
.st-key-view_toggle_wrap div[data-testid="stRadio"] > div[role="radiogroup"] {
    position: relative;
    width: 100%;
    background-color: var(--card);
    border-radius: 999px;
    padding: 4px;
    border: 1.5px solid var(--line);
    display: flex;
    flex-direction: row;
    gap: 0;
    isolation: isolate;
    height: 46px;
    box-sizing: border-box;
}
.st-key-view_toggle_wrap div[data-testid="stRadio"] > div[role="radiogroup"]::before {
    content: "";
    position: absolute;
    top: 4px;
    bottom: 4px;
    left: 4px;
    width: calc(50% - 4px);
    background-color: var(--ink);
    border-radius: 999px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.2);
    transition: transform 0.32s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 0;
}
.st-key-view_toggle_wrap div[data-testid="stRadio"] > div[role="radiogroup"]:has(label:nth-of-type(2) input:checked)::before {
    transform: translateX(100%);
}
.st-key-view_toggle_wrap div[data-testid="stRadio"] label {
    position: relative;
    z-index: 1;
    flex: 1 1 0;
    display: flex !important;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-radius: 999px !important;
    padding: 0 26px !important;
    margin: 0 !important;
    background-color: transparent !important;
    cursor: pointer;
    min-width: 0;
}
.st-key-view_toggle_wrap div[data-testid="stRadio"] label p {
    color: var(--muted) !important;
    font-size: 14.5px !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    margin: 0 !important;
    transition: color 0.2s ease;
}
.st-key-view_toggle_wrap div[data-testid="stRadio"] label[data-checked="true"] p {
    color: #ffffff !important;
}
/* Nuke every trace of the native radio button — dot, ring, tap-highlight —
   regardless of which element it's actually nested in. */
.st-key-view_toggle_wrap div[data-testid="stRadio"] input[type="radio"],
.st-key-view_toggle_wrap div[data-testid="stRadio"] span[data-baseweb="radio"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
    position: absolute !important;
}
.st-key-view_toggle_wrap div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] {
    margin: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Small circular sync icon button, sits beside the sidebar title */
.st-key-sync_icon_wrap button {
    display: flex !important;
    align-items: center;
    justify-content: center;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    padding: 0 !important;
    min-height: unset !important;
    background: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    color: var(--ink) !important;
    font-size: 15px !important;
    line-height: 1 !important;
    margin-left: auto;
}
.st-key-sync_icon_wrap button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: rotate(45deg);
}
.st-key-sync_icon_wrap { display: flex; justify-content: flex-end; margin-top: 8px; }

/* Sidebar search box — give it a visible rounded field */
[data-testid="stSidebar"] div[data-testid="stTextInput"] input {
    background: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    color: var(--ink) !important;
}
[data-testid="stSidebar"] div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* Sidebar multiselect fields — match the rounded/bordered field language */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
[data-testid="stSidebar"] div[data-baseweb="tag"] {
    background-color: var(--accent) !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] div[data-testid="stMultiSelect"] label p {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
}
[data-testid="stSidebar"] div[data-testid="stMultiSelect"] {
    margin-bottom: 14px;
}

/* Main content subtitle bar (title moved to sidebar) */
.main-subtitle-bar {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--line);
}
.main-subtitle-text {
    font-size: 14px;
    color: var(--muted);
    font-weight: 500;
}
.main-subtitle-count {
    font-size: 13px;
    color: var(--ink);
}
.main-subtitle-count strong {
    font-family: "Space Grotesk", sans-serif;
    font-weight: 700;
}

/* Editorial Summary rendered inside a native expander -> restyle it to match card language */
div[data-testid="stExpander"] {
    border: 1.5px solid var(--line) !important;
    border-radius: 14px !important;
    background: var(--card) !important;
    margin-bottom: 18px !important;
    overflow: hidden;
}
div[data-testid="stExpander"] summary {
    padding: 14px 20px !important;
}
div[data-testid="stExpander"] summary p {
    font-family: "Space Grotesk", sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--ink);
}
div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
    padding: 0 20px 20px 20px !important;
}

/* Selected-filters bar: one bordered strip holding chips + Clear All + Sort */
div[class*="st-key-filters_summary_bar"] {
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 4px;
}

/* Chips row (flexbox hack over Streamlit's vertical block). Streamlit's own
   stylesheet sets these blocks to flex-direction: column with !important, so
   every rule that needs to beat that has to carry !important too, or the
   chips stack one-per-line instead of wrapping side by side. */
.st-key-chips_row [data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: wrap !important;
    align-items: center !important;
    gap: 8px !important;
    row-gap: 10px !important;
    width: 100% !important;
}
.st-key-chips_row div[data-testid="stElementContainer"] {
    width: auto !important;
    flex: 0 0 auto !important;
}
.st-key-chips_row button {
    border-radius: 20px !important;
    padding: 4px 14px !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
    background: var(--ink) !important;
    border: 1.5px solid var(--ink) !important;
    color: #ffffff !important;
    line-height: 1.4 !important;
    min-height: unset !important;
}
.st-key-chips_row button:hover {
    opacity: 0.85;
}
.st-key-clear_all_chips button {
    background: transparent !important;
    border: none !important;
    color: var(--accent) !important;
    text-decoration: underline;
    font-weight: 600 !important;
    padding: 4px 6px !important;
}
.no-filters-text {
    font-size: 12.5px;
    color: var(--muted);
    font-style: italic;
}

/* Sort dropdown inside the same bar */
div[class*="st-key-filters_summary_bar"] div[data-testid="stSelectbox"] {
    margin-top: 0 !important;
}

/* Result count line */
.result-count-text {
    font-size: 13px;
    color: var(--muted);
    margin: 10px 0 18px 0;
}
.result-count-text strong {
    color: var(--ink);
    font-weight: 700;
}

/* Reset-filters circular icon button, aligned with the "Filters" label */
.st-key-filters_header_row div[data-testid="stHorizontalBlock"] {
    align-items: center !important;
}
.st-key-reset_icon_wrap {
    display: flex;
    justify-content: flex-end;
}
.st-key-reset_icon_wrap button {
    display: flex !important;
    align-items: center;
    justify-content: center;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    padding: 0 !important;
    min-height: unset !important;
    background: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    color: var(--ink) !important;
    line-height: 1 !important;
}
.st-key-reset_icon_wrap button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: rotate(-45deg);
}
.filters-header-title {
    display: flex;
    align-items: center;
    height: 32px;
    font-weight: 700;
    font-size: 15px;
    color: var(--ink);
}
.filters-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}

/* Country tag chips inside Editorial Summary */
.editorial-country-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 6px;
}
.editorial-country-tag {
    font-size: 10.5px;
    font-weight: 600;
    color: var(--ink);
    background: var(--bg);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 2px 7px;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=3600)
def load_data():
    response = requests.get(CSV_URL)
    response.encoding = 'utf-8'
    lines = response.text.splitlines()

    header_idx = -1
    for idx, line in enumerate(lines):
        if "Name" in line and ("Primary form" in line or "Logo" in line or "Country" in line):
            header_idx = idx
            break

    if header_idx != -1:
        clean_csv = "\n".join(lines[header_idx:])
        df = pd.read_csv(io.StringIO(clean_csv))
    else:
        df = pd.read_csv(CSV_URL)

    df.columns = [re.sub(r'\s+', ' ', str(c)).strip() for c in df.columns]

    if "Name" in df.columns:
        name_series = df["Name"].astype(str).str.strip()
        is_continuation = name_series.eq("") | name_series.eq("nan")

        for i in range(1, len(df)):
            if is_continuation.iloc[i]:
                parent_idx = df.index[i - 1]
                this_idx = df.index[i]
                for col in df.columns:
                    if col == "Name":
                        continue
                    val = df.at[this_idx, col]
                    if pd.notna(val) and str(val).strip() not in ["", "nan"]:
                        parent_val = df.at[parent_idx, col]
                        if pd.isna(parent_val) or str(parent_val).strip() in ["", "nan"]:
                            df.at[parent_idx, col] = val

        df = df.dropna(subset=["Name"]).copy()
        df = df[df["Name"].astype(str).str.strip().ne("")].copy()

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading live dataset: {e}")
    st.stop()

def transform_image_url(url_str):
    url_str = str(url_str).strip()
    if not url_str or url_str.lower() in ["nan", "n/a", "none"]:
        return ""
    if "drive.google.com" in url_str:
        match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]+)', url_str)
        if match:
            return f"https://drive.google.com/uc?export=view&id={match.group(1)}"
    return url_str

COLOR_HEX_MAP = {
    "black": "#1a1a1a", "white": "#ffffff", "blue": "#2451c9", "red": "#c0392b",
    "green": "#1e9e5a", "yellow": "#e8b923", "orange": "#e07b39", "purple": "#8e44ad",
    "pink": "#e75f95", "teal": "#159e96", "grey": "#9aa0a6", "gray": "#9aa0a6",
    "brown": "#8a5a3c", "navy": "#1f2a5e", "maroon": "#6e1f2a", "gold": "#c9a227",
    "silver": "#b8bcc2", "cyan": "#22b6c9", "magenta": "#c23aa0",
}

def color_to_hex(name):
    return COLOR_HEX_MAP.get(str(name).strip().lower(), "#6366f1")

def top_value_pct(dataframe, col_name):
    if col_name not in dataframe.columns or dataframe.empty:
        return None, 0
    vals = dataframe[col_name].astype(str).str.strip()
    vals = vals[~vals.str.lower().isin(["", "nan", "n/a"])]
    if vals.empty:
        return None, 0
    counts = vals.value_counts()
    if counts.empty:
        return None, 0
    return counts.index[0], round(100 * counts.iloc[0] / len(dataframe))

def top_n_value_pct(dataframe, col_name, n=6):
    """Top-n (value, pct) pairs for a single column, ranked by frequency."""
    if col_name not in dataframe.columns or dataframe.empty:
        return []
    vals = dataframe[col_name].astype(str).str.strip()
    vals = vals[~vals.str.lower().isin(["", "nan", "n/a"])]
    if vals.empty:
        return []
    counts = vals.value_counts().head(n)
    total = len(dataframe)
    return [(idx, round(100 * cnt / total)) for idx, cnt in counts.items()]

def top_colors(dataframe, color_cols_list, max_n=5):
    counts = {}
    for _, row in dataframe.iterrows():
        row_colors = set()
        for c in color_cols_list:
            if c in dataframe.columns:
                v = str(row.get(c, "")).strip()
                if v and v.lower() not in ["", "nan", "n/a"] and not v.startswith("#"):
                    row_colors.add(v)
        for v in row_colors:
            counts[v] = counts.get(v, 0) + 1
    total = len(dataframe) if len(dataframe) > 0 else 1
    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:max_n]
    return [(name, round(100 * count / total)) for name, count in ranked]

def _bar_rows_html(items, with_swatch=False):
    parts = []
    for name, pct in items:
        swatch = f'<span class="swatch" style="background:{color_to_hex(name)}"></span>' if with_swatch else ""
        parts.append(
            f'<div class="bar-row"><div class="bar-label">{swatch}{name}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%;"></div></div>'
            f'<div class="bar-pct">{pct}%</div></div>'
        )
    return "".join(parts) if parts else '<div style="font-size:12px; color:var(--muted);">No data in this selection.</div>'

def render_analytics_page(filtered_df, df, color_cols, sector_col, color_family_col, country_col, complexity_col):
    """Detailed, filter-aware analytics dashboard — KPIs, distribution charts,
    and a Color Family x Sector cross-tab. Built as flush-left HTML strings
    (no loop-concatenated multi-line blocks) so Streamlit's Markdown parser
    doesn't misread indented fragments as code blocks."""

    kpi_countries = (
        filtered_df[country_col].astype(str).str.strip().replace("", pd.NA).dropna().nunique()
        if country_col in filtered_df.columns else 0
    )
    top_color_list = top_colors(filtered_df, color_cols, max_n=1)
    top_color_name, top_color_pct = top_color_list[0] if top_color_list else ("—", 0)

    top_complexity_list = top_n_value_pct(filtered_df, complexity_col, n=1)
    top_complexity_name, top_complexity_pct = top_complexity_list[0] if top_complexity_list else ("—", 0)

    color_dist = top_colors(filtered_df, color_cols, max_n=8)
    sector_dist = top_n_value_pct(filtered_df, sector_col, n=6)
    country_dist = top_n_value_pct(filtered_df, country_col, n=6)
    family_dist = top_n_value_pct(filtered_df, color_family_col, n=6)

    crosstab_html = '<div style="font-size:12px; color:var(--muted);">Not enough data for a cross-tab in this selection.</div>'
    top_families = [name for name, _ in top_n_value_pct(filtered_df, color_family_col, n=4)]
    top_sectors_ct = [name for name, _ in top_n_value_pct(filtered_df, sector_col, n=4)]
    if top_families and top_sectors_ct and color_family_col in filtered_df.columns and sector_col in filtered_df.columns:
        sub = filtered_df[
            filtered_df[color_family_col].astype(str).str.strip().isin(top_families)
            & filtered_df[sector_col].astype(str).str.strip().isin(top_sectors_ct)
        ]
        if not sub.empty:
            ct = pd.crosstab(
                sub[color_family_col].astype(str).str.strip(),
                sub[sector_col].astype(str).str.strip(),
                normalize="columns"
            ) * 100
            ct = ct.reindex(index=top_families, columns=top_sectors_ct, fill_value=0)

            head_cells = "".join(f'<div class="ct-cell ct-head">{s}</div>' for s in top_sectors_ct)
            rows_html = ""
            for fam in top_families:
                row_html = f'<div class="ct-cell ct-row-label">{fam}</div>'
                for sec in top_sectors_ct:
                    val = round(ct.loc[fam, sec]) if fam in ct.index and sec in ct.columns else 0
                    opacity = max(0.08, min(0.85, val / 100))
                    row_html += f'<div class="ct-cell"><div class="heat" style="background:rgba(99,102,241,{opacity}); width:100%; padding:5px 0;">{val}%</div></div>'
                rows_html += row_html
            crosstab_html = (
                f'<div class="crosstab" style="grid-template-columns: 130px repeat({len(top_sectors_ct)}, 1fr);">'
                f'<div class="ct-cell ct-head"></div>{head_cells}{rows_html}</div>'
            )

    html = (
        f'<div class="rr-kpis">'
        f'<div class="kpi"><div class="kpi-label">Logos</div><div class="kpi-value">{len(filtered_df)}</div><div class="kpi-sub">of {len(df)} total</div></div>'
        f'<div class="kpi"><div class="kpi-label">Countries</div><div class="kpi-value">{kpi_countries}</div><div class="kpi-sub">in current filter</div></div>'
        f'<div class="kpi"><div class="kpi-label">Top Color</div><div class="kpi-value">{top_color_name}</div><div class="kpi-sub">{top_color_pct}% of set</div></div>'
        f'<div class="kpi"><div class="kpi-label">Typical Complexity</div><div class="kpi-value">{top_complexity_name}</div><div class="kpi-sub">{top_complexity_pct}% of logos</div></div>'
        f'</div>'
        f'<div class="rr-charts">'
        f'<div class="chart-card"><div class="chart-title">Color Distribution</div>{_bar_rows_html(color_dist, with_swatch=True)}</div>'
        f'<div class="chart-card"><div class="chart-title">Sector Breakdown</div>{_bar_rows_html(sector_dist)}</div>'
        f'<div class="chart-card"><div class="chart-title">Country Breakdown</div>{_bar_rows_html(country_dist)}</div>'
        f'<div class="chart-card"><div class="chart-title">Color Family Breakdown</div>{_bar_rows_html(family_dist)}</div>'
        f'<div class="chart-card full-width-card"><div class="chart-title">Color Family &times; Sector (share within sector)</div>{crosstab_html}'
        f'<div class="rr-footnote">Darker cells = a color family makes up a larger share of that sector\'s logos. Recalculates live from your current filters.</div></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

# ===================== FIELD / CATEGORY DEFINITIONS =====================

brand_col = "Name"
img_col = "Logo"
type_of_logo_col = "Type of Logo"
primary_form_col = "Primary form (Visually Dominating Form)"
color_family_col = "Color Family"
sector_col = "Sector"
org_type_col = "Type of Organization"
country_col = "Country"
complexity_col = "Complexity (Low/ Mid/ High) (Intrinsic Visual Load)"
symmetry_col = "Symmetry"
symbolism_col = "Symbolism"
case_type_col = "Case Type"
type_class_col = "Type classification"
color_cols = ["Primary Colour", "Secondary Colour", "Colour", "Colour3", "Colour4", "Colour5"]
undertone_col = "Color Undertone"

# Every filterable field, grouped into the four sidebar categories.
FILTER_FIELDS = {
    "sector":       {"label": "Sector",              "col": sector_col,          "category": "org_location"},
    "org_type":     {"label": "Organization Type",    "col": org_type_col,        "category": "org_location", "case_insensitive": True},
    "country":      {"label": "Country",              "col": country_col,         "category": "org_location"},
    "type_logo":    {"label": "Type of Logo",         "col": type_of_logo_col,    "category": "logo_design"},
    "shape":        {"label": "Shape (Primary Form)", "col": primary_form_col,    "category": "logo_design"},
    "complexity":   {"label": "Complexity",           "col": complexity_col,      "category": "logo_design"},
    "symmetry":     {"label": "Symmetry",             "col": symmetry_col,        "category": "logo_design"},
    "color_family": {"label": "Color Scheme",          "col": color_family_col,    "category": "colors"},
    "undertone":    {"label": "Color Undertone",      "col": undertone_col,       "category": "colors"},
    "color":        {"label": "Color",                "col": color_cols,          "category": "colors", "multi_col": True},
    "case_type":    {"label": "Case Type",            "col": case_type_col,       "category": "type_style"},
    "type_class":   {"label": "Type Classification",  "col": type_class_col,      "category": "type_style"},
}

CATEGORIES = [
    ("org_location", "🏢 Organization & Location"),
    ("logo_design",  "📐 Logo Details & Design"),
    ("colors",       "🎨 Colors"),
    ("type_style",   "✍️ Type Style"),
]


def get_options(col_name):
    if col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
    return []


def get_options_multi(col_names):
    values = set()
    for col_name in col_names:
        if col_name in df.columns:
            for x in df[col_name].dropna().unique():
                x = str(x).strip()
                if x and x.lower() not in ["nan", "n/a"] and not x.startswith("#"):
                    values.add(x)
    return sorted(values)


def field_options(field_key):
    conf = FILTER_FIELDS[field_key]
    if conf.get("multi_col"):
        return get_options_multi(conf["col"])
    return get_options(conf["col"])


def ms_key(field_key):
    """Session-state key for this field's multiselect widget. The widget's
    own state *is* the applied filter — no separate temp/apply/applied
    bookkeeping needed, so picking a value filters instantly."""
    return f"ms__{field_key}"


def get_applied(field_key):
    return st.session_state.get(ms_key(field_key), [])


def set_applied(field_key, values):
    st.session_state[ms_key(field_key)] = values


def reset_all_filters():
    for field_key in FILTER_FIELDS:
        st.session_state[ms_key(field_key)] = []
    st.session_state.search_query = ""
    st.session_state.exact_color_match = False


# ===================== SESSION STATE INIT =====================

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "gallery"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "exact_color_match" not in st.session_state:
    st.session_state.exact_color_match = False
if "sort_mode" not in st.session_state:
    st.session_state.sort_mode = "Name A-Z"
if "_pending_action" not in st.session_state:
    st.session_state._pending_action = None

# Every multiselect needs an initial value in session_state before it's
# instantiated (only sets keys that don't exist yet, so it never clobbers
# a choice already made this session).
for _field_key in FILTER_FIELDS:
    if ms_key(_field_key) not in st.session_state:
        st.session_state[ms_key(_field_key)] = []

# Chip-removal / Clear-All live in the main content area, which renders AFTER
# the sidebar multiselects. Streamlit forbids writing to a widget's session_state
# key once that widget has been instantiated in the same run, so those actions
# only queue a pending action + rerun; it's applied HERE, before any multiselect
# widget exists for this run, which is safe.
_pending = st.session_state._pending_action
if _pending:
    st.session_state._pending_action = None
    if _pending[0] == "reset_all":
        reset_all_filters()
    elif _pending[0] == "remove_chip":
        _, _fkey, _val = _pending
        _remaining = [v for v in get_applied(_fkey) if v != _val]
        set_applied(_fkey, _remaining)

# ===================== SIDEBAR =====================

with st.sidebar:
    st.markdown('<div class="sidebar-app-title">Logo Landscape</div>', unsafe_allow_html=True)

    with st.container(key="toggle_row"):
        pill_col, sync_col = st.columns([5, 1], gap="small")
        with pill_col:
            with st.container(key="view_toggle_wrap"):
                view_selection = st.radio(
                    "", options=["Gallery", "Analytics"], horizontal=True,
                    label_visibility="collapsed",
                    index=0 if st.session_state.view_mode == "gallery" else 1,
                    key="view_mode_radio",
                )
        with sync_col:
            with st.container(key="sync_icon_wrap"):
                if st.button("", key="sync_btn", icon=":material/cloud_sync:", help="Sync latest data from Google Sheets"):
                    st.cache_data.clear()
                    st.rerun()

    new_view_mode = "gallery" if view_selection == "Gallery" else "analytics"
    if new_view_mode != st.session_state.view_mode:
        st.session_state.view_mode = new_view_mode
        st.rerun()

    st.markdown("---")

    with st.container(key="filters_header_row"):
        header_l, header_r = st.columns([5, 1])
        with header_l:
            st.markdown('<div class="filters-header-title">Filters</div>', unsafe_allow_html=True)
        with header_r:
            with st.container(key="reset_icon_wrap"):
                if st.button("↺", key="reset_filters_btn", help="Reset filters"):
                    st.session_state._pending_action = ("reset_all",)
                    st.rerun()

    st.text_input("⌕ Search organisation...", key="search_query", label_visibility="collapsed", placeholder="⌕ Search organisation...")

    # Plain multiselect per field, grouped into category expanders. Picking a
    # value filters immediately — there's no separate "Apply" step.
    for cat_key, cat_label in CATEGORIES:
        cat_fields = [fk for fk, conf in FILTER_FIELDS.items() if conf["category"] == cat_key]
        with st.expander(cat_label, expanded=False):
            for field_key in cat_fields:
                conf = FILTER_FIELDS[field_key]
                opts = field_options(field_key)
                if not opts:
                    continue
                st.multiselect(
                    conf["label"],
                    options=opts,
                    key=ms_key(field_key),
                    placeholder=f"Select {conf['label'].lower()}...",
                )

            if cat_key == "colors":
                st.checkbox("Exact match only (no extra colors)", key="exact_color_match")

# ===================== FILTER EXECUTION =====================

filtered_df = df.copy()

search_query = st.session_state.search_query
if search_query and brand_col in df.columns:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]

for field_key, conf in FILTER_FIELDS.items():
    values = get_applied(field_key)
    if not values:
        continue

    if conf.get("multi_col"):
        present_color_cols = [c for c in conf["col"] if c in filtered_df.columns]
        if present_color_cols:
            selected_set = set(v.strip() for v in values)

            def row_color_set(row, _cols=present_color_cols):
                vals = set()
                for c in _cols:
                    v = str(row.get(c, "")).strip()
                    if v and v.lower() not in ["nan", "n/a"] and not v.startswith("#"):
                        vals.add(v)
                return vals

            exact = st.session_state.exact_color_match
            keep_mask = filtered_df.apply(
                lambda r: row_color_set(r) == selected_set if exact else selected_set.issubset(row_color_set(r)),
                axis=1,
            )
            filtered_df = filtered_df[keep_mask]
        continue

    col = conf["col"]
    if col not in filtered_df.columns:
        continue
    if conf.get("case_insensitive"):
        filtered_df = filtered_df[filtered_df[col].astype(str).str.strip().str.lower().isin([v.strip().lower() for v in values])]
    else:
        filtered_df = filtered_df[filtered_df[col].astype(str).str.strip().isin([v.strip() for v in values])]

if st.session_state.sort_mode == "Name A-Z" and brand_col in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=brand_col, key=lambda s: s.astype(str).str.lower())
elif st.session_state.sort_mode == "Name Z-A" and brand_col in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=brand_col, key=lambda s: s.astype(str).str.lower(), ascending=False)

colormix = top_colors(filtered_df, color_cols, max_n=6)

# ===================== MAIN AREA — SUBTITLE BAR =====================

st.markdown(
    f'<div class="main-subtitle-bar">'
    f'<div class="main-subtitle-text">Visual Identity Research</div>'
    f'<div class="main-subtitle-count"><strong>{len(df)}</strong> Identities</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# Analytics is a separate page: render it and stop, so none of the Gallery-only
# code below (editorial summary, chips, palette bar, flip-card grid) executes.
if st.session_state.view_mode == "analytics":
    render_analytics_page(filtered_df, df, color_cols, sector_col, color_family_col, country_col, complexity_col)
    st.stop()

# ===================== EDITORIAL SUMMARY (collapsible) =====================

headline_label, headline_value, headline_pct = None, None, None
if not get_applied("color"):
    top = top_colors(filtered_df, color_cols, max_n=1)
    if top:
        headline_value, headline_pct, headline_label = top[0][0], top[0][1], "Dominant Color"

if headline_value is None:
    headline_label, headline_value, headline_pct = "Logos in view", str(len(filtered_df)), None

headline_desc = f"{headline_pct}% of selected logos share this trait." if headline_pct else f"Out of {len(df)} total dataset entries."

sector_top, sector_pct = top_value_pct(filtered_df, sector_col)
family_top, family_pct = top_value_pct(filtered_df, color_family_col)
country_names = (
    sorted(filtered_df[country_col].astype(str).str.strip().replace("", pd.NA).dropna().unique().tolist())
    if country_col in filtered_df.columns else []
)
country_nunique = len(country_names)

MAX_COUNTRY_TAGS = 10
country_tags_html = "".join(f'<span class="editorial-country-tag">{c}</span>' for c in country_names[:MAX_COUNTRY_TAGS])
if country_nunique > MAX_COUNTRY_TAGS:
    country_tags_html += f'<span class="editorial-country-tag">+{country_nunique - MAX_COUNTRY_TAGS} more</span>'

editorial_html = (
    f'<div class="editorial-wrap" style="border:none; margin-bottom:0; padding:0;">'
    f'<div class="editorial-hero">'
    f'<div class="editorial-eyebrow">{headline_label}</div>'
    f'<div class="editorial-number">{headline_value}</div>'
    f'<div class="editorial-desc">{headline_desc}</div>'
    f'</div>'
    f'<div class="editorial-list">'
    f'<div class="editorial-row"><div class="editorial-row-label">Filtered Logos</div><div class="editorial-row-value">{len(filtered_df)}</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Major Sector<span class="editorial-sub">{sector_top or "—"}</span></div><div class="editorial-row-value">{sector_pct}%</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Primary Color Scheme<span class="editorial-sub">{family_top or "—"}</span></div><div class="editorial-row-value">{family_pct}%</div></div>'
    f'<div class="editorial-row" style="flex-direction:column; align-items:flex-start; gap:0;">'
    f'<div style="display:flex; justify-content:space-between; width:100%; align-items:baseline;">'
    f'<div class="editorial-row-label">Countries Represented</div><div class="editorial-row-value">{country_nunique}</div>'
    f'</div>'
    f'<div class="editorial-country-tags">{country_tags_html}</div>'
    f'</div>'
    f'</div>'
    f'</div>'
)

palette_items_html = "".join([
    f'<div class="palette-item"><span class="palette-swatch" style="background:{color_to_hex(name)}"></span><span class="palette-name">{name}</span><span class="palette-pct">{pct}%</span></div>'
    for name, pct in colormix
]) if colormix else '<div style="font-size:12px; color:var(--muted);">No color data available</div>'

palette_bar_html = (
    f'<div class="palette-bar-container" style="margin-bottom:0; margin-top:16px;">'
    f'<div class="palette-title">Color Palette Breakdown</div>'
    f'<div class="palette-items">{palette_items_html}</div>'
    f'</div>'
)

with st.expander("Editorial Summary", expanded=True):
    st.markdown(editorial_html, unsafe_allow_html=True)
    st.markdown(palette_bar_html, unsafe_allow_html=True)

# ===================== SELECTED FILTER CHIPS + SORT =====================

chips = []  # list of (field_key, value)
for field_key in FILTER_FIELDS:
    for value in get_applied(field_key):
        chips.append((field_key, value))

with st.container(key="filters_summary_bar"):
    chip_col, sort_col = st.columns([4, 1])

    with chip_col:
        with st.container(key="chips_row"):
            if not chips:
                st.markdown('<span class="no-filters-text">No filters applied</span>', unsafe_allow_html=True)
            else:
                for field_key, value in chips:
                    if st.button(f"{value}  ✕", key=f"chip__{field_key}__{value}"):
                        st.session_state._pending_action = ("remove_chip", field_key, value)
                        st.rerun()
                if st.button("Clear All", key="clear_all_chips"):
                    st.session_state._pending_action = ("reset_all",)
                    st.rerun()

    with sort_col:
        st.selectbox("Sort", options=["Name A-Z", "Name Z-A"], key="sort_mode", label_visibility="collapsed")

st.markdown(f'<div class="result-count-text"><strong>{len(filtered_df)}</strong> Results</div>', unsafe_allow_html=True)

# CLICK-TO-FLIP CARDS USING NATIVE HTML <details>
# All cards share the same `name` attribute, which makes the browser treat
# them as one exclusive group — opening one automatically closes any other
# open card. Native HTML behavior, no JS needed. (Requires a modern browser:
# Chrome/Edge/Firefox recent versions, Safari 17+.)
cols_per_row = 3
cols = st.columns(cols_per_row, gap="large")

for idx, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[idx % cols_per_row]
    with col:
        b_name = str(row.get(brand_col, "Unknown Brand")).strip()
        raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
        img_url = transform_image_url(raw_img)

        img_html = f'<img src="{img_url}" alt="{b_name}" />' if (img_url and img_url.startswith("http")) else '<div style="color: #a0aec0; font-size: 12px;">📷 Image unavailable</div>'

        p_form = str(row.get(primary_form_col, "—")).strip()
        c_family = str(row.get(Primary Colour_col, "—")).strip()
        sector_val = str(row.get(sector_col, "—")).strip()
        cnt_val = str(row.get(country_col, "—")).strip()
        complexity_val = str(row.get(complexity_col, "—")).strip()
        symmetry_val = str(row.get(symmetry_col, "—")).strip()
        type_class = str(row.get(type_class_col, "—")).strip()
        symbolism_text = str(row.get(symbolism_col, "No symbolism recorded.")).strip()
        case_type_val = str(row.get(case_type_col, "—")).strip()

        card_html = (
            f'<details class="flip-card" name="logo-flip-group">'
            f'<summary>'
            f'<div class="flip-card-inner">'
            f'<div class="flip-card-front">'
            f'<div class="card-image-box">{img_html}</div>'
            f'<div class="card-front-content">'
            f'<div class="card-title">{b_name}</div>'
            f'<div class="card-meta-grid">'
            f'<div class="card-meta-item">Shape: <strong>{p_form}</strong></div>'
            f'<div class="card-meta-item">Sector: <strong>{sector_val}</strong></div>'
            f'<div class="card-meta-item">Color: <strong>{c_family}</strong></div>'
            f'<div class="card-meta-item">Country: <strong>{cnt_val}</strong></div>'
            f'</div>'
            f'<div class="flip-hint">Tap card to flip details ↺</div>'
            f'</div>'
            f'</div>'
            f'<div class="flip-card-back">'
            f'<div>'
            f'<div class="back-title">{b_name}</div>'
            f'<div class="back-detail-row">Complexity: <strong>{complexity_val}</strong></div>'
            f'<div class="back-detail-row">Symmetry: <strong>{symmetry_val}</strong></div>'
            f'<div class="back-detail-row">Case Type: <strong>{case_type_val}</strong></div>'
            f'<div class="back-detail-row">Type Class: <strong>{type_class}</strong></div>'
            f'</div>'
            f'<div>'
            f'<div style="font-size:11px; font-weight:700; color:var(--accent); margin-bottom:4px;">SYMBOLISM</div>'
            f'<div class="back-symbolism">{symbolism_text}</div>'
            f'</div>'
            f'</div>'
            f'</summary>'
            f'</details>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
