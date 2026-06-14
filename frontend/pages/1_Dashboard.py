"""
dashboard.py — ADI Platform
Primary analysis workspace.

Architecture:
  1. Session state is the single source of truth.
  2. Analysis runs ONLY when the user clicks "Run Analysis".
  3. Every dashboard section reads from cached session state.
  4. Downloads, predictions, and reruns never retrigger training.
  5. Every external call is wrapped in try/except with user-visible fallback.
"""

import json
import requests
import streamlit as st
import pandas as pd

from utils.api import upload_dataset, get_metadata

BACKEND_URL = "http://127.0.0.1:8000"

# ──────────────────────────────────────────────
# SESSION STATE — initialize once
# ──────────────────────────────────────────────
_DEFAULTS = {
    "analysis_result": None,
    "dataset_name": None,
    "dataset_shape": None,
    "analysis_error": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def _section(icon: str, title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="adi-section-header">{icon} {title}</div>
        {"" if not subtitle else f'<div class="adi-section-sub">{subtitle}</div>'}
        """,
        unsafe_allow_html=True,
    )


def _card(text: str, variant: str = "blue"):
    st.markdown(
        f'<div class="adi-insight-card {variant}">{text}</div>',
        unsafe_allow_html=True,
    )


def _badge(text: str, variant: str = "blue"):
    return f'<span class="adi-badge {variant}">{text}</span>'


def _divider():
    st.markdown('<hr class="adi-divider">', unsafe_allow_html=True)


def _safe_file_bytes(path: str) -> bytes | None:
    """Read a file from disk safely. Returns None on any failure."""
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        return None


# ──────────────────────────────────────────────
# PAGE HEADER
# ──────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:0.25rem;">
        <span style="font-size:0.72rem;font-weight:600;color:#58a6ff;
                     letter-spacing:0.1em;text-transform:uppercase;">
            Analysis Workspace
        </span>
    </div>
    <h2 style="font-size:1.75rem;font-weight:800;color:#e6edf3;
               letter-spacing:-0.02em;margin:0 0 0.4rem 0;">
        Dashboard
    </h2>
    <p style="font-size:0.875rem;color:#8b949e;margin:0 0 1.5rem 0;">
        Upload a CSV dataset to begin. Analysis runs once and results are cached.
    </p>
    """,
    unsafe_allow_html=True,
)

_divider()

# ──────────────────────────────────────────────
# UPLOAD PANEL
# ──────────────────────────────────────────────
_section("📂", "Dataset Upload", "Accepts CSV files. Max recommended size: 50 MB.")

uploaded_file = st.file_uploader(
    "Drop your CSV file here",
    type=["csv"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    try:
        preview_df = pd.read_csv(uploaded_file)
        rows, cols_count = preview_df.shape
        st.markdown(
            f"""
            <div style="display:flex;gap:0.75rem;margin:0.75rem 0;">
                {_badge(uploaded_file.name, "blue")}
                {_badge(f"{rows:,} rows × {cols_count} columns", "green")}
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Preview (first 5 rows)", expanded=True):
            st.dataframe(preview_df.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        uploaded_file = None

col_btn_left, col_btn_right, _ = st.columns([1, 1, 4])

with col_btn_left:
    analyze_btn = st.button(
        "▶ Run Analysis",
        type="primary",
        disabled=(uploaded_file is None),
        use_container_width=True,
    )

with col_btn_right:
    if st.session_state.analysis_result is not None:
        if st.button("✕ Clear Results", use_container_width=True):
            for k in _DEFAULTS:
                st.session_state[k] = _DEFAULTS[k]
            st.rerun()

# ──────────────────────────────────────────────
# ANALYSIS TRIGGER — runs only on explicit click
# ──────────────────────────────────────────────
if analyze_btn and uploaded_file is not None:
    # Guard: don't re-analyse the same file unnecessarily
    if st.session_state.dataset_name == uploaded_file.name and \
       st.session_state.analysis_result is not None:
        st.info("This dataset was already analysed. Clear results to re-run.")
    else:
        st.session_state.analysis_error = None
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")
        }
        with st.spinner("Running AutoML pipeline — this may take 30–90 seconds…"):
            try:
                response = upload_dataset(files)
                if response.status_code == 200:
                    st.session_state.analysis_result = response.json()
                    st.session_state.dataset_name = uploaded_file.name
                    try:
                        st.session_state.dataset_shape = preview_df.shape
                    except Exception:
                        pass
                else:
                    st.session_state.analysis_error = (
                        f"Backend returned {response.status_code}: {response.text}"
                    )
            except requests.exceptions.ConnectionError:
                st.session_state.analysis_error = (
                    "Cannot reach the backend. Make sure the FastAPI server is running on port 8000."
                )
            except Exception as e:
                st.session_state.analysis_error = str(e)

        if st.session_state.analysis_error:
            st.error(f"Analysis failed: {st.session_state.analysis_error}")
        else:
            st.success("Analysis complete. Results cached below.")

# ──────────────────────────────────────────────
# EARLY EXIT — nothing to render yet
# ──────────────────────────────────────────────
if st.session_state.analysis_result is None:
    st.stop()

# ──────────────────────────────────────────────
# UNPACK RESULTS — all rendering below uses only
# st.session_state; no new API calls.
# ──────────────────────────────────────────────
try:
    result = st.session_state.analysis_result["insights"]
    raw = result["raw_insights"]
    cleaned_ins = result["cleaned_insights"]
    problem = result["problem_info"]
    training = result["training_results"]
    charts = result.get("charts", [])
    ai_insights = result.get("ai_insights", "")
    model_reasoning = result.get("model_reasoning", "")
    analytics_insight = result.get("analytics_insight", "")
    pdf_report = result.get("pdf_report")
    model_file = result.get("model_file")
    cleaned_dataset = result.get("cleaned_dataset")
except (KeyError, TypeError) as e:
    st.error(f"Unexpected response structure from backend: {e}")
    st.stop()

_divider()

# ══════════════════════════════════════════════
# SECTION 1 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════
_section("📋", "Executive Summary", "Key facts about your dataset and the winning model.")

best_score = max(training["scores"].values(), default=0.0)
problem_type = problem.get("problem_type", "—")
target_col = problem.get("target_column", "—")
best_model = training.get("best_model", "—")

score_label = "Accuracy" if problem_type.lower() == "classification" else "R² Score"

c1, c2, c3, c4 = st.columns(4, gap="medium")
c1.metric("Problem Type", problem_type)
c2.metric("Target Column", target_col)
c3.metric("Best Model", best_model)
c4.metric(score_label, f"{round(best_score, 4):.4f}")

if st.session_state.dataset_name:
    st.markdown(
        f"""
        <div style="margin-top:0.75rem;font-size:0.8rem;color:#8b949e;">
            Dataset: {_badge(st.session_state.dataset_name, "blue")}
            {"&nbsp;" + _badge(f'{st.session_state.dataset_shape[0]:,} rows × '
                               f'{st.session_state.dataset_shape[1]} cols', "green")
             if st.session_state.dataset_shape else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

_divider()

# ══════════════════════════════════════════════
# SECTION 2 — DATA QUALITY REPORT
# ══════════════════════════════════════════════
_section("🧹", "Data Quality Report", "Cleaning impact at a glance.")

q1, q2 = st.columns(2, gap="medium")

with q1:
    st.markdown(
        '<div style="font-size:0.78rem;font-weight:600;color:#8b949e;'
        'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.75rem;">'
        'Before Cleaning</div>',
        unsafe_allow_html=True,
    )
    b1, b2 = st.columns(2)
    b1.metric("Missing Values", raw.get("missing_values", 0))
    b2.metric("Duplicate Rows", raw.get("duplicate_rows", 0))

with q2:
    st.markdown(
        '<div style="font-size:0.78rem;font-weight:600;color:#3fb950;'
        'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.75rem;">'
        'After Cleaning</div>',
        unsafe_allow_html=True,
    )
    a1, a2 = st.columns(2)
    a1.metric("Missing Values", cleaned_ins.get("missing_values", 0))
    a2.metric("Duplicate Rows", cleaned_ins.get("duplicate_rows", 0))

st.markdown("<br>", unsafe_allow_html=True)

if cleaned_dataset:
    data_bytes = _safe_file_bytes(cleaned_dataset)
    if data_bytes:
        st.download_button(
            label="⬇ Download Cleaned Dataset (.csv)",
            data=data_bytes,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
        )
    else:
        st.warning("Cleaned dataset file could not be read from disk.")

_divider()

# ══════════════════════════════════════════════
# SECTION 3 — AI ANALYTICS SUMMARY
# ══════════════════════════════════════════════
_section(
    "🤖",
    "AI Analytics Summary",
    "Gemini-generated overview of dataset patterns and statistical behaviour.",
)
if analytics_insight:
    _card(analytics_insight, "blue")
else:
    st.caption("No analytics summary was returned by the AI.")

_divider()

# ══════════════════════════════════════════════
# SECTION 4 — MODEL PERFORMANCE
# ══════════════════════════════════════════════
_section("🏆", "Model Performance", "Scores across all trained models, sorted by performance.")

scores_df = pd.DataFrame(
    list(training["scores"].items()),
    columns=["Model", score_label],
).sort_values(score_label, ascending=False).reset_index(drop=True)

# Rank column
rank_emojis = [
    "🥇",
    "🥈",
    "🥉"
]

rank_column = []

for i in range(len(scores_df)):

    if i < 3:
        rank_column.append(
            rank_emojis[i]
        )
    else:
        rank_column.append(
            str(i + 1)
        )

scores_df.insert(
    0,
    "Rank",
    rank_column
)

ml_left, ml_right = st.columns([1, 1], gap="medium")

with ml_left:
    st.markdown(
        '<div style="font-size:0.82rem;font-weight:600;color:#8b949e;margin-bottom:0.5rem;">'
        'Leaderboard</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        scores_df,
        use_container_width=True,
        hide_index=True,
    )

with ml_right:
    st.markdown(
        '<div style="font-size:0.82rem;font-weight:600;color:#8b949e;margin-bottom:0.5rem;">'
        'Performance Comparison</div>',
        unsafe_allow_html=True,
    )
    chart_df = scores_df.set_index("Model")[[score_label]]
    st.bar_chart(chart_df, use_container_width=True)

_divider()

# ══════════════════════════════════════════════
# SECTION 5 — ADVANCED ANALYTICS CHARTS
# ══════════════════════════════════════════════
_section("📈", "Advanced Analytics", "Visual exploration of your dataset's structure and distributions.")

if not charts:
    st.markdown(
        '<div style="background:#161b22;border:1px solid #21262d;border-radius:8px;'
        'padding:2rem;text-align:center;color:#8b949e;font-size:0.875rem;">'
        '📊 No charts were generated for this dataset.</div>',
        unsafe_allow_html=True,
    )
else:
    # Render charts in 2-column grid where possible
    for i in range(0, len(charts), 2):
        row_charts = charts[i : i + 2]
        cols = st.columns(len(row_charts), gap="medium")
        for col, chart in zip(cols, row_charts):
            with col:
                st.markdown(
                    f'<div style="font-size:0.82rem;font-weight:600;color:#8b949e;'
                    f'margin-bottom:0.4rem;">{chart.get("title","Chart")}</div>',
                    unsafe_allow_html=True,
                )
                image_url = (
                    BACKEND_URL + "/" + chart["path"].replace("uploads/", "")
                )
                try:
                    st.image(image_url, use_container_width=True)
                except Exception:
                    st.caption("⚠ Chart image could not be loaded.")

_divider()

# ══════════════════════════════════════════════
# SECTION 6 — AI INSIGHTS + MODEL REASONING
# ══════════════════════════════════════════════
ins_left, ins_right = st.columns(2, gap="medium")

with ins_left:
    _section("🧠", "AI Dataset Insights", "Patterns and anomalies detected by the AI.")
    if ai_insights:
        _card(ai_insights, "green")
    else:
        st.caption("No AI insights were returned.")

with ins_right:
    _section("🎯", "Model Selection Reasoning", "Why the winning model was selected.")
    if model_reasoning:
        _card(model_reasoning, "yellow")
    else:
        st.caption("No model reasoning was returned.")

_divider()

# ══════════════════════════════════════════════
# SECTION 7 — DOWNLOADS
# ══════════════════════════════════════════════
_section("📥", "Downloads", "Export your results, reports, and trained model.")

dl1, dl2, dl3 = st.columns(3, gap="medium")

with dl1:
    st.markdown(
        '<div style="font-size:0.78rem;color:#8b949e;margin-bottom:0.5rem;">JSON Report</div>',
        unsafe_allow_html=True,
    )
    try:
        json_str = json.dumps(result, indent=4, default=str)
        st.download_button(
            label="⬇ Download JSON Report",
            data=json_str,
            file_name="adi_report.json",
            mime="application/json",
            use_container_width=True,
        )
    except Exception:
        st.warning("JSON report could not be serialised.")

with dl2:
    st.markdown(
        '<div style="font-size:0.78rem;color:#8b949e;margin-bottom:0.5rem;">PDF Report</div>',
        unsafe_allow_html=True,
    )
    if pdf_report:
        pdf_bytes = _safe_file_bytes(pdf_report)
        if pdf_bytes:
            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_bytes,
                file_name="adi_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.warning("PDF file not found on disk.")
    else:
        st.caption("PDF report was not generated.")

with dl3:
    st.markdown(
        '<div style="font-size:0.78rem;color:#8b949e;margin-bottom:0.5rem;">Trained Model</div>',
        unsafe_allow_html=True,
    )
    if model_file:
        model_bytes = _safe_file_bytes(model_file)
        if model_bytes:
            st.download_button(
                label="⬇ Download Model (.pkl)",
                data=model_bytes,
                file_name="best_model.pkl",
                mime="application/octet-stream",
                use_container_width=True,
            )
        else:
            st.warning("Model file not found on disk.")
    else:
        st.caption("No trained model file was returned.")

_divider()

# ══════════════════════════════════════════════
# SECTION 8 — PREDICTION CENTER
# ══════════════════════════════════════════════
_section(
    "🔮",
    "Prediction Center",
    "Enter feature values to run a live prediction against the trained model.",
)

# Fetch metadata — one call, isolated in its own try/except
metadata: dict = {}
try:
    meta_resp = get_metadata()
    if meta_resp.status_code == 200:
        metadata = meta_resp.json()
    else:
        st.warning(
            f"Metadata endpoint returned {meta_resp.status_code}. "
            "Prediction form cannot be displayed."
        )
except requests.exceptions.ConnectionError:
    st.warning("Backend is unreachable. Prediction is unavailable.")
except Exception as e:
    st.warning(f"Could not load metadata: {e}")

feature_columns: list = metadata.get("feature_columns", [])
feature_types: dict = metadata.get("feature_types", {})   # optional: {col: "numeric"|"categorical"}

if not feature_columns:
    st.markdown(
        '<div style="background:#161b22;border:1px solid #21262d;border-radius:8px;'
        'padding:2rem;text-align:center;color:#8b949e;font-size:0.875rem;">'
        '🔮 Prediction form unavailable — no feature columns found in metadata.</div>',
        unsafe_allow_html=True,
    )
else:
    with st.form("prediction_form", clear_on_submit=False):
        st.markdown(
            f'<div style="font-size:0.82rem;color:#8b949e;margin-bottom:1rem;">'
            f'Target: {_badge(target_col, "green")}&nbsp;&nbsp;'
            f'Model: {_badge(best_model, "blue")}'
            f'</div>',
            unsafe_allow_html=True,
        )

        payload: dict = {}
        # Render inputs in a 3-column grid
        col_chunks = [
            feature_columns[i : i + 3]
            for i in range(0, len(feature_columns), 3)
        ]
        for chunk in col_chunks:
            form_cols = st.columns(len(chunk), gap="medium")
            for fc, feature in zip(form_cols, chunk):
                with fc:
                    dtype = feature_types.get(feature, "text")
                    if dtype == "numeric":
                        payload[feature] = st.number_input(
                            feature, value=0.0, format="%.4f"
                        )
                    else:
                        payload[feature] = st.text_input(feature, "")

        submitted = st.form_submit_button(
            "▶ Run Prediction", use_container_width=True
        )

    if submitted:
        # Validate: no blank required fields
        blank_fields = [k for k, v in payload.items() if str(v).strip() == ""]
        if blank_fields:
            st.warning(
                f"Please fill in all fields before predicting. "
                f"Empty: {', '.join(blank_fields)}"
            )
        else:
            with st.spinner("Running prediction…"):
                try:
                    pred_resp = requests.post(
                        f"{BACKEND_URL}/predict", json=payload, timeout=15
                    )
                    if pred_resp.status_code == 200:
                        prediction = pred_resp.json()
                        pred_value = prediction.get("prediction", "—")
                        explanation = prediction.get("explanation", "")

                        st.markdown(
                            f"""
                            <div style="background:#1a3d2b;border:1px solid #3fb950;
                                        border-radius:10px;padding:1.25rem 1.5rem;
                                        margin-top:1rem;">
                                <div style="font-size:0.72rem;font-weight:600;
                                            color:#3fb950;text-transform:uppercase;
                                            letter-spacing:0.08em;margin-bottom:0.4rem;">
                                    Prediction Result
                                </div>
                                <div style="font-size:2rem;font-weight:800;
                                            color:#e6edf3;letter-spacing:-0.02em;">
                                    {pred_value}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if explanation:
                            st.markdown("<br>", unsafe_allow_html=True)
                            _card(f"<strong>Explanation</strong><br>{explanation}", "blue")
                    else:
                        st.error(
                            f"Prediction failed (HTTP {pred_resp.status_code}): "
                            f"{pred_resp.text}"
                        )
                except requests.exceptions.Timeout:
                    st.error("Prediction request timed out. The model may be warming up.")
                except requests.exceptions.ConnectionError:
                    st.error("Backend is unreachable. Check that the FastAPI server is running.")
                except Exception as e:
                    st.error(f"Unexpected error during prediction: {e}")
