import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="ADI Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main Background */

.stApp{
    background:#EEF5FB;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* Remove Streamlit Padding */

.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* KPI Cards */

.kpi-card{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 6px 25px rgba(0,0,0,0.08);
    transition:0.3s;
}

.kpi-card:hover{
    transform:translateY(-5px);
}

/* Header Card */

.header-card{
    background:white;
    border-radius:24px;
    padding:25px;
    box-shadow:0px 6px 25px rgba(0,0,0,0.08);
}

/* Sidebar Title */

.logo{
    font-size:40px;
    font-weight:700;
    color:#06B6D4;
}

.logo-sub{
    color:#64748B;
    font-size:14px;
}

/* Welcome */

.welcome{
    font-size:32px;
    font-weight:700;
    color:#0F172A;
}

.welcome-sub{
    color:#64748B;
}

/* Circle */

.circle-green{
    width:90px;
    height:90px;
    border-radius:50%;
    border:8px solid #22C55E;
    display:flex;
    justify-content:center;
    align-items:center;
    font-weight:700;
    font-size:22px;
}

.circle-blue{
    width:90px;
    height:90px;
    border-radius:50%;
    border:8px solid #0EA5E9;
    display:flex;
    justify-content:center;
    align-items:center;
    font-weight:700;
    font-size:22px;
}

.circle-orange{
    width:90px;
    height:90px;
    border-radius:50%;
    border:8px solid #F59E0B;
    display:flex;
    justify-content:center;
    align-items:center;
    font-weight:700;
    font-size:22px;
}

.circle-purple{
    width:90px;
    height:90px;
    border-radius:50%;
    border:8px solid #A855F7;
    display:flex;
    justify-content:center;
    align-items:center;
    font-weight:700;
    font-size:22px;
}

.metric-number{
    font-size:32px;
    font-weight:700;
    color:#111827;
}

.metric-label{
    color:#64748B;
}
            
.upload-card{
    background:white;
    border-radius:24px;
    padding:25px;
    min-height:420px;
    box-shadow:0px 6px 25px rgba(0,0,0,0.08);
}

.summary-card{
    background:white;
    border-radius:24px;
    padding:25px;
    min-height:420px;
    box-shadow:0px 6px 25px rgba(0,0,0,0.08);
}

.leaderboard-card{
    background:white;
    border-radius:24px;
    padding:25px;
    min-height:420px;
    box-shadow:0px 6px 25px rgba(0,0,0,0.08);
}

.card-title{
    font-size:24px;
    font-weight:600;
    margin-bottom:20px;
    color:#111827;
}

.summary-item{
    padding:10px 0;
    border-bottom:1px solid #E5E7EB;
}

.summary-label{
    color:#64748B;
}

.summary-value{
    float:right;
    font-weight:600;
    color:#111827;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        """
        <div class='logo'>ADI</div>
        <div class='logo-sub'>
        Autonomous Data Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Dataset Upload",
            "Model Training",
            "Visual Analytics",
            "Predictions",
            "History"
        ],
        icons=[
            "grid",
            "cloud-upload",
            "cpu",
            "bar-chart",
            "graph-up",
            "clock-history"
        ],
        default_index=0
    )

# ==========================================
# HEADER
# ==========================================

st.markdown(
"""
<div class='header-card'>

<div class='welcome'>
Welcome back, Data Scientist 👋
</div>

<div class='welcome-sub'>
Upload data, train models and generate intelligent insights.
</div>

</div>
""",
unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# KPI SECTION
# ==========================================

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.markdown(
    """
    <div class='kpi-card'>

    <div class='circle-green'>
    100%
    </div>

    <br>

    <div class='metric-label'>
    Rows
    </div>

    <div class='metric-number'>
    12,450
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

with c2:

    st.markdown(
    """
    <div class='kpi-card'>

    <div class='circle-blue'>
    100%
    </div>

    <br>

    <div class='metric-label'>
    Columns
    </div>

    <div class='metric-number'>
    28
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

with c3:

    st.markdown(
    """
    <div class='kpi-card'>

    <div class='circle-orange'>
    2%
    </div>

    <br>

    <div class='metric-label'>
    Missing Values
    </div>

    <div class='metric-number'>
    236
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

with c4:

    st.markdown(
    """
    <div class='kpi-card'>

    <div class='circle-purple'>
    0.4%
    </div>

    <br>

    <div class='metric-label'>
    Duplicate Rows
    </div>

    <div class='metric-number'>
    56
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

left, middle, right = st.columns([1.2, 1.8, 1.1])

# =====================================
# UPLOAD PANEL
# =====================================

with left:

    st.markdown(
    """
    <div class='upload-card'>

    <div class='card-title'>
    📂 Upload Dataset
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "",
        type=["csv"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

# =====================================
# LEADERBOARD
# =====================================

with middle:

    st.markdown(
    """
    <div class='leaderboard-card'>
    <div class='card-title'>
    🏆 Model Leaderboard
    </div>
    </div>
    """,
    unsafe_allow_html=True
    )

    leaderboard_df = pd.DataFrame({
        "Model":[
            "Random Forest",
            "XGBoost",
            "Linear Regression",
            "Ridge Regression"
        ],
        "Type":[
            "Regression",
            "Regression",
            "Regression",
            "Regression"
        ],
        "Score":[
            0.932,
            0.918,
            0.782,
            0.742
        ]
    })

    st.dataframe(
        leaderboard_df,
        use_container_width=True,
        hide_index=True
    )

# =====================================
# SUMMARY
# =====================================

with right:

    st.markdown(
    """
    <div class='summary-card'>

    <div class='card-title'>
    📊 Dataset Summary
    </div>

    <div class='summary-item'>
        <span class='summary-label'>Target Column</span>
        <span class='summary-value'>Salary</span>
    </div>

    <div class='summary-item'>
        <span class='summary-label'>Problem Type</span>
        <span class='summary-value'>Regression</span>
    </div>

    <div class='summary-item'>
        <span class='summary-label'>Numerical Features</span>
        <span class='summary-value'>12</span>
    </div>

    <div class='summary-item'>
        <span class='summary-label'>Categorical Features</span>
        <span class='summary-value'>16</span>
    </div>

    <div class='summary-item'>
        <span class='summary-label'>Correlation Strength</span>
        <span class='summary-value'>0.72</span>
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

left_panel, right_panel = st.columns([1.2, 1.3])

# =====================================
# FEATURE IMPORTANCE
# =====================================

with left_panel:

    st.markdown(
        """
        <div class='card-title'>
        📈 Feature Importance
        </div>
        """,
        unsafe_allow_html=True
    )

    feature_df = pd.DataFrame({
        "Feature":[
            "experience",
            "age",
            "education",
            "skills",
            "city",
            "department",
            "bonus",
            "tenure"
        ],
        "Importance":[
            0.88,
            0.73,
            0.57,
            0.43,
            0.36,
            0.25,
            0.18,
            0.12
        ]
    })

    fig = px.bar(
        feature_df,
        x="Feature",
        y="Importance"
    )

    fig.update_layout(
        height=400,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# CORRELATION HEATMAP
# =====================================

with right_panel:

    st.markdown(
        """
        <div class='card-title'>
        🔥 Correlation Heatmap
        </div>
        """,
        unsafe_allow_html=True
    )

    corr_matrix = np.array([
        [1.0,0.64,0.21,0.31,0.62],
        [0.64,1.0,0.18,0.45,0.71],
        [0.21,0.18,1.0,0.29,0.35],
        [0.31,0.45,0.29,1.0,0.66],
        [0.62,0.71,0.35,0.66,1.0]
    ])

    labels = [
        "age",
        "experience",
        "education",
        "skills",
        "salary"
    ]

    heatmap = go.Figure(
        data=go.Heatmap(
            z=corr_matrix,
            x=labels,
            y=labels
        )
    )

    heatmap.update_layout(
        height=400,
        paper_bgcolor="white"
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🕒 Recent Activity")

a1,a2,a3 = st.columns(3)

a1.success(
    "Dataset uploaded\n\n2 mins ago"
)

a2.success(
    "Model training completed\n\n5 mins ago"
)

a3.success(
    "Visualizations generated\n\n7 mins ago"
)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("⚡ System Performance")

cpu = 23
ram = 45

c1,c2 = st.columns(2)

c1.metric(
    "CPU Usage",
    f"{cpu}%"
)

c2.metric(
    "RAM Usage",
    f"{ram}%"
)
st.info(
    "✅ Part 1 Complete - Sidebar, Header and KPI Dashboard"
)