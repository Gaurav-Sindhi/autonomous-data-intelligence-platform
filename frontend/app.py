import streamlit as st

st.set_page_config(
    page_title="ADI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — injected once from the root app
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0f1117;
        border-right: 1px solid #1e2130;
    }
    [data-testid="stSidebar"] * {
        color: #c9d1d9 !important;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #58a6ff !important;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    /* ── Main background ── */
    .main .block-container {
        background: #0d1117;
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.72rem;
        font-weight: 500;
        color: #8b949e !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem;
        font-weight: 700;
        color: #e6edf3 !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid #21262d;
        border-radius: 8px;
        overflow: hidden;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: #238636;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background: #2ea043;
    }

    /* ── Download buttons ── */
    .stDownloadButton > button {
        background: #1f6feb;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        transition: background 0.2s;
        width: 100%;
    }
    .stDownloadButton > button:hover {
        background: #388bfd;
    }

    /* ── Section headers ── */
    .adi-section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e6edf3;
        letter-spacing: -0.01em;
        margin-bottom: 0.15rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .adi-section-sub {
        font-size: 0.8rem;
        color: #8b949e;
        margin-bottom: 1.25rem;
    }
    .adi-divider {
        border: none;
        border-top: 1px solid #21262d;
        margin: 2rem 0;
    }

    /* ── Insight cards ── */
    .adi-insight-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-left: 3px solid #58a6ff;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        font-size: 0.9rem;
        color: #c9d1d9;
        line-height: 1.6;
    }
    .adi-insight-card.green {
        border-left-color: #3fb950;
    }
    .adi-insight-card.yellow {
        border-left-color: #d29922;
    }

    /* ── Badge ── */
    .adi-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .adi-badge.green  { background: #1a3d2b; color: #3fb950; }
    .adi-badge.blue   { background: #1c2d4a; color: #58a6ff; }
    .adi-badge.yellow { background: #3d2e00; color: #d29922; }

    /* ── Upload zone ── */
    [data-testid="stFileUploader"] {
        border: 1px dashed #30363d;
        border-radius: 10px;
        padding: 0.5rem;
        background: #161b22;
    }

    /* ── Form inputs ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #161b22;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 6px;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 3px rgba(88,166,255,0.15);
    }

    /* ── Alerts ── */
    .stAlert {
        border-radius: 8px;
        border: none;
        font-size: 0.875rem;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #58a6ff !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# SIDEBAR BRANDING
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding:1rem 0 1.5rem 0;">
            <div style="font-size:1.35rem;font-weight:800;color:#e6edf3;letter-spacing:-0.02em;">
                🧠 ADI Platform
            </div>
            <div style="font-size:0.72rem;color:#8b949e;margin-top:0.2rem;">
                Autonomous Data Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Navigation")

# ─────────────────────────────────────────────
# HOME PAGE CONTENT
# ─────────────────────────────────────────────
st.markdown(
    """
    <div style="padding: 3rem 0 1.5rem 0;">
        <div style="font-size:0.78rem;font-weight:600;color:#58a6ff;
                    letter-spacing:0.1em;text-transform:uppercase;
                    margin-bottom:0.75rem;">
            AI · AutoML · Insights
        </div>
        <h1 style="font-size:2.6rem;font-weight:800;color:#e6edf3;
                   line-height:1.15;letter-spacing:-0.03em;margin:0 0 1rem 0;">
            Autonomous Data<br>Intelligence Platform
        </h1>
        <p style="font-size:1.05rem;color:#8b949e;max-width:560px;
                  line-height:1.65;margin:0 0 2rem 0;">
            Upload any CSV. Get AI-powered insights, automatic model training,
            and production-ready predictions — in minutes.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(3, gap="medium")
features = [
    ("🧹", "Auto Data Cleaning", "Detects and repairs missing values, duplicates, and type errors automatically."),
    ("🏆", "AutoML Training", "Trains multiple models — Logistic Regression, Random Forest, XGBoost — and selects the best."),
    ("🔮", "Live Predictions", "Enter feature values and receive instant predictions with AI-generated explanations."),
]
for col, (icon, title, desc) in zip(cols, features):
    with col:
        st.markdown(
            f"""
            <div style="background:#161b22;border:1px solid #21262d;
                        border-radius:10px;padding:1.25rem;">
                <div style="font-size:1.6rem;margin-bottom:0.6rem;">{icon}</div>
                <div style="font-size:0.95rem;font-weight:700;color:#e6edf3;
                            margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.82rem;color:#8b949e;line-height:1.55;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="background:#161b22;border:1px solid #21262d;border-radius:10px;
                padding:1.25rem 1.5rem;display:flex;align-items:center;gap:1rem;">
        <span style="font-size:1.1rem;">👈</span>
        <span style="font-size:0.9rem;color:#8b949e;">
            Use the <strong style="color:#e6edf3;">sidebar</strong> to navigate —
            start with <strong style="color:#58a6ff;">Dashboard</strong> to upload your dataset.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
