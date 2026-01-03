import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard TikTok Shop", layout="wide")

st.title("📊 Dashboard Analisis Tren vs Influencer")
st.write("Analisis Perilaku Belanja Remaja Putri berdasarkan Data Kuesioner")

uploaded_file = st.file_uploader("Upload file CSV kuesioner", type=["csv"])

if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file)
    
    # Bersihkan nama kolom (menghapus spasi jika ada)
    df.columns = df.columns.str.strip()

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # ===============================
    # PEMETAAN KOLOM (Berdasarkan File Anda)
    # ===============================
    # Kolom 5-8 adalah Tren, Kolom 9-12 adalah Influencer
    kolom_tren = df.columns[5:9] 
    kolom_influencer = df.columns[9:13]
    kolom_kategori = df.columns[3] # Kolom 'Kategori Produk yang sering dibeli'

    # Konversi ke numerik untuk memastikan perhitungan aman
    for col in list(kolom_tren) + list(kolom_influencer):
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # ===============================
    # PERHITUNGAN RATA-RATA PER KATEGORI
    # ===============================
    
    def get_avg_metrics(category_name):
        subset = df[df[kolom_kategori] == category_name]
        avg_tren = subset[kolom_tren].mean().mean()
        avg_influ = subset[kolom_influencer].mean().mean()
        return avg_tren, avg_influ

    # Ambil list kategori unik (Fashion, Make Up, Skincare)
    list_kategori = df[kolom_kategori].unique()

    st.subheader("Rata-rata Pengaruh per Kategori")
    
    metrics_data = []
    
    # Menampilkan metrik secara dinamis
    cols = st.columns(len(list_kategori))
    for i, kat in enumerate(list_kategori):
        t_avg, i_avg = get_avg_metrics(kat)
        metrics_data.append({"Kategori": kat, "Tren": t_avg, "Influencer": i_avg})
        
        with cols[i]:
            st.info(f"**{kat}**")
            st.metric("Skor Tren", round(t_avg, 2))
            st.metric("Skor Influencer", round(i_avg, 2))

    # ===============================
    # VISUALISASI
    # ===============================
    st.divider()
    st.subheader("Grafik Perbandingan Tren vs Influencer")

    plot_df = pd.DataFrame(metrics_data).set_index("Kategori")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_df.plot(kind="bar", ax=ax, color=['#ff9999','#66b3ff'])
    
    ax.set_ylabel("Skala Likert (1-5)")
    ax.set_title("Mana yang lebih berpengaruh?")
    plt.xticks(rotation=0)
    plt.legend(loc="upper right")
    
    st.pyplot(fig)

    # ===============================
    # KESIMPULAN DINAMIS
    # ===============================
    st.subheader("📌 Kesimpulan Analisis")
    for data in metrics_data:
        pemenang = "Tren" if data['Tren'] > data['Influencer'] else "Influencer"
        st.write(f"Untuk kategori **{data['Kategori']}**, pembeli lebih cenderung dipengaruhi oleh **{pemenang}**.")

else:
    st.warning("Silakan upload file CSV untuk melihat hasil analisis.")
