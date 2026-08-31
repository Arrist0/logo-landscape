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

# Inject Custom CSS matching your dark UI theme
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; color: #e2e8f0; }
    
    /* Topbar & Hero Styling */
    .eyebrow { font-size: 0.75rem; letter-spacing: 0.1em; color: #a0aec0; font-weight: 700; text-transform: uppercase; }
    .kicker { font-size: 0.7rem; letter-spacing: 0.12em; color: #cbd5e0; font-weight: 700; }
    .hero-title { font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin-bottom: 0.5rem; }
    .hero-title em { font-style: italic; color: #a3b8cc; }
    .intro { color: #a0aec0; font-size: 0.95rem; margin-bottom: 1.5rem; }

    /* Stat Cards */
    .stat-box { background: #1a202c; border: 1px solid #2d3748; padding: 1rem; border-radius: 8px; text-align: center; }
    .stat-number { font-size: 1.5rem; font-weight: 800; color: #ffffff; }
    .stat-label { font-size: 0.75rem; color: #a0aec0; text-transform: uppercase; }

    /* Card Layout */
    div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
        background-color: #1a202c !important;
        border: 1px solid #2d3748 !important;
        border-radius: 10px !important;
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
    st.error(f"Error loading live data: {e}")
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

# ----------------- TOPBAR & HERO SECTION -----------------
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown('<div class="eyebrow">VISUAL IDENTITY RESEARCH</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="margin:0; font-size:2.5rem; font-weight:800;">Logo Landscape</h1>', unsafe_allow_html=True)
with top_col2:
    st.markdown(f'<div style="text-align:right; font-size:1.1rem; font-weight:700; padding-top:1rem; color:#a0aec0;"><strong>{len(df)}</strong> identities</div>', unsafe_allow_html=True)

st.divider()

# Hero Banner & Dataset Stats
hero_col1, hero_col2 = st.columns([2, 1])
with hero_col1:
    st.markdown('<p class="kicker">EXPLORE THE DATASET</p>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">165+ visual identities.<br><em>One searchable research space.</em></div>', unsafe_allow_html=True)
    st.markdown('<p class="intro">Filter, compare and inspect the visual characteristics captured during logo research.</p>', unsafe_allow_html=True)

with hero_col2:
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(df)}</div><div class="stat-label">Total Logos</div></div>', unsafe_allow_html=True)
    with s2:
        govt_count = len(df[df['Sector'].astype(str).str.contains('Govt', case=False, na=False)]) if 'Sector' in df else 0
        st.markdown(f'<div class="stat-box"><div class="stat-number">{govt_count}</div><div class="stat-label">Govt Institutions</div></div>', unsafe_allow_html=True)

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.markdown("### FILTERS")

if st.sidebar.button("Reset Filters"):
    st.cache_data.clear()
    st.rerun()

brand_col = "Name"
img_col = "Logo"
primary_form_col = "Primary form (Visually Dominating Form)"
style_inclination_col = "Visual Form inclination (First form we visually notice)"
color_col = "Primary Colour"
color_family_col = "Color Family"
sector_col = "Sector"
org_type_col = "Type of Organization"
country_col = "Country"
symbolism_col = "Symbolism"

def get_options(col_name):
    if col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
    return []

search_query = st.sidebar.text_input("⌕ Search organisation...", "")

selected_forms = st.sidebar.multiselect("Shape (Primary Form):", options=get_options(primary_form_col))
selected_colors = st.sidebar.multiselect("Primary Color:", options=get_options(color_col))
selected_families = st.sidebar.multiselect("Color Family:", options=get_options(color_family_col))
selected_sectors = st.sidebar.multiselect("Sector:", options=get_options(sector_col))
selected_org_types = st.sidebar.multiselect("Organization Type:", options=get_options(org_type_col))
selected_countries = st.sidebar.multiselect("Country:", options=get_options(country_col))

# Filtering Logic
filtered_df = df.copy()

if search_query and brand_col in df.columns:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]

if selected_forms and primary_form_col in df.columns:
    filtered_df = filtered_df[filtered_df[primary_form_col].astype(str).isin(selected_forms)]

if selected_colors and color_col in df.columns:
    filtered_df = filtered_df[filtered_df[color_col].astype(str).isin(selected_colors)]

if selected_families and color_family_col in df.columns:
    filtered_df = filtered_df[filtered_df[color_family_col].astype(str).isin(selected_families)]

if selected_sectors and sector_col in df.columns:
    filtered_df = filtered_df[filtered_df[sector_col].astype(str).isin(selected_sectors)]

if selected_org_types and org_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[org_type_col].astype(str).isin(selected_org_types)]

if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).isin(selected_countries)]

# ----------------- SORTING & RESULTS HEAD -----------------
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

# ----------------- GRID DISPLAY & DETAIL EXPANDER -----------------
if filtered_df.empty:
    st.info("No logos match the selected criteria.")
else:
    cols_per_row = 4
    cols = st.columns(cols_per_row)
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % cols_per_row]
        with col:
            with st.container():
                raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
                img_url = transform_image_url(raw_img)
                
                if img_url and img_url.startswith("http"):
                    st.image(img_url, use_container_width=True)
                else:
                    st.warning("📷 Image Link Missing")

                b_name = str(row.get(brand_col, "")).strip()
                st.subheader(b_name if b_name else "Unnamed Brand")

                p_form = str(row.get(primary_form_col, "N/A")).strip()
                v_style = str(row.get(style_inclination_col, "N/A")).strip()
                c_family = str(row.get(color_family_col, "N/A")).strip()
                sector_val = str(row.get(sector_col, "N/A")).strip()
                cnt_val = str(row.get(country_col, "N/A")).strip()

                st.caption(f"**Shape:** {p_form} ({v_style})")
                st.caption(f"**Color Family:** {c_family}")
                st.caption(f"**Sector:** {sector_val} | **Country:** {cnt_val}")
                
                # Detail Modal Replacement (Expander)
                with st.expander("Inspect Details"):
                    symbolism_text = str(row.get(symbolism_col, "No symbolism data recorded.")).strip()
                    st.markdown(f"**Symbolism & Rationale:**\n\n{symbolism_text}")
                
                st.divider()
