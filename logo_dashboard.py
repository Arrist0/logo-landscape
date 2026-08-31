import streamlit as st
import pandas as pd
import re
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Logo Research Explorer",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
<style>
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    .header-container h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .header-container p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
</style>
<div class="header-container">
    <h1>🎨 Interactive Logo Research Gallery</h1>
    <p>Live dynamic visualization connected directly to Google Sheets • 163+ medical & healthcare logos</p>
</div>
""", unsafe_allow_html=True)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv(CSV_URL)
    # Strip whitespace from column headers
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Better Google Drive image URL transformation
def transform_image_url(url_str):
    """Convert Google Drive share/view links to direct image URLs"""
    if pd.isna(url_str):
        return ""
    
    url_str = str(url_str).strip()
    
    # Check if it's already a valid URL
    if not url_str or url_str.lower() in ["nan", "n/a", "none", ""]:
        return ""
    
    # If it's a Google Drive link, extract file ID and convert
    if "drive.google.com" in url_str:
        # Pattern 1: /d/FILE_ID/
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url_str)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        
        # Pattern 2: id=FILE_ID
        match = re.search(r'id=([a-zA-Z0-9_-]+)', url_str)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"
    
    # If it's already a direct image URL, return as is
    if url_str.startswith("http"):
        return url_str
    
    return ""

@st.cache_data(ttl=3600)
def load_image(url):
    """Try to load image from URL with better error handling"""
    try:
        if not url or not url.startswith("http"):
            return None
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        pass
    return None

# Map exact column names from your spreadsheet
brand_col = "Name"
img_col = "Logo"
country_col = "Country"
sector_col = "Sector"
org_type_col = "Type of Organization"
primary_form_col = "Primary form\n(Visually Dominating Form)"
visual_inclination_col = "Visual Form inclination\n(First form we visually notice)"
complexity_col = "Complexity (Low/ Mid/ High)\n(Intrinsic Visual Load)"
gestalt_col = "Gestalt Principle"
primary_color_col = "Primary Colour"
color_family_col = "Color Family"

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")

if st.sidebar.button("🔄 Refresh Data", key="refresh_btn"):
    st.cache_data.clear()
    st.rerun()

# Helper for sidebar options
def get_options(col_name):
    if col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A", "nan (nan)"]])
    return []

# Sidebar Controls
search_query = st.sidebar.text_input("Search Brand Name:", "")

selected_forms = st.sidebar.multiselect("Primary Form / Shape:", options=get_options(primary_form_col))
selected_colors = st.sidebar.multiselect("Primary Color:", options=get_options(primary_color_col))
selected_families = st.sidebar.multiselect("Color Family:", options=get_options(color_family_col))
selected_sectors = st.sidebar.multiselect("Sector:", options=get_options(sector_col))
selected_org_types = st.sidebar.multiselect("Type of Organization:", options=get_options(org_type_col))
selected_countries = st.sidebar.multiselect("Country:", options=get_options(country_col))
selected_gestalt = st.sidebar.multiselect("Gestalt Principle:", options=get_options(gestalt_col))
selected_complexity = st.sidebar.multiselect("Complexity:", options=get_options(complexity_col))

# Apply Filtering Logic
filtered_df = df.copy()

if search_query and brand_col in df.columns:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]

if selected_forms and primary_form_col in df.columns:
    filtered_df = filtered_df[filtered_df[primary_form_col].astype(str).isin(selected_forms)]

if selected_colors and primary_color_col in df.columns:
    filtered_df = filtered_df[filtered_df[primary_color_col].astype(str).isin(selected_colors)]

if selected_families and color_family_col in df.columns:
    filtered_df = filtered_df[filtered_df[color_family_col].astype(str).isin(selected_families)]

if selected_sectors and sector_col in df.columns:
    filtered_df = filtered_df[filtered_df[sector_col].astype(str).isin(selected_sectors)]

if selected_org_types and org_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[org_type_col].astype(str).isin(selected_org_types)]

if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).isin(selected_countries)]

if selected_gestalt and gestalt_col in df.columns:
    filtered_df = filtered_df[filtered_df[gestalt_col].astype(str).isin(selected_gestalt)]

if selected_complexity and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).isin(selected_complexity)]

# Render Results
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"### 🎯 Showing {len(filtered_df)} of {len(df)} Logos")
with col2:
    st.caption(f"📊 {len(df)} total in database")

st.divider()

if filtered_df.empty:
    st.info("No logos match the selected filter criteria. Try adjusting your filters.")
else:
    cols_per_row = 4
    cols = st.columns(cols_per_row, gap="medium")
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % cols_per_row]
        with col:
            with st.container(border=True):
                # Render Image
                raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
                img_url = transform_image_url(raw_img)
                
                if img_url:
                    img = load_image(img_url)
                    if img:
                        st.image(img, use_column_width=True)
                    else:
                        st.markdown('<div style="width:100%; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px; color:#999; font-size:0.9rem;">⚠️ Image unavailable</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="width:100%; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px; color:#999;">📷 No image</div>', unsafe_allow_html=True)

                # Brand Name
                b_name = str(row.get(brand_col, "")).strip()
                if not b_name or b_name.lower() in ["nan", "n/a"]:
                    b_name = "Unnamed Brand"
                st.markdown(f"<div style='font-weight: 700; font-size: 1rem; margin: 1rem 0 0.75rem 0;'>{b_name}</div>", unsafe_allow_html=True)

                # Metadata Badges
                p_form = str(row.get(primary_form_col, "")).strip()
                p_color = str(row.get(primary_color_col, "")).strip()
                sector_val = str(row.get(sector_col, "")).strip()
                country_val = str(row.get(country_col, "")).strip()

                badges = []
                if p_form and p_form.lower() not in ["nan", "n/a"]:
                    badges.append(f'<span style="background: #e3f2fd; color: #1976d2; padding: 0.3rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">{p_form}</span>')
                
                if p_color and p_color.lower() not in ["nan", "n/a"]:
                    badges.append(f'<span style="background: #f3e5f5; color: #7b1fa2; padding: 0.3rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">{p_color}</span>')
                
                if sector_val and sector_val.lower() not in ["nan", "n/a"]:
                    badges.append(f'<span style="background: #e8f5e9; color: #388e3c; padding: 0.3rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">{sector_val}</span>')
                
                if country_val and country_val.lower() not in ["nan", "n/a"]:
                    badges.append(f'<span style="background: #fff3e0; color: #f57c00; padding: 0.3rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">{country_val}</span>')
                
                if badges:
                    st.markdown(f'<div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">{"".join(badges)}</div>', unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.85rem; padding: 2rem 0;'>
    <p>Logo Research Dashboard • Medical & Healthcare Logo Analysis • Real-time Google Sheets sync</p>
</div>
""", unsafe_allow_html=True)
