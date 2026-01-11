import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Analisis TikTok Shop",
    layout="wide"
)

st.title("Dashboard Analisis Pengaruh Tren dan Influencer")
st.subheader("Keputusan Belanja Remaja Putri di TikTok Shop")
st.markdown("---")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader(
    "Upload File CSV Kuesioner",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Data berhasil diunggah")

    # =========================
    # RENAME KOLOM AGAR JELAS
    # =========================
    df = df.rename(columns={
        df.columns[3]: "produk"
    })

    # =========================
    # HITUNG SKOR VARIABEL
    # =========================
    tren_cols = df.columns[5:10]        # kolom 5–5.4
    influencer_cols = df.columns[10:15] # kolom 6–6.4
    keputusan_cols = df.columns[15:18]  # kolom 7–7.2

    df["tren"] = df[tren_cols].mean(axis=1)
    df["influencer"] = df[influencer_cols].mean(axis=1)
    df["keputusan_belanja"] = df[keputusan_cols].mean(axis=1)

    # =========================
    # TAMPILKAN DATA OLAHAN
    # =========================
    st.subheader("Data Setelah Pengolahan")
    st.dataframe(df[["produk", "tren", "influencer", "keputusan_belanja"]])

    st.markdown("---")

    # =========================
    # REGRESI LINIER BERGANDA (KESELURUHAN)
    # =========================
    st.subheader("Regresi Linier Berganda (Keseluruhan Data)")

    X = df[["tren", "influencer"]]
    Y = df["keputusan_belanja"]

    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()

    st.text(model.summary())

    coef = model.params.drop("const")

    fig, ax = plt.subplots()
    coef.plot(kind="bar", ax=ax)
    ax.set_title("Perbandingan Pengaruh Tren dan Influencer")
    ax.set_ylabel("Koefisien Regresi")
    st.pyplot(fig)

    if coef["tren"] > coef["influencer"]:
        st.success("Secara keseluruhan, TREN lebih dominan memengaruhi keputusan belanja.")
    else:
        st.success("Secara keseluruhan, INFLUENCER lebih dominan memengaruhi keputusan belanja.")

    st.markdown("---")

    # =========================
    # REGRESI PER PRODUK
    # =========================
    st.subheader("Analisis Regresi Berdasarkan Jenis Produk")

    for p in df["produk"].unique():
        st.markdown(f"### Produk: {p}")

        df_p = df[df["produk"] == p]

        Xp = df_p[["tren", "influencer"]]
        Yp = df_p["keputusan_belanja"]

        Xp = sm.add_constant(Xp)
        model_p = sm.OLS(Yp, Xp).fit()

        coef_p = model_p.params.drop("const")

        st.dataframe(coef_p)

        fig, ax = plt.subplots()
        coef_p.plot(kind="bar", ax=ax)
        ax.set_title(f"Pengaruh Tren vs Influencer ({p})")
        ax.set_ylabel("Koefisien Regresi")
        st.pyplot(fig)

        if coef_p["tren"] > coef_p["influencer"]:
            st.success(f"Produk {p} lebih dominan dipengaruhi oleh TREN.")
        else:
            st.success(f"Produk {p} lebih dominan dipengaruhi oleh INFLUENCER.")

        st.markdown("---")

