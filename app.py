import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Analisis Tren dan Influencer")
st.write("Perilaku Belanja Remaja Putri di TikTok Shop")

uploaded_file = st.file_uploader("Upload file CSV kuesioner", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # ===============================
    # ASUMSI POSISI KOLOM
    # ===============================
    # Fashion
    tren_fashion = df.iloc[:, 5:7].apply(pd.to_numeric, errors="coerce")
    influencer_fashion = df.iloc[:, 7:9].apply(pd.to_numeric, errors="coerce")

    # Make Up
    tren_makeup = df.iloc[:, 9:11].apply(pd.to_numeric, errors="coerce")
    influencer_makeup = df.iloc[:, 11:13].apply(pd.to_numeric, errors="coerce")

    # Hitung rata-rata
    avg_tren_fashion = tren_fashion.mean().mean()
    avg_influencer_fashion = influencer_fashion.mean().mean()

    avg_tren_makeup = tren_makeup.mean().mean()
    avg_influencer_makeup = influencer_makeup.mean().mean()

    # ===============================
    # METRIK
    # ===============================
    st.subheader("Rata-rata Pengaruh per Kategori Produk")

    col1, col2 = st.columns(2)
    col1.metric("Fashion - Tren", round(avg_tren_fashion, 2))
    col2.metric("Fashion - Influencer", round(avg_influencer_fashion, 2))

    col3, col4 = st.columns(2)
    col3.metric("Make Up - Tren", round(avg_tren_makeup, 2))
    col4.metric("Make Up - Influencer", round(avg_influencer_makeup, 2))

    # ===============================
    # GRAFIK
    # ===============================
    st.subheader("Perbandingan Pengaruh Tren vs Influencer")

    fig, ax = plt.subplots()
    labels = ["Fashion - Tren", "Fashion - Influencer", "Make Up - Tren", "Make Up - Influencer"]
    values = [
        avg_tren_fashion,
        avg_influencer_fashion,
        avg_tren_makeup,
        avg_influencer_makeup
    ]

    ax.bar(labels, values)
    ax.set_ylabel("Nilai Rata-rata")
    ax.set_title("Pengaruh Tren dan Influencer per Kategori Produk")
    plt.xticks(rotation=20)

    st.pyplot(fig)

    # ===============================
    # KESIMPULAN OTOMATIS
    # ===============================
    st.subheader("Kesimpulan Analisis")

    if avg_tren_fashion > avg_influencer_fashion:
        st.write("📌 Pada produk **Fashion**, responden cenderung lebih dipengaruhi oleh **Tren**.")
    else:
        st.write("📌 Pada produk **Fashion**, responden cenderung lebih dipengaruhi oleh **Influencer**.")

    if avg_tren_makeup > avg_influencer_makeup:
        st.write("💄 Pada produk **Make Up**, responden cenderung lebih dipengaruhi oleh **Tren**.")
    else:
        st.write("💄 Pada produk **Make Up**, responden cenderung lebih dipengaruhi oleh **Influencer**.")
