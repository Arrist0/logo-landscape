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

# 2. CSS with Reliable Hover Cards & Theme Mapping
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
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1117;
    --card: #171923;
    --ink: #f7fafc;
    --muted: #a0aec0;
    --line: #2d3748;
    --accent: #6366f1;
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

/* Pill Toggle */
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

/* Editorial Card */
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

/* Palette Bar */
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

/* Reliable Overlay Card Architecture */
.logo-card-container {
    position: relative;
    width: 100%;
    height: 340px;
    background-color: var(--card);
    border: 1.5px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 24px;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.logo-card-container:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 12px 24px rgba(99, 102, 241, 0.18);
}

.card-front {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}

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

.card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--card);
    padding: 18px;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.logo-card-container:hover .card-overlay {
    opacity: 1;
    visibility: visible;
}

.overlay-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--accent);
    border-bottom: 1px solid var(--line);
    padding-bottom: 6px;
    margin-bottom: 10px;
}

.overlay-detail-row {
    font-size: 12px;
    margin-bottom: 6px;
    color: var(--muted);
}

.overlay-detail-row strong { color: var(--ink); }

.overlay-symbolism {
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

/* Sidebar Styles */
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
    "black": "#1a1a1a", "white": "#e8e8e8", "blue": "#2451c9", "red": "#c0392b",
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

# SIDEBAR
with st.sidebar:
    st.markdown("### Sync Data")
    if st.button("🔄 Refresh Google Sheets", help="Click to sync latest data from Google Sheets"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("### Filters")

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
        values = set()
        for col_name in col_names:
            if col_name in df.columns:
                for x in df[col_name].dropna().unique():
                    x = str(x).strip()
                    if x and x.lower() not in ["nan", "n/a"] and not x.startswith("#"):
                        values.add(x)
        return sorted(values)

    search_query = st.text_input("⌕ Search organisation...", "")

    with st.expander("🏢 Organization & Location", expanded=True):
        selected_sectors = st.multiselect("Sector:", options=get_options(sector_col), default=[], key="sectors")
        selected_org_types = st.multiselect("Organization Type:", options=get_options(org_type_col), default=[], key="org_types")
        selected_countries = st.multiselect("Country:", options=get_options(country_col), default=[], key="countries")

    with st.expander("📐 Logo Details & Design", expanded=False):
        selected_logo_types = st.multiselect("Type of Logo:", options=get_options(type_of_logo_col), default=[], key="type_logo")
        selected_forms = st.multiselect("Shape (Primary Form):", options=get_options(primary_form_col), default=[], key="shapes")
        selected_complexity = st.multiselect("Complexity:", options=get_options(complexity_col), default=[], key="complexity")
        selected_symmetry = st.multiselect("Symmetry:", options=get_options(symmetry_col), default=[], key="symmetry")

    with st.expander("🎨 Colors", expanded=False):
        selected_families = st.multiselect("Color Family:", options=get_options(color_family_col), default=[], key="colors_family")
        selected_undertones = st.multiselect("Color Undertone:", options=get_options(undertone_col), default=[], key="undertones")
        selected_colors = st.multiselect("Color:", options=get_options_multi(color_cols), default=[], key="colors_combined")
        exact_color_match = st.checkbox("Exact match only (no extra colors)", value=False, key="exact_color_match")

    with st.expander("✍️ Type Style", expanded=False):
        selected_case_types = st.multiselect("Case Type:", options=get_options(case_type_col), default=[], key="case_types")
        selected_type_class = st.multiselect("Type Classification:", options=get_options(type_class_col), default=[], key="type_class")

# Filter execution
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
        keep_mask = filtered_df.apply(lambda r: row_color_set(r) == selected_set if exact_color_match else selected_set.issubset(row_color_set(r)), axis=1)
        filtered_df = filtered_df[keep_mask]

colormix = top_colors(filtered_df, color_cols, max_n=6)

# Main View Render
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "gallery"

topbar_title_col, topbar_toggle_col = st.columns([3, 1.4])
with topbar_title_col:
    st.markdown(f'<div class="topbar-container"><div><h1 class="app-title">Logo Landscape</h1></div><div class="top-meta"><strong>{len(df)}</strong> Identities</div></div>', unsafe_allow_html=True)

with topbar_toggle_col:
    view_selection = st.radio("View Mode", options=["🖼️ Gallery", "📊 Analytics"], horizontal=True, label_visibility="collapsed", index=0 if st.session_state.view_mode == "gallery" else 1)
    if view_selection == "🖼️ Gallery" and st.session_state.view_mode != "gallery":
        st.session_state.view_mode = "gallery"
        st.rerun()
    elif view_selection == "📊 Analytics" and st.session_state.view_mode != "analytics":
        st.session_state.view_mode = "analytics"
        st.rerun()

# HERO + EDITORIAL
st.markdown('<div class="hero-title">How Medical Institutions Communicate</div>', unsafe_allow_html=True)

headline_label, headline_value, headline_pct = None, None, None
if not selected_colors:
    top = top_colors(filtered_df, color_cols, max_n=1)
    if top: headline_value, headline_pct, headline_label = top[0][0], top[0][1], "Dominant Color"

if headline_value is None:
    headline_label, headline_value, headline_pct = "Logos in view", str(len(filtered_df)), None

headline_desc = f"{headline_pct}% of selected logos share this trait." if headline_pct else f"Out of {len(df)} total dataset entries."

sector_top, sector_pct = top_value_pct(filtered_df, sector_col)
family_top, family_pct = top_value_pct(filtered_df, color_family_col)
complexity_top, complexity_pct = top_value_pct(filtered_df, complexity_col)
country_nunique = filtered_df[country_col].astype(str).str.strip().replace("", pd.NA).dropna().nunique() if country_col in filtered_df.columns else 0

editorial_html = (
    f'<div class="editorial-wrap">'
    f'<div class="editorial-hero">'
    f'<div class="editorial-eyebrow">{headline_label}</div>'
    f'<div class="editorial-number">{headline_value}</div>'
    f'<div class="editorial-desc">{headline_desc}</div>'
    f'</div>'
    f'<div class="editorial-list">'
    f'<div class="editorial-row"><div class="editorial-row-label">Filtered Logos</div><div class="editorial-row-value">{len(filtered_df)}</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Leading Sector<span class="editorial-sub">{sector_top or "—"}</span></div><div class="editorial-row-value">{sector_pct}%</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Primary Color Family<span class="editorial-sub">{family_top or "—"}</span></div><div class="editorial-row-value">{family_pct}%</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Countries Represented</div><div class="editorial-row-value">{country_nunique}</div></div>'
    f'</div>'
    f'</div>'
)
st.markdown(editorial_html, unsafe_allow_html=True)

# PALETTE STRIP
palette_items_html = "".join([
    f'<div class="palette-item"><span class="palette-swatch" style="background:{color_to_hex(name)}"></span><span class="palette-name">{name}</span><span class="palette-pct">{pct}%</span></div>'
    for name, pct in colormix
]) if colormix else '<div style="font-size:12px; color:var(--muted);">No color data available</div>'

palette_bar_html = (
    f'<div class="palette-bar-container">'
    f'<div class="palette-title">Color Palette Breakdown</div>'
    f'<div class="palette-items">{palette_items_html}</div>'
    f'</div>'
)
st.markdown(palette_bar_html, unsafe_allow_html=True)

# RELIABLE GRID CARDS WITH OVERLAY REVEAL
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
        c_family = str(row.get(color_family_col, "—")).strip()
        sector_val = str(row.get(sector_col, "—")).strip()
        cnt_val = str(row.get(country_col, "—")).strip()
        complexity_val = str(row.get(complexity_col, "—")).strip()
        symmetry_val = str(row.get(symmetry_col, "—")).strip()
        type_class = str(row.get(type_class_col, "—")).strip()
        symbolism_text = str(row.get(symbolism_col, "No symbolism recorded.")).strip()
        case_type_val = str(row.get(case_type_col, "—")).strip()

        card_html = (
            f'<div class="logo-card-container">'
            f'<div class="card-front">'
            f'<div class="card-image-box">{img_html}</div>'
            f'<div class="card-front-content">'
            f'<div class="card-title">{b_name}</div>'
            f'<div class="card-meta-grid">'
            f'<div class="card-meta-item">Shape: <strong>{p_form}</strong></div>'
            f'<div class="card-meta-item">Sector: <strong>{sector_val}</strong></div>'
            f'<div class="card-meta-item">Color: <strong>{c_family}</strong></div>'
            f'<div class="card-meta-item">Country: <strong>{cnt_val}</strong></div>'
            f'</div>'
            f'</div>'
            f'</div>'
            f'<div class="card-overlay">'
            f'<div>'
            f'<div class="overlay-title">{b_name}</div>'
            f'<div class="overlay-detail-row">Complexity: <strong>{complexity_val}</strong></div>'
            f'<div class="overlay-detail-row">Symmetry: <strong>{symmetry_val}</strong></div>'
            f'<div class="overlay-detail-row">Case Type: <strong>{case_type_val}</strong></div>'
            f'<div class="overlay-detail-row">Type Class: <strong>{type_class}</strong></div>'
            f'</div>'
            f'<div>'
            f'<div style="font-size:11px; font-weight:700; color:var(--accent); margin-bottom:4px;">SYMBOLISM</div>'
            f'<div class="overlay-symbolism">{symbolism_text}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
