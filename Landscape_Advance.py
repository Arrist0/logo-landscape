import io
import re
import requests
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE & APP INITIALIZATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Logo Landscape — Identity Intelligence Platform",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core State Initialization
if "applied_filters" not in st.session_state:
    st.session_state.applied_filters = {
        "sectors": [], "org_types": [], "countries": [],
        "type_logo": [], "shapes": [], "complexity": [], "symmetry": [],
        "colors_family": [], "undertones": [], "colors_combined": [],
        "case_types": [], "type_class": []
    }

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "Gallery"

if "inspected_logo_id" not in st.session_state:
    st.session_state.inspected_logo_id = None

def reset_all_filters():
    st.session_state.applied_filters = {k: [] for k in st.session_state.applied_filters}
    st.session_state.inspected_logo_id = None

# -----------------------------------------------------------------------------
# 2. DESIGN SYSTEM & CUSTOM CSS STYLESHEET
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --surface-bg: #f8fafc;
    --surface-card: #ffffff;
    --surface-hover: #f1f5f9;
    --border-subtle: #e2e8f0;
    --border-strong: #cbd5e1;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;
    --brand-primary: #4f46e5;
    --brand-accent: #6366f1;
    --brand-subtle: #eeef2;
    --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
    --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.08);
    --shadow-lg: 0 12px 28px -4px rgba(15, 23, 42, 0.12);
}

@media (prefers-color-scheme: dark) {
    :root {
        --surface-bg: #090d16;
        --surface-card: #111827;
        --surface-hover: #1f2937;
        --border-subtle: #1f2937;
        --border-strong: #374151;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --brand-primary: #6366f1;
        --brand-accent: #818cf8;
        --brand-subtle: #1e1b4b;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 12px -2px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 12px 28px -4px rgba(0, 0, 0, 0.5);
    }
}

* { font-family: 'Inter', sans-serif; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); }

.main, .stApp { background-color: var(--surface-bg); color: var(--text-primary); }

/* Sidebar Polish */
[data-testid="stSidebar"] {
    background-color: var(--surface-card);
    border-right: 1px solid var(--border-subtle);
}

/* Header & Typography */
.platform-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 24px;
}

.platform-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0;
}

.platform-subtitle {
    font-size: 13px;
    color: var(--text-muted);
    font-weight: 500;
}

/* Nav Switcher */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    background-color: var(--surface-bg);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border-subtle);
}

div[data-testid="stRadio"] label {
    border-radius: 8px !important;
    padding: 6px 14px !important;
    cursor: pointer;
    margin: 0;
}

div[data-testid="stRadio"] label p {
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

div[data-testid="stRadio"] label[data-checked="true"] {
    background-color: var(--surface-card) !important;
    box-shadow: var(--shadow-sm);
}

div[data-testid="stRadio"] label[data-checked="true"] p {
    color: var(--brand-primary) !important;
}

div[data-testid="stRadio"] span[data-baseweb="radio"] { display: none; }

/* Dynamic Filter Chips */
.chips-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    padding: 12px 16px;
    background: var(--surface-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
}

.chip-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--brand-subtle);
    color: var(--brand-accent);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 600;
}

/* Modern Card Layout */
.logo-card {
    background: var(--surface-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    overflow: hidden;
    height: 380px;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow-sm);
    position: relative;
}

.logo-card:hover {
    border-color: var(--brand-accent);
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
}

.logo-stage {
    height: 180px;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border-bottom: 1px solid var(--border-subtle);
}

.logo-stage img {
    max-height: 130px;
    max-width: 85%;
    object-fit: contain;
}

.logo-card-body {
    padding: 16px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.3;
    margin-bottom: 10px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    font-size: 11px;
    color: var(--text-muted);
}

.card-meta-item strong {
    color: var(--text-secondary);
    display: block;
    font-size: 11.5px;
}

/* Slide-Over Inspector Drawer */
.inspector-box {
    background: var(--surface-card);
    border: 1.5px solid var(--brand-accent);
    border-radius: 16px;
    padding: 20px;
    box-shadow: var(--shadow-lg);
    margin-bottom: 24px;
}

.inspector-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 12px;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 8px;
}

.symbolism-badge {
    background: var(--surface-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 12px;
    font-size: 12px;
    line-height: 1.5;
    color: var(--text-secondary);
    max-height: 140px;
    overflow-y: auto;
}

/* Palette Strip */
.palette-strip {
    display: flex;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
    margin: 12px 0;
}
.palette-block { height: 100%; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. DATA PIPELINE & ENGINE
# -----------------------------------------------------------------------------
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-qp8XmpX4c-mvFbIaB80DxAgVt7FELa1Bb5b1z5nZjBUu_r5f1GCC24A-2DmozwoRT-umwLhu9Iyz/pub?gid=609445256&single=true&output=csv"

@st.cache_data(ttl=3600)
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
        name_series = df["Name"].astype(str).str.strip()
        is_continuation = name_series.eq("") | name_series.eq("nan")

        for i in range(1, len(df)):
            if is_continuation.iloc[i]:
                parent_idx = df.index[i - 1]
                this_idx = df.index[i]
                for col in df.columns:
                    if col == "Name":
                        continue
                    val = df.at[this_idx, col]
                    if pd.notna(val) and str(val).strip() not in ["", "nan"]:
                        parent_val = df.at[parent_idx, col]
                        if pd.isna(parent_val) or str(parent_val).strip() in ["", "nan"]:
                            df.at[parent_idx, col] = val

        df = df.dropna(subset=["Name"]).copy()
        df = df[df["Name"].astype(str).str.strip().ne("")].copy()

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to pull live dataset: {e}")
    st.stop()

def transform_image_url(url_str):
    url_str = str(url_str).strip()
    if not url_str or url_str.lower() in ["nan", "n/a", "none"]:
        return ""
    if "drive.google.com" in url_str:
        match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]+)', url_str)
        if match:
            return f"https://drive.google.com/uc?export=view&id={match.group(1)}"
    return url_str

COLOR_HEX_MAP = {
    "black": "#1a1a1a", "white": "#f1f5f9", "blue": "#2563eb", "red": "#dc2626",
    "green": "#16a34a", "yellow": "#ca8a04", "orange": "#ea580c", "purple": "#9333ea",
    "pink": "#db2777", "teal": "#0d9488", "grey": "#64748b", "gray": "#64748b",
    "brown": "#78350f", "navy": "#1e3a8a", "maroon": "#881337", "gold": "#d97706",
    "silver": "#cbd5e1", "cyan": "#0891b2", "magenta": "#c026d3"
}

def color_to_hex(name):
    return COLOR_HEX_MAP.get(str(name).strip().lower(), "#6366f1")

# Field Identifiers
brand_col = "Name"
img_col = "Logo Source Link"
type_of_logo_col = "Type of Logo"
primary_form_col = "Primary form (Visually Dominating Form)"
color_family_col = "Color Family"
sector_col = "Sector"
org_type_col = "Type of Organization"
country_col = "Country"
complexity_col = "Complexity (Low/ Mid/ High) (Intrinsic Visual Load)"
symmetry_col = "Symmetry"
symbolism_col = "Symbolism"
case_type_col = "Case Type"
type_class_col = "Type classification"
color_cols = ["Primary Colour", "Secondary Colour", "Colour", "Colour3", "Colour4", "Colour5"]
undertone_col = "Color Undertone"

def get_options(col_name):
    if col_name in df.columns:
        return sorted([str(x).strip() for x in df[col_name].dropna().unique() if str(x).strip() not in ["", "nan", "N/A"]])
    return []

# -----------------------------------------------------------------------------
# 4. SIDEBAR CONTROL PANEL
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div style="padding: 8px 0 16px 0;">', unsafe_allow_html=True)
    st.markdown("### Logo Landscape")
    st.markdown('<span style="font-size:11px; color:var(--text-muted);">Visual Identity Research Platform</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.view_mode = st.radio(
        "Navigation",
        options=["Gallery", "Analytics"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    header_col, reset_col = st.columns([3, 1], vertical_alignment="center")
    with header_col:
        st.markdown("**Filters**")
    with reset_col:
        if st.button("🧹", help="Reset all filters", use_container_width=True):
            reset_all_filters()
            st.rerun()

    search_query = st.text_input("⌕ Search identities...", "", placeholder="Organization, country...")

    with st.expander("🏢 Organization & Location", expanded=True):
        f_sec = st.multiselect("Sector", options=get_options(sector_col), default=st.session_state.applied_filters['sectors'])
        f_org = st.multiselect("Organization Type", options=get_options(org_type_col), default=st.session_state.applied_filters['org_types'])
        f_cnt = st.multiselect("Country", options=get_options(country_col), default=st.session_state.applied_filters['countries'])
        if st.button("Apply Org Filters", use_container_width=True):
            st.session_state.applied_filters['sectors'] = f_sec
            st.session_state.applied_filters['org_types'] = f_org
            st.session_state.applied_filters['countries'] = f_cnt
            st.rerun()

    with st.expander("📐 Logo Details & Design"):
        f_typ = st.multiselect("Type of Logo", options=get_options(type_of_logo_col), default=st.session_state.applied_filters['type_logo'])
        f_shp = st.multiselect("Shape / Primary Form", options=get_options(primary_form_col), default=st.session_state.applied_filters['shapes'])
        f_cmp = st.multiselect("Complexity", options=get_options(complexity_col), default=st.session_state.applied_filters['complexity'])
        f_sym = st.multiselect("Symmetry", options=get_options(symmetry_col), default=st.session_state.applied_filters['symmetry'])
        if st.button("Apply Design Filters", use_container_width=True):
            st.session_state.applied_filters['type_logo'] = f_typ
            st.session_state.applied_filters['shapes'] = f_shp
            st.session_state.applied_filters['complexity'] = f_cmp
            st.session_state.applied_filters['symmetry'] = f_sym
            st.rerun()

    with st.expander("🎨 Colors & Aesthetics"):
        f_fam = st.multiselect("Color Family", options=get_options(color_family_col), default=st.session_state.applied_filters['colors_family'])
        f_und = st.multiselect("Color Undertone", options=get_options(undertone_col), default=st.session_state.applied_filters['undertones'])
        if st.button("Apply Color Filters", use_container_width=True):
            st.session_state.applied_filters['colors_family'] = f_fam
            st.session_state.applied_filters['undertones'] = f_und
            st.rerun()

    with st.expander("✍️ Typography Style"):
        f_cas = st.multiselect("Case Type", options=get_options(case_type_col), default=st.session_state.applied_filters['case_types'])
        f_cls = st.multiselect("Type Classification", options=get_options(type_class_col), default=st.session_state.applied_filters['type_class'])
        if st.button("Apply Typography Filters", use_container_width=True):
            st.session_state.applied_filters['case_types'] = f_cas
            st.session_state.applied_filters['type_class'] = f_cls
            st.rerun()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("🔄 Sync Live Google Sheet", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# -----------------------------------------------------------------------------
# 5. DATA FILTERING ENGINE
# -----------------------------------------------------------------------------
filtered_df = df.copy()

if search_query and brand_col in df.columns:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]

af = st.session_state.applied_filters

if af['sectors'] and sector_col in df.columns:
    filtered_df = filtered_df[filtered_df[sector_col].astype(str).str.strip().isin(af['sectors'])]
if af['org_types'] and org_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[org_type_col].astype(str).str.strip().str.lower().isin([s.lower() for s in af['org_types']])]
if af['countries'] and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).str.strip().isin(af['countries'])]

if af['type_logo'] and type_of_logo_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_of_logo_col].astype(str).str.strip().isin(af['type_logo'])]
if af['shapes'] and primary_form_col in df.columns:
    filtered_df = filtered_df[filtered_df[primary_form_col].astype(str).str.strip().isin(af['shapes'])]
if af['complexity'] and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).str.strip().isin(af['complexity'])]
if af['symmetry'] and symmetry_col in df.columns:
    filtered_df = filtered_df[filtered_df[symmetry_col].astype(str).str.strip().isin(af['symmetry'])]

if af['colors_family'] and color_family_col in df.columns:
    filtered_df = filtered_df[filtered_df[color_family_col].astype(str).str.strip().isin(af['colors_family'])]
if af['undertones'] and undertone_col in df.columns:
    filtered_df = filtered_df[filtered_df[undertone_col].astype(str).str.strip().isin(af['undertones'])]

if af['case_types'] and case_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[case_type_col].astype(str).str.strip().isin(af['case_types'])]
if af['type_class'] and type_class_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_class_col].astype(str).str.strip().isin(af['type_class'])]

# -----------------------------------------------------------------------------
# 6. MAIN CONTENT AREA HEADER
# -----------------------------------------------------------------------------
st.markdown(
    f'<div class="platform-header">'
    f'<div>'
    f'<h1 class="platform-title">Visual Identity Research</h1>'
    f'<div class="platform-subtitle">Empirical breakdown of institutional identity design</div>'
    f'</div>'
    f'<div class="top-meta">Showing <strong>{len(filtered_df)}</strong> of {len(df)} Identities</div>'
    f'</div>',
    unsafe_allow_html=True
)

# Expandable Executive Summary
with st.expander("📊 Dataset Executive Summary & Color Composition", expanded=False):
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        st.metric("Total In View", len(filtered_df))
    with s_col2:
        top_sec = filtered_df[sector_col].mode().iloc[0] if not filtered_df.empty and sector_col in filtered_df.columns else "N/A"
        st.metric("Dominant Sector", top_sec)
    with s_col3:
        top_fam = filtered_df[color_family_col].mode().iloc[0] if not filtered_df.empty and color_family_col in filtered_df.columns else "N/A"
        st.metric("Primary Color Family", top_fam)
    with s_col4:
        cnt_count = filtered_df[country_col].nunique() if country_col in filtered_df.columns else 0
        st.metric("Countries Represented", cnt_count)

# Active Filter Chips Bar
active_chips = [(cat, val) for cat, vals in af.items() for val in vals]

chip_container, sort_container = st.columns([4, 1.2], vertical_alignment="center")

with chip_container:
    if active_chips:
        st.markdown('<div class="chips-wrapper">', unsafe_allow_html=True)
        cols_chips = st.columns(len(active_chips) + 1)
        for idx, (cat, val) in enumerate(active_chips):
            with cols_chips[idx]:
                if st.button(f"{val} ✕", key=f"chip_remove_{cat}_{val}"):
                    st.session_state.applied_filters[cat].remove(val)
                    st.rerun()
        with cols_chips[-1]:
            if st.button("Clear All", key="clear_all_chips"):
                reset_all_filters()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">Active Filters: None (showing full corpus)</div>', unsafe_allow_html=True)

with sort_container:
    sort_mode = st.selectbox("Sort Order", options=["Name (A-Z)", "Name (Z-A)"], label_visibility="collapsed")

if brand_col in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=(sort_mode == "Name (A-Z)"))

# -----------------------------------------------------------------------------
# 7. VIEW MODE SWITCHING (GALLERY VS ANALYTICS)
# -----------------------------------------------------------------------------
if st.session_state.view_mode == "Analytics":
    st.subheader("Visual Analytics Dashboard")
    
    a_col1, a_col2 = st.columns(2)
    with a_col1:
        st.markdown("#### Primary Shape Breakdown")
        if primary_form_col in filtered_df.columns:
            st.bar_chart(filtered_df[primary_form_col].value_counts().head(8))
            
    with a_col2:
        st.markdown("#### Color Family Distribution")
        if color_family_col in filtered_df.columns:
            st.bar_chart(filtered_df[color_family_col].value_counts().head(8))

    st.markdown("#### Geographic Spread")
    if country_col in filtered_df.columns:
        st.bar_chart(filtered_df[country_col].value_counts().head(10))

    st.stop()

# -----------------------------------------------------------------------------
# 8. GALLERY VIEW WITH SLIDE-OVER INSPECTOR DRAWER
# -----------------------------------------------------------------------------

# If an item is selected for deep inspection, display the Inspector Drawer at the top
if st.session_state.inspected_logo_id is not None and st.session_state.inspected_logo_id < len(filtered_df):
    selected_row = filtered_df.iloc[st.session_state.inspected_logo_id]
    
    b_name = str(selected_row.get(brand_col, "Unknown Brand")).strip()
    raw_img = str(selected_row.get(img_col, "")).strip()
    img_url = transform_image_url(raw_img)
    
    symbolism_text = str(selected_row.get(symbolism_col, "No detailed symbolism notes recorded for this identity.")).strip()
    
    st.markdown('<div class="inspector-box">', unsafe_allow_html=True)
    
    i_col1, i_col2 = st.columns([1, 2.5])
    
    with i_col1:
        if img_url and img_url.startswith("http"):
            st.image(img_url, use_container_width=True)
        else:
            st.info("📷 Image file unavailable in live directory")
            
    with i_col2:
        st.markdown(f'<div class="inspector-title">{b_name}</div>', unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"**Shape:** {selected_row.get(primary_form_col, '—')}")
            st.markdown(f"**Complexity:** {selected_row.get(complexity_col, '—')}")
        with m2:
            st.markdown(f"**Sector:** {selected_row.get(sector_col, '—')}")
            st.markdown(f"**Symmetry:** {selected_row.get(symmetry_col, '—')}")
        with m3:
            st.markdown(f"**Country:** {selected_row.get(country_col, '—')}")
            st.markdown(f"**Type Class:** {selected_row.get(type_class_col, '—')}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Symbolism & Design Semiotics:**")
        st.markdown(f'<div class="symbolism-badge">{symbolism_text}</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✕ Close Inspector Drawer", key="close_inspector"):
            st.session_state.inspected_logo_id = None
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# Cards Grid Setup
cols_per_row = 3
grid_cols = st.columns(cols_per_row, gap="large")

for idx, (_, row) in enumerate(filtered_df.iterrows()):
    col = grid_cols[idx % cols_per_row]
    with col:
        b_name = str(row.get(brand_col, "Unknown Brand")).strip()
        raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
        img_url = transform_image_url(raw_img)
        
        img_html = f'<img src="{img_url}" alt="{b_name}" />' if (img_url and img_url.startswith("http")) else '<div style="color: var(--text-muted); font-size: 12px;">📷 Image unavailable</div>'
        
        p_form = str(row.get(primary_form_col, "—")).strip()
        c_family = str(row.get(color_family_col, "—")).strip()
        sector_val = str(row.get(sector_col, "—")).strip()
        cnt_val = str(row.get(country_col, "—")).strip()

        card_html = (
            f'<div class="logo-card">'
            f'<div class="logo-stage">{img_html}</div>'
            f'<div class="logo-card-body">'
            f'<div class="card-title">{b_name}</div>'
            f'<div class="card-meta-grid">'
            f'<div class="card-meta-item">Shape <strong>{p_form}</strong></div>'
            f'<div class="card-meta-item">Sector <strong>{sector_val}</strong></div>'
            f'<div class="card-meta-item">Color <strong>{c_family}</strong></div>'
            f'<div class="card-meta-item">Country <strong>{cnt_val}</strong></div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
        
        if st.button("Inspect Details 🔍", key=f"inspect_btn_{idx}", use_container_width=True):
            st.session_state.inspected_logo_id = idx
            st.rerun()
