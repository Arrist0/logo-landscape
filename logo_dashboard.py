import streamlit as st
import pandas as pd

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
    # Read CSV and strip spaces from column header strings
    df = pd.read_csv(CSV_URL)
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Debug: Print detected headers in sidebar to verify connection
st.sidebar.header("🔍 Filter Options")
with st.sidebar.expander("📌 Detected Sheet Headers", expanded=False):
    st.write(list(df.columns))

if st.sidebar.button("🔄 Sync Live Data"):
    st.cache_data.clear()
    st.rerun()

# Advanced Helper function to locate columns dynamically
def find_column(df, search_terms):
    for col in df.columns:
        col_clean = str(col).lower().replace("_", " ").replace("-", " ").strip()
        for term in search_terms:
            if term.lower() in col_clean:
                return col
    return None

brand_col = find_column(df, ["brand", "name", "title", "company", "organization", "logo name"])
shape_col = find_column(df, ["shape", "geometry", "form"])
color_col = find_column(df, ["color", "primary color", "hue", "theme color"])
industry_col = find_column(df, ["industry", "organization type", "org type", "sector", "category", "type"])
country_col = find_column(df, ["country", "region", "location", "origin"])
img_col = find_column(df, ["image", "url", "link", "photo", "logo", "img", "src"])

# Filters
search_query = st.sidebar.text_input("Search Brand Name:", "")

def get_options(col_name):
    if col_name and col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() != ""])
    return []

selected_shapes = st.sidebar.multiselect("Select Shape(s):", options=get_options(shape_col))
selected_colors = st.sidebar.multiselect("Select Color(s):", options=get_options(color_col))
selected_industries = st.sidebar.multiselect("Select Industry:", options=get_options(industry_col))
selected_countries = st.sidebar.multiselect("Select Country:", options=get_options(country_col))

# Filter dataset
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

# Gallery Output
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
                # Display image or placeholder
                img_url = str(row[img_col]).strip() if img_col and pd.notna(row[img_col]) else ""
                
                if img_url and img_url.lower().startswith("http"):
                    st.image(img_url, use_container_width=True)
                else:
                    st.warning("📷 Image Link Missing or Invalid")

                # Brand Title
                b_name = str(row[brand_col]).strip() if brand_col and pd.notna(row[brand_col]) else "Unnamed Brand"
                st.subheader(b_name)

                # Attributes
                s_val = str(row[shape_col]).strip() if shape_col and pd.notna(row[shape_col]) else "N/A"
                c_val = str(row[color_col]).strip() if color_col and pd.notna(row[color_col]) else "N/A"
                i_val = str(row[industry_col]).strip() if industry_col and pd.notna(row[industry_col]) else "N/A"
                cnt_val = str(row[country_col]).strip() if country_col and pd.notna(row[country_col]) else "N/A"

                st.caption(f"**Shape:** {s_val} | **Color:** {c_val}")
                st.caption(f"**Industry:** {i_val} | **Country:** {cnt_val}")
                st.divider()
