import io
import re
import requests
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Logo Landscape — Visual Identity Research Explorer",
    page_icon="🎨",
    layout="wide"
)

# 2. Inject Dark CSS based on your stylesheet structure
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
  --bg: #0f1117;
  --ink: #f7fafc;
  --muted: #a0aec0;
  --line: #2d3748;
  --card: #171923;
  --card-hover: #1a202c;
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
    padding: 18px 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 30px;
}
.eyebrow, .kicker {
    font-size: 11px;
    letter-spacing: 0.16em;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
}
h1.app-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 26px;
    margin: 4px 0 0 0;
    color: var(--ink);
    font-weight: 700;
}
.top-meta {
    font-size: 13px;
    color: var(--muted);
}
.top-meta span {
    color: #ffffff;
    font-weight: 700;
}

/* Hero Section & Stat Boxes */
.hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(32px, 4vw, 54px);
    line-height: 1.05;
    letter-spacing: -0.03em;
    font-weight: 700;
    color: #ffffff;
    margin: 10px 0 16px 0;
}
.hero-title em {
    font-style: normal;
    color: #718096;
}
.intro {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.6;
    max-width: 550px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1px;
    background: var(--line);
    border: 1px solid var(--line);
    border-radius: 8px;
    overflow: hidden;
}
.stat-item {
    background: var(--card);
    padding: 24px;
    text-align: center;
}
.stat-item b {
    display: block;
    font-family: "Space Grotesk", sans-serif;
    font-size: 34px;
    color: #ffffff;
}
.stat-item span {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Detail Section Table Styling */
.detail-table {
    display: grid;
    grid-template-columns: 1fr 1.4fr;
    border-top: 1px solid var(--line);
    margin-top: 10px;
}
.detail-row-label {
    padding: 8px 0;
    border-bottom: 1px solid var(--line);
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.detail-row-val {
    padding: 8px 0;
    border-bottom: 1px solid var(--line);
    font-size: 12px;
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
    st.error(f"Error loading data: {e}")
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

# ----------------- TOPBAR -----------------
st.markdown(f"""
<div class="topbar-container">
  <div>
    <div class="eyebrow">VISUAL IDENTITY RESEARCH</div>
    <h1 class="app-title">Logo Landscape</h1>
  </div>
  <div class="top-meta"><span>{len(df)}</span> identities</div>
</div>
""", unsafe_allow_html=True)

# ----------------- HERO & STATS -----------------
hero_col, stat_col = st.columns([1.5, 1])

with hero_col:
    st.markdown("""
    <div>
      <p class="kicker">EXPLORE THE DATASET</p>
      <div class="hero-title">165+ visual identities.<br><em>One searchable research space.</em></div>
      <p class="intro">Filter, compare and inspect the visual characteristics captured during logo research.</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col:
    govt_count = len(df[df['Sector'].astype(str).str.contains('Govt', case=False, na=False)]) if 'Sector' in df else 0
    pvt_count = len(df[df['Sector'].astype(str).str.contains('Pvt', case=False, na=False)]) if 'Sector' in df else 0
    st.markdown(f"""
    <div class="stats-grid">
      <div class="stat-item"><b>{govt_count}</b><span>Govt. Institutions</span></div>
      <div class="stat-item"><b>{pvt_count}</b><span>Private Bodies</span></div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.markdown("### FILTERS")

if st.sidebar.button("Reset Filters"):
    st.cache_data.clear()
    st.rerun()

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

# Typography Columns
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

if selected_org_types and org_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[org_type_col].astype(str).isin(selected_org_types)]

if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).isin(selected_countries)]

if selected_complexity and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).isin(selected_complexity)]

if selected_symmetry and symmetry_col in df.columns:
    filtered_df = filtered_df[filtered_df[symmetry_col].astype(str).isin(selected_symmetry)]

# ----------------- SORTING & RESULTS HEADER -----------------
head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.markdown(f"**{len(filtered_df)}** results")

with head_col2:
    sort_option = st.selectbox(
        "Sort Order",
        ["Original order", "Name A–Z", "Name Z–A", "Country"],
        label_visibility="collapsed"
    )

if sort_option == "Name A–Z":
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=True)
elif sort_option == "Name Z–A":
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=False)
elif sort_option == "Country" and country_col in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=country_col, ascending=True)

# ----------------- GRID DISPLAY -----------------
if filtered_df.empty:
    st.info("No logos match the selected filter criteria.")
else:
    cols_per_row = 4
    cols = st.columns(cols_per_row)
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % cols_per_row]
        with col:
            with st.container():
                # Logo Image Box
                raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
                img_url = transform_image_url(raw_img)
                
                if img_url and img_url.startswith("http"):
                    st.image(img_url, use_container_width=True)
                else:
                    st.warning("📷 Image Link Missing")

                # Name
                b_name = str(row.get(brand_col, "")).strip()
                st.subheader(b_name if b_name else "Unnamed Brand")

                # Core Metadata Badges
                logo_type = str(row.get(type_of_logo_col, "N/A")).strip()
                p_form = str(row.get(primary_form_col, "N/A")).strip()
                c_family = str(row.get(color_family_col, "N/A")).strip()
                sector_val = str(row.get(sector_col, "N/A")).strip()
                cnt_val = str(row.get(country_col, "N/A")).strip()

                st.caption(f"**Type:** {logo_type} | **Shape:** {p_form}")
                st.caption(f"**Color Family:** {c_family}")
                st.caption(f"**Sector:** {sector_val} | **Country:** {cnt_val}")
                
                # Expandable Inspector Modal for Details & Typography & Symbolism
                with st.expander("Inspect Full Identity Details"):
                    st.markdown("**Visual & Geometric Properties**")
                    complexity_val = str(row.get(complexity_col, "N/A")).strip()
                    symmetry_val = str(row.get(symmetry_col, "N/A")).strip()
                    v_style = str(row.get(style_inclination_col, "N/A")).strip()
                    
                    st.markdown(f"""
                    <div class="detail-table">
                      <div class="detail-row-label">Form Inclination</div><div class="detail-row-val">{v_style}</div>
                      <div class="detail-row-label">Complexity</div><div class="detail-row-val">{complexity_val}</div>
                      <div class="detail-row-label">Symmetry</div><div class="detail-row-val">{symmetry_val}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    st.markdown("**Typography Attributes**")
                    type_class = str(row.get(type_class_col, "N/A")).strip()
                    font_weight = str(row.get(font_weight_col, "N/A")).strip()
                    case_type = str(row.get(case_type_col, "N/A")).strip()
                    letter_spacing = str(row.get(letter_spacing_col, "N/A")).strip()
                    
                    st.markdown(f"""
                    <div class="detail-table">
                      <div class="detail-row-label">Classification</div><div class="detail-row-val">{type_class}</div>
                      <div class="detail-row-label">Weight & Case</div><div class="detail-row-val">{font_weight} ({case_type})</div>
                      <div class="detail-row-label">Letter Spacing</div><div class="detail-row-val">{letter_spacing}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("")
                    st.markdown("**Symbolism & Rationale**")
                    symbolism_text = str(row.get(symbolism_col, "No symbolism data recorded.")).strip()
                    st.info(symbolism_text)

                st.divider()
