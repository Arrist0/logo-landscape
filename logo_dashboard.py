import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time
from PIL import Image
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Logo Research Dashboard",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0;
    }
    
    /* Header styling */
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
    
    /* Logo grid items */
    .logo-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #e0e0e0;
    }
    
    .logo-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        transform: translateY(-4px);
    }
    
    .logo-image-container {
        width: 100%;
        height: 200px;
        background: #f8f9fa;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    
    .logo-image {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
    
    .logo-info {
        padding: 1rem;
    }
    
    .logo-brand {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0 0 0.75rem 0;
    }
    
    .badges-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: capitalize;
    }
    
    .badge-shape {
        background: #e3f2fd;
        color: #1976d2;
    }
    
    .badge-color {
        background: #f3e5f5;
        color: #7b1fa2;
    }
    
    .badge-industry {
        background: #e8f5e9;
        color: #388e3c;
    }
    
    .badge-country {
        background: #fff3e0;
        color: #f57c00;
    }
    
    /* Sidebar styling */
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #667eea;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Stats */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
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
    
    /* Loading indicator */
    .refresh-indicator {
        color: #999;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=3600)  # Cache for 1 hour
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
    """Load image from URL with caching"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        pass
    return None

# Header
st.markdown("""
<div class="header-container">
    <h1>🎨 Logo Research Dashboard</h1>
    <p>Interactive analysis of 100+ logos across brands, industries, and countries</p>
</div>
""", unsafe_allow_html=True)

# Fetch data
df = fetch_data()

if df is None:
    st.error("Failed to load data. Please check the CSV URL and try again.")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Display refresh info
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh Data", key="refresh_btn"):
        st.cache_data.clear()
        st.rerun()

# Sidebar filters
with st.sidebar:
    st.markdown("### 🔍 Filter Options")
    
    # Multi-select filters
    shapes = sorted(df['Shape'].dropna().unique().tolist())
    selected_shapes = st.multiselect(
        "Shape",
        options=shapes,
        default=[],
        key="shape_filter"
    )
    
    colors = sorted(df['Color'].dropna().unique().tolist())
    selected_colors = st.multiselect(
        "Color",
        options=colors,
        default=[],
        key="color_filter"
    )
    
    industries = sorted(df['Industry'].dropna().unique().tolist())
    selected_industries = st.multiselect(
        "Industry",
        options=industries,
        default=[],
        key="industry_filter"
    )
    
    countries = sorted(df['Country'].dropna().unique().tolist())
    selected_countries = st.multiselect(
        "Country",
        options=countries,
        default=[],
        key="country_filter"
    )
    
    st.markdown("---")
    st.markdown(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Apply filters
filtered_df = df.copy()

if selected_shapes:
    filtered_df = filtered_df[filtered_df['Shape'].isin(selected_shapes)]
if selected_colors:
    filtered_df = filtered_df[filtered_df['Color'].isin(selected_colors)]
if selected_industries:
    filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industries)]
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
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{filtered_df['Industry'].nunique()}</div>
        <div class="stat-label">Industries</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{filtered_df['Country'].nunique()}</div>
        <div class="stat-label">Countries</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{filtered_df['Color'].nunique()}</div>
        <div class="stat-label">Color Palettes</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Display logos in responsive grid
if len(filtered_df) > 0:
    st.markdown(f"### 🎯 Showing {len(filtered_df)} logos")
    
    # Create columns for grid layout (4 columns on desktop, 2 on tablet, 1 on mobile)
    cols = st.columns(4, gap="medium")
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[idx % 4]
        
        with col:
            # Card container
            with st.container(border=True):
                # Image
                if pd.notna(row.get('Image URL')):
                    try:
                        img = load_image(row['Image URL'])
                        if img:
                            st.image(img, use_column_width=True)
                        else:
                            st.markdown('<div style="width:100%; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px; color:#999;">No image</div>', unsafe_allow_html=True)
                    except:
                        st.markdown('<div style="width:100%; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px; color:#999;">Image error</div>', unsafe_allow_html=True)
                
                # Brand name
                st.markdown(f"<div style='font-weight: 700; font-size: 1.1rem; margin: 1rem 0 0.75rem 0;'>{row['Brand Name']}</div>", unsafe_allow_html=True)
                
                # Badges
                badges_html = "<div style='display: flex; flex-wrap: wrap; gap: 0.5rem;'>"
                
                if pd.notna(row.get('Shape')):
                    badges_html += f"<span style='background: #e3f2fd; color: #1976d2; padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;'>{row['Shape']}</span>"
                
                if pd.notna(row.get('Color')):
                    badges_html += f"<span style='background: #f3e5f5; color: #7b1fa2; padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;'>{row['Color']}</span>"
                
                if pd.notna(row.get('Industry')):
                    badges_html += f"<span style='background: #e8f5e9; color: #388e3c; padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;'>{row['Industry']}</span>"
                
                if pd.notna(row.get('Country')):
                    badges_html += f"<span style='background: #fff3e0; color: #f57c00; padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;'>{row['Country']}</span>"
                
                badges_html += "</div>"
                st.markdown(badges_html, unsafe_allow_html=True)
else:
    st.info("No logos match your filter criteria. Try adjusting your selections.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.9rem; padding: 2rem 0;'>
    <p>Logo Research Dashboard • Data sourced from Google Sheets • Real-time filtering and caching</p>
</div>
""", unsafe_allow_html=True)
