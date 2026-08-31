import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logo Debug", layout="wide")

st.title("🔍 Debug: Logo URL Investigation")

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = [str(c).strip() for c in df.columns]
    return df

df = load_data()

# Show all column names
st.subheader("📋 All Column Names:")
st.write(df.columns.tolist())

# Show the first few rows
st.subheader("📊 First 5 Rows of Data:")
st.dataframe(df.head())

# Look for image/logo column
st.subheader("🖼️ Image Column Investigation:")

# Find which column might have images
image_cols = [col for col in df.columns if 'logo' in col.lower() or 'image' in col.lower() or 'url' in col.lower()]

if image_cols:
    for col_name in image_cols:
        st.write(f"**Column: {col_name}**")
        st.write(f"Sample URLs from this column:")
        
        # Get first 5 non-null values
        sample_urls = df[col_name].dropna().head(5).tolist()
        
        for i, url in enumerate(sample_urls, 1):
            st.write(f"{i}. `{url}`")
            st.write(f"   - Type: {type(url)}")
            st.write(f"   - Length: {len(str(url))}")
        
        st.divider()
else:
    st.warning("No obvious image/logo column found!")
    st.write("Looking at all columns with their first value:")
    for col in df.columns:
        first_val = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else "Empty"
        st.write(f"- **{col}**: {first_val}")

# Show data types
st.subheader("📈 Data Types:")
st.write(df.dtypes)

st.subheader("✅ To Fix:")
st.info("""
Copy the exact image column name (e.g., 'Logo', 'Image URL', etc.) and share it with me.
Also copy 2-3 sample URLs so I can see the exact format.
""")
