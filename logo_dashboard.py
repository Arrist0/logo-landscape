import io
import re
import requests
import pandas as pd
import streamlit as st

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
    # Fetch raw CSV content
    response = requests.get(CSV_URL)
    response.encoding = 'utf-8'
    lines = response.text.splitlines()

    # Locate the header row containing 'Name' and 'Primary form'
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

    # Clean column names (strip newlines & trailing spaces)
    df.columns = [re.sub(r'\s+', ' ', str(c)).strip() for c in df.columns]

    # Filter out empty rows or invalid brand entries
    if "Name" in df.columns:
        df = df.dropna(subset=["Name"]).copy()
        df = df[df["Name"].astype(str).str.strip().ne("")].copy()

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading live data: {e}")
    st.stop()

# Transform Google Drive view links to direct image URLs
def transform_image_url(url_str):
    url_str = str(url_str).strip()
    if not url_str or url_str.lower() in ["nan", "n/a", "none"]:
        return ""
    if "drive.google.com" in url_str:
        match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]+)', url_str)
        if match:
            return f"https://lh3.googleusercontent.com/d/{match.group(1)}"
    return url_str

# Sidebar Controls
st.sidebar.header("🔍 Filter Options")

if st.sidebar.button("🔄 Sync Live Data"):
    st.cache_data.clear()
    st.rerun()

# Map Exact Columns
brand_col = "Name"
img_col = "Logo"
primary_form_col = "Primary form (Visually Dominating Form)"
style_inclination_col = "Visual Form inclination (First form we visually notice)"
color_col = "Primary Colour"
color_family_col = "Color Family"
sector_col = "Sector"
org_type_col = "Type of Organization"
country_col = "Country"

def get_options(col_name):
    if col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
    return []

search_query = st.sidebar.text_input("Search Brand Name:", "")

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

# Display Results Count
st.markdown(f"**Showing {len(filtered_df)} of {len(df)} Logos**")
st.divider()

if filtered_df.empty:
    st.info("No logos match the selected criteria.")
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
                    st.warning("📷 Image Link Missing (Add URL in Sheet)")

                # Brand Name
                b_name = str(row.get(brand_col, "")).strip()
                st.subheader(b_name if b_name else "Unnamed Brand")

                # Attributes
                p_form = str(row.get(primary_form_col, "N/A")).strip()
                v_style = str(row.get(style_inclination_col, "N/A")).strip()
                c_family = str(row.get(color_family_col, "N/A")).strip()
                sector_val = str(row.get(sector_col, "N/A")).strip()
                cnt_val = str(row.get(country_col, "N/A")).strip()

                st.caption(f"**Shape:** {p_form} ({v_style})")
                st.caption(f"**Color Family:** {c_family}")
                st.caption(f"**Sector:** {sector_val} | **Country:** {cnt_val}")
                st.divider()
