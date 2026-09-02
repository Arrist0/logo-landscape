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
    case_type_col = "Case Type"
    type_class_col = "Type classification"

    def get_options(col_name):
        if col_name in df.columns:
            return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
        return []

    search_query = st.text_input("⌕ Search organisation...", "")

    # FIRST SECTION - Organization & Location
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-section-title"> Organization & Location</div>', unsafe_allow_html=True)
    
    selected_sectors = st.multiselect("Sector:", options=get_options(sector_col), default=[], key="sectors")
    selected_org_types = st.multiselect("Organization Type:", options=get_options(org_type_col), default=[], key="org_types")
    selected_countries = st.multiselect("Country:", options=get_options(country_col), default=[], key="countries")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # SECOND SECTION - Logo Details & Design
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-section-title"> Logo Details & Design</div>', unsafe_allow_html=True)
    
    selected_logo_types = st.multiselect("Type of Logo:", options=get_options(type_of_logo_col), default=[], key="type_logo")
    selected_forms = st.multiselect("Shape (Primary Form):", options=get_options(primary_form_col), default=[], key="shapes")
    selected_families = st.multiselect("Color Family:", options=get_options(color_family_col), default=[], key="colors")
    selected_complexity = st.multiselect("Complexity:", options=get_options(complexity_col), default=[], key="complexity")
    selected_symmetry = st.multiselect("Symmetry:", options=get_options(symmetry_col), default=[], key="symmetry")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # THIRD SECTION - Type Style
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-section-title"> Type Style</div>', unsafe_allow_html=True)
    
    selected_case_types = st.multiselect("Case Type:", options=get_options(case_type_col), default=[], key="case_types")
    selected_type_class = st.multiselect("Type Classification:", options=get_options(type_class_col), default=[], key="type_class")
    
    st.markdown('</div>', unsafe_allow_html=True)

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

if selected_case_types and case_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[case_type_col].astype(str).str.strip().isin([s.strip() for s in selected_case_types])]

if selected_type_class and type_class_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_class_col].astype(str).str.strip().isin([s.strip() for s in selected_type_class])]

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
<div class="hero-title">The Language of Healthcare Logos.</div>
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
            with st.expander("Details"):
                st.write(f"**Complexity:** {complexity_val}")
                st.write(f"**Symmetry:** {symmetry_val}")
                st.write(f"**Case Type:** {case_type_val}")
                st.write(f"**Type Classification:** {type_class}")
                st.write("")
                st.write(f"**Symbolism:**")
                st.write(symbolism_text)
