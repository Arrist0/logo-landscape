import io
import re
import requests
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Logo Landscape — Visual Identity Research",
    page_icon="🎨",
    layout="wide"
)

# 2. Custom CSS (Uniform Card Sizes, Dark Theme & Smooth Animations)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
  --bg: #0f1117;
  --ink: #f7fafc;
  --muted: #a0aec0;
  --line: #2d3748;
  --card: #171923;
  --accent: #6366f1;
}

/* Global Reset & Dark Canvas */
.main { background-color: var(--bg); }
.stApp { background-color: var(--bg); color: var(--ink); font-family: "DM Sans", sans-serif; }

/* Top Header */
.topbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 25px;
}
.eyebrow {
    font-size: 11px;
    letter-spacing: 0.16em;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
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
    color: #ffffff;
    margin: 0 0 14px 0;
}
.hero-intro {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.6;
    max-width: 650px;
    margin-bottom: 25px;
}

/* Square Top-Left Sync Button Styling */
[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    height: 54px !important;
    border-radius: 10px !important;
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    color: #ffffff !important;
    font-size: 18px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #2d3748 !important;
    border-color: var(--accent) !important;
    transform: scale(1.02);
}

/* Uniform Card Structure & Smooth Hover Transitions */
div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    height: 380px !important; /* Fixed Uniform Height */
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease, border-color 0.25s ease !important;
}

div[data-testid="stVerticalBlock"] > div[style*="background-color"]:hover {
    transform: translateY(-6px) scale(1.015) !important;
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.5) !important;
    border-color: var(--accent) !important;
}

/* Image Frame Inside Card */
.img-container {
    height: 170px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border-bottom: 1px solid var(--line);
    overflow: hidden;
}
.img-container img {
    max-height: 130px;
    max-width: 85%;
    object-fit: contain;
    transition: transform 0.3s ease;
}
div[data-testid="stVerticalBlock"] > div[style*="background-color"]:hover .img-container img {
    transform: scale(1.06);
}

/* Inspector Table Styling */
.detail-table {
    display: grid;
    grid-template-columns: 1fr 1.4fr;
    border-top: 1px solid var(--line);
    margin-top: 8px;
}
.detail-row-label {
    padding: 6px 0;
    border-bottom: 1px solid var(--line);
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.detail-row-val {
    padding: 6px 0;
    border-bottom: 1px solid var(--line);
    font-size: 11px;
    color: #ffffff;
    font-weight: 500;
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
    st.error(f"Error loading live dataset: {e}")
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

# ----------------- SIDEBAR (SQUARE SYNC BUTTON + FILTERS) -----------------
# Top-Left Square Sync Button matching wireframe
if st.sidebar.button("🔄  Sync Sheet Data", help="Click to refresh live data from Google Sheets"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### FILTERS")

brand_col = "Name"
img_col = "Logo"
type_of_logo_col = "Type of Logo"
primary_form_col = "Primary form (Visually Dominating Form)"
style_inclination_col = "Visual Form inclination (First form we visually notice)"
color_family_col = "Color Family"
sector_col = "Sector"
org_type_col = "Type of Organization"
country_col = "Country"
complexity_col = "Complexity (Low/ Mid/ High) (Intrinsic Visual Load)"
symmetry_col = "Symmetry"
symbolism_col = "Symbolism"

font_type_col = "Font Type"
font_weight_col = "Font Weight"
case_type_col = "Case Type"
type_class_col = "Type classification"
letter_spacing_col = "Letter Spacing"

def get_options(col_name):
    if col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
    return []

search_query = st.sidebar.text_input("⌕ Search organisation...", "")

selected_logo_types = st.sidebar.multiselect("Type of Logo:", options=get_options(type_of_logo_col))
selected_forms = st.sidebar.multiselect("Shape (Primary Form):", options=get_options(primary_form_col))
selected_families = st.sidebar.multiselect("Color Family:", options=get_options(color_family_col))
selected_sectors = st.sidebar.multiselect("Sector:", options=get_options(sector_col))
selected_org_types = st.sidebar.multiselect("Organization Type:", options=get_options(org_type_col))
selected_countries = st.sidebar.multiselect("Country:", options=get_options(country_col))
selected_complexity = st.sidebar.multiselect("Complexity:", options=get_options(complexity_col))
selected_symmetry = st.sidebar.multiselect("Symmetry:", options=get_options(symmetry_col))

# Apply Filter Criteria
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

if selected_org_types and org_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[org_type_col].astype(str).isin(selected_org_types)]

if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).isin(selected_countries)]

if selected_complexity and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).isin(selected_complexity)]

if selected_symmetry and symmetry_col in df.columns:
    filtered_df = filtered_df[filtered_df[symmetry_col].astype(str).isin(selected_symmetry)]

# ----------------- TOPBAR -----------------
st.markdown(f"""
<div class="topbar-container">
  <div>
    <h1 class="app-title">Logo Landscape</h1>
  </div>
  <div class="top-meta"><strong>{len(df)}</strong> Identities</div>
</div>
""", unsafe_allow_html=True)

# ----------------- HERO SECTION -----------------
st.markdown("""
<div class="hero-kicker">Visual Identity Research</div>
<div class="hero-title">How Medical Institutions Communicate.</div>
<div class="hero-intro">
  A curated research database analyzing logo design patterns, color psychology, and brand characteristics across medical institutions.
</div>
""", unsafe_allow_html=True)

# ----------------- RESULTS HEAD & SORTING -----------------
head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.markdown(f"**{len(filtered_df)}** Results")

with head_col2:
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

# ----------------- UNIFORM CARD GRID DISPLAY -----------------
if filtered_df.empty:
    st.info("No logos match the selected criteria.")
else:
    cols_per_row = 3  # 3 columns layout matching your wireframe grid
    cols = st.columns(cols_per_row)
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % cols_per_row]
        with col:
            with st.container():
                # Logo Image Box
                raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
                img_url = transform_image_url(raw_img)
                
                if img_url and img_url.startswith("http"):
                    st.markdown(f'<div class="img-container"><img src="{img_url}" alt="Logo" /></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="img-container" style="background:#1a202c; color:#a0aec0; font-size:12px;">📷 Image Link Missing</div>', unsafe_allow_html=True)

                # Brand Title
                b_name = str(row.get(brand_col, "")).strip()
                st.subheader(b_name if b_name else "Unnamed Brand")

                # Core Metadata Badges
                p_form = str(row.get(primary_form_col, "N/A")).strip()
                c_family = str(row.get(color_family_col, "N/A")).strip()
                sector_val = str(row.get(sector_col, "N/A")).strip()
                cnt_val = str(row.get(country_col, "N/A")).strip()

                st.caption(f"**Shape:** {p_form} | **Color:** {c_family}")
                st.caption(f"**Sector:** {sector_val} | **Country:** {cnt_val}")
                
                # Dropdown Inspector for Full Identity Details
                with st.expander("Inspect Details"):
                    complexity_val = str(row.get(complexity_col, "N/A")).strip()
                    symmetry_val = str(row.get(symmetry_col, "N/A")).strip()
                    type_class = str(row.get(type_class_col, "N/A")).strip()
                    font_weight = str(row.get(font_weight_col, "N/A")).strip()
                    symbolism_text = str(row.get(symbolism_col, "No symbolism recorded.")).strip()

                    st.markdown(f"""
                    <div class="detail-table">
                      <div class="detail-row-label">Complexity</div><div class="detail-row-val">{complexity_val}</div>
                      <div class="detail-row-label">Symmetry</div><div class="detail-row-val">{symmetry_val}</div>
                      <div class="detail-row-label">Type Class</div><div class="detail-row-val">{type_class} ({font_weight})</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"**Symbolism:**\n\n{symbolism_text}")
