"""
Styles Module — Dashboard SM CGR 2026
=======================================
Complete CSS for the executive dark-mode dashboard.
Includes glassmorphism, animations, responsive breakpoints,
and WCAG AA-compliant contrast ratios.
"""

from __future__ import annotations


def _get_css_base() -> str:
    """Return the base custom CSS for the dashboard (design tokens, global
    element overrides, cards, KPIs, charts, tables, sidebar, etc.)."""
    return """
    <style>
    /* ================================================================
       GOOGLE FONTS — Inter
       ================================================================ */

    /* ================================================================
       ROOT VARIABLES
       ================================================================ */
    :root {
        /* Paleta Roxo Moderno + Branco */
        --bg-primary: #0F0A1F;
        --bg-card: #1A1433;
        --bg-sidebar: #120D28;
        --bg-card-hover: #241C40;
        --border-color: rgba(124, 58, 237, 0.2);
        --border-glow: rgba(124, 58, 237, 0.35);

        --purple: #7C3AED;
        --purple-light: #A78BFA;
        --purple-dark: #5B21B6;
        --accent: #C026D3;

        --blue: #6366F1;
        --cyan: #22D3EE;
        --green: #34D399;
        --orange: #F59E0B;
        --red: #F87171;
        --pink: #F472B6;

        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;

        --radius-sm: 12px;
        --radius-md: 16px;
        --radius-lg: 24px;

        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
        --shadow-glow-purple: 0 0 20px rgba(124, 58, 237, 0.25);
    }

    /* ================================================================
       GLOBAL OVERRIDES
       ================================================================ */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        width: calc(100% - 2rem) !important;
        max-width: 1680px;
        margin: 0 auto !important;
        box-sizing: border-box !important;
    }

    /* Hide default Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: rgba(19, 10, 43, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(139, 92, 246, 0.15) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #170E33 0%, #130A2B 100%) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.18) !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Multiselect auto-close effect with CSS */
    section[data-testid="stSidebar"] [data-baseweb="select"] > div > div {
        transition: opacity 0.3s ease, max-height 0.3s ease !important;
    }

    /* V11 Visual Polish - Enhanced Cards & Hierarchy */
    .stCard, div[data-testid="stExpander"] {
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-card) !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stCard:hover {
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15) !important;
        transform: translateY(-2px);
    }

    /* Improved Typography */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
    }

    .subtitle {
        color: var(--text-secondary) !important;
        font-size: 1.05rem !important;
        margin-top: -8px !important;
    }

    /* Data Quality Indicators */
    .quality-good { color: #34D399; font-weight: 600; }
    .quality-warning { color: #FBBF24; font-weight: 600; }
    .quality-poor { color: #F87171; font-weight: 600; }

    /* ================================================================
       COLUMN RESPONSIVE BEHAVIOR + ELEGANT SPACING
       ================================================================ */
    div[data-testid="stHorizontalBlock"] {
        gap: 1.25rem !important;  /* Increased for breathing room & elegance */
        flex-wrap: wrap !important;
        align-items: stretch !important;
    }

    /* Consistent vertical spacing for stacked sections */
    .main .block-container > div[data-testid="stVerticalBlock"] {
        gap: 1.1rem !important;
    }

    @media (max-width: 1280px) {
        div[data-testid="stHorizontalBlock"] {
            gap: 1rem !important;
        }
    }

    @media (max-width: 1024px) {
        div[data-testid="stHorizontalBlock"] {
            gap: 0.85rem !important;
        }
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }

    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            gap: 0.65rem !important;
        }
        
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.35rem !important;
        }
        
        .main .block-container {
            padding-top: 0.6rem !important;
            padding-bottom: 1.25rem !important;
        }
    }

    @media (max-width: 480px) {
        div[data-testid="stHorizontalBlock"] {
            gap: 0.5rem !important;
        }
        .kpi-card {
            padding: 1rem 1.15rem !important;
        }
        .dq-header {
            flex-wrap: wrap;
            gap: 0.4rem;
        }
        .dq-badge {
            font-size: 0.65rem;
        }
    }

    /* Extra small screens (phones in portrait) */
    @media (max-width: 360px) {
        .main .block-container {
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }
        .kpi-value {
            font-size: 1.35rem !important;
        }
        .dq-title {
            font-size: 0.85rem;
        }
    }

    /* Ensure charts and sparklines scale well */
    .stPlotlyChart, .stAltairChart {
        width: 100% !important;
        max-width: 100% !important;
    }

    .kpi-sparkline svg {
        max-width: 100%;
        height: auto;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div {
        flex: 1;
        min-height: 100%;
    }

    /* ================================================================
       TEXT & TITLE SAFETY — Prevent cutoffs everywhere
       ================================================================ */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown p, .stText,
    .header-title, .header-subtitle,
    .kpi-card, .kpi-card * {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }

    /* Plotly titles (SVG) - ensure wrapping from our <br> logic shows correctly */
    .js-plotly-plot .plotly .gtitle {
        white-space: pre-line !important;
    }

    /* Subheader and caption polish */
    .stSubheader {
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }

    /* ================================================================
       ANIMATIONS
       ================================================================ */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ================================================================
       PREMIUM CHART ANIMATIONS (Plotly + Altair)
       ================================================================ */
    @keyframes chartFadeScaleIn {
        from {
            opacity: 0;
            transform: scale(0.985) translateY(12px);
            filter: blur(1px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
            filter: blur(0);
        }
    }

    @keyframes chartHoverLift {
        from { transform: translateY(0); box-shadow: 0 4px 20px rgba(0,0,0,0.25); }
        to { transform: translateY(-3px); box-shadow: 0 14px 35px rgba(0,0,0,0.35), 0 0 0 1px rgba(37,99,235,0.15); }
    }

    /* Plotly Chart Containers - smooth entrance + elegant hover */
    .stPlotlyChart {
        animation: chartFadeScaleIn 0.55s cubic-bezier(0.23, 1, 0.32, 1) both;
        border-radius: var(--radius-md);
        overflow: hidden;
        transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 1),
                    box-shadow 0.25s cubic-bezier(0.23, 1, 0.32, 1);
        will-change: transform, box-shadow;
    }

    .stPlotlyChart:hover {
        animation: chartHoverLift 0.25s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }

    /* Altair Chart Containers - match the premium dark executive feel */
    .stAltairChart {
        animation: chartFadeScaleIn 0.6s cubic-bezier(0.23, 1, 0.32, 1) both;
        border-radius: var(--radius-md);
        overflow: hidden;
        background: var(--bg-card);
        border: 1px solid rgba(37, 99, 235, 0.12);
        padding: 0.5rem;
        transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 1),
                    box-shadow 0.25s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .stAltairChart:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3), var(--shadow-glow-blue);
    }

    /* Subtle polish on Plotly modebar and internal elements */
    .js-plotly-plot .plotly .modebar {
        transition: opacity 0.2s ease;
        background: rgba(15, 23, 42, 0.85) !important;
        border-radius: 8px;
    }

    .js-plotly-plot .plotly:hover .modebar {
        opacity: 1 !important;
    }

    /* Altair tooltip and selection polish (dark theme friendly) */
    .stAltairChart .vega-tooltip {
        background: #0F172A !important;
        border: 1px solid rgba(37, 99, 235, 0.3) !important;
        color: #F1F5F9 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        border-radius: 8px;
        font-family: 'Inter', sans-serif !important;
    }

    /* Data Quality Card - Enriching executive component */
    .data-quality-card {
        background: linear-gradient(145deg, #111827 0%, #0f1520 100%);
        border: 1px solid rgba(37, 99, 235, 0.2);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin: 0.75rem 0 1.25rem;
        position: relative;
    }
    .data-quality-card.green { border-color: rgba(16, 185, 129, 0.35); }
    .data-quality-card.orange { border-color: rgba(245, 158, 11, 0.4); }
    .data-quality-card.red { border-color: rgba(220, 38, 38, 0.35); }

    .dq-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.6rem;
    }
    .dq-icon { font-size: 1.1rem; }
    .dq-title { font-weight: 700; font-size: 0.95rem; color: #F1F5F9; flex: 1; }
    .dq-badge {
        background: rgba(148, 163, 184, 0.15);
        color: #CBD5E1;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.12rem 0.5rem;
        border-radius: 999px;
    }

    /* SHADCN-STYLE COMPONENTS */
    .shad-card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.25rem;
        transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .shad-card:hover {
        border-color: rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .shad-card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .shad-card-title {
        font-weight: 600;
        font-size: 1.05rem;
        color: #F1F5F9;
    }
    .shad-card-content {
        color: #CBD5E1;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ========================================================================
       ADVANCED CSS ANIMATIONS (Pure CSS - High Performance)
       ======================================================================== */

    /* Staggered entrance for lists/grids */
    .animate-stagger > * {
        opacity: 0;
        animation: fadeInUpStagger 0.5s ease-out forwards;
    }
    .animate-stagger > *:nth-child(1) { animation-delay: 0.05s; }
    .animate-stagger > *:nth-child(2) { animation-delay: 0.1s; }
    .animate-stagger > *:nth-child(3) { animation-delay: 0.15s; }
    .animate-stagger > *:nth-child(4) { animation-delay: 0.2s; }
    .animate-stagger > *:nth-child(5) { animation-delay: 0.25s; }

    @keyframes fadeInUpStagger {
        from {
            opacity: 0;
            transform: translateY(25px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Attention animation for important elements */
    .animate-attention {
        animation: attentionPulse 2s ease-in-out infinite;
    }

    @keyframes attentionPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }

    /* Premium lift + glow on hover */
    .animate-lift-glow {
        transition: transform 0.3s cubic-bezier(0.23, 1, 0.32, 1),
                    box-shadow 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .animate-lift-glow:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3),
                    0 0 0 1px rgba(37, 99, 235, 0.2);
    }

    /* Enhanced Shimmer Loading */
    .animate-shimmer {
        background: linear-gradient(
            90deg,
            rgba(255,255,255,0.03) 25%,
            rgba(255,255,255,0.12) 50%,
            rgba(255,255,255,0.03) 75%
        );
        background-size: 200% 100%;
        animation: shimmerAdvanced 2s linear infinite;
    }

    @keyframes shimmerAdvanced {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* Smooth expand animation */
    .animate-expand {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s cubic-bezier(0.23, 1, 0.32, 1),
                    opacity 0.3s ease;
        opacity: 0;
    }
    .animate-expand.open {
        max-height: 500px;
        opacity: 1;
    }

    .shad-alert {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border: 1px solid;
        margin: 1rem 0;
    }

    .shad-metric {
        padding: 0.25rem 0;
    }

    /* Additional Shadcn Components */
    .shad-progress-container {
        margin: 0.75rem 0;
    }
    .shad-progress-label {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-bottom: 0.35rem;
    }
    .shad-progress-bar {
        height: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 999px;
        overflow: hidden;
    }
    .shad-progress-fill {
        height: 100%;
        background: #2563EB;
        border-radius: 999px;
        transition: width 0.4s ease;
    }
    .shad-progress-value {
        font-size: 0.75rem;
        color: #CBD5E1;
        text-align: right;
        margin-top: 0.25rem;
    }

    .shad-skeleton-container {
        padding: 1rem 0;
    }
    .shad-skeleton {
        height: 14px;
        background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
        background-size: 200% 100%;
        animation: shimmerAdvanced 1.5s infinite;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .dq-body { display: flex; flex-wrap: wrap; gap: 1.1rem; }
    .dq-item { display: flex; flex-direction: column; gap: 0.1rem; }
    .dq-label { font-size: 0.68rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em; }
    .dq-value { font-size: 0.95rem; font-weight: 600; color: #E2E8F0; }
    .dq-value.missing { color: #F59E0B; font-size: 0.82rem; }
    .dq-notes { margin-top: 0.55rem; font-size: 0.74rem; color: #64748B; line-height: 1.35; }

    /* ================================================================
       HEADER
       ================================================================ */
    .dashboard-header {
        background: linear-gradient(135deg,
            rgba(37, 99, 235, 0.1) 0%,
            rgba(168, 85, 247, 0.08) 50%,
            rgba(14, 165, 233, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(37, 99, 235, 0.2);
        border-radius: var(--radius-lg);
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }

    .dashboard-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #2563EB, #A855F7, #0EA5E9, #2563EB);
        background-size: 200% auto;
        animation: gradient-shift 3s ease infinite;
    }

    .header-title {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #F1F5F9, #2563EB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.2;
    }

    .header-subtitle {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 400;
        margin-top: 0.25rem;
    }

    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #10B981;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .header-meta {
        display: flex;
        gap: 1.5rem;
        margin-top: 0.75rem;
        flex-wrap: wrap;
    }

    .header-meta-item {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #64748B;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .header-meta-item span { color: #CBD5E1; }

    /* ================================================================
       KPI CARDS
       ================================================================ */
    .kpi-card {
        background: linear-gradient(145deg, #111827 0%, #0f1520 100%);
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out both;
        height: 100%;
        box-sizing: border-box;
    }

    .kpi-card:hover {
        border-color: rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3), var(--shadow-glow-blue);
    }

    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px;
        height: 100%;
        border-radius: 3px 0 0 3px;
    }

    .kpi-card.blue::after { background: linear-gradient(180deg, #2563EB, #1d4ed8); }
    .kpi-card.green::after { background: linear-gradient(180deg, #10B981, #059669); }
    .kpi-card.cyan::after { background: linear-gradient(180deg, #0EA5E9, #0284c7); }
    .kpi-card.orange::after { background: linear-gradient(180deg, #F97316, #ea580c); }
    .kpi-card.red::after { background: linear-gradient(180deg, #DC2626, #b91c1c); }
    .kpi-card.purple::after { background: linear-gradient(180deg, #A855F7, #9333ea); }

    .kpi-topline {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 0.35rem;
    }

    .kpi-target-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    .kpi-status {
        font-size: 0.58rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 0.2rem 0.45rem;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        background: rgba(148, 163, 184, 0.08);
        color: #CBD5E1;
        line-height: 1;
    }

    .kpi-status.success {
        background: rgba(16, 185, 129, 0.14);
        border-color: rgba(16, 185, 129, 0.25);
        color: #6EE7B7;
    }

    .kpi-status.warning {
        background: rgba(245, 158, 11, 0.14);
        border-color: rgba(245, 158, 11, 0.25);
        color: #FCD34D;
    }

    .kpi-status.danger {
        background: rgba(220, 38, 38, 0.14);
        border-color: rgba(220, 38, 38, 0.25);
        color: #FCA5A5;
    }

    .kpi-target-text {
        font-size: 0.62rem;
        color: #64748B;
        white-space: nowrap;
    }

    .kpi-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .kpi-label {
        color: #94A3B8;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
        line-height: 1.3;
    }

    .kpi-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #F1F5F9;
        line-height: 1;
        margin-bottom: 0.4rem;
        word-break: break-word;
    }

    .kpi-context {
        color: #64748B;
        font-size: 0.7rem;
        font-weight: 400;
        margin-bottom: 0.35rem;
        line-height: 1.4;
    }

    .kpi-trend {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        margin-top: 0.15rem;
    }

    .kpi-trend.up {
        color: #10B981;
        background: rgba(16, 185, 129, 0.15);
    }

    .kpi-trend.down {
        color: #DC2626;
        background: rgba(220, 38, 38, 0.15);
    }

    .kpi-trend.neutral {
        color: #94A3B8;
        background: rgba(148, 163, 184, 0.15);
    }

    .kpi-trend.good {
        color: #6EE7B7;
        background: rgba(16, 185, 129, 0.15);
    }

    .kpi-trend.bad {
        color: #FCA5A5;
        background: rgba(220, 38, 38, 0.15);
    }

    .kpi-sparkline {
        margin: 0.35rem 0 0.15rem 0;
        min-height: 1.1rem;
        line-height: 1;
    }

    .kpi-sparkline-text {
        display: inline-block;
        width: 100%;
        font-size: 1rem;
        letter-spacing: 0.08em;
        font-weight: 700;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: clip;
        opacity: 0.95;
    }

    /* ================================================================
       SECTION HEADERS
       ================================================================ */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 1.75rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(37, 99, 235, 0.15);
        animation: fadeIn 0.5s ease-out;
    }

    .section-header h2 {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F1F5F9;
        margin: 0;
    }

    .section-header .section-icon {
        font-size: 1.2rem;
    }

    /* ================================================================
       CHART CONTAINERS & PLOTLY OVERRIDES — No Scroll
       ================================================================ */
    div[data-testid="stPlotlyChart"] {
        background: linear-gradient(145deg, #111827 0%, #0d1117 100%) !important;
        border: 1px solid rgba(37, 99, 235, 0.15) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-card) !important;
        min-height: auto !important;
        width: 100% !important;
        overflow: visible !important;
        overflow-x: visible !important;
        overflow-y: visible !important;
        box-sizing: border-box !important;
    }

    /* Remove scrollbars from plotly container */
    div[data-testid="stPlotlyChart"] > div {
        overflow: hidden !important;
        overflow-x: hidden !important;
        overflow-y: hidden !important;
        max-width: 100% !important;
    }

    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plotly,
    div[data-testid="stPlotlyChart"] .plot-container,
    div[data-testid="stPlotlyChart"] .svg-container {
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    /* Plotly chart svg should not scroll */
    svg[class*="plotly"] {
        overflow: hidden !important;
        max-width: 100% !important;
    }

    div[data-testid="stPlotlyChart"]:hover {
        border-color: rgba(37, 99, 235, 0.35) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3), var(--shadow-glow-blue) !important;
    }

    /* Chart responsiveness for different screen sizes */
    @media (max-width: 1024px) {
        div[data-testid="stPlotlyChart"] {
            padding: 0.8rem !important;
            margin-bottom: 0.8rem !important;
        }
    }

    @media (max-width: 768px) {
        div[data-testid="stPlotlyChart"] {
            padding: 0.6rem !important;
            margin-bottom: 0.6rem !important;
        }
    }

    @media (max-width: 480px) {
        div[data-testid="stPlotlyChart"] {
            padding: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
    }

    .chart-container {
        background: linear-gradient(145deg, #111827 0%, #0d1117 100%);
        border: 1px solid rgba(59, 130, 246, 0.12);
        border-radius: var(--radius-md);
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .chart-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #CBD5E1;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .chart-title .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .dot-blue { background: #2563EB; box-shadow: 0 0 8px rgba(37, 99, 235, 0.5); }
    .dot-green { background: #10B981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.5); }
    .dot-cyan { background: #0EA5E9; box-shadow: 0 0 8px rgba(14, 165, 233, 0.5); }
    .dot-orange { background: #F97316; box-shadow: 0 0 8px rgba(249, 115, 22, 0.5); }
    .dot-purple { background: #A855F7; box-shadow: 0 0 8px rgba(168, 85, 247, 0.5); }
    .dot-red { background: #DC2626; box-shadow: 0 0 8px rgba(220, 38, 38, 0.5); }

    /* ================================================================
       INSIGHT CARDS
       ================================================================ */
    .insight-card {
        background: linear-gradient(135deg,
            rgba(37, 99, 235, 0.08) 0%,
            rgba(168, 85, 247, 0.08) 100%);
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        animation: fadeInUp 0.5s ease-out both;
        height: 100%;
        box-sizing: border-box;
    }

    .insight-card.warning {
        background: linear-gradient(135deg,
            rgba(249, 115, 22, 0.08) 0%,
            rgba(220, 38, 38, 0.08) 100%);
        border-color: rgba(249, 115, 22, 0.2);
    }

    .insight-card.success {
        background: linear-gradient(135deg,
            rgba(16, 185, 129, 0.08) 0%,
            rgba(14, 165, 233, 0.08) 100%);
        border-color: rgba(16, 185, 129, 0.2);
    }

    .insight-card.danger {
        background: linear-gradient(135deg,
            rgba(220, 38, 38, 0.08) 0%,
            rgba(236, 72, 153, 0.08) 100%);
        border-color: rgba(220, 38, 38, 0.2);
    }

    .insight-title {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }

    .insight-card .insight-title { color: #2563EB; }
    .insight-card.warning .insight-title { color: #F97316; }
    .insight-card.success .insight-title { color: #10B981; }
    .insight-card.danger .insight-title { color: #DC2626; }

    .insight-text {
        color: #CBD5E1;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* ================================================================
       DATA TABLES — Fully Responsive
       ================================================================ */
    .stDataFrame {
        border-radius: var(--radius-sm) !important;
        width: 100% !important;
        overflow-x: auto !important;
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        border-radius: var(--radius-sm) !important;
        width: 100% !important;
    }

    /* Make dataframe scrollable on mobile */
    @media (max-width: 768px) {
        .stDataFrame {
            font-size: 0.75rem !important;
        }
        
        .stDataFrame [data-testid="stDataFrameResizable"] {
            font-size: 0.75rem !important;
        }
    }

    /* ================================================================
       TABS
       ================================================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: var(--radius-sm);
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 500;
        font-size: 0.82rem;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #3B82F6 !important;
        border: 1px solid rgba(59, 130, 246, 0.25) !important;
    }

    /* Responsive tabs */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto;
            overflow-y: hidden;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px !important;
            font-size: 0.75rem !important;
            white-space: nowrap;
        }
    }

    /* ================================================================
       RANKING ROWS
       ================================================================ */
    .ranking-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.7rem 1rem;
        background: rgba(17, 24, 39, 0.5);
        border: 1px solid rgba(59, 130, 246, 0.08);
        border-radius: var(--radius-sm);
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }

    .ranking-row:hover {
        background: rgba(59, 130, 246, 0.06);
        border-color: rgba(59, 130, 246, 0.2);
    }

    .ranking-position {
        font-size: 0.85rem;
        font-weight: 800;
        min-width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
    }

    .ranking-position.gold { background: rgba(249, 115, 22, 0.2); color: #F97316; }
    .ranking-position.silver { background: rgba(148, 163, 184, 0.15); color: #94A3B8; }
    .ranking-position.bronze { background: rgba(217, 119, 6, 0.15); color: #D97706; }
    .ranking-position.default { background: rgba(100, 116, 139, 0.1); color: #64748B; }

    .ranking-text {
        color: #CBD5E1;
        font-size: 0.8rem;
        font-weight: 500;
        flex: 1;
    }

    .ranking-value {
        color: #3B82F6;
        font-size: 0.9rem;
        font-weight: 700;
    }

    /* ================================================================
       SIDEBAR
       ================================================================ */
    .sidebar-section {
        color: #2563EB;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid rgba(37, 99, 235, 0.2);
    }

    .nav-link {
        font-family: 'Inter', sans-serif !important;
    }

    /* Native sidebar navigation — avoids third-party React components. */
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 0.3rem !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        width: 100% !important;
        border-radius: 8px !important;
        padding: 0.55rem 0.7rem !important;
        margin: 0 !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        transition: background 0.18s ease, border-color 0.18s ease !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: rgba(59, 130, 246, 0.08) !important;
        border-color: rgba(59, 130, 246, 0.15) !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: rgba(59, 130, 246, 0.15) !important;
        border-color: rgba(59, 130, 246, 0.28) !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] > label p {
        color: #94A3B8 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
        color: #60A5FA !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stMarkdownContainer"] {
        pointer-events: none;
    }

    /* Prevent browser translation tools from rewriting dashboard text nodes. */
    html.notranslate,
    body.notranslate,
    .stApp.notranslate {
        unicode-bidi: isolate;
    }

    /* Filter badge */
    .filter-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(37, 99, 235, 0.12);
        border: 1px solid rgba(37, 99, 235, 0.25);
        color: #2563EB;
        font-size: 0.68rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    .filter-badge.active {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.3);
        color: #10B981;
    }

    /* ================================================================
       STREAMLIT BUTTON OVERRIDES & CLEAR FILTER BUTTON
       ================================================================ */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.18), rgba(168, 85, 247, 0.12)) !important;
        border: 1px solid rgba(37, 99, 235, 0.25) !important;
        color: #2563EB !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.3), rgba(168, 85, 247, 0.25)) !important;
        border-color: rgba(37, 99, 235, 0.45) !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Responsive buttons on mobile */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 0.75rem !important;
            padding: 0.5rem !important;
        }
    }

    /* ================================================================
       STREAMLIT SUCCESS/ERROR/INFO MESSAGES
       ================================================================ */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: var(--radius-md) !important;
        border: 1px solid !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(14, 165, 233, 0.12)) !important;
        border-color: rgba(16, 185, 129, 0.25) !important;
        color: #10B981 !important;
    }

    .stError {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.12), rgba(236, 72, 153, 0.12)) !important;
        border-color: rgba(220, 38, 38, 0.25) !important;
        color: #DC2626 !important;
    }

    .stInfo {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(168, 85, 247, 0.12)) !important;
        border-color: rgba(37, 99, 235, 0.25) !important;
        color: #2563EB !important;
    }

    .stWarning {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.12), rgba(220, 38, 38, 0.12)) !important;
        border-color: rgba(249, 115, 22, 0.25) !important;
        color: #F97316 !important;
    }

    /* ================================================================
       STREAMLIT SLIDER OVERRIDES
       ================================================================ */
    .stSlider > div > div > div {
        background: rgba(59, 130, 246, 0.3) !important;
    }

    /* Responsive sliders */
    @media (max-width: 768px) {
        .stSlider {
            width: 100% !important;
        }
    }

    /* ================================================================
       RESPONSIVE — Ultra Wide (2560px+)
       ================================================================ */
    @media (min-width: 2560px) {
        .main .block-container {
            max-width: 2000px !important;
        }
        .header-title { font-size: 2.2rem; }
        .kpi-value { font-size: 2rem; }
        .kpi-label { font-size: 0.9rem; }
        .section-header h2 { font-size: 1.5rem; }
    }

    /* ================================================================
       RESPONSIVE — Large screens (1920px+)
       ================================================================ */
    @media (min-width: 1920px) {
        .main .block-container {
            max-width: 1600px !important;
        }
        .header-title { font-size: 1.95rem; }
        .kpi-value { font-size: 1.8rem; }
        .kpi-label { font-size: 0.82rem; }
        .kpi-card { padding: 1.5rem; }
        .section-header h2 { font-size: 1.3rem; }
    }

    /* ================================================================
       RESPONSIVE — Standard Desktop (1200px - 1919px)
       ================================================================ */
    @media (min-width: 1200px) and (max-width: 1919px) {
        .main .block-container {
            max-width: 1400px !important;
            padding-top: 0.8rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }

    /* ================================================================
       RESPONSIVE — Landscape Tablet (1024px - 1199px)
       ================================================================ */
    @media (min-width: 1024px) and (max-width: 1199px) {
        .main .block-container {
            max-width: 100% !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        .header-title { font-size: 1.5rem; }
        .kpi-value { font-size: 1.25rem; }
        .kpi-card { padding: 1rem; }
        .kpi-label { font-size: 0.7rem; }
        .section-header h2 { font-size: 1.1rem; }
        .header-meta { gap: 0.8rem; }
        .dashboard-header { padding: 1.2rem 1.5rem; }
    }

    /* ================================================================
       RESPONSIVE — Portrait Tablet (768px - 1023px)
       ================================================================ */
    @media (min-width: 768px) and (max-width: 1023px) {
        .main .block-container {
            max-width: 100% !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }
        .header-title { font-size: 1.3rem; }
        .header-subtitle { font-size: 0.75rem; }
        .kpi-value { font-size: 1.15rem; }
        .kpi-card { padding: 0.9rem 1rem; }
        .kpi-label { font-size: 0.65rem; }
        .section-header h2 { font-size: 1rem; }
        .dashboard-header { padding: 1rem 1.2rem; }
        .header-meta { gap: 0.6rem; font-size: 0.7rem; }
        .insight-text { font-size: 0.78rem; }
    }

    /* ================================================================
       RESPONSIVE — Large Mobile (480px - 767px)
       ================================================================ */
    @media (min-width: 480px) and (max-width: 767px) {
        .main .block-container {
            max-width: 100% !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-top: 0.5rem !important;
        }
        .dashboard-header { 
            padding: 0.85rem 1rem;
            flex-direction: column !important;
        }
        .header-title { font-size: 1.15rem; }
        .header-subtitle { font-size: 0.7rem; }
        .header-meta { gap: 0.4rem; font-size: 0.65rem; flex-direction: column; }
        .kpi-value { font-size: 1rem; }
        .kpi-card { padding: 0.8rem 0.9rem; }
        .kpi-label { font-size: 0.62rem; }
        .kpi-icon { font-size: 1.2rem; }
        .section-header h2 { font-size: 0.9rem; }
        .section-header { margin: 1.2rem 0 0.75rem 0; }
        .insight-text { font-size: 0.75rem; }
        .insight-card { padding: 0.85rem 1rem; }
    }

    /* ================================================================
       RESPONSIVE — Mobile Devices (< 480px)
       ================================================================ */
    @media (max-width: 479px) {
        .main .block-container {
            max-width: 100% !important;
            padding-left: 0.4rem !important;
            padding-right: 0.4rem !important;
            padding-top: 0.3rem !important;
            padding-bottom: 1rem !important;
        }
        .dashboard-header {
            padding: 0.7rem 0.8rem;
            flex-direction: column !important;
            gap: 0.5rem;
            border-radius: 12px;
        }
        .header-title {
            font-size: 1rem;
            word-break: break-word;
        }
        .header-subtitle { font-size: 0.65rem; }
        .header-badge { font-size: 0.6rem; padding: 2px 8px; }
        .header-meta {
            gap: 0.25rem;
            font-size: 0.6rem;
            flex-direction: column;
        }
        .kpi-card {
            padding: 0.7rem 0.8rem;
            border-radius: 10px;
        }
        .kpi-value { font-size: 0.95rem; }
        .kpi-label { font-size: 0.6rem; }
        .kpi-context { font-size: 0.65rem; }
        .kpi-icon { font-size: 1rem; margin-bottom: 0.3rem; }
        .kpi-trend { font-size: 0.65rem; }
        .section-header {
            margin: 1rem 0 0.6rem 0;
            gap: 6px;
        }
        .section-header h2 { font-size: 0.85rem; }
        .section-header .section-icon { font-size: 1rem; }
        .insight-card { padding: 0.75rem 0.9rem; }
        .insight-title { font-size: 0.72rem; }
        .insight-text { font-size: 0.72rem; }
        .filter-badge { font-size: 0.62rem; padding: 2px 6px; }
        .ranking-row { padding: 0.6rem 0.8rem; gap: 8px; }
        .ranking-position { font-size: 0.75rem; min-width: 28px; height: 28px; }
        .ranking-text { font-size: 0.75rem; }
        .ranking-value { font-size: 0.85rem; }

        /* Tabs more compact on mobile */
        .stTabs [data-baseweb="tab"] { padding: 6px 12px; font-size: 0.75rem; }
    }

    /* ================================================================
       ANIMATION DELAYS
       ================================================================ */
    .delay-1 { animation-delay: 0.05s !important; }
    .delay-2 { animation-delay: 0.1s !important; }
    .delay-3 { animation-delay: 0.15s !important; }
    .delay-4 { animation-delay: 0.2s !important; }
    .delay-5 { animation-delay: 0.25s !important; }
    .delay-6 { animation-delay: 0.3s !important; }

    /* ================================================================
       Filter context, status panels and form actions
       ================================================================ */
    .filter-context-card {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.09), rgba(14, 165, 233, 0.05));
        border: 1px solid rgba(37, 99, 235, 0.22);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin: 0.35rem 0 1rem 0;
        color: #CBD5E1;
        font-size: 0.75rem;
    }
    .filter-context-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem 1.15rem;
        margin-top: 0.45rem;
        color: #94A3B8;
    }
    .filter-context-grid b { color: #E2E8F0; }
    div[data-testid="stForm"] {
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: 12px;
        padding: 0.65rem;
        background: rgba(15, 23, 42, 0.42);
    }
    div[data-testid="stDownloadButton"] button {
        width: 100%;
        border-radius: 10px;
        border-color: rgba(37, 99, 235, 0.35);
    }
    .status-chip {
        display: inline-flex;
        align-items: center;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 600;
        background: rgba(37, 99, 235, 0.12);
        border: 1px solid rgba(37, 99, 235, 0.2);
        color: #93C5FD;
        margin: 2px 4px 2px 0;
    }
    @media (max-width: 768px) {
        .filter-context-grid { flex-direction: column; gap: 0.25rem; }
    }


    /* ================================================================
       V7 analytical enhancements
       ================================================================ */
    .kpi-topline {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.5rem;
    }
    .kpi-target-row {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        flex-wrap: wrap;
        justify-content: flex-end;
    }
    .kpi-status {
        display: inline-flex;
        align-items: center;
        padding: 2px 7px;
        border-radius: 999px;
        font-size: 0.58rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        white-space: nowrap;
    }
    .kpi-status.success { color: #34D399; background: rgba(16,185,129,0.13); border: 1px solid rgba(16,185,129,0.22); }
    .kpi-status.warning { color: #FDBA74; background: rgba(249,115,22,0.13); border: 1px solid rgba(249,115,22,0.22); }
    .kpi-status.danger { color: #FCA5A5; background: rgba(220,38,38,0.13); border: 1px solid rgba(220,38,38,0.22); }
    .kpi-target-text { color: #64748B; font-size: 0.6rem; white-space: nowrap; }
    .kpi-sparkline { width: 100%; height: 34px; margin: 0.25rem 0 0.15rem 0; opacity: 0.92; }
    .kpi-sparkline svg { width: 100%; height: 100%; overflow: visible; }
    .kpi-trend.good { color: #34D399; background: rgba(16,185,129,0.13); }
    .kpi-trend.bad { color: #FCA5A5; background: rgba(220,38,38,0.13); }
    .executive-narrative {
        background: linear-gradient(135deg, rgba(37,99,235,0.12), rgba(168,85,247,0.08));
        border: 1px solid rgba(59,130,246,0.25);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        margin: 0.4rem 0 1.1rem 0;
        box-shadow: 0 8px 28px rgba(0,0,0,0.18);
    }
    .executive-narrative-title {
        color: #93C5FD;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.45rem;
    }
    .executive-narrative-text {
        color: #CBD5E1;
        font-size: 0.84rem;
        line-height: 1.65;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(37,99,235,0.14);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 18px rgba(0,0,0,0.18);
    }
    div[data-testid="stRadio"] > label,
    div[data-testid="stSelectbox"] > label {
        color: #94A3B8 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
    }
    button[kind="secondary"] { border-radius: 10px !important; }


    /* ================================================================
       V10 RESPONSIVE HEALTH SCORE
       ================================================================ */
    /* ================================================================
       V7 reliability, filter and source-status enhancements
       ================================================================ */
    .empty-state-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.25rem 1.35rem;
        margin: 1rem 0;
        border: 1px dashed rgba(96, 165, 250, 0.32);
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(17, 24, 39, 0.92));
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }
    .empty-state-icon { font-size: 2rem; line-height: 1; }
    .empty-state-title { color: #F1F5F9; font-size: 1rem; font-weight: 800; margin-bottom: 0.25rem; }
    .empty-state-message { color: #CBD5E1; font-size: 0.82rem; line-height: 1.5; }
    .empty-state-hint { color: #64748B; font-size: 0.72rem; margin-top: 0.35rem; }

    .source-status {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.45rem 1rem;
        padding: 0.55rem 0.8rem;
        margin: -0.35rem 0 0.9rem 0;
        border: 1px solid rgba(16, 185, 129, 0.18);
        border-radius: 10px;
        background: rgba(16, 185, 129, 0.055);
        color: #94A3B8;
        font-size: 0.68rem;
    }
    .source-status b { color: #CBD5E1; }
    .source-status-state {
        margin-left: auto;
        color: #6EE7B7;
        font-weight: 700;
    }
    .source-status.stale {
        border-color: rgba(245, 158, 11, 0.25);
        background: rgba(245, 158, 11, 0.07);
    }
    .source-status.stale .source-status-state { color: #FCD34D; }

    .filter-action-row button {
        min-height: 2.15rem !important;
        font-size: 0.68rem !important;
        padding: 0.35rem 0.45rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        gap: 0.35rem !important;
    }
    .kpi-sparkline-text {
        display: inline-block;
        width: 100%;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        white-space: nowrap;
        overflow: hidden;
    }
    @media (max-width: 768px) {
        .source-status { flex-direction: column; align-items: flex-start; }
        .source-status-state { margin-left: 0; }
        .empty-state-card { align-items: flex-start; }
    }


    /* ================================================================
       V10.1 PREMIUM AUTOSYNC — POWER BI EXECUTIVE THEME
       ================================================================ */
    :root {
        --bg-primary: #081321;
        --bg-secondary: #0D1D31;
        --bg-card: #10243B;
        --bg-card-hover: #142A45;
        --bg-sidebar: #091827;
        --border-color: rgba(130, 165, 205, 0.16);
        --border-glow: rgba(70, 144, 255, 0.34);
        --text-primary: #F4F8FC;
        --text-secondary: #B8C7D9;
        --text-muted: #8499B1;
        --blue: #4A8DFF;
        --cyan: #35C6E8;
        --green: #2CCB8F;
        --orange: #F5A524;
        --red: #F35B67;
        --purple: #9D7BFF;
        --shadow-card: 0 10px 30px rgba(1, 8, 18, 0.28);
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background:
            radial-gradient(circle at 82% -10%, rgba(74, 141, 255, .12), transparent 34%),
            linear-gradient(180deg, #081321 0%, #091725 54%, #07111D 100%) !important;
        color: var(--text-primary) !important;
    }

    [data-testid="stMain"], .main {
        background: transparent !important;
    }

    header[data-testid="stHeader"] {
        background: rgba(8, 19, 33, .82) !important;
        border-bottom: 1px solid rgba(130, 165, 205, .10) !important;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(13, 29, 49, .98), rgba(8, 19, 33, .99)) !important;
        border-right: 1px solid rgba(130, 165, 205, .16) !important;
        box-shadow: 12px 0 36px rgba(0, 0, 0, .18) !important;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }

    .dashboard-header {
        background:
            linear-gradient(120deg, rgba(20, 42, 69, .98), rgba(13, 29, 49, .97)),
            radial-gradient(circle at 90% 0%, rgba(74, 141, 255, .22), transparent 36%) !important;
        border: 1px solid rgba(130, 165, 205, .20) !important;
        box-shadow: 0 14px 38px rgba(1, 8, 18, .28) !important;
    }

    .header-title {
        background: linear-gradient(120deg, #FFFFFF 8%, #B9D4FF 58%, #67B8FF 100%) !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;
    }

    .kpi-card,
    .chart-card,
    .insight-card,
    .health-score-summary,
    .health-breakdown-card,
    .filter-context-card,
    .empty-state-card {
        background: linear-gradient(145deg, rgba(16, 36, 59, .98), rgba(13, 29, 49, .98)) !important;
        border-color: rgba(130, 165, 205, .16) !important;
        box-shadow: var(--shadow-card) !important;
    }

    .kpi-card:hover,
    .health-breakdown-card:hover {
        background: linear-gradient(145deg, rgba(20, 42, 69, .99), rgba(15, 35, 57, .99)) !important;
        border-color: rgba(74, 141, 255, .42) !important;
        box-shadow: 0 16px 40px rgba(1, 8, 18, .34), 0 0 0 1px rgba(74, 141, 255, .08) !important;
    }

    div[data-testid="stPlotlyChart"] {
        background: linear-gradient(145deg, rgba(16, 36, 59, .72), rgba(13, 29, 49, .76)) !important;
        border: 1px solid rgba(130, 165, 205, .13) !important;
        border-radius: 16px !important;
        padding: .25rem .35rem !important;
        box-shadow: 0 10px 28px rgba(1, 8, 18, .20) !important;
        overflow: hidden !important;
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {
        background: rgba(13, 29, 49, .96) !important;
        border: 1px solid rgba(130, 165, 205, .14) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 28px rgba(1, 8, 18, .18) !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px !important;
        border: 1px solid rgba(130, 165, 205, .18) !important;
        background: linear-gradient(180deg, rgba(20, 42, 69, .98), rgba(13, 29, 49, .98)) !important;
        color: #EAF2FC !important;
        box-shadow: 0 5px 14px rgba(1, 8, 18, .18) !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: rgba(74, 141, 255, .55) !important;
        background: linear-gradient(180deg, rgba(30, 61, 98, .98), rgba(18, 42, 70, .98)) !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stTextInput input,
    .stNumberInput input {
        background: rgba(9, 24, 39, .94) !important;
        border-color: rgba(130, 165, 205, .18) !important;
        color: #F4F8FC !important;
    }

    .source-status {
        background: linear-gradient(90deg, rgba(44, 203, 143, .08), rgba(74, 141, 255, .055)) !important;
        border-color: rgba(44, 203, 143, .22) !important;
        color: #AFC1D5 !important;
        box-shadow: 0 7px 20px rgba(1, 8, 18, .14) !important;
    }

    .source-status.stale {
        background: linear-gradient(90deg, rgba(245, 165, 36, .10), rgba(243, 91, 103, .045)) !important;
        border-color: rgba(245, 165, 36, .32) !important;
    }

    .autosync-card {
        margin: .75rem 0 .35rem;
        padding: .78rem;
        border: 1px solid rgba(44, 203, 143, .24);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(16, 36, 59, .96), rgba(9, 24, 39, .98));
        box-shadow: 0 10px 24px rgba(1, 8, 18, .24);
    }

    .autosync-card.contingency {
        border-color: rgba(245, 165, 36, .38);
        background: linear-gradient(145deg, rgba(58, 43, 23, .72), rgba(19, 29, 40, .98));
    }

    .autosync-card.warning { border-color: rgba(245, 165, 36, .30); }

    .autosync-card-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: .5rem;
        margin-bottom: .65rem;
    }

    .autosync-title {
        color: #EAF2FC;
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .02em;
    }

    .autosync-interval {
        color: #8FB6E7;
        font-size: .62rem;
        font-weight: 800;
        padding: .15rem .42rem;
        border-radius: 999px;
        background: rgba(74, 141, 255, .11);
        border: 1px solid rgba(74, 141, 255, .18);
    }

    .autosync-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: .48rem .65rem;
    }

    .autosync-grid > div {
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: .08rem;
    }

    .autosync-grid span {
        color: #7890AA;
        font-size: .57rem;
        text-transform: uppercase;
        letter-spacing: .045em;
    }

    .autosync-grid strong {
        color: #DCE8F6;
        font-size: .64rem;
        font-weight: 700;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .autosync-next { grid-column: 1 / -1; }

    .autosync-error {
        margin-top: .6rem;
        padding-top: .55rem;
        border-top: 1px solid rgba(245, 165, 36, .18);
        color: #F6C76F;
        font-size: .61rem;
        line-height: 1.35;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #081321; }
    ::-webkit-scrollbar-thumb { background: #294766; border-radius: 999px; }
    ::-webkit-scrollbar-thumb:hover { background: #38658F; }

    @media (max-width: 768px) {
        .autosync-grid { grid-template-columns: 1fr; }
        .autosync-next { grid-column: 1; }
        .main .block-container { width: calc(100% - .7rem) !important; }
    }


    /* ================================================================
       CLEAN PRESENTATION OVERRIDES
       ================================================================ */
    :root {
        --bg-primary: #081321;
        --bg-card: #10243B;
        --bg-sidebar: #0B172B;
        --bg-card-hover: #142A45;
        --border-color: rgba(151, 180, 214, 0.18);
        --border-glow: rgba(74, 141, 255, 0.24);
        --text-primary: #F8FBFF;
        --text-secondary: #D9E6F2;
        --text-muted: #A8BCD1;
    }

    body, .stApp {
        background: radial-gradient(circle at top left, rgba(18, 57, 110, 0.20), rgba(8, 19, 33, 0) 26%), #081321 !important;
        color: #F8FBFF !important;
    }

    .dashboard-header.clean-header {
        background: linear-gradient(135deg, rgba(16, 36, 59, 0.98), rgba(13, 29, 49, 0.98));
        border: 1px solid rgba(151, 180, 214, 0.18);
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.22);
        padding: 1rem 1.25rem !important;
        border-radius: 22px;
        margin-bottom: 0.85rem;
    }
    .header-main { display:flex; flex-direction:column; gap:.35rem; }
    .dashboard-header .header-title {
        color: #F8FBFF !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    .dashboard-header .header-subtitle {
        color: #D9E6F2 !important;
        font-size: 1rem !important;
    }
    .dashboard-header .header-meta.clean-meta {
        display:flex; flex-wrap:wrap; gap:.75rem 1rem; margin-top:.2rem;
    }
    .dashboard-header .header-meta-item,
    .dashboard-header .header-meta-item span {
        color: #D9E6F2 !important;
        font-size: .9rem !important;
    }
    .dashboard-header .header-badge {
        background: rgba(34, 197, 94, 0.12) !important;
        color: #8EF0B0 !important;
        border: 1px solid rgba(34, 197, 94, 0.22) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: .03em;
    }

    .compact-source-status, .compact-filter-context {
        background: linear-gradient(180deg, rgba(13, 29, 49, 0.98), rgba(10, 23, 39, 0.98)) !important;
        border: 1px solid rgba(151, 180, 214, 0.18) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
    }

    .compact-source-status {
        display:flex; justify-content:space-between; align-items:center; gap: 1rem;
        padding: .78rem 1rem !important; border-radius: 16px; margin-bottom: .75rem;
    }
    .source-status-main {
        display:flex; flex-wrap:wrap; gap: .5rem 1rem; align-items:center;
    }
    .compact-source-status span, .compact-source-status b,
    .compact-filter-context span, .compact-filter-context b {
        color: #EAF2FC !important;
        font-size: .88rem !important;
    }
    .compact-source-status .source-status-state {
        color: #9CF3B0 !important; font-weight: 800; white-space: nowrap;
    }
    .compact-source-status.stale .source-status-state { color: #F9D778 !important; }

    .compact-filter-context {
        display:flex; flex-wrap:wrap; gap: .55rem 1rem;
        padding: .72rem 1rem !important; border-radius: 16px; margin-bottom: 1rem;
    }

    .section-header {
        margin: 1.4rem 0 .7rem !important;
        padding-bottom: .5rem;
        border-bottom: 1px solid rgba(151, 180, 214, 0.12);
    }
    .section-header h2 {
        color: #F8FBFF !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    .executive-narrative, .insight-card, .empty-state-card, .kpi-card, .metric-card, .health-score-summary, .health-breakdown-card {
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.16) !important;
    }

    .executive-narrative-title, .metric-label, .insight-title, .chart-title, .kpi-label {
        color: #F8FBFF !important;
    }
    .executive-narrative-text, .kpi-context, .insight-message, .stCaption, caption {
        color: #D9E6F2 !important;
    }
    .kpi-value, .metric-value {
        color: #FFFFFF !important;
        text-shadow: 0 1px 0 rgba(0,0,0,.18);
    }

    section[data-testid="stSidebar"] * {
        color: #EAF2FC !important;
    }
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        border-radius: 14px !important;
        border: 1px solid rgba(151, 180, 214, 0.18) !important;
        background: linear-gradient(180deg, rgba(16, 36, 59, 0.98), rgba(13, 29, 49, 0.98)) !important;
        color: #F8FBFF !important;
        font-weight: 700 !important;
    }

    .safe-html-table table { background: transparent !important; }
    .safe-html-table thead th { color: #F8FBFF !important; }
    .safe-html-table tbody td { color: #EAF2FC !important; }

    .js-plotly-plot, .plotly, .svg-container {
        user-select: none !important;
    }
    .js-plotly-plot .plotly .main-svg { cursor: default !important; }

    @media (max-width: 1100px) {
        .compact-source-status { flex-direction: column; align-items:flex-start; }
        .dashboard-header .header-title { font-size: 1.65rem !important; }
    }


    /* ================================================================
       V10.2.2 CONTRAST HOTFIX — MAIN RADIO LABELS
       ================================================================ */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        gap: 0.45rem !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        border-radius: 12px !important;
        padding: 0.35rem 0.55rem !important;
        margin-right: 0.15rem !important;
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid transparent !important;
        transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: rgba(255,255,255,0.06) !important;
        border-color: rgba(151,180,214,0.16) !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label p,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label span,
    div[data-testid="stRadio"] > div[role="radiogroup"] [data-testid="stMarkdownContainer"] p {
        color: #F8FBFF !important;
        font-size: 0.96rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em !important;
        opacity: 1 !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: rgba(74,141,255,0.12) !important;
        border-color: rgba(74,141,255,0.22) !important;
        box-shadow: inset 0 -2px 0 rgba(248,251,255,0.12);
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) span {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    div[data-testid="stRadio"] input[type="radio"] + div {
        color: #FFFFFF !important;
    }


    /* ================================================================
       V10.3 GLOBAL CONTRAST SUITE
       ================================================================ */
    :root {
        --text-primary: #FFFFFF;
        --text-secondary: #EAF2FC;
        --text-muted: #C7D7EA;
    }

    h1, h2, h3, h4, h5, h6,
    p, li, label, span, small, strong, div,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {
        color: inherit;
    }

    .section-header h2,
    .header-title,
    .kpi-value,
    .metric-value,
    .ranking-value,
    .insight-title,
    .executive-narrative-title,
    .chart-title,
    .health-summary-score,
    .health-breakdown-values strong {
        color: #FFFFFF !important;
    }

    .header-subtitle,
    .header-meta-item,
    .header-meta-item span,
    .executive-narrative-text,
    .insight-message,
    .kpi-context,
    .kpi-trend,
    .ranking-text,
    .health-breakdown-gap,
    .health-breakdown-heading span,
    .health-summary-label,
    .health-summary-metrics span,
    .source-status-main span,
    .compact-filter-context span,
    .filter-badge,
    .stCaption, caption,
    .empty-state-message,
    .empty-state-hint {
        color: #EAF2FC !important;
    }

    /* Main page radios */
    div[data-testid="stRadio"] > label,
    div[data-testid="stSelectbox"] > label,
    div[data-testid="stMultiSelect"] > label,
    div[data-testid="stTextInput"] > label,
    div[data-testid="stNumberInput"] > label {
        color: #F8FBFF !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(16, 36, 59, 0.68) !important;
        border: 1px solid rgba(151,180,214,0.16);
        padding: 5px !important;
        gap: 6px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #EAF2FC !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        padding: 9px 16px !important;
        border-radius: 12px !important;
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.06) !important;
        border-color: rgba(151,180,214,0.16) !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(74,141,255,0.16) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(74,141,255,0.28) !important;
        box-shadow: inset 0 -2px 0 rgba(255,255,255,0.12);
    }

    /* Selects and multiselects */
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] div[role="combobox"] {
        background: rgba(16, 36, 59, 0.96) !important;
        border-color: rgba(151,180,214,0.18) !important;
        color: #F8FBFF !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
        color: #F8FBFF !important;
        font-weight: 600 !important;
    }

    /* Buttons */
    .stButton > button,
    button[kind="secondary"],
    [data-testid="baseButton-secondary"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: 1px solid rgba(151,180,214,0.18) !important;
        background: linear-gradient(180deg, rgba(16, 36, 59, 0.98), rgba(13, 29, 49, 0.98)) !important;
    }

    /* Dataframes and tables */
    div[data-testid="stDataFrame"] * {
        color: #F8FBFF !important;
    }
    .safe-html-table tbody td { color: #F8FBFF !important; }
    .safe-html-table tbody td div { color: #F8FBFF !important; }

    /* Expanders */
    details, summary, summary * {
        color: #F8FBFF !important;
    }

    /* Sidebar additional contrast */
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] label {
        color: #EAF2FC !important;
    }

    /* Plotly fallback text in browser */
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text,
    .js-plotly-plot .plotly .gtitle,
    .js-plotly-plot .plotly .legendtext {
        fill: #F8FBFF !important;
    }

    /* Captions */
    div[data-testid="stCaptionContainer"] p {
        color: #D9E6F2 !important;
        font-size: 0.84rem !important;
    }

    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.82rem !important;
            padding: 8px 12px !important;
        }
    }


    /* ================================================================
       V10.4 PREMIUM BOARD EDITION
       Refinamento visual executivo para apresentação institucional
       ================================================================ */

    .main .block-container {
        max-width: 1580px !important;
        padding-top: 0.85rem !important;
        padding-bottom: 1.5rem !important;
    }

    section[data-testid="stSidebar"] {
        min-width: 285px !important;
        max-width: 285px !important;
        background: linear-gradient(180deg, rgba(8,19,33,0.98), rgba(10,24,40,0.98)) !important;
        border-right: 1px solid rgba(151,180,214,0.12) !important;
    }

    .dashboard-header.clean-header {
        border-radius: 24px !important;
        padding: 1.05rem 1.35rem !important;
        box-shadow: 0 14px 36px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.03) !important;
    }

    .dashboard-header .header-title {
        font-size: 2.1rem !important;
        letter-spacing: -0.03em !important;
    }

    .dashboard-header .header-subtitle {
        font-size: 1.02rem !important;
        color: #DCE9F5 !important;
    }

    .compact-source-status, .compact-filter-context,
    .executive-narrative, .insight-card, .empty-state-card,
    .kpi-card, .health-score-summary, .health-breakdown-card,
    .safe-html-table, div[data-testid="stDataFrame"],
    .stTabs [data-baseweb="tab-list"], details {
        border-radius: 18px !important;
    }

    .compact-source-status, .compact-filter-context {
        padding: 0.82rem 1rem !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12) !important;
    }

    .executive-narrative {
        margin-top: 0.4rem !important;
        margin-bottom: 1rem !important;
        padding: 1rem 1.1rem !important;
        border: 1px solid rgba(151,180,214,0.14) !important;
        background: linear-gradient(180deg, rgba(13,29,49,0.96), rgba(10,24,40,0.96)) !important;
    }

    .executive-narrative-title {
        font-size: 0.78rem !important;
        color: #A8D5FF !important;
        margin-bottom: 0.38rem !important;
    }

    .executive-narrative-text {
        font-size: 0.96rem !important;
        line-height: 1.58 !important;
    }

    .section-header {
        margin: 1.15rem 0 0.7rem 0 !important;
        padding-bottom: 0.55rem !important;
        border-bottom: 1px solid rgba(151,180,214,0.10) !important;
    }

    .section-header h2 {
        font-size: 1.42rem !important;
        line-height: 1.15 !important;
    }

    .section-icon {
        filter: saturate(1.05);
    }

    .kpi-card {
        min-height: 176px !important;
        padding: 1rem 1rem 0.95rem !important;
        border: 1px solid rgba(151,180,214,0.14) !important;
        background: linear-gradient(180deg, rgba(16,36,59,0.98), rgba(13,29,49,0.98)) !important;
    }

    .kpi-label {
        font-size: 0.86rem !important;
        color: #EAF2FC !important;
        font-weight: 700 !important;
    }

    .kpi-value {
        font-size: 2rem !important;
        line-height: 1.04 !important;
        margin: 0.22rem 0 0.18rem !important;
    }

    .kpi-context, .kpi-trend {
        font-size: 0.83rem !important;
    }

    .kpi-sparkline-text {
        letter-spacing: 0.04em;
        font-size: 1.05rem !important;
    }

    .insight-card {
        border: 1px solid rgba(151,180,214,0.14) !important;
        padding: 0.95rem 1rem !important;
    }

    .insight-title {
        font-size: 0.9rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.2rem !important;
    }

    .insight-message {
        font-size: 0.92rem !important;
        line-height: 1.5 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        padding: 6px !important;
        gap: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 42px !important;
        padding: 10px 16px !important;
        font-size: 0.92rem !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        min-height: 38px !important;
    }

    .safe-html-table {
        border: 1px solid rgba(151,180,214,0.14) !important;
        background: linear-gradient(180deg, rgba(13,29,49,0.98), rgba(10,24,40,0.98)) !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12) !important;
    }

    .safe-html-table table thead th {
        position: sticky;
        top: 0;
        z-index: 1;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(151,180,214,0.14) !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12) !important;
    }

    .stButton > button,
    button[kind="secondary"],
    [data-testid="baseButton-secondary"] {
        min-height: 42px !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 14px rgba(0,0,0,0.10) !important;
    }

    details {
        border: 1px solid rgba(151,180,214,0.12) !important;
        background: linear-gradient(180deg, rgba(16,36,59,0.96), rgba(13,29,49,0.96)) !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.10) !important;
        overflow: hidden !important;
    }

    summary {
        padding: 0.82rem 1rem !important;
        font-weight: 700 !important;
    }

    .stTabs, .safe-html-table, .executive-narrative, .insight-card, details, div[data-testid="stDataFrame"], .compact-source-status, .compact-filter-context {
        margin-bottom: 0.95rem !important;
    }

    /* Presentation polish */
    body:has(.presentation-mode-marker) .dashboard-header.clean-header {
        padding: 0.9rem 1.2rem !important;
    }
    body:has(.presentation-mode-marker) .executive-narrative,
    body:has(.presentation-mode-marker) .compact-source-status,
    body:has(.presentation-mode-marker) .compact-filter-context {
        margin-bottom: 0.8rem !important;
    }

    /* Better visual rhythm in sidebar */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
    }

    @media (max-width: 1100px) {
        .main .block-container {
            max-width: 100% !important;
        }
        section[data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
        }
        .kpi-card { min-height: 160px !important; }
        .dashboard-header .header-title { font-size: 1.8rem !important; }
        .section-header h2 { font-size: 1.24rem !important; }
    }


    /* ================================================================
       V10.4.1 INTERACTIVE HOVER — READ-ONLY INSPECTION
       ================================================================ */
    .js-plotly-plot,
    .js-plotly-plot .plotly,
    .js-plotly-plot .plotly .main-svg {
        cursor: crosshair !important;
    }

    .js-plotly-plot .hoverlayer .hovertext,
    .js-plotly-plot .hoverlayer .axistext {
        filter: drop-shadow(0 8px 18px rgba(0,0,0,0.34));
    }

    .js-plotly-plot .hoverlayer text {
        fill: #F8FBFF !important;
        font-weight: 600 !important;
    }

    .js-plotly-plot .modebar {
        display: none !important;
    }


    /* ================================================================
       V10.5 EXECUTIVE INTELLIGENCE
       ================================================================ */
    .kpi-help {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.05rem;
        height: 1.05rem;
        margin-left: .25rem;
        border-radius: 999px;
        color: #A8D5FF !important;
        border: 1px solid rgba(168,213,255,.24);
        background: rgba(74,141,255,.08);
        font-size: .68rem;
        font-weight: 800;
        cursor: help;
        vertical-align: middle;
    }

    .kpi-label[title] { cursor: help; }

    .executive-narrative {
        position: relative;
        overflow: hidden;
    }

    .executive-narrative::before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 3px;
        background: linear-gradient(180deg, #4A8DFF, #35C6E8);
    }

    .safe-html-table td:last-child {
        font-weight: 700;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"]:first-of-type {
        margin-bottom: .75rem;
    }

    body:has(.presentation-mode-marker) .kpi-help {
        display: none !important;
    }


    /* ================================================================
       V10.5.1 LAYOUT POLISH
       ================================================================ */
    .section-header {
        margin: 1.2rem 0 0.9rem 0 !important;
    }

    div[data-testid="stPlotlyChart"] {
        padding: 0.7rem 0.85rem 0.65rem 0.85rem !important;
        margin-bottom: 1.1rem !important;
        border-radius: 18px !important;
    }

    div[data-testid="stPlotlyChart"] > div {
        padding-top: 0.12rem !important;
    }

    .safe-html-table {
        overflow: auto !important;
        padding: 0.25rem 0 0.45rem 0 !important;
        margin-top: 0.15rem !important;
    }

    .safe-html-table table {
        width: 100% !important;
    }

    .safe-html-table thead th {
        padding-top: 12px !important;
        padding-bottom: 12px !important;
        white-space: nowrap !important;
    }

    .safe-html-table tbody td,
    .safe-html-table tbody th {
        padding-top: 11px !important;
        padding-bottom: 11px !important;
        line-height: 1.28 !important;
    }

    .safe-html-table tbody tr:last-child td,
    .safe-html-table tbody tr:last-child th {
        padding-bottom: 16px !important;
        border-bottom: none !important;
    }

    .safe-html-table tbody tr:last-child {
        box-shadow: inset 0 -1px 0 rgba(130,165,205,0.08);
    }

    div[data-testid="stSelectbox"] > label {
        margin-bottom: 0.35rem !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.45rem !important;
    }

    .js-plotly-plot .plotly .main-svg {
        overflow: visible !important;
    }

    .js-plotly-plot .legend text {
        font-weight: 600 !important;
    }

    @media (max-width: 1100px) {
        div[data-testid="stPlotlyChart"] {
            padding: 0.6rem 0.7rem !important;
        }
    }


    /* ================================================================
       V10.5.2 FINE VISUAL POLISH
       ================================================================ */
    .main .block-container {
        padding-top: 0.95rem !important;
        padding-bottom: 1.65rem !important;
    }

    .dashboard-header.clean-header {
        padding: 1.08rem 1.38rem !important;
        margin-bottom: 0.75rem !important;
    }

    .dashboard-header .header-title {
        letter-spacing: -0.032em !important;
        line-height: 1.02 !important;
    }

    .dashboard-header .header-subtitle,
    .dashboard-header .header-meta-item {
        line-height: 1.42 !important;
    }

    .compact-source-status, .compact-filter-context {
        padding: 0.86rem 1.02rem !important;
        margin-bottom: 0.8rem !important;
    }

    .section-header {
        margin: 1.28rem 0 0.92rem 0 !important;
        padding-bottom: 0.62rem !important;
    }

    .section-header h2 {
        font-size: 1.4rem !important;
        letter-spacing: -0.02em !important;
    }

    .kpi-card, .insight-card, .health-breakdown-card, .health-score-summary, .empty-state-card {
        display: flex !important;
        flex-direction: column !important;
        height: 100% !important;
    }

    .kpi-card {
        min-height: 184px !important;
        padding: 1rem 1rem 1rem !important;
    }

    .kpi-value {
        margin: 0.26rem 0 0.24rem !important;
    }

    .kpi-context {
        min-height: 1.25rem;
        line-height: 1.35 !important;
    }

    .kpi-trend {
        margin-top: 0.12rem !important;
        line-height: 1.35 !important;
    }

    .kpi-sparkline-wrapper,
    .sparkline-wrap,
    .kpi-sparkline {
        margin-top: auto !important;
    }

    .insight-card {
        min-height: 118px !important;
        padding: 1rem 1rem 0.98rem !important;
    }

    .insight-message {
        line-height: 1.54 !important;
    }

    .executive-narrative {
        padding: 1.02rem 1.12rem !important;
        margin-bottom: 1.05rem !important;
    }

    .executive-narrative-text {
        line-height: 1.62 !important;
    }

    div[data-testid="stPlotlyChart"] {
        padding: 0.78rem 0.92rem 0.72rem 0.92rem !important;
        margin-bottom: 1.15rem !important;
    }

    div[data-testid="stPlotlyChart"]:hover {
        transform: translateY(-1px);
    }

    .stTabs [data-baseweb="tab-list"] {
        padding: 7px !important;
        gap: 9px !important;
        margin-bottom: 0.25rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 43px !important;
        padding: 10px 17px !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.52rem !important;
    }

    .safe-html-table {
        padding: 0.34rem 0 0.52rem 0 !important;
    }

    .safe-html-table thead th:first-child,
    .safe-html-table tbody td:first-child,
    .safe-html-table tbody th:first-child {
        padding-left: 14px !important;
    }

    .safe-html-table thead th:last-child,
    .safe-html-table tbody td:last-child {
        padding-right: 14px !important;
    }

    .safe-html-table tbody td,
    .safe-html-table tbody th {
        vertical-align: middle !important;
    }

    div[data-testid="stSelectbox"] > label,
    div[data-testid="stMultiSelect"] > label,
    div[data-testid="stRadio"] > label {
        margin-bottom: 0.42rem !important;
    }

    .stButton > button,
    button[kind="secondary"],
    [data-testid="baseButton-secondary"] {
        min-height: 43px !important;
    }

    details {
        margin-bottom: 1rem !important;
    }

    @media (max-width: 1100px) {
        .section-header { margin: 1.12rem 0 0.82rem 0 !important; }
        .kpi-card { min-height: 172px !important; }
    }


    /* ================================================================
       V10.5.3 — NOTEBOOK-FIRST RESPONSIVE RETROFIT
       ================================================================ */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        color-scheme: dark !important;
        overflow-x: clip !important;
    }

    .main .block-container {
        width: calc(100% - clamp(.8rem, 2vw, 2.6rem)) !important;
        max-width: 2200px !important;
        padding-left: clamp(.35rem, 1vw, 1.15rem) !important;
        padding-right: clamp(.35rem, 1vw, 1.15rem) !important;
        margin-inline: auto !important;
    }

    .main div[data-testid="stHorizontalBlock"] {
        gap: clamp(.78rem, 1.2vw, 1.25rem) !important;
        align-items: stretch !important;
    }

    .main div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: 0 !important;
    }

    .main div[data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        overflow: visible !important;
        padding: clamp(.55rem, .85vw, .88rem) !important;
        box-sizing: border-box !important;
    }

    .main div[data-testid="stPlotlyChart"] > div,
    .main div[data-testid="stPlotlyChart"] .js-plotly-plot,
    .main div[data-testid="stPlotlyChart"] .plot-container,
    .main div[data-testid="stPlotlyChart"] .svg-container,
    .main div[data-testid="stPlotlyChart"] svg {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        overflow: visible !important;
        box-sizing: border-box !important;
    }

    .section-header h2,
    .kpi-label,
    .insight-title,
    .insight-message {
        overflow-wrap: anywhere !important;
    }

    /* Dark interactive controls in every state. */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div:hover,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="input"] > div,
    [data-baseweb="input"] > div:focus-within,
    [data-baseweb="base-input"] {
        background: linear-gradient(180deg, #112A45, #0D223A) !important;
        color: #F8FBFF !important;
        border-color: rgba(100,164,232,.42) !important;
        box-shadow: none !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="input"] *,
    [data-baseweb="base-input"] * {
        color: #F8FBFF !important;
        -webkit-text-fill-color: #F8FBFF !important;
    }

    /* Internal search input must not become a second coloured rectangle. */
    [data-testid="stMultiSelect"] [data-baseweb="input"],
    [data-testid="stMultiSelect"] [data-baseweb="base-input"],
    [data-testid="stMultiSelect"] [data-baseweb="input"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="base-input"] > div {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        min-width: 1.3rem !important;
        width: auto !important;
    }

    [data-baseweb="tag"] {
        background: linear-gradient(180deg, #245FA9, #1C4E8F) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(128,188,255,.42) !important;
        border-radius: 9px !important;
        max-width: 100% !important;
    }

    [data-baseweb="tag"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* Preserve BaseWeb anchoring: never force geometry on popover root. */
    body [data-baseweb="popover"] {
        z-index: 1000000 !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }

    body [data-baseweb="popover"] [role="listbox"],
    body [data-baseweb="menu"],
    body [role="listbox"] {
        background: #0D2239 !important;
        color: #F8FBFF !important;
        border: 1px solid rgba(255,255,255,.10) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(0,0,0,.44) !important;
        max-width: min(420px, calc(100vw - 20px)) !important;
        overflow-x: hidden !important;
    }

    body [role="option"] {
        min-height: 40px !important;
        background: #0F2742 !important;
        color: #EAF3FD !important;
        border-radius: 8px !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }

    body [role="option"]:hover,
    body [role="option"][data-highlighted="true"] {
        background: #2E6BB8 !important;
        color: #FFFFFF !important;
    }

    body [role="option"][aria-selected="true"] {
        background: linear-gradient(180deg, #2C69B8, #23599E) !important;
        color: #FFFFFF !important;
    }

    /* Native sidebar restore control must remain visible and reachable. */
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarNavCollapseButton"],
    [data-testid="collapsedControl"] button,
    button[kind="headerNoPadding"] {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        color: #F8FBFF !important;
        background: #102A46 !important;
        border: 1px solid rgba(92,158,230,.46) !important;
        border-radius: 10px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        z-index: 1000001 !important;
    }

    /* Notebook: reorganize first; reduce typography only after reflow. */
    @media (max-width: 1439px) {
        section[data-testid="stSidebar"] {
            min-width: 286px !important;
            max-width: 286px !important;
        }

        .main .block-container {
            width: calc(100% - .8rem) !important;
            padding-left: .35rem !important;
            padding-right: .35rem !important;
        }

        .main div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) {
            flex-wrap: wrap !important;
        }

        .main div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
        }

        .main div[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"] {
            flex: 1 1 calc(50% - .55rem) !important;
            width: calc(50% - .55rem) !important;
            min-width: min(260px, 100%) !important;
        }

        .section-header h2 { font-size: 1.18rem !important; }
        .kpi-label { font-size: .78rem !important; }
    }

    @media (max-width: 767px) {
        section[data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
        }

        .main div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
        .main div[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
        }

        .main div[data-testid="stPlotlyChart"] { padding: .45rem .25rem .65rem !important; }
    }

    
    /* ================================================================
       PURPLE THEME OVERRIDE - ROXO / MAGENTA / BRANCO
       ================================================================ */
    .stApp {
        background: #130A2B !important;
        background-color: #130A2B !important;
    }
    
    /* Dashboard header - linha superior roxa em vez de azul */
    .dashboard-header {
        background: linear-gradient(135deg, #1E1240 0%, #25144A 100%) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-top: 2px solid #8B5CF6 !important;
        box-shadow: 0 4px 24px rgba(139, 92, 246, 0.15) !important;
    }
    
    /* KPI cards roxo */
    .kpi-card {
        background: linear-gradient(135deg, #1E1240 0%, #22134A 100%) !important;
        border: 1px solid rgba(139, 92, 246, 0.18) !important;
        border-top: 2px solid rgba(139, 92, 246, 0.3) !important;
    }
    .kpi-card:hover {
        border-color: rgba(236, 72, 153, 0.3) !important;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.22) !important;
        transform: translateY(-2px);
    }
    
    /* Métricas */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1E1240 0%, #25144A 100%) !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
    }
    
    /* Gráficos containers */
    .chart-card, .chart-container {
        background: #1E1240 !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
    }
    
    /* Índice de Saúde Ocupacional - anel roxo/magenta */
    .health-score-visual-card {
        background: linear-gradient(155deg, rgba(30,18,64,0.98), rgba(19,10,43,0.99)) !important;
        border: 1px solid rgba(139,92,246,0.22) !important;
    }
    .health-score-visual-ring {
        background: conic-gradient(from -90deg,
            #8B5CF6 0deg,
            #EC4899 var(--score-angle),
            rgba(139,92,246,0.15) var(--score-angle),
            rgba(139,92,246,0.15) 360deg) !important;
        box-shadow: 0 0 34px rgba(139,92,246,0.25), inset 0 0 0 1px rgba(255,255,255,.04) !important;
    }
    .health-score-visual-ring::before {
        background: linear-gradient(145deg, #1E1240, #130A2B) !important;
    }
    .health-clean-progress span {
        background: linear-gradient(90deg, #8B5CF6, #EC4899) !important;
    }
    
    /* Botões e filtros roxo */
    button[kind="secondary"], .stButton button {
        border-color: rgba(139, 92, 246, 0.25) !important;
    }
    button[kind="secondary"]:hover, .stButton button:hover {
        background: rgba(139, 92, 246, 0.12) !important;
        border-color: #8B5CF6 !important;
        color: white !important;
    }
    
    /* Scrollbar roxa */
    ::-webkit-scrollbar-thumb {
        background: #8B5CF6 !important;
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #EC4899 !important;
    }
    
    /* Remove qualquer azul restante e força roxo */
    [style*="#2563EB"], [style*="#0B0F19"], [style*="#0F172A"] {
        /* fallback */
    }

    </style>
    """


# ---------------------------------------------------------------------------
# ADDITIONAL CSS LAYERS
# Each layer below is a focused, independently named fragment appended to
# the base stylesheet by get_css() at the bottom of this file. Keeping them
# as separate functions (instead of editing the base directly) preserves the
# historical record of each hotfix/iteration while keeping get_css() itself
# a single, easy-to-audit definition.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# RESPONSIVIDADE APRIMORADA — Melhoria de Curto Prazo (Quick Win)
# Refinamentos para dispositivos móveis e tablets que complementam as
# media queries existentes.
# ---------------------------------------------------------------------------

def _v_responsive_improvements() -> str:
    """CSS adicional para melhorar a responsividade em telas pequenas."""
    return """
    <style>
    /* ================================================================
       RESPONSIVIDADE APRIMORADA — Sidebar em telas pequenas
       ================================================================ */
    @media (max-width: 767px) {
        /* Sidebar mais compacta */
        section[data-testid="stSidebar"] {
            min-width: 220px !important;
            max-width: 260px !important;
        }
        /* Busca global no sidebar */
        section[data-testid="stSidebar"] div[data-testid="stTextInput"] input {
            font-size: 0.78rem !important;
            padding: 6px 10px !important;
        }
        /* Radio de navegação mais compacto */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
            font-size: 0.78rem !important;
            padding: 5px 8px !important;
        }
    }

    /* ================================================================
       RESPONSIVIDADE APRIMORADA — KPI cards em grid adaptativo
       ================================================================ */
    @media (max-width: 767px) {
        /* KPI cards empilham em coluna única */
        .kpi-grid {
            grid-template-columns: 1fr 1fr !important;
            gap: 0.5rem !important;
        }
    }
    @media (max-width: 479px) {
        .kpi-grid {
            grid-template-columns: 1fr !important;
            gap: 0.4rem !important;
        }
    }

    /* ================================================================
       RESPONSIVIDADE APRIMORADA — Tabelas com scroll horizontal
       ================================================================ */
    @media (max-width: 767px) {
        div[data-testid="stDataFrame"] {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }
        div[data-testid="stDataFrame"] table {
            min-width: 480px !important;
        }
    }

    /* ================================================================
       RESPONSIVIDADE APRIMORADA — Gráficos Plotly em mobile
       ================================================================ */
    @media (max-width: 767px) {
        div[data-testid="stPlotlyChart"] {
            min-height: 260px !important;
        }
        div[data-testid="stPlotlyChart"] .plotly-graph-div {
            height: 260px !important;
        }
    }
    @media (max-width: 479px) {
        div[data-testid="stPlotlyChart"] {
            min-height: 220px !important;
        }
        div[data-testid="stPlotlyChart"] .plotly-graph-div {
            height: 220px !important;
        }
    }

    /* ================================================================
       RESPONSIVIDADE APRIMORADA — Abas (tabs) em mobile
       ================================================================ */
    @media (max-width: 767px) {
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            flex-wrap: nowrap !important;
            scrollbar-width: none !important;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none !important;
        }
        .stTabs [data-baseweb="tab"] {
            white-space: nowrap !important;
            padding: 6px 10px !important;
            font-size: 0.72rem !important;
        }
    }

    /* ================================================================
       RESPONSIVIDADE APRIMORADA — Expanders e cards em mobile
       ================================================================ */
    @media (max-width: 479px) {
        .insight-card {
            padding: 0.65rem 0.75rem !important;
        }
        .insight-title { font-size: 0.7rem !important; }
        .insight-text { font-size: 0.7rem !important; }
        /* Botões de ação mais acessíveis em touch */
        button[kind="secondary"],
        button[kind="primary"] {
            min-height: 40px !important;
            font-size: 0.78rem !important;
        }
    }

    /* ================================================================
       RESPONSIVIDADE APRIMORADA — Tooltip KPI em touch devices
       ================================================================ */
    @media (hover: none) and (pointer: coarse) {
        /* Em dispositivos touch, o tooltip fica visível ao toque */
        .kpi-help {
            cursor: pointer !important;
            font-size: 0.75rem !important;
            padding: 2px 4px !important;
        }
        .kpi-label[title]:active::after {
            content: attr(title);
            position: absolute;
            background: rgba(15, 10, 31, 0.96);
            border: 1px solid rgba(124, 58, 237, 0.4);
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 0.72rem;
            color: #CBD5E1;
            max-width: 220px;
            z-index: 9999;
            white-space: normal;
            line-height: 1.4;
            left: 0;
            top: 100%;
            margin-top: 4px;
        }
        .kpi-label[title] {
            position: relative !important;
        }
    }
    </style>
    """


def _v13_accessibility_css() -> str:
    """V13 — Keyboard focus visibility and reduced-motion support (WCAG 2.2).

    Two gaps confirmed by direct inspection of this stylesheet before this
    change: (1) no rule anywhere set a visible focus indicator, and the many
    ``!important`` resets elsewhere in this file suppress the browser's own
    default outline, so keyboard users had no reliable way to see which
    control was focused; (2) no ``prefers-reduced-motion`` query existed
    despite 17 ``transition`` rules and 8 ``@keyframes`` animations in the
    base stylesheet. Both additions are purely additive (new selectors /
    a new media query) and change nothing for users who don't use a
    keyboard or haven't requested reduced motion.
    """
    return r"""
    <style>
    /* -----------------------------------------------------------------
       Focus-visible ring — only shown for keyboard/assistive-tech focus,
       not for mouse clicks, so it doesn't change the look of any of the
       hover/click interactions already tuned elsewhere in this file.
       #67E8F9 (existing light-cyan brand token) keeps >10:1 contrast
       against every background used in the app.
       ----------------------------------------------------------------- */
    a:focus-visible,
    button:focus-visible,
    [role="button"]:focus-visible,
    [role="tab"]:focus-visible,
    [role="option"]:focus-visible,
    [tabindex]:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    summary:focus-visible,
    div[data-testid="stTextInput"] input:focus-visible,
    div[data-testid="stNumberInput"] input:focus-visible {
        outline: 3px solid #67E8F9 !important;
        outline-offset: 2px !important;
        border-radius: 6px;
        box-shadow: 0 0 0 5px rgba(103, 232, 249, 0.25) !important;
    }

    /* BaseWeb select and the sidebar's custom radio labels put the real
       focusable element inside a wrapper, so :focus-visible on the leaf
       element is often clipped/hidden. :focus-within on the wrapper keeps
       the ring visible while it's reachable by keyboard. */
    div[data-baseweb="select"]:focus-within {
        outline: 3px solid #67E8F9 !important;
        outline-offset: 1px !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:focus-visible),
    div[role="radiogroup"] > label:has(input:focus-visible) {
        outline: 3px solid #67E8F9 !important;
        outline-offset: 2px !important;
    }
    .stTabs [data-baseweb="tab"]:focus-visible {
        outline: 3px solid #67E8F9 !important;
        outline-offset: -3px !important;
        border-radius: 6px;
    }

    /* -----------------------------------------------------------------
       Respect the OS "reduce motion" preference (WCAG 2.3.3). Every
       transition/animation in this stylesheet is decorative polish, not
       load-bearing for functionality, so collapsing their duration to
       near-zero is safe: every element still reaches the same end state.
       ----------------------------------------------------------------- */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }
    </style>
    """


def _v14_executive_ux_css() -> str:
    """V14 — consolidated design tokens and executive UX overrides.

    This deliberately lives as the final CSS layer. It replaces the visual
    effect of historical hotfixes without adding more page-specific inline
    styles, giving the project one predictable current-state design system.
    """
    return r"""
    <style>
    :root {
        --bg-primary: #0B1020;
        --bg-secondary: #0E1628;
        --bg-card: #121C30;
        --bg-card-hover: #17243B;
        --bg-sidebar: #0C1424;
        --border-color: rgba(148, 163, 184, 0.16);
        --border-strong: rgba(148, 163, 184, 0.26);
        --brand: #8B5CF6;
        --brand-soft: rgba(139, 92, 246, 0.14);
        --brand-border: rgba(139, 92, 246, 0.30);
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --surface-shadow: 0 12px 32px rgba(2, 6, 23, 0.24);
    }

    html, body, .stApp,
    [data-testid="stAppViewContainer"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                     BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }
    body, .stApp, [data-testid="stAppViewContainer"] {
        background: #0B1020 !important;
        color: var(--text-primary) !important;
    }

    /* Sidebar: one visual language, no page-level hardcoded colors. */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1628 0%, #0A1120 100%) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding: 1rem .9rem 1.35rem !important;
    }
    .sidebar-logo {
        display: flex !important;
        align-items: center;
        gap: .75rem;
        text-align: left !important;
        padding: .55rem .35rem 1rem !important;
        margin: 0 0 1rem !important;
        border-bottom: 1px solid var(--border-color) !important;
    }
    .sidebar-logo-mark {
        width: 38px;
        height: 38px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        background: var(--brand-soft);
        border: 1px solid var(--brand-border);
        color: #DDD6FE !important;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .04em;
    }
    .sidebar-logo-copy { min-width: 0; }
    .sidebar-logo-title {
        color: var(--text-primary) !important;
        font-size: .9rem;
        line-height: 1.2;
        font-weight: 750;
        letter-spacing: .02em;
    }
    .sidebar-logo-subtitle {
        color: var(--text-muted) !important;
        font-size: .72rem;
        margin-top: .12rem;
    }
    .sidebar-section {
        color: var(--text-muted) !important;
        font-size: .7rem !important;
        font-weight: 750 !important;
        letter-spacing: .09em !important;
        margin: .85rem .25rem .45rem !important;
    }
    .sidebar-divider {
        height: 1px;
        background: var(--border-color);
        margin: 1rem 0 .75rem;
    }
    .content-divider {
        height: 1px;
        background: var(--border-color);
        margin: 1.2rem 0;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        border-radius: 10px !important;
        padding: .58rem .7rem !important;
        margin: 0 0 .22rem !important;
        min-height: 40px;
        border: 1px solid transparent !important;
        background: transparent !important;
        transition: background .14s ease, border-color .14s ease !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: rgba(255,255,255,.04) !important;
        border-color: var(--border-color) !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: var(--brand-soft) !important;
        border-color: var(--brand-border) !important;
        box-shadow: inset 3px 0 0 var(--brand) !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label p,
    section[data-testid="stSidebar"] div[role="radiogroup"] > label span {
        color: var(--text-secondary) !important;
        font-size: .84rem !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p,
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) span {
        color: #F5F3FF !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] button {
        min-height: 38px !important;
        border-radius: 9px !important;
        font-size: .78rem !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] details {
        background: rgba(255,255,255,.025) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 11px !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] details summary {
        color: var(--text-secondary) !important;
        font-size: .8rem !important;
        min-height: 42px !important;
    }

    /* Page-aware header: page title is now the strongest element. */
    .dashboard-header.clean-header.page-aware-header {
        display: flex !important;
        align-items: flex-start !important;
        justify-content: space-between !important;
        gap: 1rem !important;
        background: linear-gradient(135deg, rgba(18,28,48,.98), rgba(14,22,40,.98)) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        box-shadow: var(--surface-shadow) !important;
        padding: 1.15rem 1.3rem !important;
        margin: 0 0 .65rem !important;
        overflow: visible !important;
        animation: none !important;
    }
    .dashboard-header.clean-header.page-aware-header::before { display: none !important; }
    .header-eyebrow {
        color: #A78BFA !important;
        font-size: .7rem;
        font-weight: 800;
        letter-spacing: .1em;
        text-transform: uppercase;
        margin-bottom: .08rem;
    }
    .dashboard-header .header-title {
        color: var(--text-primary) !important;
        background: none !important;
        -webkit-text-fill-color: currentColor !important;
        font-size: clamp(1.55rem, 2.3vw, 2.15rem) !important;
        font-weight: 780 !important;
        line-height: 1.12 !important;
        letter-spacing: -.025em !important;
    }
    .dashboard-header .header-subtitle {
        color: var(--text-secondary) !important;
        font-size: .9rem !important;
        line-height: 1.45 !important;
        max-width: 760px;
        margin-top: .16rem !important;
    }
    .dashboard-header .header-meta.clean-meta {
        display: flex !important;
        gap: .45rem .85rem !important;
        margin-top: .55rem !important;
    }
    .dashboard-header .header-meta-item,
    .dashboard-header .header-meta-item span {
        color: var(--text-muted) !important;
        font-size: .73rem !important;
        font-weight: 500 !important;
    }
    .dashboard-header .header-meta-item + .header-meta-item {
        padding-left: .85rem;
        border-left: 1px solid var(--border-color);
    }
    .dashboard-header .header-badge {
        background: var(--brand-soft) !important;
        color: #DDD6FE !important;
        border: 1px solid var(--brand-border) !important;
        font-size: .68rem !important;
        font-weight: 750 !important;
        padding: .28rem .58rem !important;
        border-radius: 999px !important;
        white-space: nowrap;
    }

    /* Active analytical scope: lightweight chips instead of another card. */
    .compact-filter-context {
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        gap: .4rem !important;
        padding: 0 !important;
        margin: 0 0 1rem !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }
    .compact-filter-context .scope-chip {
        display: inline-flex;
        align-items: center;
        gap: .32rem;
        width: auto;
        padding: .32rem .58rem;
        background: rgba(148,163,184,.07) !important;
        border: 1px solid var(--border-color);
        border-radius: 999px;
        color: var(--text-secondary) !important;
        font-size: .72rem !important;
        line-height: 1.2;
    }
    .compact-filter-context .scope-chip b {
        color: var(--text-muted) !important;
        font-size: inherit !important;
    }

    /* KPI system: stable grid, readable minimum sizes, compact target line. */
    .v14-kpi-grid {
        display: grid !important;
        grid-template-columns: repeat(var(--kpi-cols, 4), minmax(0, 1fr)) !important;
        gap: .8rem !important;
        margin: .15rem 0 .95rem !important;
    }
    .v14-kpi-grid .kpi-card {
        min-width: 0 !important;
        height: 100% !important;
        margin: 0 !important;
        background: linear-gradient(180deg, rgba(18,28,48,.98), rgba(15,24,42,.98)) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 24px rgba(2,6,23,.18) !important;
        padding: .95rem 1rem !important;
        animation: none !important;
        transform: none !important;
        transition: border-color .14s ease, background .14s ease !important;
    }
    .v14-kpi-grid .kpi-card:hover {
        transform: none !important;
        background: var(--bg-card-hover) !important;
        border-color: var(--border-strong) !important;
        box-shadow: 0 8px 24px rgba(2,6,23,.22) !important;
    }
    .kpi-label {
        color: var(--text-secondary) !important;
        font-size: .76rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        min-height: auto !important;
    }
    .kpi-value {
        color: var(--text-primary) !important;
        font-size: clamp(1.7rem, 2.6vw, 2.15rem) !important;
        line-height: 1.08 !important;
        letter-spacing: -.025em !important;
    }
    .kpi-context, .kpi-trend {
        font-size: .72rem !important;
        line-height: 1.35 !important;
    }
    .kpi-target-row {
        gap: .3rem !important;
        justify-content: flex-end !important;
    }
    .kpi-target-text {
        color: var(--text-muted) !important;
        font-size: .68rem !important;
    }
    .kpi-status {
        font-size: .62rem !important;
        letter-spacing: .025em !important;
        padding: 2px 6px !important;
    }
    .kpi-help { color: var(--text-muted) !important; font-size: .72rem !important; }

    /* Internal component system — replaces Tailwind CDN dependencies. */
    .shad-card {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        box-shadow: none !important;
        transition: border-color .14s ease !important;
        animation: none !important;
    }
    .shad-card:hover { transform: none !important; border-color: var(--border-strong) !important; }
    .shad-card-header { display:flex; align-items:center; gap:.65rem; margin-bottom:.7rem; }
    .shad-card-icon { font-size: 1rem; color: #A78BFA !important; }
    .shad-card-title { color:var(--text-primary) !important; font-size:.92rem !important; font-weight:700 !important; }
    .shad-card-content { color:var(--text-secondary) !important; font-size:.82rem !important; line-height:1.5 !important; }
    .shad-badge { display:inline-flex; align-items:center; padding:.2rem .48rem; border-radius:999px; border:1px solid var(--border-color); font-size:.7rem; font-weight:650; }
    .shad-badge.default { color:var(--text-secondary)!important; background:rgba(148,163,184,.08); }
    .shad-badge.success { color:#6EE7B7!important; background:rgba(16,185,129,.10); border-color:rgba(16,185,129,.25); }
    .shad-badge.warning { color:#FCD34D!important; background:rgba(245,158,11,.10); border-color:rgba(245,158,11,.25); }
    .shad-badge.destructive { color:#FCA5A5!important; background:rgba(220,38,38,.10); border-color:rgba(220,38,38,.25); }
    .shad-badge.outline { color:var(--text-secondary)!important; background:transparent; }
    .shad-alert { display:flex; gap:.7rem; align-items:flex-start; background:rgba(148,163,184,.05); border-color:var(--border-color); }
    .shad-alert.success { background:rgba(16,185,129,.07); border-color:rgba(16,185,129,.25); }
    .shad-alert.warning { background:rgba(245,158,11,.07); border-color:rgba(245,158,11,.25); }
    .shad-alert.destructive { background:rgba(220,38,38,.07); border-color:rgba(220,38,38,.25); }
    .shad-alert-icon { width:24px; height:24px; display:grid; place-items:center; border-radius:7px; background:rgba(148,163,184,.10); color:var(--text-secondary)!important; font-weight:800; flex:0 0 auto; }
    .shad-alert-title { color:var(--text-primary)!important; font-size:.82rem; font-weight:700; }
    .shad-alert-message { color:var(--text-secondary)!important; font-size:.78rem; line-height:1.45; margin-top:.1rem; }
    .shad-metric-label { color:var(--text-muted)!important; font-size:.72rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; }
    .shad-metric-value { color:var(--text-primary)!important; font-size:1.8rem; font-weight:750; letter-spacing:-.02em; }
    .shad-metric-change { font-size:.74rem; margin-top:.15rem; }
    .shad-metric-change.up { color:#6EE7B7!important; }
    .shad-metric-change.down { color:#FCA5A5!important; }
    .shad-metric-change.neutral { color:var(--text-muted)!important; }

    /* Raise unreadably small legacy labels without inflating the interface. */
    .dq-label, .dq-notes,
    .health-summary-metrics span,
    .health-breakdown-badge,
    .health-breakdown-gap,
    .ranking-label,
    .filter-badge,
    .metric-label,
    .source-status-card span {
        font-size: max(.7rem, 11px) !important;
        color: var(--text-muted) !important;
    }
    .section-header h2 { font-size: clamp(1.12rem, 1.7vw, 1.42rem) !important; }
    .section-header { margin: 1.15rem 0 .6rem !important; }

    /* Reruns should feel stable, not replay an entrance animation. */
    .dashboard-header,
    .kpi-card,
    .section-header,
    .animate-stagger > *,
    .animate-fade-in-up,
    .animate-fade-in-down,
    .animate-fade-in,
    .animate-scale-in,
    .animate-zoom-in,
    .animate-slide-in-right,
    .animate-slide-in-left,
    .animate-float,
    .animate-attention,
    .animate-lift-glow {
        animation: none !important;
    }
    .animate-lift-glow:hover { transform: none !important; }

    @media (max-width: 900px) {
        .v14-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
        .dashboard-header.clean-header.page-aware-header { border-radius: 14px !important; }
    }
    @media (max-width: 640px) {
        .dashboard-header.clean-header.page-aware-header {
            flex-direction: column !important;
            padding: .95rem 1rem !important;
        }
        .dashboard-header .header-meta.clean-meta { gap: .3rem .55rem !important; }
        .dashboard-header .header-meta-item + .header-meta-item {
            padding-left: .55rem;
        }
        .dashboard-header .header-subtitle { font-size: .82rem !important; }
        .compact-filter-context .scope-chip { font-size: .68rem !important; }
        .v14-kpi-grid { gap: .55rem !important; }
        .v14-kpi-grid .kpi-card { padding: .8rem .82rem !important; }
        .kpi-value { font-size: 1.65rem !important; }
        .kpi-target-row { justify-content: flex-start !important; margin-top:.2rem; }
    }
    @media (max-width: 390px) {
        .v14-kpi-grid { grid-template-columns: 1fr !important; }
    }
    </style>
    """



def _v14_1_analytic_tabs_css() -> str:
    """V14.1 — focused navigation for dense analytical pages."""
    return r"""
    <style>
    /* Dense analytical pages use tabs as a quiet secondary navigation layer. */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(148, 163, 184, 0.045) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 13px !important;
        padding: 4px !important;
        gap: 4px !important;
        margin: .35rem 0 .75rem !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        min-height: 38px !important;
        padding: .48rem .82rem !important;
        border: 1px solid transparent !important;
        border-radius: 10px !important;
        background: transparent !important;
        color: var(--text-secondary) !important;
        font-size: .78rem !important;
        font-weight: 700 !important;
        letter-spacing: 0 !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(148, 163, 184, 0.07) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--brand-soft) !important;
        color: #EDE9FE !important;
        border-color: var(--brand-border) !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: .2rem !important;
    }

    /* The metric switch should read as a compact mode selector, not a form. */
    div[data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        gap: .45rem !important;
        flex-wrap: wrap !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background: rgba(148, 163, 184, 0.045) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: .42rem .68rem !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        border-color: var(--brand-border) !important;
        background: rgba(139, 92, 246, 0.07) !important;
    }

    /* Tables/charts inside tabs need less vertical ceremony. */
    .stTabs .section-header {
        margin-top: .9rem !important;
        margin-bottom: .48rem !important;
    }
    .stTabs .section-header h2 {
        font-size: clamp(1rem, 1.35vw, 1.2rem) !important;
    }

    @media (max-width: 767px) {
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            scrollbar-width: none !important;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none !important; }
        .stTabs [data-baseweb="tab"] {
            white-space: nowrap !important;
            flex: 0 0 auto !important;
            font-size: .72rem !important;
            padding: .44rem .65rem !important;
        }
    }
    </style>
    """


def _v16_visual_refinement_css() -> str:
    """V16 — single executive visual system for cards, charts and typography."""
    return r"""
    <style>
    :root {
        --bg-primary: #0B1020;
        --bg-secondary: #0E1628;
        --bg-card: #121C30;
        --bg-card-hover: #17243B;
        --bg-sidebar: #0C1424;
        --border-color: #26354D;
        --border-soft: rgba(148, 163, 184, 0.14);
        --border-strong: rgba(148, 163, 184, 0.28);
        --brand: #8B5CF6;
        --brand-soft: rgba(139, 92, 246, 0.12);
        --brand-border: rgba(139, 92, 246, 0.28);
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --metric-blue: #3B82F6;
        --metric-teal: #14B8A6;
        --metric-amber: #F59E0B;
        --metric-coral: #F97316;
        --metric-violet: #A78BFA;
        --metric-sky: #38BDF8;
        --surface-shadow: 0 8px 24px rgba(2, 6, 23, 0.18);
    }

    /* One elevation language: flat navy surfaces, thin borders, no glow. */
    .dashboard-header.clean-header.page-aware-header,
    .v14-kpi-grid .kpi-card,
    .shad-card,
    .insight-card,
    .empty-state-card {
        background: var(--bg-card) !important;
        border-color: var(--border-soft) !important;
        box-shadow: var(--surface-shadow) !important;
        filter: none !important;
    }
    .dashboard-header.clean-header.page-aware-header:hover,
    .v14-kpi-grid .kpi-card:hover,
    .shad-card:hover,
    .insight-card:hover {
        transform: none !important;
        box-shadow: var(--surface-shadow) !important;
        border-color: var(--border-strong) !important;
    }

    /* KPI: neutral card; icon/sparkline carry the metric identity. */
    .v14-kpi-grid .kpi-card {
        min-height: 142px !important;
        padding: 1rem 1.05rem .92rem !important;
    }
    .v14-kpi-grid .kpi-card::after { display: none !important; }
    .kpi-icon {
        font-size: 1.25rem !important;
        margin: 0 0 .42rem !important;
        width: 28px;
        height: 28px;
        display: grid;
        place-items: center;
        border-radius: 8px;
        background: rgba(148, 163, 184, .07);
    }
    .kpi-card.blue .kpi-icon { color: var(--metric-blue) !important; background: rgba(59,130,246,.10); }
    .kpi-card.green .kpi-icon { color: var(--metric-teal) !important; background: rgba(20,184,166,.10); }
    .kpi-card.cyan .kpi-icon { color: var(--metric-sky) !important; background: rgba(56,189,248,.10); }
    .kpi-card.orange .kpi-icon { color: var(--metric-amber) !important; background: rgba(245,158,11,.10); }
    .kpi-card.red .kpi-icon { color: var(--metric-coral) !important; background: rgba(249,115,22,.10); }
    .kpi-card.purple .kpi-icon { color: var(--metric-violet) !important; background: rgba(167,139,250,.10); }
    .kpi-label {
        font-size: 12px !important;
        color: var(--text-secondary) !important;
        letter-spacing: .045em !important;
        margin-bottom: .28rem !important;
    }
    .kpi-value {
        font-size: clamp(1.82rem, 2.5vw, 2.25rem) !important;
        color: var(--text-primary) !important;
        margin-bottom: .28rem !important;
    }
    .kpi-context, .kpi-trend, .kpi-help {
        font-size: 12px !important;
    }
    .kpi-context { color: var(--text-muted) !important; }
    .kpi-trend, .kpi-trend.neutral { color: var(--text-secondary) !important; font-weight: 650 !important; }
    .kpi-sparkline { opacity: .9; }

    /* Chart headings are outside Plotly so all plots share the page typography. */
    .v16-chart-heading {
        margin: .45rem 0 .38rem !important;
        padding: 0 .12rem !important;
    }
    .v16-chart-title {
        color: var(--text-primary) !important;
        font-size: 15px !important;
        line-height: 1.3 !important;
        font-weight: 720 !important;
        letter-spacing: -.01em !important;
    }
    .v16-chart-subtitle {
        color: var(--text-muted) !important;
        font-size: 12px !important;
        line-height: 1.4 !important;
        margin-top: .08rem !important;
    }

    /* Plotly is a quiet data surface, not a second glowing card system. */
    .main div[data-testid="stPlotlyChart"],
    div[data-testid="stPlotlyChart"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 18px rgba(2, 6, 23, .14) !important;
        padding: .18rem .32rem .24rem !important;
        overflow: hidden !important;
        animation: none !important;
        transform: none !important;
        transition: border-color .14s ease !important;
    }
    .main div[data-testid="stPlotlyChart"]:hover,
    div[data-testid="stPlotlyChart"]:hover {
        animation: none !important;
        transform: none !important;
        border-color: var(--border-strong) !important;
        box-shadow: 0 6px 18px rgba(2, 6, 23, .14) !important;
    }
    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container,
    div[data-testid="stPlotlyChart"] .svg-container {
        background: transparent !important;
    }

    /* Section hierarchy: title first, icon second. */
    .section-header {
        gap: .48rem !important;
        margin: 1.05rem 0 .5rem !important;
    }
    .section-header h2 {
        color: var(--text-primary) !important;
        font-size: clamp(1.05rem, 1.5vw, 1.3rem) !important;
        font-weight: 730 !important;
        letter-spacing: -.012em !important;
    }
    .section-icon {
        color: #A78BFA !important;
        opacity: .92;
    }

    /* Tabs and controls stay quiet so the analytical content leads. */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(148,163,184,.035) !important;
        border-color: var(--border-soft) !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(139,92,246,.10) !important;
        border-color: rgba(139,92,246,.24) !important;
    }

    /* Better projector/Teams readability for captions and table metadata. */
    .stCaption, [data-testid="stCaptionContainer"],
    .compact-filter-context .scope-chip,
    .sidebar-logo-subtitle,
    .dashboard-header .header-meta-item,
    .dashboard-header .header-meta-item span {
        font-size: 12px !important;
        color: var(--text-muted) !important;
    }

    @media (max-width: 900px) {
        .v14-kpi-grid .kpi-card { min-height: 132px !important; }
        .v16-chart-title { font-size: 14px !important; }
        .v16-chart-subtitle { font-size: 11.5px !important; }
    }
    @media (max-width: 640px) {
        .v14-kpi-grid .kpi-card { padding: .85rem .88rem !important; }
        .kpi-label, .kpi-context, .kpi-trend { font-size: 11.5px !important; }
        .main div[data-testid="stPlotlyChart"] { border-radius: 12px !important; padding: .08rem !important; }
    }
    </style>
    """



def _v18_executive_finish_css() -> str:
    """V18 — polished executive hierarchy, page accents and presentation mode."""
    return r"""
    <style>
    :root {
        --bg-primary: #09111F;
        --bg-secondary: #0D1728;
        --bg-card: #111C2E;
        --bg-card-hover: #16243A;
        --bg-sidebar: #0B1525;
        --border-color: #263852;
        --border-soft: rgba(151,166,186,.13);
        --border-strong: rgba(151,166,186,.26);
        --brand: #9B8AFB;
        --brand-soft: rgba(155,138,251,.11);
        --brand-border: rgba(155,138,251,.27);
        --text-primary: #F8FAFC;
        --text-secondary: #D7E0EC;
        --text-muted: #97A6BA;
        --metric-blue: #4C8DFF;
        --metric-teal: #26C6B5;
        --metric-amber: #F5B84B;
        --metric-coral: #FF8A5B;
        --metric-violet: #B49AF7;
        --metric-sky: #56C8F5;
        --page-accent: var(--brand);
        --page-accent-soft: rgba(155,138,251,.13);
    }

    html, body, [class*="css"] { text-rendering: optimizeLegibility; }
    body, .stApp, [data-testid="stAppViewContainer"] { background:#09111F !important; color:var(--text-primary) !important; }
    .kpi-icon svg, .section-icon svg { display:inline-block; }
    .section-icon svg { width:1.18rem; height:1.18rem; vertical-align:-.18rem; }
    .main .block-container {
        max-width: 1560px !important;
        padding-top: 1.15rem !important;
        padding-bottom: 3.5rem !important;
    }

    /* Page identity: one restrained accent, never a performance signal. */
    body:has(.page-summary) { --page-accent:#9B8AFB; --page-accent-soft:rgba(155,138,251,.12); }
    body:has(.page-exams) { --page-accent:#4C8DFF; --page-accent-soft:rgba(76,141,255,.11); }
    body:has(.page-appointments) { --page-accent:#26C6B5; --page-accent-soft:rgba(38,198,181,.11); }
    body:has(.page-leaves) { --page-accent:#F5B84B; --page-accent-soft:rgba(245,184,75,.11); }
    body:has(.page-mental) { --page-accent:#B49AF7; --page-accent-soft:rgba(180,154,247,.11); }

    .dashboard-header.clean-header.page-aware-header {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 92% 14%, var(--page-accent-soft), transparent 32%),
            linear-gradient(135deg, rgba(255,255,255,.018), transparent 46%),
            var(--bg-card) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 16px !important;
        padding: 1.12rem 1.22rem 1rem !important;
        margin-bottom: .25rem !important;
        box-shadow: 0 10px 28px rgba(2,6,23,.16) !important;
    }
    .dashboard-header.clean-header.page-aware-header::before {
        content:"";
        position:absolute;
        left:0; top:0; bottom:0;
        width:3px;
        background:var(--page-accent);
        opacity:.9;
    }
    .header-eyebrow { color: var(--page-accent) !important; letter-spacing:.12em !important; font-size:11px !important; }
    .header-title { font-size: clamp(1.55rem, 2.15vw, 2.18rem) !important; letter-spacing:-.028em !important; }
    .header-subtitle { color: var(--text-secondary) !important; font-size:13px !important; max-width:880px; }
    .header-meta.clean-meta { margin-top:.56rem !important; gap:.55rem !important; }
    .header-badge { background: var(--page-accent-soft) !important; border-color: color-mix(in srgb, var(--page-accent) 30%, transparent) !important; color:var(--text-secondary) !important; }

    /* Scope is a compact sentence, not a second card under the header. */
    .filter-context-card.compact-filter-context {
        display:flex !important;
        align-items:center !important;
        gap:.42rem !important;
        min-height:auto !important;
        margin:.32rem .08rem .7rem !important;
        padding:0 !important;
        background:transparent !important;
        border:0 !important;
        box-shadow:none !important;
    }
    .compact-filter-context .scope-chip {
        padding:0 !important;
        border:0 !important;
        background:transparent !important;
        color:var(--text-muted) !important;
        font-size:12px !important;
        font-weight:600 !important;
    }
    .compact-filter-context .scope-period { color:var(--text-secondary) !important; }
    .scope-separator { color:#56657A; font-size:12px; }
    .specific-filter-note {
        margin:-.48rem .08rem .72rem !important;
        color:var(--page-accent) !important;
        font-size:11.5px !important;
        font-weight:650 !important;
    }

    /* KPI cards: calm surfaces, compact rhythm, data first. */
    .v14-kpi-grid { gap:.72rem !important; margin:.35rem 0 .75rem !important; }
    .v14-kpi-grid .kpi-card {
        min-height:132px !important;
        border-radius:14px !important;
        padding:.92rem 1rem .84rem !important;
        background:linear-gradient(180deg, rgba(255,255,255,.012), transparent 55%), var(--bg-card) !important;
        border:1px solid var(--border-soft) !important;
        box-shadow:0 7px 20px rgba(2,6,23,.13) !important;
    }
    .v14-kpi-grid .kpi-card:hover { border-color:var(--border-strong) !important; }
    .kpi-topline { min-height:24px !important; }
    .kpi-icon { width:27px !important; height:27px !important; border-radius:8px !important; }
    .kpi-label { font-size:11.5px !important; letter-spacing:.055em !important; color:var(--text-secondary) !important; }
    .kpi-value { font-size:clamp(1.72rem,2.25vw,2.08rem) !important; line-height:1.05 !important; margin:.18rem 0 .18rem !important; }
    .kpi-context { font-size:11.5px !important; line-height:1.35 !important; }
    .kpi-trend { font-size:11.7px !important; margin-top:.18rem !important; color:var(--text-secondary) !important; }
    .kpi-trend-pct { color:var(--text-muted) !important; font-weight:600 !important; }
    .kpi-sparkline { margin-top:.24rem !important; opacity:.92; }

    /* Analytical rhythm: smaller section ceremony and more room for the plot. */
    .section-header { margin:.82rem 0 .4rem !important; gap:.42rem !important; }
    .section-header h2 { font-size:clamp(1rem,1.28vw,1.17rem) !important; }
    .section-icon, body:has(.page-exams) .section-icon, body:has(.page-appointments) .section-icon,
    body:has(.page-leaves) .section-icon, body:has(.page-mental) .section-icon { color:var(--page-accent) !important; }
    .v16-chart-heading { margin:.26rem .04rem .24rem !important; }
    .v16-chart-title { font-size:14.5px !important; font-weight:720 !important; }
    .v16-chart-subtitle { font-size:11.8px !important; color:var(--text-muted) !important; }
    div[data-testid="stPlotlyChart"] {
        border-radius:13px !important;
        border-color:var(--border-soft) !important;
        box-shadow:0 5px 16px rgba(2,6,23,.11) !important;
        background:linear-gradient(180deg, rgba(255,255,255,.008), transparent 42%), var(--bg-card) !important;
        padding:.08rem .16rem .14rem !important;
    }

    /* Tabs inherit the page accent and read like navigation, not buttons. */
    .stTabs [data-baseweb="tab-list"] {
        gap:.18rem !important;
        padding:.22rem !important;
        background:rgba(151,166,186,.028) !important;
        border:1px solid var(--border-soft) !important;
        border-radius:12px !important;
    }
    .stTabs [data-baseweb="tab"] {
        min-height:35px !important;
        border-radius:9px !important;
        padding:.42rem .72rem !important;
        font-size:12px !important;
        color:var(--text-muted) !important;
    }
    .stTabs [aria-selected="true"] {
        color:var(--text-primary) !important;
        background:var(--page-accent-soft) !important;
        border-color:color-mix(in srgb, var(--page-accent) 28%, transparent) !important;
    }

    /* Sidebar: quieter, shorter and easier to scan. */
    section[data-testid="stSidebar"] { background:var(--bg-sidebar) !important; border-right:1px solid var(--border-soft) !important; }
    .sidebar-logo { margin-bottom:1.05rem !important; }
    .sidebar-logo-mark { background:linear-gradient(135deg,#9B8AFB,#4C8DFF) !important; box-shadow:none !important; }
    .sidebar-section { font-size:10.5px !important; letter-spacing:.12em !important; color:#74849A !important; margin:.72rem 0 .38rem !important; }
    .sidebar-divider { margin:.72rem 0 !important; border-color:var(--border-soft) !important; }
    section[data-testid="stSidebar"] .stCaption { font-size:11.2px !important; }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="base-input"] {
        min-height:38px !important;
        background:#0F1B2E !important;
        border-color:var(--border-soft) !important;
    }
    section[data-testid="stSidebar"] details {
        background:rgba(151,166,186,.018) !important;
        border:1px solid var(--border-soft) !important;
        border-radius:10px !important;
    }
    section[data-testid="stSidebar"] details summary { font-size:12px !important; padding:.48rem .6rem !important; }
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stDownloadButton > button { min-height:36px !important; font-size:11.8px !important; }

    /* Insight cards use a neutral left accent and less vertical space. */
    .insight-card, [class*="shad-alert"] {
        border-color:var(--border-soft) !important;
        box-shadow:none !important;
    }

    .safe-html-table { border:1px solid var(--border-soft) !important; border-radius:12px !important; overflow:auto !important; }

    /* Native Streamlit controls — one visual language, no legacy neon. */
    .stApp {
        background:
            radial-gradient(circle at 88% -8%, var(--page-accent-soft), transparent 26%),
            radial-gradient(circle at 6% 108%, rgba(76,141,255,.035), transparent 28%),
            var(--bg-primary) !important;
        color:var(--text-primary) !important;
    }
    .stButton > button,
    .stDownloadButton > button {
        border:1px solid var(--border-soft) !important;
        background:#0F1B2E !important;
        color:var(--text-secondary) !important;
        border-radius:10px !important;
        box-shadow:none !important;
        font-weight:650 !important;
        transition:background .16s ease,border-color .16s ease,transform .16s ease !important;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background:var(--bg-card-hover) !important;
        border-color:var(--border-strong) !important;
        color:var(--text-primary) !important;
        transform:translateY(-1px);
    }
    .stButton > button:focus-visible,
    .stDownloadButton > button:focus-visible,
    [data-baseweb="select"]:focus-within,
    [data-baseweb="base-input"]:focus-within {
        outline:2px solid color-mix(in srgb,var(--brand) 55%,transparent) !important;
        outline-offset:2px !important;
        box-shadow:none !important;
    }
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background:#111C2E !important;
        border:1px solid var(--border-soft) !important;
        border-radius:12px !important;
        box-shadow:0 18px 42px rgba(2,6,23,.36) !important;
    }
    li[role="option"] {
        color:var(--text-secondary) !important;
        font-size:12.5px !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background:rgba(155,138,251,.09) !important;
        color:var(--text-primary) !important;
    }
    [data-baseweb="tag"] {
        background:rgba(155,138,251,.10) !important;
        border:1px solid rgba(155,138,251,.18) !important;
        color:var(--text-secondary) !important;
        border-radius:8px !important;
    }
    .stRadio [role="radiogroup"] { gap:.35rem !important; }
    .stRadio label,
    .stCheckbox label,
    [data-testid="stToggle"] label { color:var(--text-secondary) !important; }
    [data-testid="stToggle"] [role="switch"][aria-checked="true"] {
        background:var(--brand) !important;
    }
    div[data-testid="stExpander"] {
        background:rgba(17,28,46,.62) !important;
        border:1px solid var(--border-soft) !important;
        box-shadow:none !important;
        border-radius:12px !important;
    }
    div[data-testid="stExpander"] summary:hover { color:var(--text-primary) !important; }
    [data-testid="stAlert"] {
        border:1px solid var(--border-soft) !important;
        background:rgba(17,28,46,.72) !important;
        color:var(--text-secondary) !important;
        border-radius:12px !important;
    }
    div[data-testid="stPlotlyChart"] .modebar {
        background:rgba(17,28,46,.88) !important;
        border:1px solid var(--border-soft) !important;
        border-radius:9px !important;
        padding:2px !important;
    }
    div[data-testid="stPlotlyChart"] .modebar-btn path { fill:var(--text-muted) !important; }
    div[data-testid="stPlotlyChart"] .modebar-btn:hover path { fill:var(--text-primary) !important; }
    .safe-html-table tbody tr:hover td { background:rgba(76,141,255,.035) !important; }
    hr { border-color:var(--border-soft) !important; opacity:1 !important; }
    * { scrollbar-color:#33445E #0B1525; }
    ::-webkit-scrollbar { width:10px; height:10px; }
    ::-webkit-scrollbar-track { background:#0B1525; }
    ::-webkit-scrollbar-thumb { background:#33445E; border:2px solid #0B1525; border-radius:999px; }
    ::-webkit-scrollbar-thumb:hover { background:#425570; }

    /* Presentation mode: dashboard becomes a clean slide-like canvas. */
    body:has(.presentation-mode-marker) section[data-testid="stSidebar"] { display:none !important; }
    body:has(.presentation-mode-marker) header[data-testid="stHeader"] { background:transparent !important; }
    body:has(.presentation-mode-marker) .main .block-container {
        max-width:1780px !important;
        padding-left:2rem !important;
        padding-right:2rem !important;
        padding-top:.55rem !important;
    }
    body:has(.presentation-mode-marker) .dashboard-header.clean-header.page-aware-header { padding:1.2rem 1.35rem !important; }
    body:has(.presentation-mode-marker) .header-title { font-size:clamp(1.8rem,2.4vw,2.45rem) !important; }
    body:has(.presentation-mode-marker) .v14-kpi-grid .kpi-card { min-height:142px !important; }
    body:has(.presentation-mode-marker) .kpi-value { font-size:clamp(1.95rem,2.6vw,2.45rem) !important; }
    body:has(.presentation-mode-marker) .v16-chart-title { font-size:15.5px !important; }
    body:has(.presentation-mode-marker) .stExpander { display:none !important; }

    @media (max-width: 980px) {
        .main .block-container { padding-left:1rem !important; padding-right:1rem !important; }
        .dashboard-header.clean-header.page-aware-header { border-radius:14px !important; }
        .v14-kpi-grid { --kpi-cols:2 !important; }
    }
    @media (max-width: 560px) {
        .main .block-container { padding-left:.72rem !important; padding-right:.72rem !important; }
        .dashboard-header.clean-header.page-aware-header { padding:.9rem .9rem .82rem !important; }
        .header-subtitle { font-size:12px !important; }
        .compact-filter-context .scope-chip { font-size:11.3px !important; }
        .v14-kpi-grid { --kpi-cols:1 !important; gap:.55rem !important; }
        .v14-kpi-grid .kpi-card { min-height:122px !important; }
    }
    </style>
    """


# ---------------------------------------------------------------------------
# V19 — Executive polish: cleaner hierarchy, tactile controls and calm depth.
# ---------------------------------------------------------------------------
def _v19_executive_polish_css() -> str:
    return r"""
    <style>
    :root {
        --v19-surface-1:#0C1627;
        --v19-surface-2:#111D31;
        --v19-surface-3:#17253C;
        --v19-hairline:rgba(169,184,204,.12);
        --v19-hairline-strong:rgba(169,184,204,.22);
        --v19-shadow:0 12px 30px rgba(1,6,15,.18);
    }

    /* Canvas: depth comes from extremely soft light, not glow. */
    .stApp {
        background:
            radial-gradient(900px 460px at 86% -120px, color-mix(in srgb,var(--page-accent) 7%,transparent), transparent 72%),
            linear-gradient(180deg,#09111F 0%,#08101D 100%) !important;
    }
    .main .block-container { padding-top:.9rem !important; }
    ::selection { background:var(--page-accent-soft); color:var(--text-primary); }
    ::-webkit-scrollbar { width:8px !important; height:8px !important; }

    /* Header: compact product identity + one integrated scope rail. */
    .dashboard-header.clean-header.page-aware-header {
        isolation:isolate;
        padding:1.05rem 1.15rem .78rem !important;
        border-radius:18px !important;
        background:
            linear-gradient(135deg,rgba(255,255,255,.018),transparent 54%),
            var(--v19-surface-2) !important;
        border-color:var(--v19-hairline) !important;
        box-shadow:var(--v19-shadow) !important;
        margin-bottom:.72rem !important;
    }
    .dashboard-header.clean-header.page-aware-header::before {
        width:2px !important;
        opacity:.82 !important;
    }
    .dashboard-header.clean-header.page-aware-header::after {
        content:"";
        position:absolute;
        z-index:-1;
        width:240px;
        height:240px;
        right:-85px;
        top:-140px;
        border-radius:50%;
        background:var(--page-accent);
        opacity:.055;
        filter:blur(2px);
        pointer-events:none;
    }
    .header-identity-row {
        display:grid;
        grid-template-columns:auto minmax(0,1fr) auto;
        align-items:center;
        gap:.82rem;
    }
    .header-page-icon {
        width:43px;
        height:43px;
        border-radius:12px;
        display:grid;
        place-items:center;
        color:var(--page-accent);
        background:color-mix(in srgb,var(--page-accent) 9%,transparent);
        border:1px solid color-mix(in srgb,var(--page-accent) 18%,transparent);
        box-shadow:inset 0 1px 0 rgba(255,255,255,.035);
    }
    .header-page-icon svg { width:21px; height:21px; }
    .header-main { min-width:0; }
    .header-eyebrow { margin-bottom:.12rem !important; font-size:10px !important; font-weight:760 !important; }
    .header-title { font-size:clamp(1.48rem,2vw,2.02rem) !important; line-height:1.06 !important; }
    .header-subtitle { margin-top:.28rem !important; max-width:900px !important; line-height:1.42 !important; color:#C1CCDA !important; }
    .header-badge {
        align-self:start;
        padding:.32rem .56rem !important;
        border-radius:999px !important;
        font-size:10.5px !important;
        letter-spacing:.035em;
    }
    .header-scope {
        display:flex;
        align-items:center;
        gap:.72rem;
        margin-top:.74rem;
        padding-top:.62rem;
        border-top:1px solid var(--v19-hairline);
        min-width:0;
    }
    .header-scope-item { display:flex; align-items:baseline; gap:.38rem; min-width:0; }
    .header-scope-item span {
        font-size:10.5px;
        color:#8797AC;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:.055em;
    }
    .header-scope-item strong {
        color:#C9D4E2;
        font-size:11.5px;
        font-weight:680;
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
    }
    .header-scope-divider { width:1px; height:12px; background:var(--v19-hairline-strong); flex:0 0 auto; }
    .header-scope-update { margin-left:auto; }
    .specific-filter-note {
        display:inline-flex;
        align-items:center;
        margin:-.38rem 0 .66rem .1rem !important;
        padding:.26rem .48rem;
        border-radius:7px;
        background:var(--page-accent-soft);
        color:color-mix(in srgb,var(--page-accent) 80%,white) !important;
        border:1px solid color-mix(in srgb,var(--page-accent) 18%,transparent);
        font-size:10.8px !important;
    }

    /* Sidebar navigation behaves like a calm app rail. */
    section[data-testid="stSidebar"] { box-shadow:14px 0 40px rgba(1,6,15,.08); }
    section[data-testid="stSidebar"] .sidebar-logo { padding:.22rem .18rem .08rem; }
    section[data-testid="stSidebar"] .sidebar-logo-mark {
        border-radius:11px !important;
        background:linear-gradient(145deg,#8E7DF2,#4C8DFF) !important;
        box-shadow:inset 0 1px 0 rgba(255,255,255,.16) !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] { gap:.18rem !important; }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        min-height:37px;
        padding:.38rem .52rem !important;
        border-radius:9px;
        border:1px solid transparent;
        transition:background .14s ease,border-color .14s ease,color .14s ease !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background:rgba(169,184,204,.045) !important;
        border-color:var(--v19-hairline) !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has([aria-checked="true"]) {
        background:var(--page-accent-soft) !important;
        border-color:color-mix(in srgb,var(--page-accent) 19%,transparent) !important;
        color:var(--text-primary) !important;
        box-shadow:inset 2px 0 0 var(--page-accent);
    }
    section[data-testid="stSidebar"] [data-testid="stToggle"] {
        margin:.18rem 0 .3rem;
        padding:.48rem .55rem;
        border:1px solid var(--v19-hairline);
        background:rgba(169,184,204,.025);
        border-radius:10px;
    }
    .v19-filter-status {
        display:flex;
        align-items:center;
        gap:.4rem;
        color:#AAB8C9;
        font-size:10.8px;
        font-weight:650;
        margin:.48rem .04rem .34rem;
    }
    .v19-filter-status span {
        width:6px;
        height:6px;
        border-radius:999px;
        background:var(--page-accent);
        box-shadow:0 0 0 3px var(--page-accent-soft);
    }

    /* KPI: one tiny metric accent, no colored card border. */
    .kpi-card.blue { --kpi-accent:var(--metric-blue); --kpi-soft:rgba(76,141,255,.08); }
    .kpi-card.green { --kpi-accent:var(--metric-teal); --kpi-soft:rgba(38,198,181,.08); }
    .kpi-card.cyan { --kpi-accent:var(--metric-sky); --kpi-soft:rgba(86,200,245,.08); }
    .kpi-card.orange { --kpi-accent:var(--metric-amber); --kpi-soft:rgba(245,184,75,.08); }
    .kpi-card.red { --kpi-accent:var(--metric-coral); --kpi-soft:rgba(255,138,91,.08); }
    .kpi-card.purple { --kpi-accent:var(--metric-violet); --kpi-soft:rgba(180,154,247,.08); }
    .v14-kpi-grid { gap:.66rem !important; }
    .v14-kpi-grid .kpi-card {
        position:relative;
        overflow:hidden;
        min-height:130px !important;
        border-radius:15px !important;
        background:
            radial-gradient(160px 105px at 100% 0%,var(--kpi-soft,rgba(155,138,251,.06)),transparent 72%),
            var(--v19-surface-2) !important;
        border:1px solid var(--v19-hairline) !important;
        box-shadow:0 8px 20px rgba(1,6,15,.12) !important;
        transition:transform .15s ease,border-color .15s ease,background .15s ease !important;
    }
    .v14-kpi-grid .kpi-card::before {
        content:"";
        position:absolute;
        top:0;
        left:14px;
        right:14px;
        height:2px;
        border-radius:0 0 4px 4px;
        background:linear-gradient(90deg,var(--kpi-accent,transparent),transparent 72%);
        opacity:.78;
    }
    .v14-kpi-grid .kpi-card:hover {
        transform:translateY(-1px);
        border-color:var(--v19-hairline-strong) !important;
        background:
            radial-gradient(170px 115px at 100% 0%,var(--kpi-soft,rgba(155,138,251,.07)),transparent 72%),
            var(--v19-surface-2) !important;
    }
    .kpi-icon {
        border:1px solid color-mix(in srgb,var(--kpi-accent,var(--page-accent)) 13%,transparent) !important;
        box-shadow:inset 0 1px 0 rgba(255,255,255,.025);
    }
    .kpi-label { color:#BFCCDB !important; font-weight:720 !important; }
    .kpi-value { letter-spacing:-.035em !important; font-variant-numeric:tabular-nums; }
    .kpi-context { color:#8292A7 !important; }
    .kpi-trend { font-variant-numeric:tabular-nums; }
    .kpi-help { color:#708198 !important; opacity:.78; }

    /* Sections gain a visual rail so scanning a long page is easier. */
    .section-header { display:flex !important; width:100%; align-items:center !important; }
    .section-header::after {
        content:"";
        height:1px;
        flex:1 1 auto;
        margin-left:.42rem;
        background:linear-gradient(90deg,color-mix(in srgb,var(--page-accent) 17%,transparent),transparent 88%);
    }
    .section-icon {
        width:25px !important;
        height:25px !important;
        display:grid !important;
        place-items:center !important;
        border-radius:7px !important;
        background:var(--page-accent-soft) !important;
        border:1px solid color-mix(in srgb,var(--page-accent) 13%,transparent);
        flex:0 0 auto;
    }
    .section-icon svg { width:14px !important; height:14px !important; vertical-align:0 !important; }
    .section-header h2 { letter-spacing:-.012em !important; }

    /* Plot cards: calmer border and a tiny title accent. */
    .v16-chart-heading { position:relative; padding-left:.58rem; margin-top:.32rem !important; }
    .v16-chart-heading::before {
        content:"";
        position:absolute;
        left:0;
        top:.2rem;
        bottom:.22rem;
        width:2px;
        border-radius:4px;
        background:var(--page-accent);
        opacity:.68;
    }
    .v16-chart-title { color:#E7EEF7 !important; font-size:14px !important; }
    .v16-chart-subtitle { margin-top:.08rem; line-height:1.35; }
    div[data-testid="stPlotlyChart"] {
        border:1px solid var(--v19-hairline) !important;
        border-radius:14px !important;
        background:var(--v19-surface-2) !important;
        box-shadow:0 7px 18px rgba(1,6,15,.10) !important;
        overflow:hidden;
    }
    div[data-testid="stPlotlyChart"]:hover { border-color:var(--v19-hairline-strong) !important; }

    /* Segmented tabs with a clearer selected state. */
    .stTabs [data-baseweb="tab-list"] {
        padding:.2rem !important;
        border-radius:11px !important;
        background:#0C1728 !important;
        border-color:var(--v19-hairline) !important;
    }
    .stTabs [data-baseweb="tab"] {
        min-height:36px !important;
        padding:.42rem .78rem !important;
        font-weight:650 !important;
    }
    .stTabs [aria-selected="true"] {
        background:color-mix(in srgb,var(--page-accent) 9%,#111D31) !important;
        box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--page-accent) 14%,transparent) !important;
    }

    /* Insights: page identity instead of generic grey boxes. */
    .shad-alert {
        position:relative;
        overflow:hidden;
        padding:.72rem .78rem !important;
        background:linear-gradient(90deg,var(--page-accent-soft),rgba(17,29,49,.82) 42%) !important;
        border:1px solid var(--v19-hairline) !important;
        border-radius:12px !important;
    }
    .shad-alert::before {
        content:"";
        position:absolute;
        inset:0 auto 0 0;
        width:2px;
        background:var(--page-accent);
        opacity:.72;
    }
    .shad-alert-icon {
        width:26px !important;
        height:26px !important;
        color:var(--page-accent) !important;
        background:color-mix(in srgb,var(--page-accent) 9%,transparent) !important;
        border:1px solid color-mix(in srgb,var(--page-accent) 14%,transparent);
    }
    .shad-alert-icon svg { width:14px; height:14px; }
    .shad-alert-title { font-size:12.5px !important; letter-spacing:-.005em; }
    .shad-alert-message { font-size:12px !important; color:#B7C4D4 !important; }

    /* Purpose-built empty state: clear next action, no alert semantics. */
    .v19-empty-state {
        min-height:180px;
        display:flex;
        align-items:center;
        justify-content:center;
        gap:1rem;
        padding:1.4rem;
        border:1px dashed var(--v19-hairline-strong);
        border-radius:15px;
        background:linear-gradient(135deg,rgba(169,184,204,.025),transparent),var(--v19-surface-1);
        text-align:left;
    }
    .v19-empty-icon {
        width:48px;
        height:48px;
        display:grid;
        place-items:center;
        flex:0 0 auto;
        border-radius:14px;
        color:var(--page-accent);
        background:var(--page-accent-soft);
        border:1px solid color-mix(in srgb,var(--page-accent) 16%,transparent);
    }
    .v19-empty-icon svg { width:22px; height:22px; }
    .v19-empty-copy { max-width:520px; }
    .v19-empty-title { color:var(--text-primary); font-size:15px; font-weight:760; letter-spacing:-.01em; }
    .v19-empty-message { color:#B7C4D4; font-size:12.5px; line-height:1.5; margin-top:.22rem; }
    .v19-empty-hint { color:#7F90A6; font-size:11.5px; line-height:1.45; margin-top:.38rem; }

    /* Tables: sticky quiet header + tabular numerals. */
    .safe-html-table { background:var(--v19-surface-2) !important; box-shadow:0 7px 18px rgba(1,6,15,.08); }
    .safe-html-table thead th {
        position:sticky;
        top:0;
        z-index:2;
        background:#132036 !important;
        color:#B9C6D6 !important;
        font-size:10.8px !important;
        letter-spacing:.035em;
        text-transform:uppercase;
        border-bottom:1px solid var(--v19-hairline-strong) !important;
    }
    .safe-html-table tbody td { font-variant-numeric:tabular-nums; }
    .safe-html-table tbody tr:nth-child(even) td { background:rgba(169,184,204,.012); }
    .safe-html-table tbody tr:hover td { background:var(--page-accent-soft) !important; }

    /* Inputs and expanders feel like one product surface. */
    div[data-testid="stExpander"] {
        border-radius:11px !important;
        background:rgba(12,22,39,.72) !important;
    }
    div[data-testid="stExpander"] summary { min-height:38px; }
    .stButton > button,
    .stDownloadButton > button {
        border-radius:9px !important;
        background:#101C2F !important;
    }
    .stButton > button:active,
    .stDownloadButton > button:active { transform:translateY(0) scale(.995); }

    /* Presentation: scope remains readable but technical update detail recedes. */
    body:has(.presentation-mode-marker) .dashboard-header.clean-header.page-aware-header { padding:1.18rem 1.32rem .88rem !important; }
    body:has(.presentation-mode-marker) .header-page-icon { width:48px; height:48px; }
    body:has(.presentation-mode-marker) .header-scope-update { opacity:.76; }

    @media (max-width: 980px) {
        .header-identity-row { grid-template-columns:auto minmax(0,1fr); }
        .header-badge { display:none; }
        .header-scope { flex-wrap:wrap; gap:.38rem .58rem; }
        .header-scope-update { margin-left:0; }
    }
    @media (max-width: 620px) {
        .dashboard-header.clean-header.page-aware-header { padding:.82rem !important; border-radius:14px !important; }
        .header-page-icon { width:38px; height:38px; border-radius:10px; }
        .header-page-icon svg { width:18px; height:18px; }
        .header-subtitle { font-size:11.8px !important; }
        .header-scope { gap:.28rem .48rem; margin-top:.6rem; padding-top:.52rem; }
        .header-scope-item span { display:none; }
        .header-scope-item strong { font-size:10.8px; }
        .header-scope-update { flex-basis:100%; }
        .v19-empty-state { min-height:150px; align-items:flex-start; justify-content:flex-start; padding:1rem; }
        .section-header::after { opacity:.55; }
    }

    @media (prefers-reduced-motion: reduce) {
        .v14-kpi-grid .kpi-card,
        section[data-testid="stSidebar"] div[role="radiogroup"] > label { transition:none !important; }
        .v14-kpi-grid .kpi-card:hover { transform:none !important; }
    }
    </style>
    """



# ---------------------------------------------------------------------------
# V25 — Elegant Vibrancy Refresh
#
# Goal: keep every structural/functional rule from V14–V20 untouched (grid,
# spacing, responsive breakpoints, accessibility contrast) and only turn up
# *presence* — depth, glow, gradient, contrast — on the same tokens/classes
# those layers already expose (--v19-hairline, --v19-shadow, --kpi-accent,
# --page-accent, .kpi-icon, .section-header, etc.). Nothing here introduces
# a new hue: every accent used is already part of the existing metric/page
# color system, so identity stays consistent — the metric that was blue
# stays blue, the page that was violet stays violet. Appended after V20 and
# before V22/V23/V24 on purpose: those three layers own the select/dropdown
# fix that's already confirmed working, so this layer never touches
# `[data-baseweb=...]`/`[role="option"]` selectors at all.
# ---------------------------------------------------------------------------
def _v25_elegant_vibrancy_css() -> str:
    return r"""
    <style>
    :root {
        /* Same hairline tokens V19 already defined, just given more presence
           so card/header/sidebar edges read as intentional, not accidental. */
        --v19-hairline: rgba(169, 184, 204, .20);
        --v19-hairline-strong: rgba(169, 184, 204, .36);
        --v19-shadow: 0 16px 38px rgba(1, 6, 15, .38);
    }

    /* ----- Atmosphere: two soft glow sources instead of flat black ----- */
    .stApp {
        background:
            radial-gradient(1100px 560px at 88% -160px, color-mix(in srgb, var(--page-accent) 14%, transparent), transparent 70%),
            radial-gradient(760px 460px at 4% 108%, color-mix(in srgb, #4C8DFF 10%, transparent), transparent 68%),
            linear-gradient(180deg, #09111F 0%, #060A14 100%) !important;
    }

    /* ----- Header: stronger identity glow, tied to the page accent ----- */
    .dashboard-header.clean-header.page-aware-header {
        box-shadow: var(--v19-shadow), inset 0 1px 0 rgba(255,255,255,.035) !important;
        border-color: color-mix(in srgb, var(--page-accent) 22%, var(--v19-hairline)) !important;
    }
    .dashboard-header.clean-header.page-aware-header::after {
        background: radial-gradient(closest-side, color-mix(in srgb, var(--page-accent) 32%, transparent), transparent 72%) !important;
        opacity: .95 !important;
    }
    .header-eyebrow {
        text-shadow: 0 0 22px color-mix(in srgb, var(--page-accent) 60%, transparent);
    }

    /* ----- Section headers: icon becomes a real chip + accent underline ----- */
    .section-header .section-icon {
        width: 34px !important;
        height: 34px !important;
        display: inline-grid !important;
        place-items: center !important;
        border-radius: 10px !important;
        background: linear-gradient(145deg, color-mix(in srgb, var(--page-accent) 26%, transparent), color-mix(in srgb, var(--page-accent) 7%, transparent)) !important;
        border: 1px solid color-mix(in srgb, var(--page-accent) 32%, transparent) !important;
        color: var(--page-accent) !important;
        box-shadow: 0 8px 18px -8px color-mix(in srgb, var(--page-accent) 70%, transparent);
    }
    .section-header h2 {
        position: relative;
        padding-bottom: .3rem;
    }
    .section-header h2::after {
        content: "";
        position: absolute;
        left: 0;
        bottom: 0;
        width: 46px;
        height: 3px;
        border-radius: 3px;
        background: linear-gradient(90deg, var(--page-accent), transparent);
    }

    /* ----- KPI cards: richer tint, colored glow on hover, gradient chip ----- */
    .kpi-card.blue   { --kpi-soft: rgba(76,141,255,.18);  --kpi-glow: rgba(76,141,255,.45); }
    .kpi-card.green  { --kpi-soft: rgba(38,198,181,.18);  --kpi-glow: rgba(38,198,181,.45); }
    .kpi-card.cyan   { --kpi-soft: rgba(86,200,245,.18);  --kpi-glow: rgba(86,200,245,.45); }
    .kpi-card.orange { --kpi-soft: rgba(245,184,75,.18);  --kpi-glow: rgba(245,184,75,.45); }
    .kpi-card.red    { --kpi-soft: rgba(255,138,91,.18);  --kpi-glow: rgba(255,138,91,.45); }
    .kpi-card.purple { --kpi-soft: rgba(180,154,247,.18); --kpi-glow: rgba(180,154,247,.45); }

    .v14-kpi-grid .kpi-card {
        box-shadow: 0 12px 28px rgba(1,6,15,.32) !important;
        transition: transform .18s ease, border-color .18s ease, box-shadow .22s ease !important;
    }
    .v14-kpi-grid .kpi-card:hover {
        transform: translateY(-3px) !important;
        border-color: color-mix(in srgb, var(--kpi-accent, var(--page-accent)) 38%, var(--v19-hairline-strong)) !important;
        box-shadow:
            0 18px 40px rgba(1,6,15,.4),
            0 0 48px -14px var(--kpi-glow, transparent) !important;
    }
    .v14-kpi-grid .kpi-card::before {
        height: 3px !important;
        opacity: 1 !important;
        box-shadow: 0 0 14px -2px var(--kpi-accent, transparent);
    }
    .kpi-icon {
        width: 36px !important;
        height: 36px !important;
        border-radius: 11px !important;
        background: linear-gradient(150deg, var(--kpi-accent, #4C8DFF), color-mix(in srgb, var(--kpi-accent, #4C8DFF) 60%, #060A14)) !important;
        box-shadow: 0 8px 18px -7px var(--kpi-glow, transparent);
    }
    .kpi-icon, .kpi-icon svg { color: #F8FAFC !important; }
    .kpi-value {
        background: linear-gradient(135deg, #FFFFFF 0%, color-mix(in srgb, var(--kpi-accent, #4C8DFF) 55%, white) 100%);
        -webkit-background-clip: text !important;
        background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -.01em;
    }

    /* ----- Sidebar: active item glows, logo mark gets a real gradient ----- */
    .sidebar-logo-mark {
        background: linear-gradient(150deg, #6AA3FF, #2F6FE4) !important;
        border-color: rgba(255,255,255,.16) !important;
        color: #F8FAFC !important;
        box-shadow: 0 8px 18px -8px rgba(76,141,255,.55);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has([aria-checked="true"]) {
        box-shadow:
            inset 3px 0 0 var(--page-accent),
            0 0 22px -10px color-mix(in srgb, var(--page-accent) 70%, transparent) !important;
    }
    .v19-filter-status span {
        box-shadow: 0 0 0 4px var(--page-accent-soft), 0 0 10px -2px var(--page-accent);
    }

    /* ----- Chart title dot: brighter glow ring ----- */
    .chart-title .dot {
        box-shadow: 0 0 0 3px color-mix(in srgb, currentColor 18%, transparent), 0 0 10px -1px currentColor !important;
    }

    /* ----- Insight / alert icon chips: match the variant color, not gray ----- */
    .shad-alert.success .shad-alert-icon { background: rgba(16,185,129,.16) !important; color: #34D399 !important; }
    .shad-alert.warning .shad-alert-icon { background: rgba(245,158,11,.16) !important; color: #FBBF24 !important; }
    .shad-alert.destructive .shad-alert-icon { background: rgba(220,38,38,.16) !important; color: #F87171 !important; }

    /* ----- Buttons: a little more presence on primary actions ----- */
    button[kind="primary"], .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5B9BFF, #2F6FE4) !important;
        border: none !important;
        box-shadow: 0 10px 22px -8px rgba(47,111,228,.6) !important;
        transition: transform .15s ease, box-shadow .15s ease !important;
    }
    button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 14px 28px -8px rgba(47,111,228,.7) !important;
    }

    /* ----- Tabs: active tab gets a glowing underline instead of a flat line ----- */
    .stTabs [data-baseweb="tab-list"] [aria-selected="true"] {
        box-shadow: inset 0 -2px 0 var(--page-accent), 0 8px 16px -12px var(--page-accent) !important;
    }

    @media (prefers-reduced-motion: reduce) {
        .v14-kpi-grid .kpi-card:hover { transform: none !important; }
        button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover { transform: none !important; }
    }
    </style>
    """



# ---------------------------------------------------------------------------
# V22 — Native Controls Polish
# ---------------------------------------------------------------------------
def _v22_controls_polish_css() -> str:
    return r"""
    <style>
    /* Global control palette: functional blue on neutral navy/slate surfaces. */
    :root {
        --control-accent:#4C8DFF;
        --control-accent-strong:#76A9FF;
        --control-accent-soft:rgba(76,141,255,.14);
        --control-bg:#0F1B2E;
        --control-bg-hover:#16263D;
        --control-bg-selected:#1D3150;
        --control-border:#29415F;
        --control-border-hover:#3B587B;
        --control-text:#F8FAFC;
        --control-muted:#A9B8CC;
    }

    /* Selectbox / multiselect shell. */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        min-height:40px !important;
        background:var(--control-bg) !important;
        border:1px solid var(--control-border) !important;
        border-radius:10px !important;
        box-shadow:none !important;
        color:var(--control-text) !important;
        transition:background .15s ease,border-color .15s ease,box-shadow .15s ease !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div:hover,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div:hover {
        background:var(--control-bg-hover) !important;
        border-color:var(--control-border-hover) !important;
    }

    /* One focus ring on the OUTER control only. This removes the tiny cyan/blue
       rectangle created by the hidden BaseWeb input receiving the global ring. */
    div[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within,
    div[data-testid="stMultiSelect"] [data-baseweb="select"]:focus-within {
        outline:none !important;
        box-shadow:0 0 0 2px rgba(76,141,255,.22) !important;
        border-radius:11px !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div,
    div[data-testid="stMultiSelect"] [data-baseweb="select"]:focus-within > div {
        border-color:var(--control-accent) !important;
        box-shadow:0 0 0 1px rgba(76,141,255,.16) !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] input:focus,
    div[data-testid="stSelectbox"] [data-baseweb="select"] input:focus-visible,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] input:focus,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] input:focus-visible {
        outline:none !important;
        outline-offset:0 !important;
        box-shadow:none !important;
        border:none !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] input {
        caret-color:transparent !important;
    }

    /* Text and dropdown arrow. */
    div[data-testid="stSelectbox"] [data-baseweb="select"] span,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] span {
        color:var(--control-text) !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] svg,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] svg {
        fill:var(--control-muted) !important;
        color:var(--control-muted) !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within svg,
    div[data-testid="stMultiSelect"] [data-baseweb="select"]:focus-within svg {
        fill:var(--control-accent-strong) !important;
        color:var(--control-accent-strong) !important;
    }

    /* Dropdown / popover surface. Keep BaseWeb geometry intact. */
    body [data-baseweb="popover"] > div,
    body [data-baseweb="menu"],
    body [role="listbox"] {
        background:#101A2B !important;
        background-color:#101A2B !important;
        border:1px solid var(--control-border) !important;
        border-radius:12px !important;
        box-shadow:0 16px 40px rgba(2,6,23,.42) !important;
        overflow:hidden !important;
    }
    body [role="option"],
    body li[role="option"] {
        min-height:38px !important;
        padding:.58rem .78rem !important;
        background:#101A2B !important;
        background-color:#101A2B !important;
        color:#D7E0EC !important;
        border-bottom:1px solid rgba(148,163,184,.07) !important;
        font-size:12.5px !important;
        font-weight:500 !important;
    }
    body [role="option"]:last-child,
    body li[role="option"]:last-child { border-bottom:none !important; }
    body [role="option"]:hover,
    body [role="option"][data-highlighted="true"],
    body li[role="option"]:hover {
        background:var(--control-bg-hover) !important;
        background-color:var(--control-bg-hover) !important;
        color:var(--control-text) !important;
    }
    body [role="option"][aria-selected="true"],
    body li[role="option"][aria-selected="true"] {
        background:var(--control-bg-selected) !important;
        background-color:var(--control-bg-selected) !important;
        color:var(--control-text) !important;
        font-weight:650 !important;
        box-shadow:inset 3px 0 0 var(--control-accent) !important;
    }
    body [role="option"] * { color:inherit !important; }

    /* Selected multiselect tags: quieter and consistent with the blue control accent. */
    [data-baseweb="tag"] {
        background:rgba(76,141,255,.11) !important;
        border:1px solid rgba(76,141,255,.22) !important;
        color:#DCE9FF !important;
        border-radius:8px !important;
        box-shadow:none !important;
    }
    [data-baseweb="tag"] svg { fill:#9DBDFF !important; }

    /* Table toolbar controls: compact, clear and aligned. */
    .stTextInput input {
        background:var(--control-bg) !important;
        border-color:var(--control-border) !important;
        color:var(--control-text) !important;
        border-radius:10px !important;
    }
    .stTextInput input:focus {
        border-color:var(--control-accent) !important;
        box-shadow:0 0 0 2px rgba(76,141,255,.15) !important;
        outline:none !important;
    }
    .stTextInput input::placeholder { color:#7F91A8 !important; }

    /* Sidebar controls follow the same neutral language. */
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        background:#0D192A !important;
        border-color:#233A55 !important;
    }

    /* Small screens: preserve touch target and avoid clipping long selected values. */
    @media (max-width: 980px) {
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
        div[data-testid="stMultiSelect"] [data-baseweb="select"] > div { min-height:42px !important; }
        body [role="option"], body li[role="option"] { min-height:40px !important; font-size:12px !important; }
    }

    @media (prefers-reduced-motion: reduce) {
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
        div[data-testid="stMultiSelect"] [data-baseweb="select"] > div { transition:none !important; }
    }
    </style>
    """


# ---------------------------------------------------------------------------
# get_css() — single source of truth
#
# Concatenates the base stylesheet with every active CSS layer, in the order
# they were introduced. This replaced a chain of same-named get_css()
# redefinitions (each one wrapping the previous) that had accumulated across
# many hotfixes. That pattern silently broke in five consecutive iterations
# (V10.5.6 through the pre-V10.6 purple/button/chart/image touch-ups): each
# added a new CSS fragment function but never re-wrapped get_css() to include
# it, so ~556 lines of intended styling were defined but never reached the
# page. This
# version is behavior-preserving for every layer that WAS reachable before —
# only the dead, unreachable fragments were removed.
# ---------------------------------------------------------------------------
def get_css() -> str:
    return (
        _get_css_base()
        + _v_responsive_improvements()
        + _v13_accessibility_css()
        + _v14_executive_ux_css()
        + _v14_1_analytic_tabs_css()
        + _v16_visual_refinement_css()
        + _v18_executive_finish_css()
        + _v19_executive_polish_css()
        + _v19_1_header_hotfix_css()
        + _v20_adaptive_responsive_css()
        + _v25_elegant_vibrancy_css()
        + _v22_controls_polish_css()
        + _v23_dropdown_definitive_fix_css()
        + _v26_micro_interactions_css()
        + _v27_fluid_zoom_polish_css()
    )

# ---------------------------------------------------------------------------
# V19.1 — Header rendering hotfix
# ---------------------------------------------------------------------------
def _v19_1_header_hotfix_css() -> str:
    return r"""
    <style>
    /* Older V14/V16 layers set this container to flex!important.  The V19
       header has two vertical rows (identity + scope), so force the intended
       block layout at the final cascade position. */
    .dashboard-header.clean-header.page-aware-header {
        display:block !important;
        width:100% !important;
        min-width:0 !important;
    }
    .dashboard-header.clean-header.page-aware-header .header-identity-row {
        display:grid !important;
        grid-template-columns:43px minmax(0,1fr) auto !important;
        width:100% !important;
        min-width:0 !important;
    }
    .dashboard-header.clean-header.page-aware-header .header-main {
        width:100% !important;
        min-width:0 !important;
    }
    .dashboard-header.clean-header.page-aware-header .header-title,
    .dashboard-header.clean-header.page-aware-header .header-subtitle {
        max-width:none !important;
        overflow-wrap:normal !important;
        word-break:normal !important;
    }
    .dashboard-header.clean-header.page-aware-header .header-scope {
        display:flex !important;
        width:100% !important;
        box-sizing:border-box !important;
    }

    @media (max-width: 720px) {
        .dashboard-header.clean-header.page-aware-header .header-identity-row {
            grid-template-columns:38px minmax(0,1fr) !important;
            gap:.68rem !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-page-icon {
            width:38px !important;
            height:38px !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-badge {
            grid-column:1 / -1 !important;
            justify-self:start !important;
            margin-top:.15rem !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-title {
            font-size:clamp(1.42rem,7vw,1.82rem) !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-scope {
            flex-wrap:wrap !important;
            gap:.32rem .55rem !important;
        }
    }
    </style>
    """


# ---------------------------------------------------------------------------
# V20 — Adaptive Responsive UX + hover/readability safety
# ---------------------------------------------------------------------------
def _v20_adaptive_responsive_css() -> str:
    return r"""
    <style>
    /*
       Browser-native resolution engine.
       The browser itself knows the real viewport, so CSS media queries are
       more reliable than syncing width back to Python through a JS component.
       Profiles cover notebook, Full HD, QHD and 4K without fixed card widths.
    */
    :root {
        --v20-content-max: 1560px;
        --v20-inline-pad: clamp(.72rem, 1.35vw, 1.5rem);
        --v20-section-gap: clamp(.72rem, 1vw, 1.05rem);
        --v20-chart-radius: 14px;
        --v20-tooltip-bg: #0D182A;
        --v20-tooltip-border: #33445E;
    }

    /* Never let a Streamlit flex/grid child force the page wider than viewport. */
    .main .block-container,
    .main div[data-testid="stVerticalBlock"],
    .main div[data-testid="stHorizontalBlock"],
    .main div[data-testid="stColumn"] {
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    .main .block-container {
        width: min(calc(100% - (2 * var(--v20-inline-pad))), var(--v20-content-max)) !important;
        max-width: var(--v20-content-max) !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Plotly hover must be allowed to float over the card edge. V19 used
       overflow:hidden, which could clip tooltips, outside labels and legends. */
    div[data-testid="stPlotlyChart"] {
        position: relative !important;
        overflow: visible !important;
        isolation: isolate;
        z-index: 1;
        min-width: 0 !important;
        width: 100% !important;
    }
    div[data-testid="stPlotlyChart"]:hover,
    div[data-testid="stPlotlyChart"]:focus-within { z-index: 20 !important; }
    div[data-testid="stPlotlyChart"] > div,
    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container,
    div[data-testid="stPlotlyChart"] .svg-container,
    div[data-testid="stPlotlyChart"] .main-svg {
        max-width: 100% !important;
        overflow: visible !important;
    }
    .main div[data-testid="stColumn"]:has(div[data-testid="stPlotlyChart"]),
    .main div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) {
        overflow: visible !important;
    }

    /* Hover: compact, readable, high-contrast, and visually lighter than the
       data labels it complements. Unified hover avoids multiple boxes. */
    .js-plotly-plot .hoverlayer { pointer-events: none !important; }
    .js-plotly-plot .hoverlayer .hovertext,
    .js-plotly-plot .hoverlayer .axistext {
        filter: drop-shadow(0 6px 14px rgba(0,0,0,.24)) !important;
    }
    .js-plotly-plot .hoverlayer .hovertext path,
    .js-plotly-plot .hoverlayer .axistext path {
        fill: var(--v20-tooltip-bg) !important;
        stroke: var(--v20-tooltip-border) !important;
        stroke-width: 1px !important;
        opacity: .98 !important;
    }
    .js-plotly-plot .hoverlayer text {
        fill: #F8FAFC !important;
        font-size: 12px !important;
        font-weight: 580 !important;
        font-variant-numeric: tabular-nums;
    }
    .js-plotly-plot .hoverlayer .axistext text { font-weight: 720 !important; }

    /* Plot labels/legends remain legible but never dominate the data. */
    .js-plotly-plot .legendtext { fill: #C5D0DE !important; }
    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text { fill: #94A3B8 !important; }
    .v16-chart-heading {
        min-width: 0 !important;
        max-width: 100% !important;
        padding-right: .15rem !important;
    }
    .v16-chart-title,
    .v16-chart-subtitle {
        overflow-wrap: anywhere;
        text-wrap: pretty;
    }

    /* Long tab sets and tables scroll inside themselves instead of widening the page. */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        flex-wrap: nowrap !important;
        scrollbar-width: none;
        overscroll-behavior-inline: contain;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
    .stTabs [data-baseweb="tab"] { flex: 0 0 auto !important; white-space: nowrap !important; }
    .safe-html-table,
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {
        max-width: 100% !important;
        overflow-x: auto !important;
        overscroll-behavior-inline: contain;
    }

    /* Scope and controls wrap naturally; no ellipsis that hides selected context. */
    .dashboard-header.clean-header.page-aware-header .header-scope {
        flex-wrap: wrap !important;
        row-gap: .35rem !important;
    }
    .dashboard-header.clean-header.page-aware-header .header-scope-item {
        min-width: 0 !important;
        max-width: 100% !important;
    }
    .dashboard-header.clean-header.page-aware-header .header-scope-item strong {
        overflow-wrap: anywhere;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"],
    section[data-testid="stSidebar"] div[data-baseweb="base-input"] { max-width: 100% !important; }

    /* Content-aware fallback for notebooks with the sidebar open. Unlike a
       viewport breakpoint, this reacts to the REAL width left for the chart
       row after the sidebar and surrounding layout have consumed space. */
    @supports (container-type: inline-size) {
        .main div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) {
            container-type: inline-size;
            container-name: dashboard-chart-row;
        }
        @container dashboard-chart-row (max-width: 1200px) {
            div[data-testid="stColumn"] {
                flex: 1 1 100% !important;
                width: 100% !important;
                min-width: 0 !important;
            }
        }
    }

    /* Notebook / compact desktop: chart pairs become fluid and wrap only when
       the available width can no longer support two readable visualizations. */
    @media (max-width: 1240px) {
        :root { --v20-content-max: 1180px; --v20-inline-pad: clamp(.65rem, 1.2vw, 1rem); }
        .main div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) {
            flex-wrap: wrap !important;
            align-items: stretch !important;
            gap: .78rem !important;
        }
        .main div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 0 !important;
        }
        .header-subtitle { max-width: 760px !important; }
    }

    /* Small notebook / tablet landscape: one chart per row, 2-column KPIs. */
    @media (max-width: 980px) {
        :root { --v20-content-max: 100%; --v20-inline-pad: .78rem; }
        .main div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 0 !important;
        }
        .v14-kpi-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            --kpi-cols: 2 !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-scope-update {
            margin-left: 0 !important;
        }
        .v16-chart-title { font-size: 13.5px !important; }
        .v16-chart-subtitle { font-size: 11.5px !important; }
        .js-plotly-plot .legendtext,
        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text { font-size: 11px !important; }
    }

    /* Mobile/small browser window: nothing is truncated; content stacks and
       controls/tabs become touch friendly. */
    @media (max-width: 620px) {
        :root { --v20-inline-pad: .58rem; }
        .main .block-container { width: calc(100% - 1.16rem) !important; }
        .dashboard-header.clean-header.page-aware-header { padding: .82rem !important; }
        .dashboard-header.clean-header.page-aware-header .header-identity-row {
            grid-template-columns: 36px minmax(0,1fr) !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-title {
            font-size: clamp(1.36rem, 7vw, 1.72rem) !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-scope-divider { display: none !important; }
        .dashboard-header.clean-header.page-aware-header .header-scope-item {
            flex: 1 1 100% !important;
            justify-content: space-between !important;
            gap: .75rem !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-scope-item span { display: inline !important; }
        .v14-kpi-grid {
            grid-template-columns: 1fr !important;
            --kpi-cols: 1 !important;
        }
        .stTabs [data-baseweb="tab"] { min-height: 40px !important; padding: .5rem .72rem !important; }
        div[data-testid="stPlotlyChart"] { border-radius: 12px !important; }
        .js-plotly-plot .hoverlayer text { font-size: 11.5px !important; }
        .section-header { gap: .45rem !important; }
    }

    /* Short-height notebooks (e.g. 1366×768 / browser with large OS chrome):
       reclaim vertical space from decoration, never from the data itself. */
    @media (max-height: 820px) and (min-width: 900px) {
        .main .block-container { padding-top: .55rem !important; padding-bottom: 2rem !important; }
        .dashboard-header.clean-header.page-aware-header {
            padding-top: .82rem !important;
            padding-bottom: .72rem !important;
            margin-bottom: .12rem !important;
        }
        .dashboard-header.clean-header.page-aware-header .header-scope {
            margin-top: .42rem !important;
            padding-top: .42rem !important;
        }
        .v14-kpi-grid { margin-top: .22rem !important; margin-bottom: .58rem !important; }
        .v14-kpi-grid .kpi-card { min-height: 118px !important; padding-top: .78rem !important; padding-bottom: .7rem !important; }
        .section-header { margin-top: .58rem !important; margin-bottom: .42rem !important; }
        .v16-chart-heading { margin-top: .08rem !important; margin-bottom: .3rem !important; }
    }

    /* Full HD: preserve the editorial 4-card rhythm and a restrained canvas. */
    @media (min-width: 1440px) and (max-width: 1919px) {
        :root { --v20-content-max: 1560px; --v20-inline-pad: clamp(1rem, 1.4vw, 1.4rem); }
    }

    /* QHD / high-density desktop: use extra resolution for breathing room,
       never by stretching charts across the entire display. */
    @media (min-width: 1920px) and (max-width: 2559px) {
        :root { --v20-content-max: 1760px; --v20-inline-pad: 1.5rem; }
        .main .block-container { padding-top: 1.05rem !important; }
        .dashboard-header.clean-header.page-aware-header { padding: 1.18rem 1.3rem 1.02rem !important; }
        .v14-kpi-grid { gap: .82rem !important; }
        .v14-kpi-grid .kpi-card { min-height: 138px !important; }
        .v16-chart-title { font-size: 14.5px !important; }
    }

    /* 4K: readable centered canvas, slightly larger type, no 3840px-long charts. */
    @media (min-width: 2560px) {
        :root { --v20-content-max: 1920px; --v20-inline-pad: 2rem; }
        .header-title { font-size: 2.18rem !important; }
        .header-subtitle { font-size: 13.5px !important; }
        .v14-kpi-grid .kpi-card { min-height: 144px !important; padding: 1rem 1.08rem !important; }
        .kpi-value { font-size: 2.18rem !important; }
        .section-header h2 { font-size: 1.18rem !important; }
        .v16-chart-title { font-size: 15px !important; }
        .v16-chart-subtitle { font-size: 12.3px !important; }
        .js-plotly-plot .legendtext,
        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text { font-size: 12.5px !important; }
    }

    /* Touch devices do not have hover; remove hover-only chrome and keep taps clean. */
    @media (hover: none) and (pointer: coarse) {
        div[data-testid="stPlotlyChart"] .modebar { display: none !important; }
        div[data-testid="stPlotlyChart"]:hover { z-index: 1 !important; }
        .v14-kpi-grid .kpi-card:hover { transform: none !important; }
    }

    @media (prefers-reduced-motion: reduce) {
        div[data-testid="stPlotlyChart"],
        .stTabs [data-baseweb="tab-list"] { scroll-behavior: auto !important; }
    }
    </style>
    """


# ---------------------------------------------------------------------------
# V24 — JS enforcement for the select/multiselect dropdown palette
#
# Context: V23's CSS layer (below) still lost to BaseWeb in production even
# though it uses !important on every rule. The likely reason: BaseWeb mounts
# the popover's <style> tag dynamically, the first time it opens — which is
# AFTER our static stylesheet has already been parsed at page load. When
# BaseWeb's own dynamically-injected rule for the same element is *also*
# !important (common for its selected/highlighted states), the one inserted
# later in the document wins the tie, and that is now BaseWeb's, not ours.
# No amount of extra CSS selectors fixes an insertion-order tie — the only
# thing that reliably outranks a later !important stylesheet rule is an
# INLINE style, which is always highest priority regardless of order. So
# this layer re-applies the same palette as plain inline styles, redone on
# every DOM mutation, via a tiny script mounted through
# `st.components.v1.html`. It reaches the *parent* document (where the real
# app lives) through `window.parent`, since the component itself only gets
# an isolated iframe. This is intentionally a belt-and-suspenders addition
# on top of V23, not a replacement — keep both.
# ---------------------------------------------------------------------------
def get_dropdown_js_fix() -> str:
    """HTML+JS payload for st.components.v1.html(..., height=0). Repaints the
    select/multiselect popover and kills the stray input caret using inline
    !important styles, which always beat stylesheet rules regardless of
    when BaseWeb inserts its own CSS."""
    return r"""
    <script>
    (function () {
        var PALETTE = {
            menuBg: "#101A2B",
            menuBorder: "#29415F",
            optionBg: "#101A2B",
            optionHoverBg: "#16263D",
            optionSelectedBg: "#1D3150",
            text: "#D7E0EC",
            textStrong: "#F8FAFC",
            accent: "#4C8DFF"
        };

        function setImportant(el, props) {
            for (var k in props) {
                if (Object.prototype.hasOwnProperty.call(props, k)) {
                    try { el.style.setProperty(k, props[k], "important"); } catch (e) {}
                }
            }
        }

        function paint(doc) {
            if (!doc) return;

            var menus = doc.querySelectorAll(
                '[data-baseweb="menu"], [role="listbox"], [data-baseweb="popover"] ul'
            );
            for (var i = 0; i < menus.length; i++) {
                setImportant(menus[i], {
                    "background-color": PALETTE.menuBg,
                    "background": PALETTE.menuBg,
                    "border": "1px solid " + PALETTE.menuBorder,
                    "border-radius": "12px",
                    "box-shadow": "0 16px 40px rgba(2,6,23,.45)"
                });
            }

            var options = doc.querySelectorAll(
                '[role="option"], li[role="option"], div[role="option"]'
            );
            for (var j = 0; j < options.length; j++) {
                var opt = options[j];
                var selected = opt.getAttribute("aria-selected") === "true";
                setImportant(opt, {
                    "background-color": selected ? PALETTE.optionSelectedBg : PALETTE.optionBg,
                    "background": selected ? PALETTE.optionSelectedBg : PALETTE.optionBg,
                    "color": selected ? PALETTE.textStrong : PALETTE.text
                });
                if (!opt.dataset.dashHoverBound) {
                    opt.dataset.dashHoverBound = "1";
                    opt.addEventListener("mouseenter", function () {
                        setImportant(this, { "background-color": PALETTE.optionHoverBg, "background": PALETTE.optionHoverBg, "color": PALETTE.textStrong });
                    });
                    opt.addEventListener("mouseleave", function () {
                        var stillSelected = this.getAttribute("aria-selected") === "true";
                        setImportant(this, {
                            "background-color": stillSelected ? PALETTE.optionSelectedBg : PALETTE.optionBg,
                            "background": stillSelected ? PALETTE.optionSelectedBg : PALETTE.optionBg,
                            "color": stillSelected ? PALETTE.textStrong : PALETTE.text
                        });
                    });
                }
            }

            var carets = doc.querySelectorAll(
                '[data-testid="stSelectbox"] input, [data-testid="stMultiSelect"] input'
            );
            for (var k = 0; k < carets.length; k++) {
                setImportant(carets[k], {
                    "caret-color": "transparent",
                    "color": "transparent",
                    "background": "transparent",
                    "border": "0",
                    "box-shadow": "none",
                    "outline": "none",
                    "text-shadow": "none"
                });
            }
        }

        function start(doc) {
            paint(doc);
            try {
                var observer = new MutationObserver(function () { paint(doc); });
                observer.observe(doc.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["aria-selected", "class", "style"] });
            } catch (e) {}
            // Defensive fallback in case a mutation is missed (e.g. React
            // batching); cheap no-op when nothing changed.
            setInterval(function () { paint(doc); }, 500);
        }

        try {
            start(window.parent.document);
        } catch (e) {
            start(document);
        }
    })();
    </script>
    """


# ---------------------------------------------------------------------------
# V23 — Dropdown definitive fix (stray caret box + off-palette popover color)
#
# Context: two earlier layers (_get_css_base's "Dark interactive controls"
# block and _v22_controls_polish_css) already targeted this same select /
# multiselect dropdown, but both key on `role="option"` / `role="listbox"`
# and a fixed nesting depth for the hidden BaseWeb <input>. If the installed
# Streamlit/BaseWeb version renders the popover through a virtualized list
# (rows as plain <div>s instead of role="option" <li>s) or nests the caret
# input one level deeper, those selectors silently stop matching and the
# control falls back to BaseWeb's own default accent — which is a violet,
# not this dashboard's blue. This layer is intentionally broader (menu/list
# children by position, not just by role) and is appended last so it always
# wins the cascade tie-break, regardless of which structure is present.
# ---------------------------------------------------------------------------
def _v23_dropdown_definitive_fix_css() -> str:
    return r"""
    <style>
    /* 1) Kill the stray caret/focus rectangle on the CLOSED control.
          Broadened beyond input:focus — some BaseWeb builds keep the caret
          visible via an inline style on the input itself, which only an
          unconditional !important rule (not just a :focus one) can beat. */
    div[data-testid="stSelectbox"] [data-baseweb="select"] input,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] input,
    div[data-testid="stSelectbox"] [data-baseweb="base-input"] input,
    div[data-testid="stMultiSelect"] [data-baseweb="base-input"] input {
        caret-color: transparent !important;
        color: transparent !important;
        background: transparent !important;
        border: 0 !important;
        outline: none !important;
        box-shadow: none !important;
        text-shadow: none !important;
    }

    /* 2) Force the popover shell to the dashboard's blue-navy palette no
          matter how BaseWeb structures it — by role, by data-baseweb, and
          by plain position (first-level children of the menu/listbox) so a
          virtualized row markup is covered even without role="option". */
    body [data-baseweb="popover"] [data-baseweb="menu"],
    body [data-baseweb="popover"] [role="listbox"],
    body [data-baseweb="menu"],
    body [role="listbox"],
    body ul[data-baseweb="menu"] {
        background-color: #101A2B !important;
        background: #101A2B !important;
        border: 1px solid #29415F !important;
        border-radius: 12px !important;
        box-shadow: 0 16px 40px rgba(2, 6, 23, .45) !important;
    }

    body [data-baseweb="menu"] li,
    body [data-baseweb="menu"] > div > div,
    body [role="listbox"] li,
    body [role="listbox"] > div,
    body [role="option"],
    body li[role="option"],
    body div[role="option"] {
        background-color: #101A2B !important;
        background: #101A2B !important;
        color: #D7E0EC !important;
    }

    body [data-baseweb="menu"] li:hover,
    body [data-baseweb="menu"] > div > div:hover,
    body [role="listbox"] li:hover,
    body [role="listbox"] > div:hover,
    body [role="option"]:hover,
    body [role="option"][data-highlighted="true"],
    body li[role="option"]:hover,
    body div[role="option"]:hover {
        background-color: #16263D !important;
        background: #16263D !important;
        color: #F8FAFC !important;
    }

    body [role="option"][aria-selected="true"],
    body li[role="option"][aria-selected="true"],
    body div[role="option"][aria-selected="true"] {
        background-color: #1D3150 !important;
        background: #1D3150 !important;
        color: #F8FAFC !important;
        box-shadow: inset 3px 0 0 #4C8DFF !important;
    }

    /* Anything BaseWeb renders inside a listed option (icons, check marks,
       secondary text) must inherit the same palette instead of a default
       accent color. */
    body [role="option"] *,
    body [data-baseweb="menu"] li * {
        color: inherit !important;
        fill: currentColor !important;
    }
    </style>
    """


# ---------------------------------------------------------------------------
# V26 — Micro-interactions, accessible focus and small delighters
#
# Everything here is additive and scoped to classes/attributes that already
# exist (`.kpi-help`, `.kpi-value`, `.kpi-card.delay-N`) or a new opt-in
# element the JS helper creates itself (`.v26-back-to-top`). Nothing here
# redefines a selector V22/V23/V24 already own, so the dropdown fix from
# earlier stays exactly as-is.
# ---------------------------------------------------------------------------
def _v26_micro_interactions_css() -> str:
    return r"""
    <style>
    /* ----- Custom tooltip on the KPI info icon (was a native title=) ----- */
    .kpi-help {
        position: relative;
        display: inline-flex;
        cursor: help;
        outline: none;
        border-radius: 4px;
    }
    .kpi-help::after {
        content: attr(data-tooltip);
        position: absolute;
        left: 50%;
        bottom: calc(100% + 9px);
        transform: translateX(-50%) translateY(4px);
        background: #101A2B;
        color: #F8FAFC;
        border: 1px solid var(--v19-hairline-strong, rgba(169,184,204,.32));
        border-radius: 8px;
        padding: .5rem .65rem;
        font-size: 11px;
        font-weight: 500;
        line-height: 1.4;
        white-space: normal;
        width: max-content;
        max-width: 220px;
        box-shadow: 0 14px 30px rgba(1,6,15,.5);
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity .15s ease, transform .15s ease;
        z-index: 60;
    }
    .kpi-help::before {
        content: "";
        position: absolute;
        left: 50%;
        bottom: 100%;
        transform: translateX(-50%) translateY(4px);
        border: 5px solid transparent;
        border-top-color: #101A2B;
        opacity: 0;
        visibility: hidden;
        transition: opacity .15s ease, transform .15s ease;
        z-index: 60;
    }
    .kpi-help:hover::after, .kpi-help:focus-visible::after,
    .kpi-help:hover::before, .kpi-help:focus-visible::before {
        opacity: 1;
        visibility: visible;
        transform: translateX(-50%) translateY(0);
    }
    .kpi-help:focus-visible {
        box-shadow: 0 0 0 2px color-mix(in srgb, var(--page-accent, #4C8DFF) 55%, transparent);
    }

    /* ----- KPI value: a quiet "materialize" reveal instead of a static
       number appearing mid-layout-shift. No digits are parsed or re-
       formatted, so the already-correct pt-BR formatted string is never at
       risk of showing wrong mid-animation. ----- */
    @keyframes kpiValueReveal {
        0%   { opacity: 0; filter: blur(5px); transform: translateY(5px) scale(.95); }
        65%  { opacity: 1; filter: blur(0); transform: translateY(0) scale(1.015); }
        100% { opacity: 1; filter: blur(0); transform: translateY(0) scale(1); }
    }
    .kpi-value {
        animation: kpiValueReveal .6s cubic-bezier(.22,1,.36,1) both;
    }
    .kpi-card.delay-1 .kpi-value { animation-delay: .16s; }
    .kpi-card.delay-2 .kpi-value { animation-delay: .21s; }
    .kpi-card.delay-3 .kpi-value { animation-delay: .26s; }
    .kpi-card.delay-4 .kpi-value { animation-delay: .31s; }
    .kpi-card.delay-5 .kpi-value { animation-delay: .36s; }
    .kpi-card.delay-6 .kpi-value { animation-delay: .41s; }

    /* ----- Keyboard accessibility: a visible, on-brand focus ring
       everywhere a sighted mouse user gets a hover cue, so keyboard/screen-
       reader users get equivalent feedback. Only fires for real keyboard
       focus (:focus-visible), never on a mouse click. ----- */
    .kpi-card:focus-visible,
    .v14-kpi-grid .kpi-card:focus-visible,
    button:focus-visible,
    a:focus-visible,
    [role="button"]:focus-visible,
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:focus-visible) {
        outline: none !important;
        box-shadow: 0 0 0 2px #0B1020, 0 0 0 4px color-mix(in srgb, var(--page-accent, #4C8DFF) 70%, transparent) !important;
    }

    /* ----- Buttons: tactile press feedback ----- */
    .stButton > button, button[kind] {
        transition: transform .12s ease, box-shadow .15s ease, background .15s ease !important;
    }
    .stButton > button:active, button[kind]:active {
        transform: scale(.97) !important;
    }

    /* ----- Floating "back to top" button, created and toggled by the JS
       helper (get_ux_effects_js). Pure CSS here so the script only ever
       has to add/remove one class. ----- */
    .v26-back-to-top {
        position: fixed;
        right: 22px;
        bottom: 22px;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        background: linear-gradient(150deg, #5B9BFF, #2F6FE4);
        color: #F8FAFC;
        border: 1px solid rgba(255,255,255,.18);
        box-shadow: 0 12px 26px -8px rgba(47,111,228,.55);
        cursor: pointer;
        font-size: 18px;
        line-height: 1;
        opacity: 0;
        visibility: hidden;
        transform: translateY(10px);
        transition: opacity .2s ease, transform .2s ease, visibility .2s;
        z-index: 999999;
    }
    .v26-back-to-top.is-visible {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }
    .v26-back-to-top:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 32px -8px rgba(47,111,228,.68);
    }
    .v26-back-to-top:active { transform: scale(.94); }

    @media (prefers-reduced-motion: reduce) {
        .kpi-value { animation: none !important; }
        .v26-back-to-top { transition: opacity .01s linear !important; }
    }
    @media print {
        .v26-back-to-top { display: none !important; }
    }
    </style>
    """


# ---------------------------------------------------------------------------
# V27 — Fluid zoom responsiveness, spacing rhythm & elegance polish
#
# Everything below is additive and appended last in get_css(), so it wins
# the cascade tie-break over every earlier layer without deleting or
# rewriting them. Three concerns, kept in one layer because they reinforce
# each other:
#
#   1) Zoom/viewport fluidity — V20's breakpoints are correct but they are
#      *stepped*: a value holds flat then jumps at the next media query.
#      Browser zoom (100%→125%→150%…) and unusual notebook widths land
#      between those steps constantly, so this layer switches the highest-
#      traffic spacing/sizing values (page padding, KPI grid gap, card
#      padding, section rhythm) to clamp()-based fluid scaling instead.
#      The result: it doesn't jump, it eases. The old fixed values still
#      apply as a floor/ceiling via the clamp() bounds, so nothing regresses
#      on the extreme ends.
#   2) Overflow safety at extreme zoom — grid/flex children without
#      min-width:0 can force a horizontal scrollbar once zoom pushes their
#      intrinsic content width past the shrunken viewport. This is the
#      single most common "broken at 150% zoom" bug class in Streamlit
#      dashboards, so it is patched broadly here.
#   3) Elegance/effects polish — consistent hover elevation, a slim gradient
#      accent, calmer easing curves, refined focus-visible rings and a
#      themed scrollbar. Same visual language as V16/V25/V26, just filling
#      in the remaining surfaces (insight cards, shad-cards, tabs).
# ---------------------------------------------------------------------------
def _v27_fluid_zoom_polish_css() -> str:
    return r"""
    <style>
    /* ---- 1. Fluid design tokens (namespaced to avoid clobbering V20's) --- */
    :root {
        --v27-space-2xs: clamp(.35rem, .3rem + .25vw, .5rem);
        --v27-space-xs:  clamp(.55rem, .48rem + .35vw, .75rem);
        --v27-space-sm:  clamp(.85rem, .72rem + .5vw, 1.1rem);
        --v27-space-md:  clamp(1.1rem, .92rem + .7vw, 1.5rem);
        --v27-space-lg:  clamp(1.5rem, 1.2rem + 1vw, 2.1rem);
        --v27-ease: cubic-bezier(.22, 1, .36, 1);
    }

    /* ---- 2. Zoom/overflow safety net ------------------------------------ */
    html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
    *, *::before, *::after { box-sizing: border-box; }

    .main .block-container,
    div[data-testid="stHorizontalBlock"],
    div[data-testid="column"],
    .v14-kpi-grid,
    .header-identity-row,
    .header-scope {
        min-width: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        row-gap: var(--v27-space-sm) !important;
    }
    .main .block-container {
        overflow-x: clip;
    }

    /* ---- 3. Fluid spacing rhythm (smooths V20's stepped breakpoints) ---- */
    .main .block-container {
        padding-left: var(--v27-space-md) !important;
        padding-right: var(--v27-space-md) !important;
        row-gap: var(--v27-space-md) !important;
    }
    .v14-kpi-grid {
        gap: var(--v27-space-sm) !important;
        margin-bottom: var(--v27-space-md) !important;
    }
    .kpi-card, .insight-card, .shad-card {
        padding: var(--v27-space-sm) var(--v27-space-md) !important;
    }
    .section-header {
        margin-top: var(--v27-space-lg) !important;
        margin-bottom: var(--v27-space-sm) !important;
        gap: var(--v27-space-xs) !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: var(--v27-space-sm) !important;
    }

    /* Progressive enhancement: once a browser supports container queries,
       let KPI cards react to the column's real width rather than only the
       viewport — this keeps the grid aligned even when the sidebar is
       toggled or a zoom level shrinks one column but not the viewport. */
    @supports (container-type: inline-size) {
        .v14-kpi-grid { container-type: inline-size; }
        @container (max-width: 220px) {
            .kpi-value { font-size: 1.5rem !important; }
        }
    }

    /* ---- 4. Elegance & effects polish ------------------------------------ */
    .kpi-card, .insight-card, .shad-card,
    .stCard, div[data-testid="stExpander"] {
        transition: transform .32s var(--v27-ease),
                    box-shadow .32s var(--v27-ease),
                    border-color .32s var(--v27-ease) !important;
        position: relative;
        isolation: isolate;
    }
    .kpi-card::before, .insight-card::before, .shad-card::before {
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 2px;
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        background: linear-gradient(90deg, var(--purple), var(--cyan));
        opacity: 0;
        transform: scaleX(.6);
        transform-origin: left;
        transition: opacity .32s var(--v27-ease), transform .32s var(--v27-ease);
        pointer-events: none;
    }
    .kpi-card:hover::before, .insight-card:hover::before, .shad-card:hover::before {
        opacity: .85;
        transform: scaleX(1);
    }
    .kpi-card:hover, .insight-card:hover, .shad-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-glow) !important;
        box-shadow: 0 18px 40px -14px rgba(124, 58, 237, .35),
                    0 2px 10px rgba(0, 0, 0, .3) !important;
    }

    /* Calmer, consistent tab underline motion */
    .stTabs [data-baseweb="tab-highlight"] {
        transition: left .28s var(--v27-ease), width .28s var(--v27-ease) !important;
    }

    /* Accessible + elegant focus rings, unified across controls */
    a:focus-visible, button:focus-visible,
    .stButton button:focus-visible,
    div[data-baseweb="select"] > div:focus-within,
    input:focus-visible, textarea:focus-visible {
        outline: 2px solid var(--purple-light) !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 0 4px rgba(167, 139, 250, .22) !important;
    }

    /* Themed scrollbar (webkit) for the main scroll surface */
    section.main::-webkit-scrollbar, .main::-webkit-scrollbar { width: 10px; height: 10px; }
    section.main::-webkit-scrollbar-track, .main::-webkit-scrollbar-track { background: transparent; }
    section.main::-webkit-scrollbar-thumb, .main::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--purple-dark), var(--purple));
        border-radius: 8px;
        border: 2px solid var(--bg-primary);
    }
    section.main::-webkit-scrollbar-thumb:hover, .main::-webkit-scrollbar-thumb:hover {
        background: var(--purple-light);
    }
    * { scrollbar-width: thin; scrollbar-color: var(--purple) transparent; }

    /* Buttons: slightly springier, elegant press feedback */
    .stButton button, .stDownloadButton button {
        transition: transform .18s var(--v27-ease), box-shadow .18s var(--v27-ease),
                    filter .18s var(--v27-ease) !important;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        transform: translateY(-1px);
        filter: brightness(1.06);
    }
    .stButton button:active, .stDownloadButton button:active {
        transform: translateY(0) scale(.98);
    }

    @media (max-width: 480px) {
        .kpi-card::before, .insight-card::before, .shad-card::before { display: none; }
    }
    @media (prefers-reduced-motion: reduce) {
        .kpi-card, .insight-card, .shad-card,
        .stCard, div[data-testid="stExpander"],
        .stButton button, .stDownloadButton button,
        .stTabs [data-baseweb="tab-highlight"] {
            transition: none !important;
        }
    }

    /* ---- 5. Branded initial-load screen ---------------------------------- */
    .v27-load-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: .4rem;
        min-height: 62vh;
        padding: var(--v27-space-lg);
        text-align: center;
        animation: v27FadeIn .4s var(--v27-ease);
    }
    .v27-load-mark {
        font-size: 2.4rem;
        line-height: 1;
        margin-bottom: .3rem;
        filter: drop-shadow(0 0 18px rgba(124, 58, 237, .45));
        animation: v27Pulse 1.8s ease-in-out infinite;
    }
    .v27-load-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -.01em;
    }
    .v27-load-sub {
        font-size: .88rem;
        color: var(--text-muted);
        margin-bottom: var(--v27-space-md);
    }
    .v27-load-bars {
        width: min(320px, 80vw);
    }
    .v27-load-bars .shad-skeleton {
        height: 10px;
        margin-bottom: .55rem;
    }
    @keyframes v27FadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes v27Pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.08); opacity: .82; }
    }
    @media (prefers-reduced-motion: reduce) {
        .v27-load-screen { animation: none !important; }
        .v27-load-mark { animation: none !important; }
    }

    /* ---- 6. Native alert boxes (st.error/warning/info/success) ---------- */
    /* Kept selector-agnostic about severity (Streamlit's internal class
       names for each kind are not a stable public contract), but every
       alert gets the same glass-card treatment as the rest of the
       dashboard: soft entrance, a gradient accent edge and breathing
       room, instead of the flat default block. */
    [data-testid="stAlert"] {
        border-radius: var(--radius-md) !important;
        padding: .95rem 1.1rem !important;
        border-left: 3px solid var(--purple-light) !important;
        animation: v27FadeIn .32s var(--v27-ease);
    }
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0 !important;
    }
    @media (prefers-reduced-motion: reduce) {
        [data-testid="stAlert"] { animation: none !important; }
    }

    /* ---- 7. Removable per-filter chips (sidebar) ------------------------- */
    /* st.container(key="v27_filter_chip_row") renders a real wrapping div
       with class "st-key-v27_filter_chip_row" (Streamlit >=1.36) — unlike
       st.markdown, which never actually nests the elements that follow it,
       this lets the selector below reliably reach only these buttons. */
    .st-key-v27_filter_chip_row div[data-testid="stHorizontalBlock"] {
        gap: .35rem !important;
    }
    .st-key-v27_filter_chip_row .stButton button {
        font-size: .72rem !important;
        padding: .2rem .55rem !important;
        min-height: unset !important;
        height: auto !important;
        border-radius: 999px !important;
        background: rgba(124, 58, 237, .12) !important;
        border: 1px solid rgba(167, 139, 250, .3) !important;
        color: var(--text-primary) !important;
        white-space: nowrap;
    }
    .st-key-v27_filter_chip_row .stButton button:hover {
        background: rgba(124, 58, 237, .22) !important;
        border-color: var(--purple-light) !important;
        transform: none;
    }

    /* ---- 8. Expanded content must inherit the dark surface -------------- */
    /* div[data-testid="stExpander"] only paints the OUTER shell. Streamlit
       renders the expanded body in its own nested wrapper (stExpanderDetails
       in current versions, falling back to stVerticalBlock either way) that
       ships with Streamlit's own default background — opaque and light —
       completely unrelated to this dashboard's dark theme. Since every
       label/value inside is styled for a dark surface (light text colors),
       that leftover light background was rendering text-on-near-white,
       unreadable the moment an expander was opened. Neutralizing every
       structural wrapper's background (not its content — tables, chips and
       buttons keep their own explicit colors, which take precedence as
       more specific selectors) lets the dark shell show through everywhere
       inside, on any Streamlit version's internal naming. */
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"],
    div[data-testid="stExpander"] div[data-testid="stVerticalBlock"],
    div[data-testid="stExpander"] div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stExpander"] div[data-testid="stElementContainer"] {
        background-color: transparent !important;
    }
    </style>
    """


# ---------------------------------------------------------------------------
# V26 — UX effects JS: floating "back to top" button
#
# Same mechanism as get_dropdown_js_fix(): mounted via st.components.v1.html,
# reaches the real app through window.parent since the component itself only
# gets an isolated iframe. Creates one small button once, then just toggles
# visibility on scroll and smooth-scrolls to top on click — no MutationObserver
# needed here since the button itself is static, not repainting other people's
# elements.
# ---------------------------------------------------------------------------
def get_ux_effects_js() -> str:
    """HTML+JS payload for st.components.v1.html(..., height=0). Adds a
    floating back-to-top button to the main app once scroll passes a small
    threshold. Idempotent — safe to mount on every rerun."""
    return r"""
    <script>
    (function () {
        function setup(doc, win) {
            if (!doc || !win) return;
            var main = doc.querySelector('section.main') || doc.querySelector('[data-testid="stAppViewContainer"]') || doc.body;

            var btn = doc.querySelector('.v26-back-to-top');
            if (!btn) {
                btn = doc.createElement('button');
                btn.className = 'v26-back-to-top';
                btn.type = 'button';
                btn.setAttribute('aria-label', 'Voltar ao topo');
                btn.innerText = '↑';
                btn.addEventListener('click', function () {
                    (main.scrollTo ? main : win).scrollTo({ top: 0, behavior: 'smooth' });
                    doc.body.scrollIntoView && doc.body.scrollIntoView({ behavior: 'smooth' });
                });
                doc.body.appendChild(btn);
            }

            function onScroll() {
                var y = (main.scrollTop || win.pageYOffset || doc.documentElement.scrollTop || 0);
                if (y > 480) {
                    btn.classList.add('is-visible');
                } else {
                    btn.classList.remove('is-visible');
                }
            }

            main.addEventListener('scroll', onScroll, { passive: true });
            win.addEventListener('scroll', onScroll, { passive: true });
            onScroll();
        }

        try {
            setup(window.parent.document, window.parent);
        } catch (e) {
            setup(document, window);
        }
    })();
    </script>
    """
