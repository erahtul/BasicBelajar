import streamlit as st
import pandas as pd
import os
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import io

# Setup
st.set_page_config(page_title="Kas Kelas VII", layout="wide")

# Judul
st.markdown("<h2 style='text-align: center;'>SMPI Al HAYYAN</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Kas Ortu/Wali Kelas VII</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Tahun Ajaran 2024/2025</h4>", unsafe_allow_html=True)
st.markdown("---")

# Data
nama_siswa = [
    "Afiqah Naura R.", "Ahdani Nurrohmah", "Ahmad Haikal Zufar", "Ahmad Zaki Alghifari",
    "Annisa Mutia Azizah", "Aqilah Athaya Yuvita", "Aqila Qonita Mumtaza", "Bima Wahianto Sitepu",
    "Bryan Keama Huda", "Darrel Muhammad Ziqrillah", "Falya Azqya Nadheera", "Herjuno Caesar Ali",
    "Iksan Fahmi", "Kayla Julia Rahma", "Ladysha Qanita Wijaya", "Lakeisha Safilla Budiyanto",
    "Muhammad Athar Rafianza", "Muhammad Dimas Prasetyo", "Muhammad Kresna Akbar S.",
    "Muhammad Wijaya K.", "Najmi Al Irsyaq Nurhadi", "Rachel Kireina Axelle", "Ragil Albar Fahrezi",
    "Rizqi Heriansyah", "Ruby Aqilah A.", "Salsabila Putri Kurniawan", "Yuko Haadi Pratama"
]

bulan = ["Juli", "Agustus", "September", "Oktober", "November", "Desember",
         "Januari", "Febuari", "Maret", "April", "Mei", "Juni"]

# File penyimpanan
DATA_FILE = "kas_data.xlsx"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE, index_col=0)
    else:
        return pd.DataFrame(index=bulan, columns=nama_siswa).fillna("")

# Simpan data
def save_data(df):
    df.to_excel(DATA_FILE)

# Inisialisasi data
if "data_siswa" not in st.session_state:
    st.session_state.data_siswa = load_data()

# Layout input
st.markdown("### 🔄 Input Data Kas")
selected_bulan = st.selectbox("Pilih Bulan", bulan, index=0)
st.markdown(f"#### 📅 Input untuk Bulan **{selected_bulan}**")

with st.form("form_kas"):
    for siswa in nama_siswa:
        col1, col2 = st.columns([2, 3])
        with col1:
            status = st.radio(f"{siswa}", ["Belum", "Lunas", "Sebagian"], key=f"{siswa}_status")
        with col2:
            if status == "Sebagian":
                nominal = st.text_input("Nominal", value=str(st.session_state.data_siswa.loc[selected_bulan, siswa]), key=f"{siswa}_nominal")
                st.session_state.data_siswa.loc[selected_bulan, siswa] = nominal
            elif status == "Lunas":
                st.session_state.data_siswa.loc[selected_bulan, siswa] = "TRUE"
            else:
                st.session_state.data_siswa.loc[selected_bulan, siswa] = ""
    submitted = st.form_submit_button("💾 Simpan Data")
    if submitted:
        save_data(st.session_state.data_siswa)
        st.success("Data berhasil disimpan!")

# Rekap Kas
st.markdown("---")
st.markdown("### 📊 Rekap Kas Kelas")
df_display = st.session_state.data_siswa.T
st.dataframe(df_display, use_container_width=True, height=600)

# Fungsi gambar
def dataframe_to_image(df):
    df_vis = df.fillna("").astype(str)
    n_rows, n_cols = df_vis.shape_
