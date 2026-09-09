html_summary = (
    f'<div class="editorial-wrap">'
    f'<div class="editorial-hero">'
    f'<div class="editorial-eyebrow">{headline_label}</div>'
    f'<div class="editorial-number">{headline_value}</div>'
    f'<div class="editorial-desc">{headline_desc}</div>'
    f'<div class="editorial-colormix">'
    f'<div class="editorial-colormix-title">Color Mix</div>'
    f'<div class="editorial-colormix-rings">{colormix_rings}</div>'
    f'</div>'
    f'</div>'
    f'<div class="editorial-list">'
    f'<div class="editorial-row"><div class="editorial-row-label">Results in view<span class="editorial-sub">of {len(df)} total logos</span></div><div class="editorial-row-value">{len(filtered_df)}</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Leading sector<span class="editorial-sub">{sector_top or "—"}</span></div><div class="editorial-row-value">{sector_pct}%</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Leading color family<span class="editorial-sub">{family_top or "—"}</span></div><div class="editorial-row-value">{family_pct}%</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Countries represented</div><div class="editorial-row-value">{country_nunique}</div></div>'
    f'<div class="editorial-row"><div class="editorial-row-label">Typical complexity<span class="editorial-sub">{complexity_top or "—"}</span></div><div class="editorial-row-value">{complexity_pct}%</div></div>'
    f'</div>'
    f'</div>'
)

st.markdown(html_summary, unsafe_allow_html=True)
