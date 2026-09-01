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

# 2. Theme Detection & Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* CSS Variables for Light/Dark Theme */
:root {
  --bg-light: #ffffff;
  --bg-dark: #0f1117;
  --card-light: #f8f9fa;
  --card-dark: #171923;
  --ink-light: #1a1a1a;
  --ink-dark: #f7fafc;
  --muted-light: #666666;
  --muted-dark: #a0aec0;
  --line-light: #e0e0e0;
  --line-dark: #2d3748;
  --accent: #6366f1;
}

/* Global Reset & Dark Canvas by default */
* {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main { 
  background-color: var(--bg-dark);
}

.stApp { 
  background-color: var(--bg-dark);
  color: var(--ink-dark);
  font-family: "DM Sans", sans-serif; 
}

/* Light Theme Detection */
@media (prefers-color-scheme: light) {
  .main { background-color: var(--bg-light); }
  .stApp { 
    background-color: var(--bg-light);
    color: var(--ink-light);
  }
  .topbar-container { border-bottom-color: var(--line-light); }
  h1.app-title { color: var(--ink-light); }
  .hero-intro { color: var(--muted-light); }
  .top-meta { color: var(--muted-light); }
  .eyebrow, .hero-kicker { color: var(--muted-light); }
  .results-count { color: var(--ink-light); }
  .card-title { color: var(--ink-light); }
  .card-meta { color: var(--muted-light); }
  .logo-card-wrapper {
    background-color: var(--card-light) !important;
    border-color: var(--line-light) !important;
  }
  .logo-card-wrapper:hover {
    background-color: #f0f0f0 !important;
  }
  [data-testid="stSidebar"] { background-color: var(--bg-light) !important; }
  [data-testid="stSidebar"] div.stButton > button {
    background-color: var(--card-light) !important;
    border-color: var(--line-light) !important;
    color: var(--ink-light) !important;
  }
  [data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #e0e0e0 !important;
    border-color: var(--accent) !important;
  }
  .stMultiSelect > div { background-color: var(--card-light) !important; }
  .stSelectbox > div { background-color: var(--card-light) !important; }
  .stTextInput > div > div > input {
    background-color: var(--card-light) !important;
    color: var(--ink-light) !important;
    border-color: var(--line-light) !important;
  }
}

/* Dark Theme (Default) */
.main { background-color: var(--bg-dark); }
.stApp { background-color: var(--bg-dark); color: var(--ink-dark); }

/* Top Header */
.topbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid var(--line-dark);
    margin-bottom: 25px;
}

h1.app-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 28px;
    margin: 2px 0 0 0;
    color: var(--ink-dark);
    font-weight: 700;
}

.top-meta {
    font-size: 13px;
    color: var(--muted-dark);
}

/* Hero Section */
.hero-kicker {
    font-size: 12px;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: var(--muted-dark);
    text-transform: uppercase;
    margin-bottom: 6px;
}

.hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(32px, 4vw, 50px);
    line-height: 1.05;
    letter-spacing: -0.03em;
    font-weight: 700;
    color: var(--ink-dark);
    margin: 0 0 14px 0;
}

.hero-intro {
    color: var(--muted-dark);
    font-size: 15px;
    line-height: 1.6;
    max-width: 650px;
    margin-bottom: 25px;
}

/* SYNC BUTTON */
[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    height: 48px !important;
    border-radius: 8px !important;
    background-color: var(--card-dark) !important;
    border: 1px solid var(--line-dark) !important;
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

/* FILTER DROPDOWNS - Styled Multiselect & Selectbox */
.stMultiSelect > div {
    background-color: var(--card-dark) !important;
    border: 1.5px solid var(--line-dark) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    transition: all 0.3s ease !important;
}

.stMultiSelect > div:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.2) !important;
}

.stSelectbox > div {
    background-color: var(--card-dark) !important;
    border: 1.5px solid var(--line-dark) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.2) !important;
}

.stTextInput > div > div > input {
    background-color: var(--card-dark) !important;
    border: 1.5px solid var(--line-dark) !important;
    border-radius: 10px !important;
    color: var(--ink-dark) !important;
    padding: 10px 12px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.2) !important;
}

/* UNIFORM CARD CONTAINER - NO EXTRA SPACE */
.logo-card-wrapper {
    background-color: var(--card-dark) !important;
    border: 1.5px solid var(--line-dark) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    height: 380px !important;
    display: flex !important;
    flex-direction: column !important;
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
    height: 180px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border-bottom: 1.5px solid var(--line-dark);
    overflow: hidden;
    position: relative;
}

.logo-image-box img {
    max-height: 140px;
    max-width: 90%;
    object-fit: contain;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo-card-wrapper:hover .logo-image-box img {
    transform: scale(1.08);
}

/* Card Content - NO PADDING BLOAT */
.card-content {
    padding: 12px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.card-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--ink-dark);
    margin: 0 0 6px 0;
    line-height: 1.3;
}

.card-meta {
    font-size: 11px;
    color: var(--muted-dark);
    line-height: 1.4;
    margin-bottom: 0;
}

/* Details Button - Compact */
.details-btn {
    font-size: 11px;
    padding: 6px 8px !important;
    margin-top: 8px !important;
    border-radius: 6px !important;
    background-color: rgba(99, 102, 241, 0.1) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    transition: all 0.2s ease !important;
}

.details-btn:hover {
    background-color: rgba(99, 102, 241, 0.2) !important;
}

/* Results Header */
.results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--line-dark);
}

.results-count {
    font-family: "Space Grotesk", sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--ink-dark);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg-dark);
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

    selected_logo_types = st.multiselect("Type of Logo:", options=get_options(type_of_logo_col), default=[])
    selected_forms = st.multiselect("Shape (Primary Form):", options=get_options(primary_form_col), default=[])
    selected_families = st.multiselect("Color Family:", options=get_options(color_family_col), default=[])
    selected_sectors = st.multiselect("Sector:", options=get_options(sector_col), default=[])
    selected_org_types = st.multiselect("Organization Type:", options=get_options(org_type_col), default=[])
    selected_countries = st.multiselect("Country:", options=get_options(country_col), default=[])
    selected_complexity = st.multiselect("Complexity:", options=get_options(complexity_col), default=[])
    selected_symmetry = st.multiselect("Symmetry:", options=get_options(symmetry_col), default=[])

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

# HERO SECTION (From Reference Image)
st.markdown("""
<div class="hero-kicker">Visual Identity Research</div>
<div class="hero-title">The Language Of Healthcare Logos.</div>
<div class="hero-intro">
  A curated research database analyzing logo design patterns, color psychology, and brand characteristics across 82 medical institutions in 6 countries.
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

# UNIFORM CARD GRID (3 COLUMNS) - NO EXTRA SPACE
if filtered_df.empty:
    st.info("No logos match the selected criteria.")
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
            
            # Card HTML - COMPACT, NO EXTRA SPACE
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
                **Complexity:** {complexity_val}  
                **Symmetry:** {symmetry_val}  
                **Type:** {type_class}  
                
                **Symbolism:**  
                {symbolism_text}
                """)
