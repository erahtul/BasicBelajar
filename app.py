import streamlit as st
import pandas as pd
from io import BytesIO
import os
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io

# Setup
st.set_page_config(page_title="Kas Kelas VII", layout="wide")

# Welcome Header
st.markdown("<h1 style='text-align: center;'>Welcome to My Application</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Created by Bang Imat</p>", unsafe_allow_html=True)

# Judul
st.markdown("<h2 style='text-align: center;'>SMPI Al HAYYAN</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Kas Ortu/Wali Kelas VII</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Tahun Ajaran 2024/2025</h4>", unsafe_allow_html=True)
st.markdown("---")

# Data setup
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

DATA_FILE = "kas_data.xlsx"
PENGELUARAN_FILE = "pengeluaran_data.xlsx"

# Nominal pilihan
nominal_values = list(range(5000, 50001, 5000))
nominal_display = [f"Rp {x:,}".replace(",", ".") for x in nominal_values]
nominal_mapping = dict(zip(nominal_display, nominal_values))

# Load or initialize data
if os.path.exists(DATA_FILE):
    df_kas = pd.read_excel(DATA_FILE, index_col=0)
else:
    df_kas = pd.DataFrame(index=bulan, columns=nama_siswa).fillna("")

if os.path.exists(PENGELUARAN_FILE):
    df_pengeluaran = pd.read_excel(PENGELUARAN_FILE)
else:
    df_pengeluaran = pd.DataFrame(columns=["Bulan", "Keterangan", "Nominal"])

# Layout input
st.markdown("### 🔄 Input Data Kas")
selected_bulan = st.selectbox("Pilih Bulan", bulan, index=0)
st.markdown(f"#### 🗓️ Input untuk Bulan **{selected_bulan}**")

st.markdown("#### 🧲 Formulir Input Kas")
st.write("Silakan isi status kas masing-masing siswa di bawah ini:")

# Header Tabel
col_nama, col_status, col_nominal = st.columns([3, 2, 2])
with col_nama:
    st.markdown("**Nama Siswa**")
with col_status:
    st.markdown("**Status**")
with col_nominal:
    st.markdown("**Nominal**")

# Loop input per siswa
for siswa in nama_siswa:
    col_nama, col_status, col_nominal = st.columns([3, 2, 2])

    with col_nama:
        st.markdown(siswa)

    key_status = f"{selected_bulan}_{siswa}_status"
    key_nominal = f"{selected_bulan}_{siswa}_nominal"

    previous_value = df_kas.at[selected_bulan, siswa]
    if previous_value == "TRUE":
        default_option = "Sudah Bayar"
        previous_nominal = "0"
    elif str(previous_value).strip().isdigit():
        default_option = "Bayar Sebagian"
        previous_nominal = str(previous_value)
    else:
        default_option = "Belum Bayar"
        previous_nominal = ""

    with col_status:
        status = st.selectbox(
            label="",
            options=["Belum Bayar", "Sudah Bayar", "Bayar Sebagian"],
            index=["Belum Bayar", "Sudah Bayar", "Bayar Sebagian"].index(default_option),
            key=key_status
        )

    with col_nominal:
        if status in ["Sudah Bayar", "Bayar Sebagian"]:
            default_nominal = f"Rp {int(previous_nominal):,}".replace(",", ".") if previous_nominal.isdigit() else nominal_display[0]
            nominal = st.selectbox(
                label="",
                options=[""] + nominal_display,
                index=(nominal_display.index(default_nominal) + 1) if default_nominal in nominal_display else 0,
                key=key_nominal
            )
        else:
            nominal = ""

    if status == "Belum Bayar":
        df_kas.at[selected_bulan, siswa] = ""
    elif status == "Sudah Bayar":
        df_kas.at[selected_bulan, siswa] = "TRUE"
    else:
        if nominal and nominal in nominal_mapping:
            df_kas.at[selected_bulan, siswa] = str(nominal_mapping[nominal])
        else:
            df_kas.at[selected_bulan, siswa] = ""

# Auto save setelah input kas
df_kas.to_excel(DATA_FILE)
st.success("✅ Data kas siswa otomatis tersimpan.")

# Input pengeluaran
st.header("💸 Input Pengeluaran")
st.markdown("Masukkan pengeluaran untuk bulan ini:")

with st.form("form_pengeluaran"):
    col1, col2 = st.columns(2)
    with col1:
        keterangan = st.text_input("Keterangan")
    with col2:
        nominal_pengeluaran_display = st.selectbox("Nominal", nominal_display)
        nominal_pengeluaran = nominal_mapping[nominal_pengeluaran_display] if nominal_pengeluaran_display else 0

    submitted = st.form_submit_button("Simpan Pengeluaran")

    if submitted and keterangan and nominal_pengeluaran > 0:
        new_row = {"Bulan": selected_bulan, "Keterangan": keterangan, "Nominal": int(nominal_pengeluaran)}
        df_pengeluaran = pd.concat([df_pengeluaran, pd.DataFrame([new_row])], ignore_index=True)
        df_pengeluaran.to_excel(PENGELUARAN_FILE, index=False)
        st.success("Pengeluaran berhasil disimpan!")

# Rekap kas
st.header("📊 Rekap Kas")
df_display = df_kas.T
st.dataframe(df_display, use_container_width=True, height=600)

# Rekap Total
st.header("💰 Total Rekapitulasi")
total_masuk = 0
for val in df_kas.values.flatten():
    if isinstance(val, str) and val.upper() == "TRUE":
        total_masuk += 10000
    elif str(val).strip().isdigit() or str(val).replace('.', '', 1).isdigit():
        total_masuk += int(float(val))

total_pengeluaran = df_pengeluaran[df_pengeluaran['Bulan'] == selected_bulan]['Nominal'].sum()
sisa_kas = total_masuk - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Kas Masuk", f"Rp {total_masuk:,}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,}")
col3.metric("Sisa Kas", f"Rp {sisa_kas:,}")
