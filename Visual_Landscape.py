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
  --accent: #2563eb;
}

/* Force Light Theme Canvas */
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

/* Logo Image Container */
.logo-image-box {
    height: 160px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
    border: 1px solid var(--line);
    border-radius: 10px;
    margin-bottom: 12px;
}

.logo-image-box img {
    max-height: 130px;
    max-width: 90%;
    object-fit: contain;
    transition: transform 0.35s ease;
}

.logo-image-box:hover img {
    transform: scale(1.06);
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

    df.columns = [re.sub(r'\s+', ' ', str(c)).strip() for c in df.columns]

    if "Name" in df.columns:
        df = df.dropna(subset=["Name"]).copy()
        df = df[df["Name"].astype(str).str.strip().ne("")].copy()

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

def transform_image_url(url_str):
    url_str = str(url_str).strip()
    if not url_str or url_str.lower() in ["nan", "n/a", "none"]:
        return ""
    if "drive.google.com" in url_str:
        match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]+)', url_str)
        if match:
            return f"https://lh3.googleusercontent.com/d/{match.group(1)}"
    return url_str

def normalize_text(text):
    return re.sub(r'\s+', ' ', str(text)).replace('&', 'and').strip().lower()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### Sync Data")
    if st.button("🔄 Refresh Google Sheets"):
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

# Robust matching for Organization Type
if selected_org_types and org_type_col in df.columns:
    norm_selected = [normalize_text(x) for x in selected_org_types]
    filtered_df = filtered_df[filtered_df[org_type_col].apply(lambda val: normalize_text(val) in norm_selected)]

if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).isin(selected_countries)]

if selected_complexity and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).isin(selected_complexity)]

if selected_symmetry and symmetry_col in df.columns:
    filtered_df = filtered_df[filtered_df[symmetry_col].astype(str).isin(selected_symmetry)]

# ----------------- MAIN CONTENT -----------------
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

# UNIFORM CARD GRID (3 COLUMNS)
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
            
            # 1. Render Image Box
            if img_url and img_url.startswith("http"):
                st.markdown(f'<div class="logo-image-box"><img src="{img_url}" alt="{b_name}" /></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="logo-image-box" style="color:#66635b; font-size:12px;">📷 Image unavailable</div>', unsafe_allow_html=True)
            
            # 2. Render Brand Name (Larger Font)
            st.markdown(f"### {b_name}")

            p_form = str(row.get(primary_form_col, "—")).strip()
            c_family = str(row.get(color_family_col, "—")).strip()
            sector_val = str(row.get(sector_col, "—")).strip()
            org_type_val = str(row.get(org_type_col, "—")).strip()
            cnt_val = str(row.get(country_col, "—")).strip()
            logo_type_val = str(row.get(type_of_logo_col, "—")).strip()
            complexity_val = str(row.get(complexity_col, "—")).strip()
            symbolism_text = str(row.get(symbolism_col, "No symbolism recorded.")).strip()

            # 3. BOX 1: Organization & Sector Container
            with st.container(border=True):
                st.caption("ORGANIZATION & SECTOR")
                st.markdown(f"**Org:** {org_type_val}")
                st.markdown(f"**Sector:** {sector_val} | **Country:** {cnt_val}")

            # 4. BOX 2: Visual Analysis Container
            with st.container(border=True):
                st.caption("VISUAL ANALYSIS")
                st.markdown(f"**Type:** {logo_type_val} | **Shape:** {p_form}")
                st.markdown(f"**Color:** {c_family} | **Complexity:** {complexity_val}")

            # 5. Symbolism Expander
            with st.expander("📋 View Symbolism & Rationale"):
                st.markdown(symbolism_text)
