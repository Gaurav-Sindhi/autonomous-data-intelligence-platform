"""
history.py — ADI Platform
Displays past training runs fetched from the backend.
"""

import streamlit as st
import pandas as pd
from utils.api import get_history

st.markdown(
    """
    <div style="margin-bottom:0.25rem;">
        <span style="font-size:0.72rem;font-weight:600;color:#58a6ff;
                     letter-spacing:0.1em;text-transform:uppercase;">
            Training Records
        </span>
    </div>
    <h2 style="font-size:1.75rem;font-weight:800;color:#e6edf3;
               letter-spacing:-0.02em;margin:0 0 0.4rem 0;">
        Training History
    </h2>
    <p style="font-size:0.875rem;color:#8b949e;margin:0 0 1.5rem 0;">
        A log of every AutoML run performed on this platform.
    </p>
    <hr style="border:none;border-top:1px solid #21262d;margin:0 0 1.5rem 0;">
    """,
    unsafe_allow_html=True,
)

with st.spinner("Loading history…"):
    try:
        response = get_history()
    except Exception as e:
        st.error(f"Could not reach backend: {e}")
        st.stop()

if response.status_code != 200:
    st.error(f"Backend returned {response.status_code}. History unavailable.")
    st.stop()

try:
    history = response.json()
except Exception:
    st.error("Could not parse history response.")
    st.stop()

if not history:
    st.markdown(
        """
        <div style="background:#161b22;border:1px solid #21262d;border-radius:10px;
                    padding:3rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:0.75rem;">📭</div>
            <div style="font-size:0.95rem;font-weight:600;color:#e6edf3;
                        margin-bottom:0.4rem;">No history yet</div>
            <div style="font-size:0.82rem;color:#8b949e;">
                Upload and analyse a dataset on the Dashboard to create your first record.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ── Build dataframe ──
records = []
for item in history:
    records.append(
        {
            "Timestamp": item.get("timestamp", "—"),
            "Dataset": item.get("dataset_name", "—"),
            "Problem Type": item.get("problem_type", "—"),
            "Target Column": item.get("target_column", "—"),
            "Best Model": item.get("best_model", "—"),
            "Best Score": round(float(item.get("best_score", 0)), 4)
            if item.get("best_score") is not None
            else "—",
        }
    )

history_df = pd.DataFrame(records)

# ── Summary strip ──
col1, col2, col3 = st.columns(3, gap="medium")
col1.metric("Total Runs", len(history_df))
if "Best Score" in history_df.columns:
    numeric_scores = pd.to_numeric(history_df["Best Score"], errors="coerce")
    col2.metric("Avg Best Score", f"{numeric_scores.mean():.4f}" if not numeric_scores.isna().all() else "—")
if "Best Model" in history_df.columns:
    top_model = history_df["Best Model"].mode()
    col3.metric("Most Frequent Model", top_model.iloc[0] if not top_model.empty else "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── Search / filter ──
search = st.text_input(
    "Filter runs",
    placeholder="Search by dataset name, model, or problem type…",
    label_visibility="collapsed",
)

if search.strip():
    mask = history_df.apply(
        lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1
    )
    display_df = history_df[mask]
else:
    display_df = history_df

if display_df.empty:
    st.info(f'No runs match "{search}".')
else:
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Showing {len(display_df)} of {len(history_df)} records.")
