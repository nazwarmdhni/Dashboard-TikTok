import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Analisis Pengaruh Tren dan Influencer")
st.write("Keputusan Belanja Remaja Putri di TikTok Shop")

uploaded_file = st.file_uploader("Upload file CSV kuesioner", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("Contoh data:")
    st.dataframe(df.head())

    # Ambil kolom berdasarkan POSISI
    tren = df.iloc[:, [5, 6, 7, 8, 9]].apply(pd.to_numeric, errors="coerce")
    influencer = df.iloc[:, [10, 11, 12, 13, 14]].apply(pd.to_numeric, errors="coerce")

    avg_tren = tren.mean().mean()
    avg_influencer = influencer.mean().mean()

    st.subheader("Hasil Analisis")
    st.metric("Rata-rata Pengaruh Tren", round(avg_tren, 2))
    st.metric("Rata-rata Pengaruh Influencer", round(avg_influencer, 2))

    fig, ax = plt.subplots()
    ax.bar(["Tren", "Influencer"], [avg_tren, avg_influencer])
    ax.set_ylabel("Nilai Rata-rata")
    ax.set_title("Perbandingan Pengaruh Tren vs Influencer")

    st.pyplot(fig)

    st.subheader("Kesimpulan")
    if avg_tren > avg_influencer:
        st.success("Tren lebih berpengaruh terhadap keputusan belanja remaja putri.")
    else:
        st.success("Influencer lebih berpengaruh terhadap keputusan belanja remaja putri.")
