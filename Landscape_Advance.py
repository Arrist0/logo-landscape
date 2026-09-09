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

# 2. CSS — clean research UI inspired by the provided Figma reference
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Space+Grotesk:wght@500;700&display=swap');
:root { --bg:#fff; --card:#f8f9fa; --ink:#1a1a1a; --muted:#6b6b6b; --line:#e2e5ea; --chip:#8a8a8a; }
* { transition:background-color .18s ease,border-color .18s ease; }
html,body,.stApp { background:var(--bg)!important; color:var(--ink); font-family:"DM Sans",sans-serif; }
[data-testid="stSidebar"] { background:#fff!important; border-right:1px solid var(--line); }
[data-testid="stSidebarContent"] { padding:0 24px 28px 24px; }
.sidebar-brand { font-family:"Space Grotesk",sans-serif; font-size:24px; font-weight:700; color:var(--ink); margin:0 0 16px 0; }
div[data-testid="stRadio"] > div[role="radiogroup"] { display:inline-flex; width:100%; max-width:182px; gap:0; padding:3px; border:1px solid var(--line); border-radius:999px; background:#f1f1f1; }
div[data-testid="stRadio"] label { flex:1; min-width:0; border-radius:999px!important; padding:7px 12px!important; margin:0!important; cursor:pointer; text-align:center; }
div[data-testid="stRadio"] label p { color:#555!important; font-size:12.5px!important; font-weight:500!important; margin:0!important; }
div[data-testid="stRadio"] label[data-checked="true"] { background:#6c6c6c!important; }
div[data-testid="stRadio"] label[data-checked="true"] p { color:#fff!important; font-weight:600!important; }
div[data-testid="stRadio"] span[data-baseweb="radio"] { display:none; }
.sidebar-divider { border-top:1px solid var(--line); margin:16px 0 18px 0; }
.sidebar-filter-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
.sidebar-filter-head h3 { margin:0; font-family:"Space Grotesk",sans-serif; font-size:16px; font-weight:700; }
.reset-wrap button { width:34px!important; min-height:34px!important; height:34px!important; padding:0!important; border-radius:50%!important; background:#f6f6f6!important; border:1px solid var(--line)!important; font-size:15px!important; }
[data-testid="stSidebar"] div[data-testid="stTextInput"] input { border:1px solid var(--line)!important; border-radius:8px!important; background:#fafafa!important; min-height:38px!important; font-size:12px!important; }
[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p { font-size:11px!important; color:#666!important; }
[data-testid="stSidebar"] details { border:1px solid var(--line)!important; border-radius:8px!important; margin:9px 0!important; background:#fff!important; overflow:hidden!important; }
[data-testid="stSidebar"] details summary { padding:10px 12px!important; font-size:12px!important; font-weight:600!important; color:#383838!important; }
[data-testid="stSidebar"] details summary:hover { background:#fafafa!important; }
[data-testid="stSidebar"] details > div { padding:8px 12px 12px 12px!important; }
[data-testid="stSidebar"] .stCheckbox { margin:0 0 3px 0!important; }
[data-testid="stSidebar"] .stCheckbox label p { font-size:12px!important; color:#4d4d4d!important; }
[data-testid="stSidebar"] .stCheckbox label { gap:7px!important; }
[data-testid="stSidebar"] .apply-btn button { width:auto!important; min-height:30px!important; height:30px!important; padding:2px 12px!important; border-radius:999px!important; border:1px solid #cfcfcf!important; background:#f7f7f7!important; color:#333!important; font-size:11px!important; font-weight:600!important; }
[data-testid="stSidebar"] .apply-btn button:hover { border-color:#999!important; background:#ededed!important; }
.main-topbar { display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid var(--line); padding:2px 0 8px 0; margin-bottom:10px; }
.main-topbar-title { font-size:13px; font-weight:600; color:#666; }
.main-topbar-count { font-size:12px; color:#777; }
[data-testid="stExpander"] { border:1px solid var(--line)!important; border-radius:8px!important; box-shadow:none!important; background:#fff!important; margin-bottom:8px!important; }
[data-testid="stExpander"] details summary { padding:10px 14px!important; }
[data-testid="stExpander"] details summary p { font-size:12px!important; font-weight:600!important; }
[data-testid="stExpander"] details > div { border-top:1px solid var(--line)!important; padding:14px!important; }
.editorial-mini-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.editorial-mini-item { border-right:1px solid var(--line); padding-right:12px; }
.editorial-mini-item:last-child { border-right:none; }
.editorial-mini-label { font-size:10px; color:#777; margin-bottom:4px; }
.editorial-mini-value { font-size:16px; font-family:"Space Grotesk",sans-serif; font-weight:700; color:#222; }
.editorial-mini-sub { font-size:10px; color:#888; margin-top:2px; }
.filter-status { display:flex; align-items:center; justify-content:space-between; min-height:34px; background:#efefef; border-radius:8px; padding:4px 6px; margin-bottom:7px; }
.filter-chip-label { font-size:11px; color:#8a8a8a; margin-right:2px; }
.result-sort-row { display:flex; align-items:center; justify-content:space-between; margin:7px 0 12px 0; }
.result-count-label { font-size:11px; color:#666; }
.chip-button button { min-height:28px!important; height:28px!important; border-radius:999px!important; background:#8a8a8a!important; color:#fff!important; border:0!important; padding:2px 11px!important; font-size:10.5px!important; font-weight:600!important; }
.clear-button button { min-height:28px!important; height:28px!important; padding:2px 9px!important; border:0!important; background:transparent!important; color:#333!important; font-size:10.5px!important; text-decoration:underline!important; }
/* Existing logo card architecture — preserve animations and proportions */
details.flip-card { width:100%; height:350px; margin-bottom:24px; perspective:1000px; outline:none; }
details.flip-card summary { list-style:none; cursor:pointer; width:100%; height:100%; }
details.flip-card summary::-webkit-details-marker { display:none; }
.flip-card-inner { position:relative; width:100%; height:100%; transition:transform .6s cubic-bezier(.4,0,.2,1),box-shadow .25s ease; transform-style:preserve-3d; border-radius:12px; }
details.flip-card:hover .flip-card-inner { transform:translateY(-4px); box-shadow:0 12px 24px rgba(99,102,241,.18); }
details.flip-card[open] .flip-card-inner { transform:rotateY(180deg); }
details.flip-card[open]:hover .flip-card-inner { transform:rotateY(180deg) translateY(-4px); }
.flip-card-front,.flip-card-back { position:absolute; width:100%; height:100%; -webkit-backface-visibility:hidden; backface-visibility:hidden; border-radius:12px; border:1.5px solid var(--line); overflow:hidden; }
.flip-card-front { background:var(--card); display:flex; flex-direction:column; }
.flip-card-back { background:#fff; color:var(--ink); transform:rotateY(180deg); padding:18px; display:flex; flex-direction:column; justify-content:space-between; border-color:#6366f1; }
.card-image-box { height:170px; background:#fff; display:flex; align-items:center; justify-content:center; padding:16px; border-bottom:1.5px solid var(--line); }
.card-image-box img { max-height:130px; max-width:90%; object-fit:contain; }
.card-front-content { padding:14px; display:flex; flex-direction:column; justify-content:space-between; flex-grow:1; }
.card-title { font-family:"Space Grotesk",sans-serif; font-size:15px; font-weight:700; color:var(--ink); margin-bottom:8px; line-height:1.25; }
.card-meta-grid { display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:12px; color:var(--muted); }
.card-meta-item strong { color:var(--ink); }
.flip-hint { font-size:10.5px; color:#6366f1; text-transform:uppercase; letter-spacing:.05em; font-weight:700; margin-top:10px; }
.back-title { font-family:"Space Grotesk",sans-serif; font-size:14px; font-weight:700; color:#6366f1; border-bottom:1px solid var(--line); padding-bottom:6px; margin-bottom:10px; }
.back-detail-row { font-size:12px; margin-bottom:6px; color:var(--muted); }
.back-detail-row strong { color:var(--ink); }
.back-symbolism { font-size:11.5px; color:var(--ink); line-height:1.45; background:rgba(0,0,0,.03); padding:8px 10px; border-radius:6px; border:1px solid var(--line); max-height:110px; overflow-y:auto; }
/* Analytics */
.swatch { width:14px; height:14px; border-radius:4px; border:1px solid rgba(0,0,0,.08); display:inline-block; margin-right:7px; vertical-align:middle; }
.rr-kpis { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:20px; }
.kpi { background:var(--card); border:1.5px solid var(--line); border-radius:10px; padding:14px 16px; }
.kpi-label { font-size:11px; font-weight:700; color:#666; text-transform:uppercase; letter-spacing:.05em; margin-bottom:6px; }
.kpi-value { font-family:"Space Grotesk",sans-serif; font-size:22px; font-weight:700; color:var(--ink); }
.kpi-sub { font-size:12px; color:var(--muted); margin-top:2px; }
.rr-charts { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.chart-card { background:var(--card); border:1.5px solid var(--line); border-radius:12px; padding:18px 20px; }
.chart-title { font-family:"Space Grotesk",sans-serif; font-size:14px; font-weight:700; color:var(--ink); margin-bottom:14px; }
.bar-row { display:grid; grid-template-columns:110px 1fr 40px; align-items:center; gap:10px; margin-bottom:10px; font-size:12.5px; }
.bar-row:last-child { margin-bottom:0; }
.bar-label { display:flex; align-items:center; color:var(--ink); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.bar-track { background:var(--bg); border:1px solid var(--line); border-radius:5px; height:14px; overflow:hidden; }
.bar-fill { height:100%; border-radius:5px 0 0 5px; background:#6366f1; }
.bar-pct { text-align:right; color:var(--muted); font-weight:600; }
.full-width-card { grid-column:1 / -1; }
.crosstab { display:grid; gap:0; font-size:12px; }
.crosstab .ct-cell { padding:8px 6px; border-bottom:1px solid var(--line); display:flex; align-items:center; color:var(--ink); }
.crosstab .ct-head { font-weight:700; color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:.04em; border-bottom:1.5px solid var(--ink); }
.ct-row-label { font-weight:600; }
.heat { justify-content:center; border-radius:4px; margin:3px; font-weight:700; color:var(--ink); display:flex; }
.rr-footnote { font-size:11.5px; color:var(--muted); margin-top:14px; line-height:1.5; }
@media (max-width:900px) { .editorial-mini-grid { grid-template-columns:1fr 1fr; } }
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
    if col_name not in dataframe.columns or dataframe.empty:
        return None, 0
    vals = dataframe[col_name].astype(str).str.strip()
    vals = vals[~vals.str.lower().isin(["", "nan", "n/a"])]
    if vals.empty:
        return None, 0
    counts = vals.value_counts()
    if counts.empty:
        return None, 0
    return counts.index[0], round(100 * counts.iloc[0] / len(dataframe))

def top_n_value_pct(dataframe, col_name, n=6):
    """Top-n (value, pct) pairs for a single column, ranked by frequency."""
    if col_name not in dataframe.columns or dataframe.empty:
        return []
    vals = dataframe[col_name].astype(str).str.strip()
    vals = vals[~vals.str.lower().isin(["", "nan", "n/a"])]
    if vals.empty:
        return []
    counts = vals.value_counts().head(n)
    total = len(dataframe)
    return [(idx, round(100 * cnt / total)) for idx, cnt in counts.items()]

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

def render_analytics_page(filtered_df, df, color_cols, sector_col, color_family_col, country_col, complexity_col):
    """Detailed, filter-aware analytics dashboard — KPIs, distribution charts,
    and a Color Family x Sector cross-tab. Built as flush-left HTML strings
    (no loop-concatenated multi-line blocks) so Streamlit's Markdown parser
    doesn't misread indented fragments as code blocks."""

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
    family_dist = top_n_value_pct(filtered_df, color_family_col, n=6)

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
        f'<div class="chart-card"><div class="chart-title">Color Family Breakdown</div>{_bar_rows_html(family_dist)}</div>'
        f'<div class="chart-card full-width-card"><div class="chart-title">Color Family &times; Sector (share within sector)</div>{crosstab_html}'
        f'<div class="rr-footnote">Darker cells = a color family makes up a larger share of that sector\'s logos. Recalculates live from your current filters.</div></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

# SIDEBAR — navigation, search, filters, and reset
brand_col = "Name"
img_col = "Logo"
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

FILTER_GROUPS = {
    "organization": {
        "label": "Organization & Location",
        "fields": {
            "Sector": ("sector", sector_col, get_options(sector_col)),
            "Organization Type": ("org_types", org_type_col, get_options(org_type_col)),
            "Country": ("countries", country_col, get_options(country_col)),
        },
    },
    "design": {
        "label": "Logo Details & Design",
        "fields": {
            "Type of Logo": ("type_logo", type_of_logo_col, get_options(type_of_logo_col)),
            "Shape (Primary Form)": ("shapes", primary_form_col, get_options(primary_form_col)),
            "Complexity": ("complexity", complexity_col, get_options(complexity_col)),
            "Symmetry": ("symmetry", symmetry_col, get_options(symmetry_col)),
        },
    },
    "colors": {
        "label": "Colors",
        "fields": {
            "Color Family": ("colors_family", color_family_col, get_options(color_family_col)),
            "Color Undertone": ("undertones", undertone_col, get_options(undertone_col)),
            "Color": ("colors_combined", "__multi_color__", get_options_multi(color_cols)),
        },
    },
    "type_style": {
        "label": "Type Style",
        "fields": {
            "Case Type": ("case_types", case_type_col, get_options(case_type_col)),
            "Type Classification": ("type_class", type_class_col, get_options(type_class_col)),
        },
    },
}

if "applied_filters" not in st.session_state:
    st.session_state.applied_filters = {key: {} for key in FILTER_GROUPS}
if "temp_filters" not in st.session_state:
    st.session_state.temp_filters = {key: {} for key in FILTER_GROUPS}
if "applied_exact_color_match" not in st.session_state:
    st.session_state.applied_exact_color_match = False
if "temp_exact_color_match" not in st.session_state:
    st.session_state.temp_exact_color_match = False
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "gallery"

# Keep checkbox widget states synchronized with the last applied values.
def _safe_key(text):
    return re.sub(r"[^a-zA-Z0-9]+", "_", str(text)).strip("_")[:90]

def sync_temp_widget_state(group_key):
    group_applied = st.session_state.applied_filters.get(group_key, {})
    for field_label, (state_key, _, options) in FILTER_GROUPS[group_key]["fields"].items():
        selected = set(group_applied.get(state_key, []))
        for option in options:
            widget_key = f"tmp__{group_key}__{state_key}__{_safe_key(option)}"
            if widget_key not in st.session_state:
                st.session_state[widget_key] = option in selected


def clear_all_filters():
    st.session_state.applied_filters = {key: {} for key in FILTER_GROUPS}
    st.session_state.temp_filters = {key: {} for key in FILTER_GROUPS}
    st.session_state.applied_exact_color_match = False
    st.session_state.temp_exact_color_match = False
    # Reset all checkbox values that have already been instantiated.
    for key in list(st.session_state.keys()):
        if str(key).startswith("tmp__"):
            st.session_state[key] = False
    st.rerun()


def apply_group(group_key):
    group_values = {}
    for field_label, (state_key, _, options) in FILTER_GROUPS[group_key]["fields"].items():
        selected = []
        for option in options:
            widget_key = f"tmp__{group_key}__{state_key}__{_safe_key(option)}"
            if st.session_state.get(widget_key, False):
                selected.append(option)
        group_values[state_key] = selected
    st.session_state.applied_filters[group_key] = group_values
    st.session_state.temp_filters[group_key] = {k: list(v) for k, v in group_values.items()}
    if group_key == "colors":
        st.session_state.applied_exact_color_match = st.session_state.temp_exact_color_match
    st.rerun()

with st.sidebar:
    st.markdown('<div class="sidebar-brand">Logo Landscape</div>', unsafe_allow_html=True)

    view_selection = st.radio(
        "View Mode",
        options=["Gallery", "Analytics"],
        horizontal=True,
        label_visibility="collapsed",
        index=0 if st.session_state.view_mode == "gallery" else 1,
    )
    if view_selection.lower() != st.session_state.view_mode:
        st.session_state.view_mode = view_selection.lower()
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    head_left, head_right = st.columns([4, 1], vertical_alignment="center")
    with head_left:
        st.markdown('<div class="sidebar-filter-head"><h3>Filters</h3></div>', unsafe_allow_html=True)
    with head_right:
        st.markdown('<div class="reset-wrap">', unsafe_allow_html=True)
        if st.button("↗", key="reset_all_filters", help="Reset filters", use_container_width=True):
            clear_all_filters()
        st.markdown('</div>', unsafe_allow_html=True)

    search_query = st.text_input("⌕ Search organisation...", "", key="search_organisation")

    for group_key, group in FILTER_GROUPS.items():
        sync_temp_widget_state(group_key)
        with st.expander(group["label"], expanded=(group_key == "organization")):
            for field_label, (state_key, _, options) in group["fields"].items():
                st.markdown(f'<div style="font-weight:700;font-size:12px;margin:8px 0 5px 0;color:#262626;">{field_label}</div>', unsafe_allow_html=True)
                for option in options:
                    widget_key = f"tmp__{group_key}__{state_key}__{_safe_key(option)}"
                    st.checkbox(option, key=widget_key)

            if group_key == "colors":
                st.checkbox("Exact match only (no extra colors)", key="temp_exact_color_match")

            st.markdown('<div class="apply-row"></div>', unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="apply-btn">', unsafe_allow_html=True)
                if st.button("Apply", key=f"apply__{group_key}"):
                    apply_group(group_key)
                st.markdown('</div>', unsafe_allow_html=True)

# Build the actively applied selections for filtering.
applied = st.session_state.applied_filters
selected_logo_types = applied["design"].get("type_logo", [])
selected_forms = applied["design"].get("shapes", [])
selected_complexity = applied["design"].get("complexity", [])
selected_symmetry = applied["design"].get("symmetry", [])
selected_families = applied["colors"].get("colors_family", [])
selected_undertones = applied["colors"].get("undertones", [])
selected_colors = applied["colors"].get("colors_combined", [])
selected_sectors = applied["organization"].get("sector", [])
selected_org_types = applied["organization"].get("org_types", [])
selected_countries = applied["organization"].get("countries", [])
selected_case_types = applied["type_style"].get("case_types", [])
selected_type_class = applied["type_style"].get("type_class", [])
exact_color_match = st.session_state.applied_exact_color_match

# Filter execution
filtered_df = df.copy()
if search_query and brand_col in df.columns:
    filtered_df = filtered_df[filtered_df[brand_col].astype(str).str.contains(search_query, case=False, na=False)]
if selected_logo_types and type_of_logo_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_of_logo_col].astype(str).str.strip().isin([s.strip() for s in selected_logo_types])]
if selected_forms and primary_form_col in df.columns:
    filtered_df = filtered_df[filtered_df[primary_form_col].astype(str).str.strip().isin([s.strip() for s in selected_forms])]
if selected_families and color_family_col in df.columns:
    filtered_df = filtered_df[filtered_df[color_family_col].astype(str).str.strip().isin([s.strip() for s in selected_families])]
if selected_undertones and undertone_col in df.columns:
    filtered_df = filtered_df[filtered_df[undertone_col].astype(str).str.strip().isin([s.strip() for s in selected_undertones])]
if selected_sectors and sector_col in df.columns:
    filtered_df = filtered_df[filtered_df[sector_col].astype(str).str.strip().isin([s.strip() for s in selected_sectors])]
if selected_org_types and org_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[org_type_col].astype(str).str.strip().str.lower().isin([s.strip().lower() for s in selected_org_types])]
if selected_countries and country_col in df.columns:
    filtered_df = filtered_df[filtered_df[country_col].astype(str).str.strip().isin([s.strip() for s in selected_countries])]
if selected_complexity and complexity_col in df.columns:
    filtered_df = filtered_df[filtered_df[complexity_col].astype(str).str.strip().isin([s.strip() for s in selected_complexity])]
if selected_symmetry and symmetry_col in df.columns:
    filtered_df = filtered_df[filtered_df[symmetry_col].astype(str).str.strip().isin([s.strip() for s in selected_symmetry])]
if selected_case_types and case_type_col in df.columns:
    filtered_df = filtered_df[filtered_df[case_type_col].astype(str).str.strip().isin([s.strip() for s in selected_case_types])]
if selected_type_class and type_class_col in df.columns:
    filtered_df = filtered_df[filtered_df[type_class_col].astype(str).str.strip().isin([s.strip() for s in selected_type_class])]

if selected_colors:
    present_color_cols = [c for c in color_cols if c in df.columns]
    if present_color_cols:
        selected_set = set(s.strip() for s in selected_colors)
        def row_color_set(row):
            vals = set()
            for c in present_color_cols:
                v = str(row.get(c, "")).strip()
                if v and v.lower() not in ["nan", "n/a"] and not v.startswith("#"):
                    vals.add(v)
            return vals
        # Multiple color choices behave as OR by default. Exact mode remains available when selected.
        if exact_color_match:
            keep_mask = filtered_df.apply(lambda r: row_color_set(r) == selected_set, axis=1)
        else:
            keep_mask = filtered_df.apply(lambda r: bool(row_color_set(r) & selected_set), axis=1)
        filtered_df = filtered_df[keep_mask]

colormix = top_colors(filtered_df, color_cols, max_n=6)

# Main View Render
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "gallery"

if st.session_state.view_mode == "analytics":
    st.markdown(
        f'<div class="main-topbar"><div class="main-topbar-title">Visual Identity Research</div><div class="main-topbar-count"><strong>{len(df)}</strong> Identities</div></div>',
        unsafe_allow_html=True,
    )
    render_analytics_page(filtered_df, df, color_cols, sector_col, color_family_col, country_col, complexity_col)
    st.stop()

# Main header: closely follows the Figma reference.
st.markdown(
    f'<div class="main-topbar"><div class="main-topbar-title">Visual Identity Research</div><div class="main-topbar-count"><strong>{len(df)}</strong> Identities</div></div>',
    unsafe_allow_html=True,
)

# Dynamic Editorial Summary — collapsed by default.
headline_top = top_colors(filtered_df, color_cols, max_n=1)
if headline_top:
    headline_value, headline_pct = headline_top[0]
    headline_desc = f"{headline_pct}% of the current selection shares this dominant color."
else:
    headline_value, headline_pct = "—", 0
    headline_desc = "No dominant color can be determined from the current selection."
sector_top, sector_pct = top_value_pct(filtered_df, sector_col)
family_top, family_pct = top_value_pct(filtered_df, color_family_col)
country_nunique = filtered_df[country_col].astype(str).str.strip().replace("", pd.NA).dropna().nunique() if country_col in filtered_df.columns else 0

with st.expander("Editorial Summary", expanded=False):
    st.markdown(
        f'<div class="editorial-mini-grid">'
        f'<div class="editorial-mini-item"><div class="editorial-mini-label">Dominant Color</div><div class="editorial-mini-value">{headline_value}</div><div class="editorial-mini-sub">{headline_desc}</div></div>'
        f'<div class="editorial-mini-item"><div class="editorial-mini-label">Filtered Logos</div><div class="editorial-mini-value">{len(filtered_df)}</div><div class="editorial-mini-sub">of {len(df)} total</div></div>'
        f'<div class="editorial-mini-item"><div class="editorial-mini-label">Leading Sector</div><div class="editorial-mini-value">{sector_top or "—"}</div><div class="editorial-mini-sub">{sector_pct}% of current selection</div></div>'
        f'<div class="editorial-mini-item"><div class="editorial-mini-label">Countries Represented</div><div class="editorial-mini-value">{country_nunique}</div><div class="editorial-mini-sub">within current selection</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# Applied filter chips. Each chip is individually removable.
chip_items = []
for group_key, group in FILTER_GROUPS.items():
    for field_label, (state_key, _, _) in group["fields"].items():
        for value in applied[group_key].get(state_key, []):
            chip_items.append((f"{value}", group_key, state_key, value))
if exact_color_match and selected_colors:
    chip_items.append(("Exact color", "colors", "__exact__", "__exact__"))

chip_bar_cols = st.columns([0.84, 0.16], vertical_alignment="center")
with chip_bar_cols[0]:
    chip_inner = st.columns(max(1, min(len(chip_items), 8)))
    if chip_items:
        for idx, (label, group_key, state_key, value) in enumerate(chip_items):
            col = chip_inner[idx % len(chip_inner)]
            with col:
                st.markdown('<div class="chip-button">', unsafe_allow_html=True)
                if st.button(f"{label}  ×", key=f"remove_chip__{group_key}__{state_key}__{_safe_key(value)}"):
                    if state_key == "__exact__":
                        st.session_state.applied_exact_color_match = False
                        st.session_state.temp_exact_color_match = False
                    else:
                        vals = list(st.session_state.applied_filters[group_key].get(state_key, []))
                        st.session_state.applied_filters[group_key][state_key] = [v for v in vals if v != value]
                        # Keep the corresponding temporary checkbox in sync.
                        widget_key = f"tmp__{group_key}__{state_key}__{_safe_key(value)}"
                        if widget_key in st.session_state:
                            st.session_state[widget_key] = False
                    st.session_state.temp_filters[group_key] = {k:list(v) for k,v in st.session_state.applied_filters[group_key].items()}
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:11px;color:#8a8a8a;padding:7px 10px;">No filters applied</div>', unsafe_allow_html=True)
with chip_bar_cols[1]:
    st.markdown('<div class="clear-button">', unsafe_allow_html=True)
    if st.button("Clear all", key="clear_all_filters"):
        clear_all_filters()
    st.markdown('</div>', unsafe_allow_html=True)

# Result count and sort control.
sort_col, count_col = st.columns([1, 5], vertical_alignment="center")
with sort_col:
    sort_option = st.selectbox("Sort", ["Name A–Z", "Name Z–A"], index=0, label_visibility="collapsed", key="sort_option")
with count_col:
    st.markdown(f'<div class="result-count-label">{len(filtered_df)} Results</div>', unsafe_allow_html=True)

if brand_col in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=brand_col, ascending=(sort_option == "Name A–Z"), key=lambda s: s.astype(str).str.lower())

colormix = top_colors(filtered_df, color_cols, max_n=6)

# CLICK-TO-FLIP CARDS USING NATIVE HTML <details>
# All cards share the same `name` attribute, which makes the browser treat
# them as one exclusive group — opening one automatically closes any other
# open card. Native HTML behavior, no JS needed. (Requires a modern browser:
# Chrome/Edge/Firefox recent versions, Safari 17+.)
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

        card_html = (
            f'<details class="flip-card" name="logo-flip-group">'
            f'<summary>'
            f'<div class="flip-card-inner">'
            f'<div class="flip-card-front">'
            f'<div class="card-image-box">{img_html}</div>'
            f'<div class="card-front-content">'
            f'<div class="card-title">{b_name}</div>'
            f'<div class="card-meta-grid">'
            f'<div class="card-meta-item">Shape: <strong>{p_form}</strong></div>'
            f'<div class="card-meta-item">Sector: <strong>{sector_val}</strong></div>'
            f'<div class="card-meta-item">Color: <strong>{c_family}</strong></div>'
            f'<div class="card-meta-item">Country: <strong>{cnt_val}</strong></div>'
            f'</div>'
            f'<div class="flip-hint">Tap card to flip details ↺</div>'
            f'</div>'
            f'</div>'
            f'<div class="flip-card-back">'
            f'<div>'
            f'<div class="back-title">{b_name}</div>'
            f'<div class="back-detail-row">Complexity: <strong>{complexity_val}</strong></div>'
            f'<div class="back-detail-row">Symmetry: <strong>{symmetry_val}</strong></div>'
            f'<div class="back-detail-row">Case Type: <strong>{case_type_val}</strong></div>'
            f'<div class="back-detail-row">Type Class: <strong>{type_class}</strong></div>'
            f'</div>'
            f'<div>'
            f'<div style="font-size:11px; font-weight:700; color:var(--accent); margin-bottom:4px;">SYMBOLISM</div>'
            f'<div class="back-symbolism">{symbolism_text}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
            f'</summary>'
            f'</details>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
