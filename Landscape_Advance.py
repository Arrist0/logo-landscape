import io
import re
import requests
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Logo Landscape — Visual Identity Research",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States for Applied Filters
filter_keys = [
    "sectors", "org_types", "countries", 
    "type_logo", "shapes", "complexity", "symmetry",
    "colors_family", "undertones", "colors_combined",
    "case_types", "type_class"
]

if "applied_filters" not in st.session_state:
    st.session_state.applied_filters = {k: [] for k in filter_keys}

def reset_filters():
    st.session_state.applied_filters = {k: [] for k in filter_keys}

# 2. Dynamic Light & Dark Theme CSS + UI Overrides
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Space+Grotesk:wght@500;700&display=swap');

/* Dynamic Theme Variables */
:root {
  --bg: #ffffff;
  --card: #f8f9fa;
  --ink: #1a1a1a;
  --muted: #666666;
  --line: #e2e8f0;
  --accent: #6366f1;
  --card-back: #ffffff;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1117;
    --card: #171923;
    --ink: #f7fafc;
    --muted: #a0aec0;
    --line: #2d3748;
    --accent: #6366f1;
    --card-back: #1a1d29;
  }
}

* { transition: background-color 0.2s ease, border-color 0.2s ease; }

.main, .stApp { 
  background-color: var(--bg);
  color: var(--ink);
  font-family: "DM Sans", sans-serif; 
}

/* Sidebar App Title */
h1.sidebar-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 24px;
    margin: 0 0 15px 0;
    color: var(--ink);
    font-weight: 700;
}

/* Topbar Main Content */
.topbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 15px 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 15px;
}

.topbar-subtitle {
    font-size: 14px;
    color: var(--muted);
    font-weight: 500;
}

.top-meta {
    font-size: 13px;
    color: var(--muted);
}

/* Sidebar Pill Toggle Switch */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    background-color: var(--card);
    border-radius: 30px;
    padding: 4px;
    border: 1.5px solid var(--line);
    display: flex;
    width: 100%;
}
div[data-testid="stRadio"] label {
    border-radius: 26px !important;
    padding: 8px 0 !important;
    background-color: transparent;
    cursor: pointer;
    margin: 0;
    flex: 1;
    text-align: center;
    justify-content: center;
}
div[data-testid="stRadio"] label p { color: var(--ink) !important; font-size: 13px !important;}
div[data-testid="stRadio"] label[data-checked="true"] { background-color: var(--muted) !important; }
div[data-testid="stRadio"] label[data-checked="true"] p { color: #ffffff !important; font-weight: 600 !important; }
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] { margin-left: 0; display: flex; justify-content: center;}
div[data-testid="stRadio"] span[data-baseweb="radio"] { display: none; }

/* Filter Apply Buttons */
[data-testid="stFormSubmitButton"] > button {
    float: right;
    padding: 2px 14px !important;
    min-height: 32px !important;
    font-size: 13px !important;
    border-radius: 6px !important;
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
}

/* Chips / Active Filters Row */
.chip-row-container {
    background-color: var(--card);
    padding: 12px 16px;
    border-radius: 8px;
    border: 1px solid var(--line);
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}
div[data-testid="column"] { 
    width: auto !important; 
    flex: 0 0 auto !important; 
    min-width: 0 !important; 
    padding: 0 !important;
}
.chip-btn button {
    border-radius: 20px !important;
    padding: 2px 12px !important;
    font-size: 11.5px !important;
    min-height: 28px !important;
    background-color: var(--muted) !important;
    color: white !important;
    border: none !important;
}
.clear-all-btn button {
    background: transparent !important;
    border: none !important;
    color: var(--ink) !important;
    font-size: 11.5px !important;
    text-decoration: underline !important;
    padding: 2px 8px !important;
    min-height: 28px !important;
}

/* Form Headings */
.filter-subhead {
    font-size: 12.5px;
    font-weight: 700;
    color: var(--ink);
    margin: 12px 0 6px 0;
}

/* Editorial Summary Card */
.editorial-wrap {
    display: grid;
    grid-template-columns: 0.9fr 1.3fr;
    gap: 32px;
    align-items: center;
    padding: 12px 14px;
}
.editorial-hero { border-right: 1px solid var(--line); padding-right: 28px; }
.editorial-eyebrow { font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--accent); margin-bottom: 6px; }
.editorial-number { font-family: "Space Grotesk", sans-serif; font-size: 40px; font-weight: 700; color: var(--ink); line-height: 1.0; }
.editorial-desc { font-size: 12.5px; color: var(--muted); margin-top: 8px; }
.editorial-row { display: flex; justify-content: space-between; align-items: baseline; padding: 6px 0; border-bottom: 1px solid var(--line); }
.editorial-row:last-child { border-bottom: none; padding-bottom: 0; }
.editorial-row-label { font-size: 12.5px; color: var(--ink); }
.editorial-sub { color: var(--muted); font-size: 10.5px; display: block; }
.editorial-row-value { font-family: "Space Grotesk", sans-serif; font-size: 15px; font-weight: 700; color: var(--ink); }
.palette-bar-container { background: var(--card); border-top: 1.5px solid var(--line); padding: 14px 20px; display: flex; align-items: center; }
.palette-title { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--accent); margin-right: 20px; }
.palette-items { display: flex; gap: 24px; flex-wrap: wrap; width: 100%; }
.palette-item { display: flex; align-items: center; gap: 8px; }
.palette-swatch { width: 14px; height: 14px; border-radius: 50%; border: 1px solid rgba(0, 0, 0, 0.15); }
.palette-name { font-size: 12.5px; font-weight: 500; color: var(--ink); }

/* Clean Native Card UI Container */
.logo-card-box {
    background-color: var(--card);
    border: 1.5px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    height: 360px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 20px;
}
.logo-card-back-box {
    background-color: var(--card-back);
    border: 1.5px solid var(--accent);
    border-radius: 12px;
    overflow: hidden;
    height: 360px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 16px;
    margin-bottom: 20px;
}
.card-image-box { height: 150px; background-color: #ffffff; display: flex; align-items: center; justify-content: center; padding: 12px; border-bottom: 1.5px solid var(--line); }
.card-image-box img { max-height: 120px; max-width: 90%; object-fit: contain; }
.card-content { padding: 12px 14px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
.card-title { font-family: "Space Grotesk", sans-serif; font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 6px; line-height: 1.25; }
.card-meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 11.5px; color: var(--muted); }
.card-meta-grid strong { color: var(--ink); }
.back-title { font-family: "Space Grotesk", sans-serif; font-size: 13px; font-weight: 700; color: var(--accent); border-bottom: 1px solid var(--line); padding-bottom: 4px; margin-bottom: 6px; }
.back-detail-row { font-size: 11.5px; margin-bottom: 4px; color: var(--muted); }
.back-detail-row strong { color: var(--ink); }
.back-symbolism { font-size: 11px; color: var(--ink); line-height: 1.4; background: rgba(0, 0, 0, 0.03); padding: 6px 8px; border-radius: 6px; border: 1px solid var(--line); max-height: 85px; overflow-y: auto; }

/* Analytics CSS */
.swatch { width: 14px; height: 14px; border-radius: 4px; border: 1px solid rgba(0,0,0,0.08); display: inline-block; margin-right: 7px; vertical-align: middle; }
.rr-kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
.kpi { background: var(--card); border: 1.5px solid var(--line); border-radius: 10px; padding: 14px 16px; }
.kpi-label { font-size: 11px; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 6px; }
.kpi-value { font-family: "Space Grotesk", sans-serif; font-size: 22px; font-weight: 700; color: var(--ink); }
.kpi-sub { font-size: 12px; color: var(--muted); margin-top: 2px; }
.rr-charts { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.chart-card { background: var(--card); border: 1.5px solid var(--line); border-radius: 12px; padding: 18px 20px; }
.chart-title { font-family: "Space Grotesk", sans-serif; font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 14px; }
.bar-row { display: grid; grid-template-columns: 110px 1fr 40px; align-items: center; gap: 10px; margin-bottom: 10px; font-size: 12.5px; }
.bar-label { display: flex; align-items: center; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-track { background: var(--bg); border: 1px solid var(--line); border-radius: 5px; height: 14px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 5px 0 0 5px; background: var(--accent); }
.bar-pct { text-align: right; color: var(--muted); font-weight: 600; }
.full-width-card { grid-column: 1 / -1; }
.crosstab { display: grid; gap: 0; font-size: 12px; }
.crosstab .ct-cell { padding: 8px 6px; border-bottom: 1px solid var(--line); display: flex; align-items: center; }
.crosstab .ct-head { font-weight: 700; color: var(--muted); font-size: 11px; text-transform: uppercase; border-bottom: 1.5px solid var(--ink); }
.ct-row-label { font-weight: 600; color: var(--ink); }
.heat { justify-content: center; border-radius: 4px; margin: 3px; font-weight: 700; color: var(--ink); display: flex; }

[data-testid="stSidebar"] { background-color: var(--bg); }
</style>
""", unsafe_allow_html=True)

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
    st.error(f"Error loading live dataset: {e}")
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
    "black": "#1a1a1a", "white": "#e8e8e8", "blue": "#2451c9", "red": "#c0392b",
    "green": "#1e9e5a", "yellow": "#e8b923", "orange": "#e07b39", "purple": "#8e44ad",
    "pink": "#e75f95", "teal": "#159e96", "grey": "#9aa0a6", "gray": "#9aa0a6",
    "brown": "#8a5a3c", "navy": "#1f2a5e", "maroon": "#6e1f2a", "gold": "#c9a227",
    "silver": "#b8bcc2", "cyan": "#22b6c9", "magenta": "#c23aa0",
}

def color_to_hex(name):
    return COLOR_HEX_MAP.get(str(name).strip().lower(), "#6366f1")

def top_value_pct(dataframe, col_name):
    if dataframe.empty or col_name not in dataframe.columns:
        return None, 0
    vals = dataframe[col_name].dropna().astype(str).str.strip()
    vals = vals[~vals.str.lower().isin(["", "nan", "n/a", "none"])]
    if len(vals) == 0:
        return None, 0
    counts = vals.value_counts()
    if len(counts) == 0:
        return None, 0
    return counts.index[0], round(100 * counts.iloc[0] / len(dataframe))

def top_colors(dataframe, color_cols_list, max_n=5):
    counts = {}
    for _, row in dataframe.iterrows():
        row_colors = set()
        for c in color_cols_list:
            if c in dataframe.columns:
                v = str(row.get(c, "")).strip()
                if v and v.lower() not in ["", "nan", "n/a"] and not v.startswith("#"):
                    row_colors.add(v)
        for v in row_colors:
            counts[v] = counts.get(v, 0) + 1
    total = len(dataframe) if len(dataframe) > 0 else 1
    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:max_n]
    return [(name, round(100 * count / total)) for name, count in ranked]

def top_n_value_pct(dataframe, col_name, n=6):
    if dataframe.empty or col_name not in dataframe.columns:
        return []
    vals = dataframe[col_name].dropna().astype(str).str.strip()
    vals = vals[~vals.str.lower().isin(["", "nan", "n/a", "none"])]
    if len(vals) == 0:
        return []
    counts = vals.value_counts().head(n)
    total = len(dataframe)
    return [(idx, round(100 * cnt / total)) for idx, cnt in counts.items()]

def _bar_rows_html(items, with_swatch=False):
    parts = []
    for name, pct in items:
        swatch = f'<span class="swatch" style="background:{color_to_hex(name)}"></span>' if with_swatch else ""
        parts.append(
            f'<div class="bar-row"><div class="bar-label">{swatch}{name}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%;"></div></div>'
            f'<div class="bar-pct">{pct}%</div></div>'
        )
    return "".join(parts) if parts else '<div style="font-size:12px; color:var(--muted);">No data in this selection.</div>'

# SIDEBAR ARCHITECTURE
with st.sidebar:
    st.markdown('<h1 class="sidebar-title">Logo Landscape</h1>', unsafe_allow_html=True)
    
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "Gallery"
        
    view_selection = st.radio("View Mode", options=["Gallery", "Analytics"], horizontal=True, label_visibility="collapsed", index=0 if st.session_state.view_mode == "Gallery" else 1)
    if view_selection != st.session_state.view_mode:
        st.session_state.view_mode = view_selection
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1.2], vertical_alignment="center")
    with col1:
        st.markdown("### Filters")
    with col2:
        if st.button("🧹", help="Reset all filters", use_container_width=True):
            reset_filters()
            st.rerun()

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

    def get_options_multi(col_names):
        values = set()
        for col_name in col_names:
            if col_name in df.columns:
                for x in df[col_name].dropna().unique():
                    x = str(x).strip()
                    if x and x.lower() not in ["nan", "n/a"] and not x.startswith("#"):
                        values.add(x)
        return sorted(values)

    search_query = st.text_input("⌕ Search organisation...", "")

    # CATEGORY 1
    with st.expander("🏢 Organization & Location"):
        with st.form("form_org", border=False):
            st.markdown('<p class="filter-subhead">Sector</p>', unsafe_allow_html=True)
            sec_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['sectors'], key=f"sec_{opt}") for opt in get_options(sector_col)}
            
            st.markdown('<p class="filter-subhead">Organization Type</p>', unsafe_allow_html=True)
            org_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['org_types'], key=f"org_{opt}") for opt in get_options(org_type_col)}
            
            st.markdown('<p class="filter-subhead">Country</p>', unsafe_allow_html=True)
            cntry_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['countries'], key=f"cntry_{opt}") for opt in get_options(country_col)}
            
            if st.form_submit_button("Apply"):
                st.session_state.applied_filters['sectors'] = [k for k, v in sec_checks.items() if v]
                st.session_state.applied_filters['org_types'] = [k for k, v in org_checks.items() if v]
                st.session_state.applied_filters['countries'] = [k for k, v in cntry_checks.items() if v]
                st.rerun()

    # CATEGORY 2
    with st.expander("📐 Logo Details & Design"):
        with st.form("form_design", border=False):
            st.markdown('<p class="filter-subhead">Type of Logo</p>', unsafe_allow_html=True)
            type_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['type_logo'], key=f"type_{opt}") for opt in get_options(type_of_logo_col)}
            
            st.markdown('<p class="filter-subhead">Shape (Primary Form)</p>', unsafe_allow_html=True)
            shape_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['shapes'], key=f"shape_{opt}") for opt in get_options(primary_form_col)}
            
            st.markdown('<p class="filter-subhead">Complexity</p>', unsafe_allow_html=True)
            comp_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['complexity'], key=f"comp_{opt}") for opt in get_options(complexity_col)}
            
            st.markdown('<p class="filter-subhead">Symmetry</p>', unsafe_allow_html=True)
            sym_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['symmetry'], key=f"sym_{opt}") for opt in get_options(symmetry_col)}
            
            if st.form_submit_button("Apply"):
                st.session_state.applied_filters['type_logo'] = [k for k, v in type_checks.items() if v]
                st.session_state.applied_filters['shapes'] = [k for k, v in shape_checks.items() if v]
                st.session_state.applied_filters['complexity'] = [k for k, v in comp_checks.items() if v]
                st.session_state.applied_filters['symmetry'] = [k for k, v in sym_checks.items() if v]
                st.rerun()

    # CATEGORY 3
    with st.expander("🎨 Colors"):
        with st.form("form_colors", border=False):
            st.markdown('<p class="filter-subhead">Color Family</p>', unsafe_allow_html=True)
            fam_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['colors_family'], key=f"fam_{opt}") for opt in get_options(color_family_col)}
            
            st.markdown('<p class="filter-subhead">Color Undertone</p>', unsafe_allow_html=True)
            under_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['undertones'], key=f"under_{opt}") for opt in get_options(undertone_col)}
            
            st.markdown('<p class="filter-subhead">Color Contains</p>', unsafe_allow_html=True)
            col_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['colors_combined'], key=f"col_{opt}") for opt in get_options_multi(color_cols)}
            
            if st.form_submit_button("Apply"):
                st.session_state.applied_filters['colors_family'] = [k for k, v in fam_checks.items() if v]
                st.session_state.applied_filters['undertones'] = [k for k, v in under_checks.items() if v]
                st.session_state.applied_filters['colors_combined'] = [k for k, v in col_checks.items() if v]
                st.rerun()

    # CATEGORY 4
    with st.expander("✍️ Type Style"):
        with st.form("form_type", border=False):
            st.markdown('<p class="filter-subhead">Case Type</p>', unsafe_allow_html=True)
            case_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['case_types'], key=f"case_{opt}") for opt in get_options(case_type_col)}
            
            st.markdown('<p class="filter-subhead">Type Classification</p>', unsafe_allow_html=True)
            class_checks = {opt: st.checkbox(opt, value=opt in st.session_state.applied_filters['type_class'], key=f"class_{opt}") for opt in get_options(type_class_col)}
            
            if st.form_submit_button("Apply"):
                st.session_state.applied_filters['case_types'] = [k for k, v in case_checks.items() if v]
                st.session_state.applied_filters['type_class'] = [k for k, v in class_checks.items() if v]
                st.rerun()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("🔄 Sync Google Sheets", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ----------------- FILTER LOGIC (AND across categories, OR within) -----------------
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

if af['colors_combined']:
    present_color_cols = [c for c in color_cols if c in df.columns]
    if present_color_cols:
        selected_set = set(s.strip() for s in af['colors_combined'])
        def row_color_set(row):
            vals = set()
            for c in present_color_cols:
                v = str(row.get(c, "")).strip()
                if v and v.lower() not in ["nan", "n/a"] and not v.startswith("#"):
                    vals.add(v)
            return vals
        keep_mask = filtered_df.apply(lambda r: selected_set.issubset(row_color_set(r)), axis=1)
        filtered_df = filtered_df[keep_mask]

if af['case_types'] and case_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[case_type_col].astype(str).str.strip().isin(af['case_types'])]
if af['type_class'] and type_class_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_class_col].astype(str).str.strip().isin(af['type_class'])]

colormix = top_colors(filtered_df, color_cols, max_n=6)

# Session state tracker for exclusive card flipping
if "flipped_card_idx" not in st.session_state:
    st.session_state.flipped_card_idx = None

# TOP MAIN BAR
st.markdown(
    f'<div class="topbar-container">'
    f'<div class="topbar-subtitle">Visual Identity Research</div>'
    f'<div class="top-meta"><strong>{len(df)}</strong> Identities</div>'
    f'</div>', 
    unsafe_allow_html=True
)

# EDITORIAL SUMMARY
headline_label, headline_value, headline_pct = "Logos in view", str(len(filtered_df)), None
if not af['colors_combined']:
    top = top_colors(filtered_df, color_cols, max_n=1)
    if top: 
        headline_value, headline_pct, headline_label = top[0][0], top[0][1], "Dominant Color"

headline_desc = f"{headline_pct}% of selected logos share this trait." if headline_pct else f"Out of {len(df)} total dataset entries."

sector_top, sector_pct = top_value_pct(filtered_df, sector_col)
family_top, family_pct = top_value_pct(filtered_df, color_family_col)
country_nunique = filtered_df[country_col].astype(str).str.strip().replace("", pd.NA).dropna().nunique() if country_col in filtered_df.columns else 0

editorial_html = (
    f'<div class="editorial-wrap">'
    f'<div class="editorial-hero">'
    f'<div class="editorial-eyebrow">{headline_label}</div>'
    f'<div class="editorial-number">{headline_value}</div>'
    f'<div class="editorial-desc">{headline_desc}</div>'
    f'</div>'
    f'<div class="editorial-list">'
    f'<div class="editorial-row"><div class="editorial-row-label">Filtered Logos</div><div class="editorial-row-value">{len(filtered_df)}</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Leading Sector<span class="editorial-sub">{sector_top or "—"}</span></div><div class="editorial-row-value">{sector_pct}%</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Primary Color Family<span class="editorial-sub">{family_top or "—"}</span></div><div class="editorial-row-value">{family_pct}%</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Countries Represented</div><div class="editorial-row-value">{country_nunique}</div></div>'
    f'</div>'
    f'</div>'
)

palette_items_html = "".join([
    f'<div class="palette-item"><span class="palette-swatch" style="background:{color_to_hex(name)}"></span><span class="palette-name">{name}</span></div>'
    for name, pct in colormix
]) if colormix else '<div style="font-size:12px; color:var(--muted);">No color data</div>'

palette_bar_html = f'<div class="palette-bar-container"><div class="palette-title">Palette</div><div class="palette-items">{palette_items_html}</div></div>'

with st.expander("Editorial Summary", expanded=False):
    st.markdown(editorial_html, unsafe_allow_html=True)
    st.markdown(palette_bar_html, unsafe_allow_html=True)


# DYNAMIC FILTER CHIPS ROW
active_chips = [(cat, val) for cat, vals in af.items() for val in vals]

if active_chips:
    st.markdown('<div class="chip-row-container">', unsafe_allow_html=True)
    chip_cols = st.columns(len(active_chips) + 1, vertical_alignment="center")
    
    for i, (cat, val) in enumerate(active_chips):
        with chip_cols[i]:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(f"{val} ✕", key=f"chip_{cat}_{val}"):
                st.session_state.applied_filters[cat].remove(val)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    with chip_cols[-1]:
        st.markdown('<div class="clear-all-btn">', unsafe_allow_html=True)
        if st.button("Clear All"):
            reset_filters()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<p style="font-size:12.5px; color:var(--muted); font-weight:600; margin-bottom:18px;">{len(filtered_df)} Results</p>', unsafe_allow_html=True)

# ---------------------- ANALYTICS VIEW ----------------------
def render_analytics_page():
    kpi_countries = (
        filtered_df[country_col].astype(str).str.strip().replace("", pd.NA).dropna().nunique()
        if country_col in filtered_df.columns else 0
    )
    top_color_list = top_colors(filtered_df, color_cols, max_n=1)
    top_color_name, top_color_pct = top_color_list[0] if top_color_list else ("—", 0)

    top_complexity_list = top_n_value_pct(filtered_df, complexity_col, n=1)
    top_complexity_name, top_complexity_pct = top_complexity_list[0] if top_complexity_list else ("—", 0)

    color_dist = top_colors(filtered_df, color_cols, max_n=8)
    sector_dist = top_n_value_pct(filtered_df, sector_col, n=6)
    country_dist = top_n_value_pct(filtered_df, country_col, n=6)

    crosstab_html = '<div style="font-size:12px; color:var(--muted);">Not enough data for a cross-tab in this selection.</div>'
    top_families = [name for name, _ in top_n_value_pct(filtered_df, color_family_col, n=4)]
    top_sectors_ct = [name for name, _ in top_n_value_pct(filtered_df, sector_col, n=4)]
    if top_families and top_sectors_ct and color_family_col in filtered_df.columns and sector_col in filtered_df.columns:
        sub = filtered_df[
            filtered_df[color_family_col].astype(str).str.strip().isin(top_families)
            & filtered_df[sector_col].astype(str).str.strip().isin(top_sectors_ct)
        ]
        if not sub.empty:
            ct = pd.crosstab(
                sub[color_family_col].astype(str).str.strip(),
                sub[sector_col].astype(str).str.strip(),
                normalize="columns"
            ) * 100
            ct = ct.reindex(index=top_families, columns=top_sectors_ct, fill_value=0)

            head_cells = "".join(f'<div class="ct-cell ct-head">{s}</div>' for s in top_sectors_ct)
            rows_html = ""
            for fam in top_families:
                row_html = f'<div class="ct-cell ct-row-label">{fam}</div>'
                for sec in top_sectors_ct:
                    val = round(ct.loc[fam, sec]) if fam in ct.index and sec in ct.columns else 0
                    opacity = max(0.08, min(0.85, val / 100))
                    row_html += f'<div class="ct-cell"><div class="heat" style="background:rgba(99,102,241,{opacity}); width:100%; padding:5px 0;">{val}%</div></div>'
                rows_html += row_html
            crosstab_html = (
                f'<div class="crosstab" style="grid-template-columns: 130px repeat({len(top_sectors_ct)}, 1fr);">'
                f'<div class="ct-cell ct-head"></div>{head_cells}{rows_html}</div>'
            )

    html = (
        f'<div class="rr-kpis">'
        f'<div class="kpi"><div class="kpi-label">Logos</div><div class="kpi-value">{len(filtered_df)}</div><div class="kpi-sub">of {len(df)} total</div></div>'
        f'<div class="kpi"><div class="kpi-label">Countries</div><div class="kpi-value">{kpi_countries}</div><div class="kpi-sub">in current filter</div></div>'
        f'<div class="kpi"><div class="kpi-label">Top Color</div><div class="kpi-value">{top_color_name}</div><div class="kpi-sub">{top_color_pct}% of set</div></div>'
        f'<div class="kpi"><div class="kpi-label">Typical Complexity</div><div class="kpi-value">{top_complexity_name}</div><div class="kpi-sub">{top_complexity_pct}% of logos</div></div>'
        f'</div>'
        f'<div class="rr-charts">'
        f'<div class="chart-card"><div class="chart-title">Color Distribution</div>{_bar_rows_html(color_dist, with_swatch=True)}</div>'
        f'<div class="chart-card"><div class="chart-title">Sector Breakdown</div>{_bar_rows_html(sector_dist)}</div>'
        f'<div class="chart-card"><div class="chart-title">Country Breakdown</div>{_bar_rows_html(country_dist)}</div>'
        f'<div class="chart-card"><div class="chart-title">Color Family Breakdown</div>{_bar_rows_html(top_n_value_pct(filtered_df, color_family_col, n=6))}</div>'
        f'<div class="chart-card full-width-card"><div class="chart-title">Color Family &times; Sector</div>{crosstab_html}'
        f'<div style="font-size: 11.5px; color: var(--muted); margin-top: 14px;">Darker cells = a color family makes up a larger share of that sector\'s logos.</div></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

if st.session_state.view_mode == "Analytics":
    render_analytics_page()
    st.stop()


# ---------------------- GALLERY VIEW ----------------------
cols_per_row = 3
cols = st.columns(cols_per_row, gap="large")

for idx, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[idx % cols_per_row]
    with col:
        b_name = str(row.get(brand_col, "Unknown Brand")).strip()
        raw_img = str(row.get(img_col, "")).strip() if pd.notna(row.get(img_col, "")) else ""
        img_url = transform_image_url(raw_img)
        
        img_html = f'<img src="{img_url}" alt="{b_name}" />' if (img_url and img_url.startswith("http")) else '<div style="color: #a0aec0; font-size: 12px;">📷 Image unavailable</div>'
        
        p_form = str(row.get(primary_form_col, "—")).strip()
        c_family = str(row.get(color_family_col, "—")).strip()
        sector_val = str(row.get(sector_col, "—")).strip()
        cnt_val = str(row.get(country_col, "—")).strip()
        complexity_val = str(row.get(complexity_col, "—")).strip()
        symmetry_val = str(row.get(symmetry_col, "—")).strip()
        type_class = str(row.get(type_class_col, "—")).strip()
        symbolism_text = str(row.get(symbolism_col, "No symbolism recorded.")).strip()
        case_type_val = str(row.get(case_type_col, "—")).strip()

        is_flipped = (st.session_state.flipped_card_idx == idx)

        if not is_flipped:
            card_html = (
                f'<div class="logo-card-box">'
                f'<div>'
                f'<div class="card-image-box">{img_html}</div>'
                f'<div class="card-content">'
                f'<div class="card-title">{b_name}</div>'
                f'<div class="card-meta-grid">'
                f'<div>Shape: <strong>{p_form}</strong></div>'
                f'<div>Sector: <strong>{sector_val}</strong></div>'
                f'<div>Color: <strong>{c_family}</strong></div>'
                f'<div>Country: <strong>{cnt_val}</strong></div>'
                f'</div>'
                f'</div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button("TAP CARD TO FLIP DETAILS ↺", key=f"flip_btn_{idx}", use_container_width=True):
                st.session_state.flipped_card_idx = idx
                st.rerun()
        else:
            back_html = (
                f'<div class="logo-card-back-box">'
                f'<div>'
                f'<div class="back-title">{b_name}</div>'
                f'<div class="back-detail-row">Complexity: <strong>{complexity_val}</strong></div>'
                f'<div class="back-detail-row">Symmetry: <strong>{symmetry_val}</strong></div>'
                f'<div class="back-detail-row">Case Type: <strong>{case_type_val}</strong></div>'
                f'<div class="back-detail-row">Type Class: <strong>{type_class}</strong></div>'
                f'</div>'
                f'<div>'
                f'<div style="font-size:10px; font-weight:700; color:var(--accent); margin-bottom:2px; text-transform:uppercase;">Symbolism</div>'
                f'<div class="back-symbolism">{symbolism_text}</div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(back_html, unsafe_allow_html=True)
            if st.button("TAP CARD TO FLIP DETAILS ↺", key=f"unflip_btn_{idx}", use_container_width=True):
                st.session_state.flipped_card_idx = None
                st.rerun()
