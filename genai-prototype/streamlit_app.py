# import packages
import streamlit as st
import pandas as pd
import re
import os
import string


def clean_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    # Strip leading and trailing whitespace
    text = text.strip()
    return text

# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "data", "customer_reviews.csv")
    return csv_path


st.title("Hello, GenAI!")
st.write("This is your GenAI-powered data processing app.")

# layout two buttons side by side
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Ingest dataset"):
        try:
            csv_path = get_dataset_path()
            st.session_state['df'] = pd.read_csv(csv_path)
            st.success("Dataset loaded successfully!")
        except FileNotFoundError:
            st.error("Dataset not found. Please check the file path.")

with col2:
    if st.button("🧹 Parse reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest the dataset first.")

# display the dataset if it exists
if "df" in st.session_state:
    # Product filter dropdown
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
    st.subheader(f"📁 Reviews for {product}")

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df)

    st.subheader("Sentiment Score by Product")
    grouped = st.session_state["df"].groupby("PRODUCT")["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)
    

        