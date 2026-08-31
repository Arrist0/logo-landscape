import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Logo Research Explorer",
    page_icon="🎨",
    layout="wide"
)

# Title & Subheading
st.title("🎨 Interactive Logo Research Gallery")
st.markdown("Live dynamic visualization connected directly to Google Sheets.")

# Your Published Google Sheet CSV URL
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?output=csv"

# Function to load live data with cache controls
@st.cache_data(ttl=5)  # Re-checks Google Sheet every 5 seconds
def load_data():
    df = pd.read_csv(CSV_URL)
    # Clean up column names (trim whitespace)
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Failed to load live data from Google Sheets. Please verify connection.")
    st.stop()

# Helper function to find matching columns regardless of case
def get_col_name(candidates):
    for col in df.columns:
        if col.lower() in [c.lower() for c in candidates]:
            return col
    return None

brand_col = get_col_name(["brand", "brand name", "name", "organization", "company"])
shape_col = get_col_name(["shape", "shapes"])
color_col = get_col_name(["color", "colors", "primary color"])
industry_col = get_col_name(["industry", "organization type", "org type", "category"])
country_col = get_col_name(["country", "region", "location"])
img_col = get_col_name(["image_url", "image url", "logo", "image", "url", "link"])

# Sidebar Navigation & Filters
st.sidebar.header("🔍 Filter Options")

if st.sidebar.button("🔄 Sync Live Data"):
    st.cache_data.clear()
    st.rerun()

search_query = st.sidebar.text_input("Search Brand Name:", "")

def get_options(column):
    if column and column in df.columns:
        return sorted([str(x) for x in df[column].dropna().unique()])
    return []

selected_shapes = st.sidebar.multiselect("Select Shape(s):", options=get_options(shape_col))
selected_colors = st.sidebar.multiselect("Select Color(s):", options=get_options(color_col))
selected_industries = st.sidebar.multiselect("Select Industry:", options=get_options(industry_col))
selected_countries = st.sidebar.multiselect("Select Country:", options=get_options(country_col))

# Filtering Logic
filtered_df = df.copy()

if search_query and brand_col:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]

if selected_shapes and shape_col:
    filtered_df = filtered_df[filtered_df[shape_col].astype(str).isin(selected_shapes)]

if selected_colors and color_col:
    filtered_df = filtered_df[filtered_df[color_col].astype(str).isin(selected_colors)]

if selected_industries and industry_col:
    filtered_df = filtered_df[filtered_df[industry_col].astype(str).isin(selected_industries)]

if selected_countries and country_col:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).isin(selected_countries)]

# Display Results Count
st.markdown(f"**Showing {len(filtered_df)} of {len(df)} Logos**")
st.divider()

if filtered_df.empty:
    st.info("No logos found matching your selected criteria.")
else:
    # 4-Column Grid
    cols = st.columns(4)
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[idx % 4]:
            with st.container():
                # Render Image
                img_url = str(row[img_col]) if img_col and pd.notna(row[img_col]) else ""
                if img_url:
                    st.image(img_url, use_container_width=True)
                else:
                    st.caption("📷 Image Link Missing")

                # Brand Title
                brand_name = str(row[brand_col]) if brand_col and pd.notna(row[brand_col]) else "Unnamed Brand"
                st.subheader(brand_name)

                # Metadata Badges
                s_val = str(row[shape_col]) if shape_col and pd.notna(row[shape_col]) else "N/A"
                c_val = str(row[color_col]) if color_col and pd.notna(row[color_col]) else "N/A"
                i_val = str(row[industry_col]) if industry_col and pd.notna(row[industry_col]) else "N/A"
                
                st.caption(f"**Shape:** {s_val} | **Color:** {c_val}")
                st.caption(f"**Industry:** {i_val}")
                st.divider()
