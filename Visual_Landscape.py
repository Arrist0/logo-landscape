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
* {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

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

/* SYNC BUTTON - Square, Top Left, Premium Feel */
[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    height: 48px !important;
    border-radius: 8px !important;
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #2d3748 !important;
    border-color: var(--accent) !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3) !important;
    transform: translateY(-2px);
}

[data-testid="stSidebar"] div.stButton > button:active {
    transform: translateY(0px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
}

/* UNIFORM CARD CONTAINER - Fixed Size Grid */
.logo-card-wrapper {
    background-color: var(--card) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    height: 420px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.logo-card-wrapper:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.25) !important;
    border-color: var(--accent) !important;
    background-color: #1f2937 !important;
}

/* Image Container - Uniform Height */
.logo-image-box {
    height: 200px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border-bottom: 1.5px solid var(--line);
    overflow: hidden;
    position: relative;
}

.logo-image-box img {
    max-height: 160px;
    max-width: 90%;
    object-fit: contain;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo-card-wrapper:hover .logo-image-box img {
    transform: scale(1.08);
}

/* Card Content Area */
.card-content {
    padding: 16px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.card-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
    line-height: 1.3;
}

.card-meta {
    font-size: 12px;
    color: var(--muted);
    line-height: 1.5;
    margin-bottom: 8px;
}

.card-badges {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
}

.card-badge {
    font-size: 10px;
    padding: 4px 10px;
    border-radius: 4px;
    background-color: rgba(99, 102, 241, 0.15);
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

/* Inspector/Details Expander */
.details-expander {
    border-top: 1px solid var(--line);
    padding-top: 12px;
    margin-top: 12px;
    font-size: 11px;
}

.detail-row {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    padding: 6px 0;
    border-bottom: 1px solid rgba(160, 174, 192, 0.1);
}

.detail-label {
    color: var(--muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 9px;
}

.detail-value {
    color: #ffffff;
    font-weight: 500;
}

/* Results Header */
.results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--line);
}

.results-count {
    font-family: "Space Grotesk", sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
}

/* Sort Selector */
.stSelectbox {
    transition: all 0.3s ease;
}

.stSelectbox:hover {
    opacity: 0.8;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--bg);
}

[data-testid="stSidebar"] .sidebar-title {
    font-family: "Space Grotesk", sans-serif;
    font-weight: 700;
    color: var(--ink);
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 16px 0 12px 0;
}

/* Loading Animation */
@keyframes shimmer {
    0% {
        opacity: 0.6;
    }
    50% {
        opacity: 1;
    }
    100% {
        opacity: 0.6;
    }
}

.loading {
    animation: shimmer 2s infinite;
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

# SIDEBAR WITH SYNC BUTTON
with st.sidebar:
    st.markdown("### Sync Data")
    if st.button("🔄 Refresh Google Sheets", help="Click to sync latest data from Google Sheets"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Filters")

    # Column mappings
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
    font_type_col = "Font Type"
    font_weight_col = "Font Weight"
    type_class_col = "Type classification"

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

# Apply Filters
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

# MAIN CONTENT
st.markdown(f"""
<div class="topbar-container">
  <div>
    <h1 class="app-title">Logo Landscape</h1>
  </div>
  <div class="top-meta"><strong>{len(df)}</strong> Identities</div>
</div>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="hero-kicker">Visual Identity Research</div>
<div class="hero-title">The Design of Care & Innovation.</div>
<div class="hero-intro">
  Explore 165+ visual identities across the medical ecosystem: hospitals delivering care, research centers advancing knowledge, educational institutes training leaders, and tech companies solving problems—all through design.
</div>
""", unsafe_allow_html=True)

# RESULTS HEADER WITH SORT
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
            # Build card HTML
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
            
            # Card HTML
            card_html = f"""
            <div class="logo-card-wrapper fade-in">
                <div class="logo-image-box">
                    {img_html}
                </div>
                <div class="card-content">
                    <div>
                        <div class="card-title">{b_name}</div>
                        <div class="card-meta">
                            <strong>Shape:</strong> {p_form} | <strong>Color:</strong> {c_family}<br>
                            <strong>Sector:</strong> {sector_val} | <strong>Country:</strong> {cnt_val}
                        </div>
                    </div>
                </div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Expandable details
            with st.expander("📋 Details"):
                st.markdown(f"""
                <div class="details-expander">
                    <div class="detail-row">
                        <div class="detail-label">Complexity</div>
                        <div class="detail-value">{complexity_val}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Symmetry</div>
                        <div class="detail-value">{symmetry_val}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Type</div>
                        <div class="detail-value">{type_class}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Symbolism:**\n\n{symbolism_text}")
