import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# JUDUL DASHBOARD
# =============================
st.title("Dashboard Analisis Pengaruh Tren dan Influencer")
st.subheader("Perilaku Belanja Remaja Putri di TikTok Shop")

st.write("Dashboard ini bertujuan untuk mengetahui faktor yang lebih "
         "berpengaruh antara tren dan influencer terhadap keputusan belanja.")

# =============================
# LOAD DATA
# =============================
data = pd.read_csv("data_kuesioner_likert_numerik.csv")

st.write("Jumlah responden:", len(data))

# =============================
# PILIH KATEGORI PRODUK
# =============================
kategori = st.selectbox(
    "Pilih kategori produk:",
    ["Fashion", "Make Up", "Skincare"]
)

# =============================
# HITUNG RATA-RATA SKOR
# =============================
tren_cols = [col for col in data.columns if "Tren" in col and kategori in col]
influencer_cols = [col for col in data.columns if "Influencer" in col and kategori in col]

tren_mean = data[tren_cols].mean().mean()
influencer_mean = data[influencer_cols].mean().mean()

# =============================
# TAMPILKAN HASIL
# =============================
st.write("### Rata-rata Pengaruh")
st.write("Pengaruh Tren:", round(tren_mean, 2))
st.write("Pengaruh Influencer:", round(influencer_mean, 2))

# =============================
# GRAFIK PERBANDINGAN
# =============================
fig, ax = plt.subplots()
ax.bar(["Tren", "Influencer"], [tren_mean, influencer_mean])
ax.set_ylabel("Skor Rata-rata")
ax.set_title("Perbandingan Pengaruh Tren dan Influencer")

st.pyplot(fig)

# =============================
# KESIMPULAN SEDERHANA
# =============================
if tren_mean > influencer_mean:
    st.success("Kesimpulan: Tren lebih berpengaruh terhadap keputusan belanja.")
else:
    st.success("Kesimpulan: Influencer lebih berpengaruh terhadap keputusan belanja.")

