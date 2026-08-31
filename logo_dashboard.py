import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Logo Research Dashboard",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 0; }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .header-container p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    .stat-box {
        flex: 1;
        min-width: 150px;
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=3600)
def fetch_data():
    """Fetch CSV data from Google Sheets"""
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

@st.cache_data(ttl=3600)
def load_image(url):
    """Load image from URL"""
    try:
        if pd.isna(url) or url == '':
            return None
        response = requests.get(str(url), timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        pass
    return None

# Header
st.markdown("""
<div class="header-container">
    <h1>🎨 Logo Research Dashboard</h1>
    <p>Interactive analysis of medical & healthcare logos across brands, countries, and design characteristics</p>
</div>
""", unsafe_allow_html=True)

# Fetch data
df = fetch_data()

if df is None:
    st.error("Failed to load data. Please check the CSV URL and try again.")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Refresh button
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh Data", key="refresh_btn"):
        st.cache_data.clear()
        st.rerun()

with col1:
    st.caption(f"📋 Total logos in dataset: {len(df)}")

# Sidebar filters
with st.sidebar:
    st.markdown("### 🔍 Filter Options")
    
    # Filter by Type of Logo (Shape)
    if 'Type of Logo' in df.columns:
        logo_types = sorted(df['Type of Logo'].dropna().unique().tolist())
        selected_logo_types = st.multiselect(
            "Logo Type (Shape)",
            options=logo_types,
            default=[],
            key="logo_type_filter"
        )
    else:
        selected_logo_types = []
        st.warning("⚠️ Type of Logo column not found")
    
    # Filter by Primary Colour
    if 'Primary Colour' in df.columns:
        primary_colors = sorted(df['Primary Colour'].dropna().unique().tolist())
        selected_primary_colors = st.multiselect(
            "Primary Colour",
            options=primary_colors,
            default=[],
            key="primary_color_filter"
        )
    else:
        selected_primary_colors = []
        st.warning("⚠️ Primary Colour column not found")
    
    # Filter by Sector
    if 'Sector' in df.columns:
        sectors = sorted(df['Sector'].dropna().unique().tolist())
        selected_sectors = st.multiselect(
            "Sector",
            options=sectors,
            default=[],
            key="sector_filter"
        )
    else:
        selected_sectors = []
        st.warning("⚠️ Sector column not found")
    
    # Filter by Country
    if 'Country' in df.columns:
        countries = sorted(df['Country'].dropna().unique().tolist())
        selected_countries = st.multiselect(
            "Country",
            options=countries,
            default=[],
            key="country_filter"
        )
    else:
        selected_countries = []
        st.warning("⚠️ Country column not found")
    
    st.markdown("---")
    st.markdown(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Apply filters
filtered_df = df.copy()

if selected_logo_types:
    filtered_df = filtered_df[filtered_df['Type of Logo'].isin(selected_logo_types)]
if selected_primary_colors:
    filtered_df = filtered_df[filtered_df['Primary Colour'].isin(selected_primary_colors)]
if selected_sectors:
    filtered_df = filtered_df[filtered_df['Sector'].isin(selected_sectors)]
if selected_countries:
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]

# Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{len(filtered_df)}</div>
        <div class="stat-label">Logos Displayed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    sector_count = filtered_df['Sector'].nunique() if 'Sector' in filtered_df.columns else 0
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{sector_count}</div>
        <div class="stat-label">Sectors</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    country_count = filtered_df['Country'].nunique() if 'Country' in filtered_df.columns else 0
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{country_count}</div>
        <div class="stat-label">Countries</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    color_count = filtered_df['Primary Colour'].nunique() if 'Primary Colour' in filtered_df.columns else 0
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{color_count}</div>
        <div class="stat-label">Primary Colors</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Display logos in grid
if len(filtered_df) > 0:
    st.markdown(f"### 🎯 Showing {len(filtered_df)} logos")
    
    cols = st.columns(4, gap="medium")
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % 4]
        
        with col:
            with st.container(border=True):
                # Image
                if 'Logo' in row and pd.notna(row['Logo']):
                    try:
                        img = load_image(row['Logo'])
                        if img:
                            st.image(img, use_column_width=True)
                        else:
                            st.markdown('<div style="width:100%; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px; color:#999; font-size:0.9rem;">Image not available</div>', unsafe_allow_html=True)
                    except:
                        st.markdown('<div style="width:100%; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px; color:#999;">Error loading image</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="width:100%; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px; color:#999;">No image</div>', unsafe_allow_html=True)
                
                # Brand name
                brand_name = row['Name'] if 'Name' in row else "Unknown Brand"
                st.markdown(f"<div style='font-weight: 700; font-size: 1rem; margin: 1rem 0 0.75rem 0; word-wrap: break-word;'>{brand_name}</div>", unsafe_allow_html=True)
                
                # Badges
                badges_html = "<div style='display: flex; flex-wrap: wrap; gap: 0.4rem;'>"
                
                if 'Type of Logo' in row and pd.notna(row['Type of Logo']):
                    badges_html += f"<span style='background: #e3f2fd; color: #1976d2; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;'>{str(row['Type of Logo']).strip()}</span>"
                
                if 'Primary Colour' in row and pd.notna(row['Primary Colour']):
                    badges_html += f"<span style='background: #f3e5f5; color: #7b1fa2; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;'>{str(row['Primary Colour']).strip()}</span>"
                
                if 'Sector' in row and pd.notna(row['Sector']):
                    badges_html += f"<span style='background: #e8f5e9; color: #388e3c; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;'>{str(row['Sector']).strip()}</span>"
                
                if 'Country' in row and pd.notna(row['Country']):
                    badges_html += f"<span style='background: #fff3e0; color: #f57c00; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;'>{str(row['Country']).strip()}</span>"
                
                badges_html += "</div>"
                st.markdown(badges_html, unsafe_allow_html=True)
else:
    st.info("No logos match your filter criteria. Try adjusting your selections.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.9rem; padding: 2rem 0;'>
    <p>Logo Research Dashboard • Medical & Healthcare Logo Analysis</p>
</div>
""", unsafe_allow_html=True)
