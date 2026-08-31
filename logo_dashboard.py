import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Logo Research Explorer",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Interactive Logo Research Gallery")
st.markdown("Live dynamic visualization connected directly to Google Sheets.")

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=2)
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

# Helper function to convert Google Drive view links to direct image URLs
def transform_image_url(url_str):
    url_str = str(url_str).strip()
    if not url_str or url_str.lower() in ["nan", "n/a", "none"]:
        return ""
    
    if "drive.google.com" in url_str:
        match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]+)', url_str)
        if match:
            file_id = match.group(1)
            return f"https://lh3.googleusercontent.com/d/{file_id}"
            
    return url_str

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")

if st.sidebar.button("🔄 Sync Live Data"):
    st.cache_data.clear()
    st.rerun()

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

# Helper for sidebar options
def get_options(col_name):
    if col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
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
st.markdown(f"**Showing {len(filtered_df)} of {len(df)} Logos**")
st.divider()

if filtered_df.empty:
    st.info("No logos match the selected filter criteria.")
else:
    cols_per_row = 4
    cols = st.columns(cols_per_row)
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % cols_per_row]
        with col:
            with st.container():
                # Render Image
                raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
                img_url = transform_image_url(raw_img)
                
                if img_url and img_url.startswith("http"):
                    st.image(img_url, use_container_width=True)
                else:
                    st.warning("📷 Image Link Missing")

                # Brand Name
                b_name = str(row.get(brand_col, "")).strip()
                if not b_name or b_name.lower() in ["nan", "n/a"]:
                    b_name = "Unnamed Brand"
                st.subheader(b_name)

                # Metadata Cards
                p_form = str(row.get(primary_form_col, "N/A")).strip()
                v_form = str(row.get(visual_inclination_col, "N/A")).strip()
                p_color = str(row.get(primary_color_col, "N/A")).strip()
                sector_val = str(row.get(sector_col, "N/A")).strip()
                country_val = str(row.get(country_col, "N/A")).strip()

                st.caption(f"**Primary Form:** {p_form} ({v_form})")
                st.caption(f"**Color:** {p_color}")
                st.caption(f"**Sector:** {sector_val} | **Country:** {country_val}")
                st.divider()
