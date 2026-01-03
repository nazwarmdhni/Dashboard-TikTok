import streamlit as st
import pandas as pd

st.title("CEK STRUKTUR CSV")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Nama Kolom & Urutannya")
    for i, col in enumerate(df.columns):
        st.write(f"{i} : {col}")

    st.subheader("5 Baris Pertama")
    st.dataframe(df.head())
