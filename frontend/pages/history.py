import streamlit as st
import pandas as pd

from utils.api import (
    get_history
)

st.title("📜 Training History")

response = get_history()

if response.status_code == 200:

    history = response.json()

    if history:

        records = []

        for item in history:

            records.append({

                "Date":
                    item["timestamp"],

                "Best Model":
                    item["best_model"],

                "Problem Type":
                    item["problem_type"],

                "Target":
                    item["target_column"]
            })

        history_df = pd.DataFrame(
            records
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

    else:

        st.info(
            "No history available."
        )