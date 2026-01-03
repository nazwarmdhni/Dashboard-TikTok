import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Analisis Pengaruh Tren dan Influencer")
st.write("Studi pada Keputusan Belanja Remaja Putri di TikTok Shop")

uploaded_file = st.file_uploader("Upload file CSV kuesioner", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # =============================
    # AMBIL KOLOM TREN (5 PERTANYAAN)
    # =============================
    kolom_tren = df.iloc[:, [5, 6, 7, 8, 9]]
    kolom_tren = kolom_tren.apply(pd.to_numeric, errors="coerce")

    # =============================
    # AMBIL KOLOM INFLUENCER (5 PERTANYAAN)
    # =============================
    kolom_influencer = df.iloc[:, [10, 11, 12, 13, 14]]
    kolom_influencer = kolom_influencer.apply(pd.to_numeric, errors="coerce")

    # HITUNG RATA-RATA
    avg_tren = kolom_tren.mean().mean()
    avg_influencer = kolom_influencer.mean().mean()

    # TAMPILKAN METRIC
    st.subheader("Hasil Analisis")
    st.metric("Rata-rata Pengaruh Tren", round(avg_tren, 2))
    st.metric("Rata-rata Pengaruh Influencer", round(avg_influencer, 2))

    # =============================
    # VISUALISASI
    # =============================
    fig, ax = plt.subplots()
    ax.bar(["Tren", "Influencer"], [avg_tren, avg_influencer])
    ax.set_ylabel("Nilai Rata-rata")
    ax.set_title("Perbandingan Pengaruh Tren vs Influencer")

    st.pyplot(fig)

    # =============================
    # KESIMPULAN OTOMATIS
    # =============================
    st.subheader("Kesimpulan")
    if avg_tren > avg_influencer:
        st.success("Variabel Tren lebih berpengaruh terhadap keputusan belanja remaja putri di TikTok Shop.")
    else:
        st.success("Variabel Influencer lebih berpengaruh terhadap keputusan belanja remaja putri di TikTok Shop.")
