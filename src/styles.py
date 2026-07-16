"""
Styles Module — Dashboard SM CGR 2026
=======================================
Complete CSS for the executive dark-mode dashboard.
Includes glassmorphism, animations, responsive breakpoints,
and WCAG AA-compliant contrast ratios.
"""

from __future__ import annotations


def get_css() -> str:
    """Return the complete custom CSS for the dashboard."""
    return """
    <style>
    /* ================================================================
       GOOGLE FONTS — Inter
       ================================================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

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
        --text-muted: #64748B;

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

    .health-score-gauge {
        width: 100%;
        max-width: 100%;
        min-height: 230px;
        max-height: 270px;
        overflow: hidden;
        box-sizing: border-box;
        border-radius: var(--radius-md);
    }

    .health-score-gauge + div[data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
        max-height: 270px !important;
        min-height: 230px !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
        padding: 0.8rem !important;
        margin-bottom: 1rem !important;
    }

    .health-score-gauge + div[data-testid="stPlotlyChart"] > div {
        overflow: hidden !important;
        box-sizing: border-box !important;
    }

    .health-score-gauge + div[data-testid="stPlotlyChart"] svg {
        width: 100% !important;
        max-width: 100% !important;
        height: 100% !important;
        max-height: 100% !important;
        overflow: hidden !important;
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
    .st-key-health_score_section {
        position: relative;
        isolation: isolate;
        margin: 1.15rem 0 1.45rem;
        padding: clamp(1rem, 1.5vw, 1.5rem);
        border: 1px solid rgba(59, 130, 246, 0.18);
        border-radius: 22px;
        background:
            radial-gradient(circle at 12% 12%, rgba(37, 99, 235, 0.10), transparent 31%),
            radial-gradient(circle at 86% 88%, rgba(16, 185, 129, 0.065), transparent 28%),
            linear-gradient(145deg, rgba(15, 23, 42, 0.97), rgba(8, 13, 23, 0.985));
        box-shadow:
            0 18px 50px rgba(0, 0, 0, 0.24),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);
        overflow: hidden;
    }

    .st-key-health_score_section::before {
        content: "";
        position: absolute;
        inset: 0 auto auto 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(
            90deg,
            rgba(37, 99, 235, 0),
            rgba(96, 165, 250, 0.85),
            rgba(16, 185, 129, 0.7),
            rgba(37, 99, 235, 0)
        );
        z-index: -1;
    }

    .st-key-health_score_section .section-header {
        margin: 0 0 0.2rem 0;
        padding-bottom: 0.7rem;
        border-bottom-color: rgba(96, 165, 250, 0.14);
    }

    .st-key-health_score_section .section-header h2 {
        font-size: clamp(1rem, 1.25vw, 1.25rem);
        letter-spacing: -0.015em;
    }

    .health-section-subtitle {
        margin: 0 0 1rem 0;
        color: #94A3B8;
        font-size: clamp(0.72rem, 0.85vw, 0.84rem);
        line-height: 1.55;
    }

    .st-key-health_score_section div[data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
        gap: clamp(1rem, 1.8vw, 1.8rem) !important;
    }

    .st-key-health_score_section div[data-testid="column"] {
        min-width: 0 !important;
    }

    .st-key-health_score_chart,
    .st-key-health_score_breakdown {
        height: 100%;
        min-width: 0;
    }

    .st-key-health_score_chart {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }

    .st-key-health_score_chart div[data-testid="stPlotlyChart"] {
        min-height: 320px !important;
        height: 320px !important;
        margin: 0 !important;
        padding: 0.35rem !important;
        border: 1px solid rgba(96, 165, 250, 0.17) !important;
        border-radius: 18px !important;
        background:
            radial-gradient(circle at 50% 45%, rgba(37, 99, 235, 0.10), transparent 46%),
            linear-gradient(160deg, rgba(17, 24, 39, 0.92), rgba(9, 14, 24, 0.96)) !important;
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.025),
            0 12px 30px rgba(0, 0, 0, 0.20) !important;
        overflow: hidden !important;
    }

    .st-key-health_score_chart div[data-testid="stPlotlyChart"]:hover {
        transform: none !important;
        border-color: rgba(96, 165, 250, 0.30) !important;
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.03),
            0 16px 36px rgba(0, 0, 0, 0.24) !important;
    }

    .st-key-health_score_chart div[data-testid="stPlotlyChart"] > div,
    .st-key-health_score_chart .js-plotly-plot,
    .st-key-health_score_chart .plot-container,
    .st-key-health_score_chart .svg-container {
        height: 100% !important;
        min-height: 0 !important;
        width: 100% !important;
        min-width: 0 !important;
    }

    .health-score-summary {
        --summary-accent: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.16);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        background: rgba(15, 23, 42, 0.76);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
    }

    .health-score-summary.danger { --summary-accent: #F87171; }
    .health-score-summary.warning { --summary-accent: #FB923C; }
    .health-score-summary.info { --summary-accent: #60A5FA; }
    .health-score-summary.success { --summary-accent: #34D399; }

    .health-summary-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
    }

    .health-summary-label {
        display: block;
        color: #64748B;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .health-summary-status {
        display: block;
        margin-top: 0.16rem;
        color: var(--summary-accent);
        font-size: 0.94rem;
    }

    .health-summary-score {
        color: #F8FAFC;
        font-size: 1.15rem;
        font-weight: 850;
        font-variant-numeric: tabular-nums;
    }

    .health-summary-progress {
        height: 6px;
        margin: 0.75rem 0;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(51, 65, 85, 0.72);
    }

    .health-summary-progress span {
        display: block;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, var(--summary-accent), #22D3EE);
        box-shadow: 0 0 16px color-mix(in srgb, var(--summary-accent) 40%, transparent);
    }

    .health-summary-metrics {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.55rem;
    }

    .health-summary-metrics > div {
        min-width: 0;
        padding: 0.48rem 0.55rem;
        border-radius: 10px;
        background: rgba(2, 6, 23, 0.34);
        border: 1px solid rgba(148, 163, 184, 0.08);
    }

    .health-summary-metrics span,
    .health-summary-metrics strong {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .health-summary-metrics span {
        color: #64748B;
        font-size: 0.58rem;
        text-transform: uppercase;
        letter-spacing: 0.055em;
    }

    .health-summary-metrics strong {
        margin-top: 0.18rem;
        color: #CBD5E1;
        font-size: 0.76rem;
        font-variant-numeric: tabular-nums;
    }

    .health-breakdown-intro {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.8rem;
    }

    .health-breakdown-eyebrow {
        display: block;
        color: #60A5FA;
        font-size: 0.58rem;
        font-weight: 850;
        letter-spacing: 0.095em;
    }

    .health-breakdown-intro h3 {
        margin: 0.18rem 0 0 0;
        color: #F8FAFC;
        font-size: clamp(0.95rem, 1.1vw, 1.12rem);
        letter-spacing: -0.015em;
    }

    .health-breakdown-intro p {
        max-width: 310px;
        margin: 0;
        color: #64748B;
        font-size: 0.68rem;
        line-height: 1.45;
        text-align: right;
    }

    .health-breakdown-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: clamp(0.7rem, 1vw, 0.9rem);
    }

    .health-breakdown-card {
        --component-accent: #60A5FA;
        min-width: 0;
        padding: 0.9rem;
        border: 1px solid rgba(96, 165, 250, 0.13);
        border-radius: 15px;
        background:
            linear-gradient(145deg, rgba(17, 24, 39, 0.90), rgba(10, 15, 25, 0.95));
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.02),
            0 8px 22px rgba(0, 0, 0, 0.16);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .health-breakdown-card:hover {
        transform: translateY(-2px);
        border-color: color-mix(in srgb, var(--component-accent) 38%, transparent);
    }

    .health-breakdown-card.success { --component-accent: #34D399; }
    .health-breakdown-card.warning { --component-accent: #FB923C; }
    .health-breakdown-card.danger { --component-accent: #F87171; }

    .health-breakdown-head {
        display: grid;
        grid-template-columns: auto minmax(0, 1fr) auto;
        align-items: start;
        gap: 0.65rem;
    }

    .health-breakdown-icon {
        display: grid;
        place-items: center;
        width: 2rem;
        height: 2rem;
        border-radius: 10px;
        background: color-mix(in srgb, var(--component-accent) 12%, transparent);
        border: 1px solid color-mix(in srgb, var(--component-accent) 22%, transparent);
        font-size: 0.92rem;
    }

    .health-breakdown-heading {
        min-width: 0;
    }

    .health-breakdown-heading strong,
    .health-breakdown-heading span {
        display: block;
    }

    .health-breakdown-heading strong {
        color: #E2E8F0;
        font-size: 0.78rem;
        line-height: 1.3;
    }

    .health-breakdown-heading span {
        margin-top: 0.18rem;
        color: #64748B;
        font-size: 0.6rem;
    }

    .health-breakdown-badge {
        align-self: start;
        padding: 0.22rem 0.42rem;
        border-radius: 999px;
        background: color-mix(in srgb, var(--component-accent) 12%, transparent);
        border: 1px solid color-mix(in srgb, var(--component-accent) 24%, transparent);
        color: var(--component-accent);
        font-size: 0.54rem;
        font-weight: 800;
        text-transform: uppercase;
        white-space: nowrap;
    }

    .health-breakdown-values {
        display: flex;
        align-items: end;
        justify-content: space-between;
        gap: 0.8rem;
        margin: 0.85rem 0 0.5rem;
    }

    .health-breakdown-values strong {
        color: #F8FAFC;
        font-size: clamp(1.18rem, 1.55vw, 1.5rem);
        font-variant-numeric: tabular-nums;
        letter-spacing: -0.025em;
    }

    .health-breakdown-values span {
        color: #94A3B8;
        font-size: 0.64rem;
        white-space: nowrap;
    }

    .health-breakdown-progress {
        height: 6px;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(51, 65, 85, 0.70);
    }

    .health-breakdown-progress span {
        display: block;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, var(--component-accent), #38BDF8);
        box-shadow: 0 0 14px color-mix(in srgb, var(--component-accent) 36%, transparent);
    }

    .health-breakdown-gap {
        margin-top: 0.5rem;
        color: #64748B;
        font-size: 0.6rem;
        line-height: 1.35;
    }

    .st-key-health_score_breakdown div[data-testid="stCaptionContainer"] {
        margin-top: 0.7rem;
        color: #64748B !important;
        font-size: 0.62rem !important;
    }

    @media (max-width: 1180px) {
        .st-key-health_score_section div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }

        .st-key-health_score_section div[data-testid="column"] {
            flex: 1 1 100% !important;
            width: 100% !important;
        }

        .st-key-health_score_chart {
            max-width: 720px;
            margin: 0 auto;
        }
    }

    @media (max-width: 760px) {
        .main .block-container {
            width: calc(100% - 0.8rem) !important;
            padding-left: 0.4rem !important;
            padding-right: 0.4rem !important;
        }

        .st-key-health_score_section {
            margin-top: 0.8rem;
            padding: 0.8rem;
            border-radius: 16px;
        }

        .st-key-health_score_chart div[data-testid="stPlotlyChart"] {
            min-height: 285px !important;
            height: 285px !important;
        }

        .health-breakdown-grid {
            grid-template-columns: 1fr;
        }

        .health-breakdown-intro {
            align-items: flex-start;
            flex-direction: column;
            gap: 0.35rem;
        }

        .health-breakdown-intro p {
            max-width: none;
            text-align: left;
        }
    }

    @media (max-width: 430px) {
        .st-key-health_score_section {
            padding: 0.65rem;
        }

        .st-key-health_score_chart div[data-testid="stPlotlyChart"] {
            min-height: 255px !important;
            height: 255px !important;
        }

        .health-score-summary {
            padding: 0.75rem;
        }

        .health-summary-metrics {
            gap: 0.35rem;
        }

        .health-summary-metrics > div {
            padding: 0.42rem 0.4rem;
        }

        .health-summary-metrics span {
            font-size: 0.52rem;
        }

        .health-summary-metrics strong {
            font-size: 0.68rem;
        }

        .health-breakdown-card {
            padding: 0.75rem;
        }

        .health-breakdown-head {
            grid-template-columns: auto minmax(0, 1fr);
        }

        .health-breakdown-badge {
            grid-column: 2;
            justify-self: start;
        }
    }

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


# V10.5.4 — Global chart title safety and clean occupational health index
_v1054_previous_get_css = get_css

def _v1054_chart_title_health_css() -> str:
    return r"""
    <style>
    /* Plotly title safety: the SVG owns the dimensions; outer cards must not crop it. */
    .main div[data-testid="stPlotlyChart"],
    .main div[data-testid="stPlotlyChart"] > div,
    .main div[data-testid="stPlotlyChart"] .js-plotly-plot,
    .main div[data-testid="stPlotlyChart"] .plot-container,
    .main div[data-testid="stPlotlyChart"] .svg-container {
        overflow: visible !important;
        max-height: none !important;
        clip-path: none !important;
    }

    .main div[data-testid="stPlotlyChart"] {
        padding-top: clamp(.72rem, .9vw, .95rem) !important;
        padding-bottom: clamp(.62rem, .8vw, .82rem) !important;
    }

    .main div[data-testid="stPlotlyChart"] svg.main-svg {
        overflow: visible !important;
    }

    /* Clean health index: two balanced cards with no target/status clutter. */
    .st-key-health_score_section .health-section-subtitle {
        max-width: 760px !important;
        margin-bottom: .9rem !important;
        line-height: 1.55 !important;
    }

    .st-key-health_score_chart div[data-testid="stPlotlyChart"] {
        min-height: 300px !important;
        height: auto !important;
        max-height: none !important;
        padding: .45rem !important;
        background: radial-gradient(circle at 50% 45%, rgba(74,141,255,.13), transparent 52%),
                    linear-gradient(160deg, rgba(16,36,59,.94), rgba(8,19,33,.98)) !important;
    }

    .health-clean-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: clamp(.8rem, 1vw, 1rem) !important;
    }

    .health-clean-card {
        min-height: 205px !important;
        padding: 1.05rem !important;
        border-radius: 17px !important;
        border: 1px solid rgba(130,165,205,.17) !important;
        background: linear-gradient(155deg, rgba(19,43,70,.96), rgba(12,29,49,.98)) !important;
        box-shadow: 0 12px 28px rgba(1,8,18,.20) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }

    .health-clean-card::before {
        background: linear-gradient(90deg, #4A8DFF, #35C6E8) !important;
    }

    .health-clean-value-row {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: .75rem;
        margin: 1rem 0 .85rem;
    }

    .health-clean-value-row strong {
        color: #FFFFFF;
        font-size: clamp(1.75rem, 2.2vw, 2.25rem);
        line-height: 1;
        font-variant-numeric: tabular-nums;
        letter-spacing: -.035em;
    }

    .health-clean-value-row span {
        color: #AFC1D4;
        font-size: .74rem;
        text-align: right;
        line-height: 1.35;
    }

    .health-clean-progress span {
        background: linear-gradient(90deg, #4A8DFF, #35C6E8) !important;
    }

    .health-clean-intro {
        margin-bottom: .8rem !important;
    }

    @media (max-width: 1180px) {
        .health-clean-grid {
            grid-template-columns: 1fr !important;
        }
        .health-clean-card {
            min-height: 178px !important;
        }
    }

    @media (max-width: 760px) {
        .health-clean-value-row {
            align-items: flex-start;
            flex-direction: column;
        }
        .health-clean-value-row span { text-align: left; }
    }
    </style>
    """

def get_css() -> str:  # type: ignore[override]
    return _v1054_previous_get_css() + _v1054_chart_title_health_css()


# V10.5.5 — Restore occupational health radial visual and desktop side-by-side layout
_v1055_previous_get_css = get_css

def _v1055_health_chart_restore_css() -> str:
    return r"""
    <style>
    /* Keep the index visual and component cards side by side on notebooks/desktops. */
    .st-key-health_score_section div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        align-items: stretch !important;
    }

    .st-key-health_score_section div[data-testid="stColumn"] {
        min-width: 0 !important;
    }

    .st-key-health_score_chart {
        display: flex !important;
        height: 100% !important;
        min-height: 330px !important;
    }

    .health-score-visual-card {
        position: relative;
        isolation: isolate;
        width: 100%;
        min-height: 330px;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 1.2rem 1rem 1rem;
        overflow: hidden;
        border: 1px solid rgba(96,165,250,.22);
        border-radius: 19px;
        background:
            radial-gradient(circle at 50% 38%, rgba(74,141,255,.17), transparent 42%),
            linear-gradient(155deg, rgba(18,42,68,.98), rgba(8,22,38,.99));
        box-shadow: inset 0 1px 0 rgba(255,255,255,.035), 0 14px 34px rgba(0,0,0,.22);
        box-sizing: border-box;
    }

    .health-score-visual-glow {
        position: absolute;
        width: 210px;
        height: 210px;
        border-radius: 50%;
        background: rgba(74,141,255,.12);
        filter: blur(28px);
        z-index: -1;
    }

    .health-score-visual-ring {
        --score-angle: 0deg;
        position: relative;
        width: clamp(170px, 15vw, 216px);
        aspect-ratio: 1;
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background:
            conic-gradient(from -90deg,
                #4A8DFF 0deg,
                #35C6E8 var(--score-angle),
                rgba(57,78,104,.46) var(--score-angle),
                rgba(57,78,104,.46) 360deg);
        box-shadow: 0 0 34px rgba(74,141,255,.18), inset 0 0 0 1px rgba(255,255,255,.035);
    }

    .health-score-visual-ring::before {
        content: "";
        position: absolute;
        inset: 15px;
        border-radius: 50%;
        background: linear-gradient(145deg, #102A46, #091C30);
        box-shadow: inset 0 0 0 1px rgba(138,181,226,.15), 0 8px 22px rgba(0,0,0,.24);
    }

    .health-score-visual-core {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: .28rem;
        text-align: center;
    }

    .health-score-visual-core strong {
        color: #FFFFFF;
        font-size: clamp(2rem, 3vw, 2.7rem);
        line-height: 1;
        font-weight: 850;
        letter-spacing: -.045em;
        font-variant-numeric: tabular-nums;
    }

    .health-score-visual-core span {
        color: #AFC5DA;
        font-size: .66rem;
        font-weight: 800;
        letter-spacing: .105em;
    }

    .health-score-visual-caption {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: .22rem;
        text-align: center;
        max-width: 290px;
    }

    .health-score-visual-caption strong {
        color: #F5F9FD;
        font-size: .92rem;
        line-height: 1.25;
    }

    .health-score-visual-caption span {
        color: #93A9BE;
        font-size: .72rem;
        line-height: 1.45;
    }

    /* With two active components, keep both analytical cards readable side by side. */
    .st-key-health_score_breakdown .health-clean-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }

    @media (max-width: 920px) {
        .st-key-health_score_section div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        .st-key-health_score_section div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
        }
        .st-key-health_score_chart {
            max-width: 720px;
            min-height: 300px !important;
            margin: 0 auto;
        }
        .health-score-visual-card { min-height: 300px; }
    }

    @media (max-width: 620px) {
        .st-key-health_score_breakdown .health-clean-grid {
            grid-template-columns: 1fr !important;
        }
        .health-score-visual-card {
            min-height: 280px;
            padding: 1rem .8rem;
        }
        .health-score-visual-ring {
            width: 170px;
        }
    }
    </style>
    """


def get_css() -> str:  # type: ignore[override]
    return _v1055_previous_get_css() + _v1055_health_chart_restore_css()

# V10.5.6 — FINAL PURPLE OVERRIDE - garante que TODO azul vire roxo/magenta/branco
_v1056_previous_get_css = get_css

def _v1056_final_purple_override() -> str:
    return r"""
    <style>
    /* ===== FORÇA ROXO EM TUDO QUE AINDA TAVA AZUL ===== */
    
    /* Cards Componentes do Índice - era azul escuro #0B1220 etc, agora roxo */
    .health-clean-card,
    div:has(> .health-clean-card),
    [class*="health-clean"] {
        background: linear-gradient(135deg, #1E1240 0%, #25144A 100%) !important;
        border: 1px solid rgba(139,92,246,0.20) !important;
        border-radius: 16px !important;
    }
    
    /* Breakdown cards específicos do Índice de Saúde Ocupacional */
    .st-key-health_score_breakdown div[data-testid="stVerticalBlock"] > div > div {
        background: transparent !important;
    }
    
    /* Todos os containers com fundo azul antigo */
    div[style*="background: #0B1220"],
    div[style*="background:#0B1220"],
    div[style*="background: #0D2239"],
    div[style*="background: #112A45"],
    div[style*="background: #1A1433"] {
        background: linear-gradient(135deg, #1E1240 0%, #25144A 100%) !important;
    }
    
    /* Selects e inputs - de azul #112A45 para roxo */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div:hover,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="input"] > div,
    [data-baseweb="input"] > div:focus-within,
    [data-baseweb="base-input"] {
        background: linear-gradient(180deg, #1E1240, #25144A) !important;
        border-color: rgba(139,92,246,0.35) !important;
    }
    
    /* Tags de filtro - de azul #245FA9 para roxo */
    [data-baseweb="tag"] {
        background: linear-gradient(180deg, #7C3AED, #6D28D9) !important;
        border: 1px solid rgba(168,85,247,0.4) !important;
    }
    
    /* Popovers e menus - de #0D2239 para roxo escuro */
    body [data-baseweb="popover"] [role="listbox"],
    body [data-baseweb="menu"],
    body [role="listbox"] {
        background: #1A1033 !important;
        border: 1px solid rgba(139,92,246,0.25) !important;
    }
    
    body [role="option"] {
        background: #1E1240 !important;
    }
    body [role="option"]:hover,
    body [role="option"][data-highlighted="true"] {
        background: #7C3AED !important;
    }
    body [role="option"][aria-selected="true"] {
        background: linear-gradient(180deg, #8B5CF6, #7C3AED) !important;
    }
    
    /* Componentes do índice - cards específicos */
    .health-clean-grid > div,
    .health-clean-grid > div > div {
        background: linear-gradient(135deg, #1E1240 0%, #25144A 100%) !important;
        border: 1px solid rgba(139,92,246,0.18) !important;
    }
    
    /* Dashboard header já está roxo, mas garante */
    .dashboard-header {
        background: linear-gradient(135deg, #1E1240 0%, #2A1A52 100%) !important;
        border-top: 2px solid #8B5CF6 !important;
        border-left: 1px solid rgba(139,92,246,0.2) !important;
        border-right: 1px solid rgba(139,92,246,0.2) !important;
        border-bottom: 1px solid rgba(139,92,246,0.2) !important;
    }
    
    /* Remove qualquer azul restante com !important global */
    * {
        scrollbar-color: #8B5CF6 #130A2B !important;
    }
    
    /* Gráficos e containers escuros */
    .stPlotlyChart, div[data-testid="stPlotlyChart"] {
        background: transparent !important;
    }
    
    /* Força todos os backgrounds que eram #0B1220, #0F172A, #111827, #0B0F19 para roxo */
    div[style*="#0B1220"],
    div[style*="#0F172A"],
    div[style*="#111827"],
    div[style*="#0B0F19"],
    div[style*="#112A45"] {
        /* será sobrescrito pelos seletores acima */
    }
    </style>
    """


# V10.5.6 — PURPLE FINAL OVERRIDE - força roxo/magenta/branco em TUDO que ficou azul
_v1056_previous_get_css = get_css

def _v1056_purple_final_override() -> str:
    return r"""
    <style>
    /* ===== OVERRIDE FINAL - TUDO ROXO ===== */
    .stApp, .main, body {
        background: #130A2B !important;
        background-color: #130A2B !important;
    }
    
    /* Cards de componentes do índice (os 20.2% e 84.1% que ficaram azuis) */
    .health-clean-card {
        background: linear-gradient(155deg, rgba(30,18,64,0.96), rgba(19,10,43,0.98)) !important;
        border: 1px solid rgba(139,92,246,0.22) !important;
        box-shadow: 0 12px 28px rgba(19,10,43,0.4), inset 0 1px 0 rgba(139,92,246,0.08) !important;
    }
    .health-clean-card::before {
        background: linear-gradient(90deg, #8B5CF6, #EC4899) !important;
    }
    .health-clean-progress span {
        background: linear-gradient(90deg, #8B5CF6, #EC4899) !important;
    }
    
    /* Visual card 52.1% */
    .health-score-visual-card {
        background:
            radial-gradient(circle at 50% 38%, rgba(139,92,246,.18), transparent 42%),
            linear-gradient(155deg, rgba(30,18,64,.98), rgba(19,10,43,.99)) !important;
        border: 1px solid rgba(139,92,246,.24) !important;
    }
    .health-score-visual-glow {
        background: rgba(139,92,246,.14) !important;
    }
    .health-score-visual-ring {
        background:
            conic-gradient(from -90deg,
                #8B5CF6 0deg,
                #EC4899 var(--score-angle),
                rgba(139,92,246,.18) var(--score-angle),
                rgba(139,92,246,.18) 360deg) !important;
        box-shadow: 0 0 34px rgba(139,92,246,.22), inset 0 0 0 1px rgba(255,255,255,.04) !important;
    }
    .health-score-visual-ring::before {
        background: linear-gradient(145deg, #1E1240, #130A2B) !important;
        box-shadow: inset 0 0 0 1px rgba(167,139,250,.18), 0 8px 22px rgba(0,0,0,.28) !important;
    }
    
    /* Todos os containers escuros que eram azuis */
    .dashboard-header, .kpi-card, .chart-card, .metric-card,
    div[data-testid="stMetric"], .st-key-health_score_section > div {
        border-color: rgba(139,92,246,0.18) !important;
    }
    
    /* Selects e inputs - roxo em vez de azul */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div:hover,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="input"] > div,
    [data-baseweb="input"] > div:focus-within,
    [data-baseweb="base-input"] {
        background: linear-gradient(180deg, #25144A, #1E1240) !important;
        border-color: rgba(139,92,246,.32) !important;
    }
    
    [data-baseweb="tag"] {
        background: linear-gradient(180deg, #7C3AED, #6D28D9) !important;
        border: 1px solid rgba(167,139,250,.35) !important;
    }
    
    body [data-baseweb="popover"] [role="listbox"],
    body [data-baseweb="menu"],
    body [role="listbox"] {
        background: #1E1240 !important;
        border: 1px solid rgba(139,92,246,.18) !important;
    }
    
    body [role="option"] {
        background: #1E1240 !important;
    }
    body [role="option"]:hover,
    body [role="option"][data-highlighted="true"] {
        background: #7C3AED !important;
    }
    body [role="option"][aria-selected="true"] {
        background: linear-gradient(180deg, #8B5CF6, #7C3AED) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #170E33 0%, #130A2B 100%) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.18) !important;
    }
    header[data-testid="stHeader"] {
        background: rgba(19, 10, 43, 0.9) !important;
        border-bottom: 1px solid rgba(139, 92, 246, 0.12) !important;
    }
    
    /* Remove azul de qualquer gradiente inline */
    [style*="rgba(18,42,68"], [style*="rgba(8,22,38"], [style*="#102A46"], [style*="#4A8DFF"] {
        /* será sobrescrito pelas classes acima */
    }
    
    /* Bordas superiores dos cards - roxo */
    .health-clean-card, .kpi-card, .dashboard-header {
        border-top-color: rgba(139,92,246,0.35) !important;
    }
    

    /* ===== TABELA COMPARAÇÃO - BARRAS AZUIS -> ROXO ===== */
    table td div[style*="background"],
    td div[style*="background: #"],
    .stDataFrame td div,
    div[data-testid="stDataFrame"] div[style*="background"] {
        background: linear-gradient(90deg, #8B5CF6 0%, #A78BFA 100%) !important;
        background-color: #8B5CF6 !important;
    }
    
    /* Barras de comparação - força roxo */
    div[style*="width:"][style*="background-color: rgb(30"],
    div[style*="width:"][style*="background-color: #1E"],
    div[style*="width:"][style*="#2563EB"],
    div[style*="background: #1E3A"],
    div[style*="background: #1E40"] {
        background: #8B5CF6 !important;
        background-color: #8B5CF6 !important;
    }
    
    /* Botões Restaurar filtros / Sincronizar / Relatório - FUNDO ROXO FORTE + TEXTO BRANCO FORTE */
    button[kind="secondary"], 
    .stButton button,
    div[data-testid="stButton"] button,
    button[data-testid="stBaseButton-secondary"],
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
        background-color: #7C3AED !important;
        border: 1.5px solid rgba(124,58,237,0.55) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.02em !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.25) !important;
        box-shadow: 0 4px 14px rgba(124,58,237,0.32), inset 0 1px 0 rgba(255,255,255,0.18) !important;
        border-radius: 12px !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
    }
    /* Texto dentro do botão - garante branco forte */
    button[kind="secondary"] *, 
    .stButton button *,
    div[data-testid="stButton"] button * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    button[kind="secondary"]:hover,
    .stButton button:hover,
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
        background-color: #8B5CF6 !important;
        border-color: #A78BFA !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(124,58,237,0.45), 0 0 18px rgba(124,58,237,0.25), inset 0 1px 0 rgba(255,255,255,0.22) !important;
    }
    button[kind="secondary"]:active,
    .stButton button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px rgba(124,58,237,0.35) !important;
    }
    
    /* Gráficos Plotly - fundo roxo escuro */
    .js-plotly-plot, .plot-container, .svg-container {
        background: transparent !important;
    }
    
    /* Bullet charts e coberturas - barras vermelhas -> roxo/magenta */
    .bullet-chart-bar, div[style*="background: rgb(248"],
    div[style*="#FB7185"], div[style*="#F87171"] {
        background: linear-gradient(90deg, #8B5CF6, #EC4899) !important;
    }
    
    /* Força todos os azuis restantes para roxo via filter */
    /* Tabelas */
    .stDataFrame, .stDataFrame table, .stDataFrame th, .stDataFrame td {
        border-color: rgba(139,92,246,0.15) !important;
    }
    .stDataFrame th {
        background: #1E1240 !important;
        color: #C4B5FD !important;
    }
    .stDataFrame td {
        background: rgba(30,18,64,0.5) !important;
    }

    /* Texto secundário mais lavanda */
    .health-clean-value-row span, .text-secondary {
        color: #C4B5FD !important;
    }
    </style>
    """


def _v1057_strong_charts() -> str:
    return r"""
    <style>
    /* GRÁFICOS MAIS FORTES - FINAL */
    .js-plotly-plot .plotly .bg { fill: rgba(15,10,31,0.55) !important; }
    .js-plotly-plot .barlayer .bars path {
        filter: drop-shadow(0 3px 10px rgba(124,58,237,0.45)) !important;
        stroke: rgba(255,255,255,0.30) !important;
        stroke-width: 1.3px !important;
    }
    .js-plotly-plot .scatterlayer .lines path {
        stroke-width: 3.8px !important;
        filter: drop-shadow(0 0 8px rgba(124,58,237,0.55)) !important;
    }
    .js-plotly-plot .legend {
        background: rgba(30,11,58,0.75) !important;
        border: 1px solid rgba(124,58,237,0.35) !important;
        border-radius: 14px !important;
        padding: 10px 14px !important;
        backdrop-filter: blur(14px) !important;
    }
    .kpi-card, .chart-card, .health-clean-card {
        border: 1px solid rgba(124,58,237,0.38) !important;
        box-shadow: 0 10px 36px rgba(0,0,0,0.45), 0 0 24px rgba(124,58,237,0.18), inset 0 1px 0 rgba(255,255,255,0.10) !important;
    }
    .kpi-card:hover { transform: translateY(-2px) !important; border-color: rgba(124,58,237,0.60) !important; box-shadow: 0 14px 44px rgba(0,0,0,0.55), 0 0 36px rgba(124,58,237,0.30) !important; }
    .health-score-visual-ring {
        background: conic-gradient(from -90deg, #7C3AED 0deg, #EC4899 50deg, #D946EF 100deg, #F472B6 var(--score-angle), rgba(124,58,237,0.18) var(--score-angle), rgba(124,58,237,0.18) 360deg) !important;
        box-shadow: 0 0 48px rgba(124,58,237,0.42), inset 0 0 0 1px rgba(255,255,255,0.10) !important;
    }
    .health-clean-progress span { background: linear-gradient(90deg, #7C3AED 0%, #A78BFA 50%, #EC4899 100%) !important; box-shadow: 0 2px 14px rgba(124,58,237,0.55) !important; height: 9px !important; }
    .health-clean-progress { background: rgba(124,58,237,0.18) !important; height: 9px !important; border-radius: 9px !important; }
    .js-plotly-plot .gtitle { font-weight: 800 !important; fill: #FFFFFF !important; font-size: 16px !important; }
    </style>
    """

_prev_1057 = get_css

def _v1058_fixes_imagens() -> str:
    return r"""
    <style>
    /* ===== CORREÇÕES DAS IMAGENS ENVIADAS ===== */
    
    /* 1. MAPA DE INTENSIDADE - tira azul, põe roxo forte + corrige mês cortado */
    /* heatmap fix - sem hue-rotate */ .js-plotly-plot .heatmaplayer .hm {
        /* filtro removido - estava deixando verde */
    }
    /* Heatmap - colorscale roxo */
    /* heatmap vars removidas - cores via Python */
    /* Garante que o mês não corta - aumenta margem inferior */
    .js-plotly-plot .xaxislayer {
        transform: translateY(8px) !important;
    }
    .js-plotly-plot .xtick text {
        font-size: 11px !important;
        fill: #C4B5FD !important;
        font-weight: 500 !important;
    }
    /* Colorbar do heatmap - roxo */
    .js-plotly-plot .colorbar {
        border: 1px solid rgba(124,58,237,0.3) !important;
        border-radius: 8px !important;
    }
    .js-plotly-plot .colorbar .bg {
        fill: url(#purple-gradient) !important;
    }
    
    /* 2. TABELA - tira azul, 100% roxo */
    .stDataFrame, div[data-testid="stDataFrame"] {
        border: 1px solid rgba(124,58,237,0.25) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    .stDataFrame thead tr th {
        background: linear-gradient(180deg, #2D1B4E 0%, #1E0B3A 100%) !important;
        background-color: #2D1B4E !important;
        color: #E9D5FF !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.03em !important;
        border-bottom: 2px solid rgba(124,58,237,0.35) !important;
        border-right: 1px solid rgba(124,58,237,0.15) !important;
    }
    .stDataFrame tbody tr {
        background: rgba(26, 20, 51, 0.6) !important;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background: rgba(36, 28, 64, 0.8) !important;
    }
    .stDataFrame tbody tr:hover {
        background: rgba(124,58,237,0.12) !important;
    }
    .stDataFrame tbody td {
        background: transparent !important;
        background-color: transparent !important;
        color: #E9D5FF !important;
        border-bottom: 1px solid rgba(124,58,237,0.10) !important;
        border-right: 1px solid rgba(124,58,237,0.08) !important;
        font-size: 12.5px !important;
    }
    /* Remove qualquer azul inline da tabela */
    .stDataFrame [style*="background: rgb"],
    .stDataFrame [style*="background-color: rgb"],
    .stDataFrame [style*="#1E3A"],
    .stDataFrame [style*="#1E40"],
    .stDataFrame [style*="#2563EB"] {
        background: transparent !important;
    }
    
    /* 3. COMPONENTES DO ÍNDICE - centraliza e diminui texto */
    /* Cards de composição */
    .health-clean-card, div:has(> div > .health-clean-value) {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: stretch !important;
        padding: 18px 20px !important;
        min-height: 140px !important;
    }
    /* Valor principal 32.7% - menor */
    .health-clean-value, div:has(> .health-clean-value) .health-clean-value,
    [class*="health-clean"] > div:first-child > div:first-child {
        font-size: 26px !important;
        font-weight: 700 !important;
        line-height: 1.1 !important;
        color: #FFFFFF !important;
        text-align: left !important;
    }
    /* Texto secundário 16.4 pontos - menor e centralizado à direita */
    .health-clean-label, .health-clean-context {
        font-size: 11px !important;
        color: #A78BFA !important;
        font-weight: 500 !important;
        text-align: right !important;
    }
    /* Barra de progresso mais centralizada */
    .health-clean-progress {
        margin: 14px 0 6px 0 !important;
        height: 6px !important;
        background: rgba(124,58,237,0.15) !important;
        border-radius: 6px !important;
    }
    .health-clean-progress span {
        height: 6px !important;
        border-radius: 6px !important;
        background: linear-gradient(90deg, #7C3AED 0%, #D946EF 50%, #EC4899 100%) !important;
    }
    
    /* 4. BULLET CHART 40.9% - centraliza e diminui */
    .js-plotly-plot .indicatorlayer .number,
    .js-plotly-plot .indicatorlayer text {
        font-size: 20px !important;
    }
    /* Bullet gauge - centraliza no container */
    .js-plotly-plot[data-title*="40"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    /* Título do bullet menor */
    .js-plotly-plot .gtitle, .js-plotly-plot .infolayer .gtitle {
        font-size: 12px !important;
        font-weight: 600 !important;
        fill: #C4B5FD !important;
    }
    /* Delta -54.1 menor */
    .js-plotly-plot .delta {
        font-size: 11px !important;
    }
    
    /* 5. GARANTE QUE NENHUM AZUL SOBREVIVA - força roxo em tudo que for azul */
    [style*="#3B82F6"], [style*="#2563EB"], [style*="#1D4ED8"], 
    [style*="rgb(59, 130, 246)"], [style*="rgb(37, 99, 235)"],
    div[style*="background: #3B82F6"], div[style*="background-color: #3B82F6"] {
        background: #7C3AED !important;
        background-color: #7C3AED !important;
        border-color: #7C3AED !important;
    }
    
    /* Heatmap específico - força gradiente roxo via CSS */
    /* heatmap rect - sem filtro */ .js-plotly-plot .heatmaplayer {
        /* Será controlado pelo colorscale do Python, mas garante saturação */
        /* filtro removido */
    }
    </style>
    """

_prev_1058 = get_css

def _v1059_botoes_roxo_branco_forte() -> str:
    return r"""
    <style>
    /* BOTÕES - FUNDO ROXO + TEXTO BRANCO BEM FORTE - OVERRIDE FINAL ABSOLUTO */
    /* Restaurar filtros, Sincronizar agora, Preparar relatório, Baixar PDF */
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button[kind="secondary"],
    button[kind="secondary"],
    .stButton > button,
    [data-testid="stBaseButton-secondary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
        background-color: #7C3AED !important;
        border: 1.5px solid #8B5CF6 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.3px !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.35) !important;
        box-shadow: 0 4px 16px rgba(124,58,237,0.38), inset 0 1px 0 rgba(255,255,255,0.20) !important;
        border-radius: 12px !important;
    }
    /* Garante que ícones e spans internos fiquem brancos */
    div[data-testid="stButton"] button div,
    div[data-testid="stButton"] button span,
    div[data-testid="stButton"] button p,
    button[kind="secondary"] div,
    button[kind="secondary"] span {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    /* Hover - mais claro */
    div[data-testid="stButton"] button:hover,
    button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 50%, #EC4899 100%) !important;
        border-color: #FFFFFF !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 28px rgba(124,58,237,0.50), 0 0 20px rgba(124,58,237,0.30) !important;
    }
    /* Foco */
    div[data-testid="stButton"] button:focus,
    button[kind="secondary"]:focus {
        border-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.35), 0 4px 16px rgba(124,58,237,0.38) !important;
    }
    /* Botões de relatório executivo - especificamente */
    button:has-text("Preparar relatório executivo"),
    button:has-text("Baixar relatório PDF") {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    </style>
    """

_prev_1059 = get_css

def _v1060_dropdown_roxo() -> str:
    return r"""
    <style>
    /* DROPDOWN UNIDADES - tira azul, põe roxo forte */
    /* Select all - azul -> roxo */
    div[role="listbox"] [role="option"],
    li[role="option"],
    div[data-baseweb="select"] div[role="option"],
    body [role="option"] {
        background: #1E0B3A !important;
        background-color: #1E0B3A !important;
        color: #E9D5FF !important;
        border-bottom: 1px solid rgba(124,58,237,0.10) !important;
    }
    /* Hover e selecionado - roxo forte */
    div[role="listbox"] [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"][aria-selected="true"],
    div[role="option"][data-highlighted="true"],
    body [role="option"]:hover,
    body [role="option"][data-highlighted="true"],
    body [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
        background-color: #7C3AED !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    /* Select all específico - estava azul */
    div[role="listbox"] div:first-child[role="option"],
    [data-baseweb="select"] [role="option"]:first-child {
        background: #7C3AED !important;
        background-color: #7C3AED !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-bottom: 2px solid rgba(124,58,237,0.4) !important;
    }
    /* Fundo do popover do select - roxo escuro */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"],
    div[role="listbox"] {
        background: #1E0B3A !important;
        background-color: #1E0B3A !important;
        border: 1.5px solid rgba(124,58,237,0.35) !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 32px rgba(0,0,0,0.5), 0 0 24px rgba(124,58,237,0.20) !important;
        overflow: hidden !important;
    }
    /* Checkbox dentro do multiselect */
    div[role="option"] input[type="checkbox"] {
        accent-color: #7C3AED !important;
        border-color: #7C3AED !important;
    }
    /* Texto das opções */
    div[role="option"] div,
    div[role="option"] span {
        color: inherit !important;
    }
    </style>
    """

_prev_1060 = get_css
def get_css() -> str:
    return _prev_1060() + _v1060_dropdown_roxo()
