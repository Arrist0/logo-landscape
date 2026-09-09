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

# 2. Light Theme Default + Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* Light Theme DEFAULT */
:root {
  --bg: #ffffff;
  --card: #f8f9fa;
  --ink: #1a1a1a;
  --muted: #666666;
  --line: #e0e0e0;
  --accent: #6366f1;
}

* {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main { background-color: var(--bg); }
.stApp { 
  background-color: var(--bg);
  color: var(--ink);
  font-family: "DM Sans", sans-serif; 
}

/* Top Header */
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
    margin: 2px 0 0 0;
    color: var(--ink);
    font-weight: 700;
}

.top-meta {
    font-size: 13px;
    color: var(--muted);
}

/* Hero Section */
.hero-kicker {
    font-size: 12px;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 6px;
}

.hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(32px, 4vw, 50px);
    line-height: 1.05;
    letter-spacing: -0.03em;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 14px 0;
}

.hero-intro {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.6;
    max-width: 650px;
    margin-bottom: 25px;
}

/* PILL TOGGLE SWITCH */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    background-color: var(--card);
    border-radius: 30px;
    padding: 4px;
    border: 1.5px solid var(--line);
    display: inline-flex;
    gap: 0px;
}
div[data-testid="stRadio"] label {
    border-radius: 26px !important;
    padding: 8px 20px !important;
    background-color: transparent;
    cursor: pointer;
    margin: 0;
}
div[data-testid="stRadio"] label[data-checked="true"] {
    background-color: var(--accent) !important;
}
div[data-testid="stRadio"] label[data-checked="true"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] { margin-left: 0; }
div[data-testid="stRadio"] span[data-baseweb="radio"] { display: none; }


/* SYNC BUTTON */
[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    height: 48px !important;
    border-radius: 8px !important;
    background-color: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    color: var(--ink) !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #f0f0f0 !important;
    border-color: var(--accent) !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2) !important;
    transform: translateY(-2px);
}

/* FILTER BOXES - Rounded */
.stMultiSelect > div {
    background-color: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    transition: all 0.3s ease !important;
}

.stMultiSelect > div:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.15) !important;
}

.stSelectbox > div {
    background-color: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.15) !important;
}

.stTextInput > div > div > input {
    background-color: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
    padding: 10px 12px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.15) !important;
}

/* FILTER SECTION BOXES */
.filter-section {
    background-color: #fafbfc;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 14px;
}

.filter-section-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}

/* UNIFORM CARD CONTAINER */
.logo-card-wrapper {
    background-color: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    height: 350px !important;
    display: flex !important;
    flex-direction: column !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.logo-card-wrapper:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15) !important;
    border-color: var(--accent) !important;
    background-color: #f0f4ff !important;
}

/* Image Container */
.logo-image-box {
    height: 160px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border-bottom: 1.5px solid var(--line);
    overflow: hidden;
    position: relative;
}

.logo-image-box img {
    max-height: 130px;
    max-width: 90%;
    object-fit: contain;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo-card-wrapper:hover .logo-image-box img {
    transform: scale(1.08);
}

/* Card Content */
.card-content {
    padding: 10px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

.card-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 6px 0;
    line-height: 1.3;
}

.card-meta {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.5;
    margin: 0;
}

/* Results Header */
.results-count {
    font-family: "Space Grotesk", sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--ink);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg);
}

/* Smooth Fade In */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1117;
    --card: #171923;
    --ink: #f7fafc;
    --muted: #a0aec0;
    --line: #2d3748;
  }
  
  .main { background-color: var(--bg); }
  .stApp { background-color: var(--bg); color: var(--ink); }
  
  .filter-section {
    background-color: #1a202c;
    border-color: var(--line);
  }
  
  [data-testid="stSidebar"] div.stButton > button {
    background-color: var(--card) !important;
    border-color: var(--line) !important;
    color: var(--ink) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
  }
  
  [data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #2d3748 !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3) !important;
  }
}

/* ===== Editorial summary (main content, above the grid) ===== */
.editorial-wrap {
    display: grid;
    grid-template-columns: 1fr 1.3fr;
    gap: 36px;
    align-items: start;
    border: 1.5px solid var(--line);
    border-radius: 14px;
    padding: 26px 28px;
    margin-bottom: 26px;
    background: var(--card);
}

.editorial-hero {
    border-right: 1px solid var(--line);
    padding-right: 32px;
}

.editorial-eyebrow {
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 8px;
}

.editorial-number {
    font-family: "Space Grotesk", sans-serif;
    font-size: 52px;
    line-height: 1.0;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.02em;
}

.editorial-desc {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.6;
    margin-top: 10px;
    max-width: 260px;
}

.editorial-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 11px 0;
    border-bottom: 1px solid var(--line);
}

.editorial-row:last-child { border-bottom: none; padding-bottom: 0; }
.editorial-row:first-child { padding-top: 0; }

.editorial-row-label { font-size: 13.5px; color: var(--ink); }
.editorial-sub { color: var(--muted); font-size: 11.5px; display: block; margin-top: 2px; }
.editorial-row-value {
    font-family: "Space Grotesk", sans-serif;
    font-size: 17px;
    font-weight: 700;
    white-space: nowrap;
    margin-left: 12px;
}

@media (prefers-color-scheme: dark) {
    .editorial-wrap { background: #171923; border-color: #2d3748; }
    .editorial-hero { border-color: #2d3748; }
    .editorial-row { border-color: #2d3748; }
}

/* ===== Sidebar summary rail ===== */
.sidebar-rail {
    background: #fafbfc;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px;
    margin-top: 4px;
}

.sidebar-rail-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}

.ring-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

.ring-row:last-child { margin-bottom: 0; }

.ring {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ring-inner {
    width: 21px;
    height: 21px;
    border-radius: 50%;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 8px;
    font-weight: 700;
    color: var(--ink);
}

.ring-name { font-size: 12px; color: var(--ink); }

/* ===== Color Mix (inside the Editorial box on the Gallery page) ===== */
.editorial-colormix {
    margin-top: 24px;
}

.editorial-colormix-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
    margin-bottom: 12px;
}

.editorial-colormix-rings {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    align-items: center;
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
    background: #ffffff;
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

@media (prefers-color-scheme: dark) {
    .kpi, .chart-card { background: #171923; border-color: #2d3748; }
    .bar-track { background: #0f1117; border-color: #2d3748; }
    .crosstab .ct-cell { border-color: #2d3748; }
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
        # Some rows carry extra data (e.g. colors) on a "continuation" row directly
        # below the main entry, where Name is blank. Fold any such values up into
        # the parent row before dropping blank-Name rows, so nothing gets lost.
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

# Rough name -> swatch color, for the summary rings. Falls back to the app accent color
# for any name not in this list (hex-only entries in the sheet, unusual color names, etc.)
COLOR_HEX_MAP = {
    "black": "#1a1a1a", "white": "#e8e8e8", "blue": "#2451c9", "red": "#c0392b",
    "green": "#1e9e5a", "yellow": "#e8b923", "orange": "#e07b39", "purple": "#8e44ad",
    "pink": "#e75f95", "teal": "#159e96", "grey": "#9aa0a6", "gray": "#9aa0a6",
    "brown": "#8a5a3c", "navy": "#1f2a5e", "maroon": "#6e1f2a", "gold": "#c9a227",
    "silver": "#b8bcc2", "cyan": "#22b6c9", "magenta": "#c23aa0",
}

def color_to_hex(name):
    return COLOR_HEX_MAP.get(str(name).strip().lower(), "#6366f1")

def top_value_pct(dataframe, col_name):
    """Most common value in a column, and what % of the (non-empty) dataframe it covers."""
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

def top_colors(dataframe, color_cols_list, max_n=4):
    """Ranked (name, pct) pairs — counts each color once per logo (row), even if
    it appears in more than one color column on that row, so percentages can't exceed 100%."""
    counts = {}
    for _, row in dataframe.iterrows():
        row_colors = set()
        for c in color_cols_list:
            if c in dataframe.columns:
                v = str(row.get(c, "")).strip()
                # Ignoring blank, nan, n/a, and anything starting with a hashtag (hex)
                if v and v.lower() not in ["", "nan", "n/a"] and not v.startswith("#"):
                    row_colors.add(v)
        for v in row_colors:
            counts[v] = counts.get(v, 0) + 1
    total = len(dataframe) if len(dataframe) > 0 else 1
    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:max_n]
    return [(name, round(100 * count / total)) for name, count in ranked]

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

def render_analytics_page():
    """Detailed, filter-aware analytics dashboard — KPIs, distribution charts,
    and a Color Family x Sector cross-tab. All built as one flush-left HTML
    string (no loop-concatenated multi-line blocks) to avoid Streamlit's
    Markdown parser misreading indented fragments as code blocks."""

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

    # Color Family x Sector cross-tab (share within each sector), top 4 families x top 4 sectors
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
        f'<div class="chart-card"><div class="chart-title">Color Family Breakdown</div>{_bar_rows_html(top_n_value_pct(filtered_df, color_family_col, n=6))}</div>'
        f'<div class="chart-card full-width-card"><div class="chart-title">Color Family &times; Sector (share within sector)</div>{crosstab_html}'
        f'<div class="rr-footnote">Darker cells = a color family makes up a larger share of that sector\'s logos. Recalculates live from your current filters.</div></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### Sync Data")
    if st.button("🔄 Refresh Google Sheets", help="Click to sync latest data from Google Sheets"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("### Filters")

    # Column mappings
    brand_col = "Name"
    img_col = "Logo Source Link"
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

    def get_options(col_name):
        if col_name in df.columns:
            return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
        return []

    def get_options_multi(col_names):
        """Combine unique values across several columns into one option list."""
        values = set()
        for col_name in col_names:
            if col_name in df.columns:
                for x in df[col_name].dropna().unique():
                    x = str(x).strip()
                    # Ignore nan, n/a, and hex codes
                    if x and x.lower() not in ["nan", "n/a"] and not x.startswith("#"):
                        values.add(x)
        return sorted(values)

    search_query = st.text_input("⌕ Search organisation...", "")

    # FIRST SECTION - Organization & Location
    with st.expander("🏢 Organization & Location", expanded=True):
        selected_sectors = st.multiselect("Sector:", options=get_options(sector_col), default=[], key="sectors")
        selected_org_types = st.multiselect("Organization Type:", options=get_options(org_type_col), default=[], key="org_types")
        selected_countries = st.multiselect("Country:", options=get_options(country_col), default=[], key="countries")

    # SECOND SECTION - Logo Details & Design
    with st.expander("📐 Logo Details & Design", expanded=False):
        selected_logo_types = st.multiselect("Type of Logo:", options=get_options(type_of_logo_col), default=[], key="type_logo")
        selected_forms = st.multiselect("Shape (Primary Form):", options=get_options(primary_form_col), default=[], key="shapes")
        selected_complexity = st.multiselect("Complexity:", options=get_options(complexity_col), default=[], key="complexity")
        selected_symmetry = st.multiselect("Symmetry:", options=get_options(symmetry_col), default=[], key="symmetry")

    # THIRD SECTION - Colors
    with st.expander("🎨 Colors", expanded=False):
        selected_families = st.multiselect("Color Family:", options=get_options(color_family_col), default=[], key="colors_family")
        selected_undertones = st.multiselect("Color Undertone:", options=get_options(undertone_col), default=[], key="undertones")
        selected_colors = st.multiselect("Color:", options=get_options_multi(color_cols), default=[], key="colors_combined")
        exact_color_match = st.checkbox("Exact match only (no extra colors)", value=False, key="exact_color_match")

    # FOURTH SECTION - Type Style
    with st.expander("✍️ Type Style", expanded=False):
        selected_case_types = st.multiselect("Case Type:", options=get_options(case_type_col), default=[], key="case_types")
        selected_type_class = st.multiselect("Type Classification:", options=get_options(type_class_col), default=[], key="type_class")

# Apply Filters
filtered_df = df.copy()

if search_query and brand_col in df.columns:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]

if selected_logo_types and type_of_logo_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_of_logo_col].astype(str).str.strip().isin([s.strip() for s in selected_logo_types])]

if selected_forms and primary_form_col in df.columns:
    filtered_df = filtered_df[filtered_df[primary_form_col].astype(str).str.strip().isin([s.strip() for s in selected_forms])]

if selected_families and color_family_col in df.columns:
    filtered_df = filtered_df[filtered_df[color_family_col].astype(str).str.strip().isin([s.strip() for s in selected_families])]

if selected_sectors and sector_col in df.columns:
    filtered_df = filtered_df[filtered_df[sector_col].astype(str).str.strip().isin([s.strip() for s in selected_sectors])]

if selected_org_types and org_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[org_type_col].astype(str).str.strip().str.lower().isin([s.strip().lower() for s in selected_org_types])]

if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).str.strip().isin([s.strip() for s in selected_countries])]

if selected_complexity and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).str.strip().isin([s.strip() for s in selected_complexity])]

if selected_symmetry and symmetry_col in df.columns:
    filtered_df = filtered_df[filtered_df[symmetry_col].astype(str).str.strip().isin([s.strip() for s in selected_symmetry])]

if selected_colors:
    present_color_cols = [c for c in color_cols if c in df.columns]
    if present_color_cols:
        selected_set = set(s.strip() for s in selected_colors)

        def row_color_set(row):
            vals = set()
            for c in present_color_cols:
                v = str(row.get(c, "")).strip()
                if v and v.lower() not in ["nan", "n/a"] and not v.startswith("#"):
                    vals.add(v)
            return vals

        if exact_color_match:
            # Logo's full color set must match the selection exactly - no extra colors allowed
            keep_mask = filtered_df.apply(lambda r: row_color_set(r) == selected_set, axis=1)
        else:
            # Logo must contain all selected colors, but may have others too
            keep_mask = filtered_df.apply(lambda r: selected_set.issubset(row_color_set(r)), axis=1)

        filtered_df = filtered_df[keep_mask]

if selected_undertones and undertone_col in df.columns:
    filtered_df = filtered_df[filtered_df[undertone_col].astype(str).str.strip().isin([s.strip() for s in selected_undertones])]

if selected_case_types and case_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[case_type_col].astype(str).str.strip().isin([s.strip() for s in selected_case_types])]

if selected_type_class and type_class_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_class_col].astype(str).str.strip().isin([s.strip() for s in selected_type_class])]

# Color mix for the current filtered set — reused by the Editorial "Color Mix"
# rings below and available to the Analytics page too.
colormix = top_colors(filtered_df, color_cols, max_n=6)

# MAIN CONTENT
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "gallery"

topbar_title_col, topbar_toggle_col = st.columns([3, 1.6])
with topbar_title_col:
    st.markdown(f"""
<div class="topbar-container">
  <div>
    <h1 class="app-title">Logo Landscape</h1>
  </div>
  <div class="top-meta"><strong>{len(df)}</strong> Identities</div>
</div>
""", unsafe_allow_html=True)
with topbar_toggle_col:
    # Use a styled radio button to create the pill effect
    view_selection = st.radio(
        "View Mode",
        options=["🖼️ Gallery", "📊 Analytics"],
        horizontal=True,
        label_visibility="collapsed",
        index=0 if st.session_state.view_mode == "gallery" else 1
    )

    # Check if the selection changed and update session state
    if view_selection == "🖼️ Gallery" and st.session_state.view_mode != "gallery":
        st.session_state.view_mode = "gallery"
        st.rerun()
    elif view_selection == "📊 Analytics" and st.session_state.view_mode != "analytics":
        st.session_state.view_mode = "analytics"
        st.rerun()

if st.session_state.view_mode == "analytics":
    render_analytics_page()
    st.stop()

# HERO SECTION
st.markdown("""
<div class="hero-kicker">Visual Identity Research</div>
<div class="hero-title">How Medical Institutions Communicate.</div>
<div class="hero-intro">
  A curated research database analyzing logo design patterns, color psychology, and brand characteristics across 82 medical institutions in 6 countries.
</div>
""", unsafe_allow_html=True)

# EDITORIAL SUMMARY
headline_label = None
headline_value = None
headline_pct = None

if not selected_colors:
    top = top_colors(filtered_df, color_cols, max_n=1)
    if top:
        headline_value, headline_pct = top[0]
        headline_label = "Most common color"

if headline_value is None and not selected_sectors:
    val, pct = top_value_pct(filtered_df, sector_col)
    if val:
        headline_value, headline_pct = val, pct
        headline_label = "Most common sector"

if headline_value is None and not selected_families:
    val, pct = top_value_pct(filtered_df, color_family_col)
    if val:
        headline_value, headline_pct = val, pct
        headline_label = "Most common color family"

if headline_value is None and not selected_countries:
    val, pct = top_value_pct(filtered_df, country_col)
    if val:
        headline_value, headline_pct = val, pct
        headline_label = "Most common country"

if headline_value is None:
    headline_label = "Logos in view"
    headline_value = str(len(filtered_df))
    headline_pct = None

headline_desc = (
    f"{headline_pct}% of the {len(filtered_df)} logos currently shown share this."
    if headline_pct is not None else
    f"out of {len(df)} logos total in the dataset."
)

sector_top, sector_pct = top_value_pct(filtered_df, sector_col)
family_top, family_pct = top_value_pct(filtered_df, color_family_col)
complexity_top, complexity_pct = top_value_pct(filtered_df, complexity_col)
country_nunique = (
    filtered_df[country_col].astype(str).str.strip().replace("", pd.NA).dropna().nunique()
    if country_col in filtered_df.columns else 0
)

colormix_rings = "".join(
    f'<div class="ring-row"><div class="ring" style="background: conic-gradient({color_to_hex(name)} 0% {pct}%, #eeeeee {pct}% 100%);"><div class="ring-inner">{pct}%</div></div><div class="ring-name">{name}</div></div>'
    for name, pct in colormix
) if colormix else '<div style="font-size:12px; color:var(--muted);">No color data in this selection.</div>'

st.markdown(f"""
<div class="editorial-wrap">
    <div class="editorial-hero">
        <div class="editorial-eyebrow">{headline_label}</div>
        <div class="editorial-number">{headline_value}</div>
        <div class="editorial-desc">{headline_desc}</div>
        
        <div class="editorial-colormix">
            <div class="editorial-colormix-title">Color Mix</div>
            <div class="editorial-colormix-rings">{colormix_rings}</div>
        </div>
    </div>
    
    <div class="editorial-list">
        <div class="editorial-row">
            <div class="editorial-row-label">Results in view<span class="editorial-sub">of {len(df)} total logos</span></div>
            <div class="editorial-row-value">{len(filtered_df)}</div>
        </div>
        <div class="editorial-row">
            <div class="editorial-row-label">Leading sector<span class="editorial-sub">{sector_top or "—"}</span></div>
            <div class="editorial-row-value">{sector_pct}%</div>
        </div>
        <div class="editorial-row">
            <div class="editorial-row-label">Leading color family<span class="editorial-sub">{family_top or "—"}</span></div>
            <div class="editorial-row-value">{family_pct}%</div>
        </div>
        <div class="editorial-row">
            <div class="editorial-row-label">Countries represented</div>
            <div class="editorial-row-value">{country_nunique}</div>
        </div>
        <div class="editorial-row">
            <div class="editorial-row-label">Typical complexity<span class="editorial-sub">{complexity_top or "—"}</span></div>
            <div class="editorial-row-value">{complexity_pct}%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# RESULTS HEADER WITH SORT
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"<div class='results-count'>{len(filtered_df)} Results</div>", unsafe_allow_html=True)

with col2:
    sort_option = st.selectbox(
        "Sort Order",
        ["Name A–Z", "Original Order", "Name Z–A", "Country"],
        index=0,
        label_visibility="collapsed"
    )

if sort_option == "Name A–Z":
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=True)
elif sort_option == "Name Z–A":
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=False)
elif sort_option == "Country" and country_col in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=country_col, ascending=True)

st.write("")

# UNIFORM CARD GRID (3 COLUMNS)
if filtered_df.empty:
    st.info("No logos match the selected criteria. Try adjusting your filters!")
else:
    cols_per_row = 3
    cols = st.columns(cols_per_row, gap="large")
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % cols_per_row]
        
        with col:
            b_name = str(row.get(brand_col, "Unknown Brand")).strip()
            
            # Image handling
            raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
            img_url = transform_image_url(raw_img)
            
            img_html = ""
            if img_url and img_url.startswith("http"):
                img_html = f'<img src="{img_url}" alt="{b_name}" />'
            else:
                img_html = '<div style="color: #a0aec0; font-size: 12px;">📷 Image unavailable</div>'
            
            # Metadata
            p_form = str(row.get(primary_form_col, "—")).strip()
            c_family = str(row.get(color_family_col, "—")).strip()
            sector_val = str(row.get(sector_col, "—")).strip()
            cnt_val = str(row.get(country_col, "—")).strip()
            complexity_val = str(row.get(complexity_col, "—")).strip()
            symmetry_val = str(row.get(symmetry_col, "—")).strip()
            type_class = str(row.get(type_class_col, "—")).strip()
            symbolism_text = str(row.get(symbolism_col, "No symbolism recorded.")).strip()
            case_type_val = str(row.get(case_type_col, "—")).strip()
            
            # Card HTML
            card_html = f"""
            <div class="logo-card-wrapper fade-in">
                <div class="logo-image-box">
                    {img_html}
                </div>
                <div class="card-content">
                    <div class="card-title">{b_name}</div>
                    <div class="card-meta">
                        <strong>Shape:</strong> {p_form}<br>
                        <strong>Color:</strong> {c_family}<br>
                        <strong>Sector:</strong> {sector_val}<br>
                        <strong>Country:</strong> {cnt_val}
                    </div>
                </div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Expandable details
            with st.expander("📋 Details"):
                st.write(f"**Complexity:** {complexity_val}")
                st.write(f"**Symmetry:** {symmetry_val}")
                st.write(f"**Case Type:** {case_type_val}")
                st.write(f"**Type Classification:** {type_class}")
                st.write("")
                st.write(f"**Symbolism:**")
                st.write(symbolism_text)
