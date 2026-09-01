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

# 2. Light Theme Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --bg-light: #f6f5f0;
  --card-bg: #ffffff;
  --ink: #171717;
  --muted: #66635b;
  --line: #e2dfd7;
  --box-sub: #f8f7f4;
  --accent: #2563eb;
}

/* Force Light Canvas */
.main, .stApp { 
  background-color: var(--bg-light) !important; 
  color: var(--ink) !important;
  font-family: "DM Sans", sans-serif !important; 
}

/* Header & Hero */
.topbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0 18px 0;
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

.hero-kicker {
    font-size: 11px;
    letter-spacing: 0.16em;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 6px;
}

.hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(32px, 4vw, 48px);
    line-height: 1.05;
    letter-spacing: -0.03em;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 12px 0;
}

.hero-intro {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.6;
    max-width: 650px;
    margin-bottom: 25px;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #faf9f6 !important;
    border-right: 1px solid var(--line) !important;
}

[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    height: 44px !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    border: 1px solid var(--line) !important;
    color: var(--ink) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background-color: #f0f4ff !important;
}

/* Tight Uniform Card Layout */
.logo-card-wrapper {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    margin-bottom: 20px !important;
}

.logo-card-wrapper:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 24px rgba(0,0,0,0.08) !important;
    border-color: #b0ad9e !important;
}

/* Image Box */
.logo-image-box {
    height: 170px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border-bottom: 1px solid var(--line);
}

.logo-image-box img {
    max-height: 135px;
    max-width: 90%;
    object-fit: contain;
}

/* Card Content & Bigger Typography */
.card-content {
    padding: 16px;
}

.card-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 15px; /* Larger Title */
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 12px 0;
    line-height: 1.3;
}

/* Two Separate Attribute Boxes */
.meta-box {
    background-color: var(--box-sub);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
}

.meta-box-header {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 4px;
}

.meta-box-text {
    font-size: 12px; /* Larger Metadata Font */
    color: var(--ink);
    line-height: 1.45;
}

.results-count {
    font-family: "Space Grotesk", sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--ink);
}
</style>
""", unsafe_allow_html=True)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=2)
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

    # Clean whitespace in column headers
    df.columns = [re.sub(r'\s+', ' ', str(c)).strip() for c in df.columns]

    if "Name" in df.columns:
        df = df.dropna(subset=["Name"]).copy()
        df = df[df["Name"].astype(str).str.strip().ne("")].copy()

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading live dataset: {e}")
    st.stop()

# Transform Google Drive links directly to image URLs
def transform_image_url(url_str):
    url_str = str(url_str).strip()
    if not url_str or url_str.lower() in ["nan", "n/a", "none"]:
        return ""
    if "drive.google.com" in url_str:
        match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]+)', url_str)
        if match:
            return f"https://lh3.googleusercontent.com/d/{match.group(1)}"
    return url_str

# Clean strings for robust matching (Fixes Education & Research Center match issue)
def normalize_text(text):
    return re.sub(r'\s+', ' ', str(text)).replace('&', 'and').strip().lower()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### Sync Data")
    if st.button("🔄 Refresh Google Sheets", help="Click to sync latest data"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Filters")

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

    def get_options(col_name):
        if col_name in df.columns:
            return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
        return []

    search_query = st.text_input("⌕ Search organisation...", "")

    selected_logo_types = st.multiselect("Type of Logo:", options=get_options(type_of_logo_col))
    selected_forms = st.multiselect("Shape (Primary Form):", options=get_options(primary_form_col))
    selected_families = st.multiselect("Color Family:", options=get_options(color_family_col))
    selected_sectors = st.multiselect("Sector:", options=get_options(sector_col))
    selected_org_types = st.multiselect("Organization Type:", options=get_options(org_type_col))
    selected_countries = st.multiselect("Country:", options=get_options(country_col))
    selected_complexity = st.multiselect("Complexity:", options=get_options(complexity_col))
    selected_symmetry = st.multiselect("Symmetry:", options=get_options(symmetry_col))

# Filtering Logic
filtered_df = df.copy()

if search_query and brand_col in df.columns:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]

if selected_logo_types and type_of_logo_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_of_logo_col].astype(str).isin(selected_logo_types)]

if selected_forms and primary_form_col in df.columns:
    filtered_df = filtered_df[filtered_df[primary_form_col].astype(str).isin(selected_forms)]

if selected_families and color_family_col in df.columns:
    filtered_df = filtered_df[filtered_df[color_family_col].astype(str).isin(selected_families)]

if selected_sectors and sector_col in df.columns:
    filtered_df = filtered_df[filtered_df[sector_col].astype(str).isin(selected_sectors)]

# Robust matching for Organization Type (handles & vs and & trailing spaces)
if selected_org_types and org_type_col in df.columns:
    norm_selected = [normalize_text(x) for x in selected_org_types]
    filtered_df = filtered_df[filtered_df[org_type_col].apply(lambda val: normalize_text(val) in norm_selected)]

if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).isin(selected_countries)]

if selected_complexity and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).isin(selected_complexity)]

if selected_symmetry and symmetry_col in df.columns:
    filtered_df = filtered_df[filtered_df[symmetry_col].astype(str).isin(selected_symmetry)]

# ----------------- MAIN LAYOUT -----------------
st.markdown(f"""
<div class="topbar-container">
  <div>
    <h1 class="app-title">Logo Landscape</h1>
  </div>
  <div style="color: var(--muted); font-size: 13px;"><strong>{len(df)}</strong> Identities</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-kicker">Visual Identity Research</div>
<div class="hero-title">The Language Of Healthcare Logos.</div>
<div class="hero-intro">
  A curated research database analyzing logo design patterns, color psychology, and brand characteristics across medical institutions.
</div>
""", unsafe_allow_html=True)

# Results Header with Sort Options
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"<div class='results-count'>{len(filtered_df)} Results</div>", unsafe_allow_html=True)

with col2:
    sort_option = st.selectbox(
        "Sort Order",
        ["Original Order", "Name A–Z", "Name Z–A", "Country"],
        label_visibility="collapsed"
    )

if sort_option == "Name A–Z":
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=True)
elif sort_option == "Name Z–A":
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=False)
elif sort_option == "Country" and country_col in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=country_col, ascending=True)

st.write("")

# UNIFORM TIGHT CARD GRID (3 COLUMNS)
if filtered_df.empty:
    st.info("No logos match the selected criteria.")
else:
    cols_per_row = 3
    cols = st.columns(cols_per_row, gap="large")
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % cols_per_row]
        
        with col:
            b_name = str(row.get(brand_col, "Unknown Brand")).strip()
            raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
            img_url = transform_image_url(raw_img)
            
            if img_url and img_url.startswith("http"):
                img_html = f'<img src="{img_url}" alt="{b_name}" />'
            else:
                img_html = '<div style="color: #a0aec0; font-size: 12px;">📷 Image unavailable</div>'
            
            p_form = str(row.get(primary_form_col, "—")).strip()
            c_family = str(row.get(color_family_col, "—")).strip()
            sector_val = str(row.get(sector_col, "—")).strip()
            org_type_val = str(row.get(org_type_col, "—")).strip()
            cnt_val = str(row.get(country_col, "—")).strip()
            logo_type_val = str(row.get(type_of_logo_col, "—")).strip()
            complexity_val = str(row.get(complexity_col, "—")).strip()
            symmetry_val = str(row.get(symmetry_col, "—")).strip()
            symbolism_text = str(row.get(symbolism_col, "No symbolism recorded.")).strip()
            
            # Card HTML with 2 Primary Sub-Boxes
            card_html = f"""
            <div class="logo-card-wrapper">
                <div class="logo-image-box">
                    {img_html}
                </div>
                <div class="card-content">
                    <div class="card-title">{b_name}</div>
                    
                    <!-- BOX 1: Organization & Sector -->
                    <div class="meta-box">
                        <div class="meta-box-header">Organization & Sector</div>
                        <div class="meta-box-text">
                            <strong>Org:</strong> {org_type_val}<br>
                            <strong>Sector:</strong> {sector_val} | <strong>Country:</strong> {cnt_val}
                        </div>
                    </div>

                    <!-- BOX 2: Visual & Form Details -->
                    <div class="meta-box">
                        <div class="meta-box-header">Visual Analysis</div>
                        <div class="meta-box-text">
                            <strong>Type:</strong> {logo_type_val} | <strong>Shape:</strong> {p_form}<br>
                            <strong>Color:</strong> {c_family} | <strong>Complexity:</strong> {complexity_val}
                        </div>
                    </div>
                </div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Expandable Details for Symbolism
            with st.expander("📋 View Symbolism & Rationale"):
                st.markdown(f"**Symbolism:**\n\n{symbolism_text}")
