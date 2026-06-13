"""
about.py — ADI Platform
Project information, tech stack, and developer credits.
"""

import streamlit as st

st.markdown(
    """
    <div style="margin-bottom:0.25rem;">
        <span style="font-size:0.72rem;font-weight:600;color:#58a6ff;
                     letter-spacing:0.1em;text-transform:uppercase;">
            Project
        </span>
    </div>
    <h2 style="font-size:1.75rem;font-weight:800;color:#e6edf3;
               letter-spacing:-0.02em;margin:0 0 0.4rem 0;">
        About
    </h2>
    <p style="font-size:0.875rem;color:#8b949e;margin:0 0 1.5rem 0;">
        Architecture, capabilities, and the people who built it.
    </p>
    <hr style="border:none;border-top:1px solid #21262d;margin:0 0 2rem 0;">
    """,
    unsafe_allow_html=True,
)

# ── Platform overview ──
st.markdown(
    """
    <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;
                padding:1.75rem 2rem;margin-bottom:1.5rem;">
        <div style="font-size:1.1rem;font-weight:700;color:#e6edf3;margin-bottom:0.75rem;">
            Autonomous Data Intelligence Platform
        </div>
        <div style="font-size:0.9rem;color:#8b949e;line-height:1.7;">
            ADI is an end-to-end AutoML platform that takes a raw CSV file and
            automatically cleans it, detects the machine learning problem type,
            trains and benchmarks multiple models, selects the best performer,
            and generates AI-powered insights and predictions — all without
            requiring any manual configuration.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Capabilities ──
st.markdown(
    '<div style="font-size:0.78rem;font-weight:600;color:#8b949e;'
    'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.75rem;">'
    'Capabilities</div>',
    unsafe_allow_html=True,
)

features = [
    ("🧹", "Auto Data Cleaning", "Handles missing values, duplicates, and type coercion."),
    ("🔍", "Problem Detection", "Classifies tasks as regression or classification automatically."),
    ("🤖", "AutoML Training", "Benchmarks Logistic Regression, Random Forest, and XGBoost."),
    ("🏆", "Model Selection Agent", "Picks the highest-scoring model using an AI reasoning chain."),
    ("🧠", "AI Insights", "Gemini API generates natural-language explanations of patterns."),
    ("📊", "Visual Analytics", "Auto-generates relevant charts per dataset type."),
    ("🔮", "Live Predictions", "Dynamic form + AI explanation for every prediction."),
    ("📄", "Report Generation", "Exports PDF and JSON reports of the full analysis."),
    ("📜", "Training History", "Persists every run for comparison and audit."),
]

for i in range(0, len(features), 3):
    row = features[i : i + 3]
    cols = st.columns(len(row), gap="medium")
    for col, (icon, title, desc) in zip(cols, row):
        with col:
            st.markdown(
                f"""
                <div style="background:#161b22;border:1px solid #21262d;
                            border-radius:8px;padding:1rem;">
                    <div style="font-size:1.25rem;margin-bottom:0.4rem;">{icon}</div>
                    <div style="font-size:0.85rem;font-weight:700;color:#e6edf3;
                                margin-bottom:0.3rem;">{title}</div>
                    <div style="font-size:0.78rem;color:#8b949e;line-height:1.5;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<hr style="border:none;border-top:1px solid #21262d;margin:0.5rem 0 1.5rem 0;">',
    unsafe_allow_html=True,
)

# ── Tech stack ──
st.markdown(
    '<div style="font-size:0.78rem;font-weight:600;color:#8b949e;'
    'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.75rem;">'
    'Tech Stack</div>',
    unsafe_allow_html=True,
)

stack = {
    "Frontend": [("Streamlit", "blue")],
    "Backend": [("FastAPI", "blue")],
    "Machine Learning": [("Scikit-Learn", "green"), ("XGBoost", "green")],
    "Generative AI": [("Google Gemini API", "yellow")],
    "Storage": [("AWS S3", "blue")],
}


def _badge(text, variant):
    colors = {
        "blue": ("#1c2d4a", "#58a6ff"),
        "green": ("#1a3d2b", "#3fb950"),
        "yellow": ("#3d2e00", "#d29922"),
    }
    bg, fg = colors.get(variant, colors["blue"])
    return (
        f'<span style="background:{bg};color:{fg};padding:0.2rem 0.65rem;'
        f'border-radius:20px;font-size:0.72rem;font-weight:700;'
        f'letter-spacing:0.04em;text-transform:uppercase;">{text}</span>'
    )


rows_html = ""
for category, items in stack.items():
    badges = " ".join(_badge(name, variant) for name, variant in items)
    rows_html += (
        f'<div style="display:flex;align-items:center;gap:1rem;'
        f'padding:0.65rem 0;border-bottom:1px solid #21262d;">'
        f'<div style="font-size:0.82rem;color:#8b949e;width:140px;'
        f'flex-shrink:0;">{category}</div>'
        f'<div style="display:flex;gap:0.4rem;flex-wrap:wrap;">{badges}</div>'
        f'</div>'
    )

st.markdown(
    f'<div style="background:#161b22;border:1px solid #21262d;'
    f'border-radius:10px;padding:0.25rem 1.25rem;">{rows_html}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<hr style="border:none;border-top:1px solid #21262d;margin:1.5rem 0;">',
    unsafe_allow_html=True,
)

# ── Developer card ──
st.markdown(
    """
    <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;
                padding:1.5rem 2rem;display:flex;align-items:center;gap:1.5rem;">
        <div style="width:52px;height:52px;background:#1c2d4a;border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.4rem;flex-shrink:0;">👨‍💻</div>
        <div>
            <div style="font-size:1rem;font-weight:700;color:#e6edf3;">
                Gaurav Narayani
            </div>
            <div style="font-size:0.8rem;color:#58a6ff;margin-top:0.15rem;">
                B.Tech — Artificial Intelligence & Machine Learning
            </div>
            <div style="font-size:0.78rem;color:#8b949e;margin-top:0.25rem;">
                Final Year Project · Autonomous Data Intelligence Platform
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
