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
    # Read raw CSV
    df = pd.read_csv(CSV_URL)
    
    # Check if the first row contains actual column headers (if S.No. is in header or first row)
    first_col = str(df.columns[0]).strip().lower()
    if first_col in ["s.no.", "s.no", "sno", "sr.no"]:
        # Headers are fine, clean column names
        df.columns = [str(c).strip() for c in df.columns]
    else:
        # Check if row 0 has the headers
        first_row = [str(x).strip().lower() for x in df.iloc[0].values]
        if "s.no." in first_row or "s.no" in first_row or "logo" in first_row:
            df.columns = [str(x).strip() for x in df.iloc[0].values]
            df = df.iloc[1:].reset_index(drop=True)

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.sidebar.header("🔍 Filter Options")
with st.sidebar.expander("📌 Detected Sheet Headers", expanded=True):
    st.write(list(df.columns))

if st.sidebar.button("🔄 Sync Live Data"):
    st.cache_data.clear()
    st.rerun()

# Specific column term mapping matching your screenshot's labels
def find_column(df, search_terms):
    for col in df.columns:
        col_clean = str(col).lower().replace("_", " ").replace("-", " ").strip()
        for term in search_terms:
            if term.lower() == col_clean or term.lower() in col_clean:
                return col
    return None

brand_col = find_column(df, ["brand name", "logo name", "brand", "company", "name", "title"])
shape_col = find_column(df, ["shape", "geometry", "form", "structure"])
color_col = find_column(df, ["colour", "color", "primary color", "hex"])
industry_col = find_column(df, ["industry", "organization type", "org type", "sector", "category", "type"])
country_col = find_column(df, ["country", "region", "location", "origin"])
img_col = find_column(df, ["image url", "image_url", "logo", "image", "url", "link", "photo", "src"])

# Filters
search_query = st.sidebar.text_input("Search Brand Name:", "")

def get_options(col_name):
    if col_name and col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
    return []

selected_shapes = st.sidebar.multiselect("Select Shape(s):", options=get_options(shape_col))
selected_colors = st.sidebar.multiselect("Select Color(s):", options=get_options(color_col))
selected_industries = st.sidebar.multiselect("Select Industry:", options=get_options(industry_col))
selected_countries = st.sidebar.multiselect("Select Country:", options=get_options(country_col))

# Apply filters
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

# Display Gallery Grid
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
                img_url = str(row[img_col]).strip() if img_col and pd.notna(row[img_col]) else ""
                
                if img_url and img_url.lower().startswith("http"):
                    st.image(img_url, use_container_width=True)
                else:
                    st.warning("📷 Image Link Missing or Invalid")

                # Brand Title
                b_name = str(row[brand_col]).strip() if brand_col and pd.notna(row[brand_col]) else "Unnamed Brand"
                st.subheader(b_name)

                # Metadata
                s_val = str(row[shape_col]).strip() if shape_col and pd.notna(row[shape_col]) else "N/A"
                c_val = str(row[color_col]).strip() if color_col and pd.notna(row[color_col]) else "N/A"
                i_val = str(row[industry_col]).strip() if industry_col and pd.notna(row[industry_col]) else "N/A"
                cnt_val = str(row[country_col]).strip() if country_col and pd.notna(row[country_col]) else "N/A"

                st.caption(f"**Shape:** {s_val} | **Color:** {c_val}")
                st.caption(f"**Industry:** {i_val} | **Country:** {cnt_val}")
                st.divider()
