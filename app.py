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

bulan = ["Juli", "Agustus", "September", "Oktober", "November", "Desember", "Januari", "Febuari", "Maret", "April", "Mei", "Juni"]

DATA_FILE = "data_kas.csv"

# Fungsi simpan dan load
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, index_col=0)
    else:
        df = pd.DataFrame(index=bulan, columns=nama_siswa)
        return df.fillna("")

def save_data(df):
    df.to_csv(DATA_FILE)

# Inisialisasi session state
if "data_siswa" not in st.session_state:
    st.session_state.data_siswa = load_data()

# Layout input
st.markdown("### 🔄 Input Data Kas")
selected_bulan = st.selectbox("Pilih Bulan", bulan, index=0)
st.markdown(f"#### 📅 Input untuk Bulan **{selected_bulan}**")

col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    for siswa in nama_siswa:
        pilihan = st.radio(
            label=siswa,
            options=["Belum Bayar", "Sudah (True)", "Sebagian (isi nominal)"],
            key=f"opsi_{selected_bulan}_{siswa}",
            horizontal=True
        )
        if pilihan == "Sudah (True)":
            st.session_state.data_siswa.loc[selected_bulan, siswa] = "TRUE"
        elif pilihan == "Sebagian (isi nominal)":
            nominal = st.text_input(f"Nominal untuk {siswa}", key=f"nominal_{selected_bulan}_{siswa}")
            st.session_state.data_siswa.loc[selected_bulan, siswa] = nominal
        else:
            st.session_state.data_siswa.loc[selected_bulan, siswa] = ""

# Tombol Simpan
if st.button("💾 Simpan Data"):
    save_data(st.session_state.data_siswa)
    st.success("Data berhasil disimpan!")

# Tampilkan tabel rekap
st.markdown("---")
st.markdown("### 📊 Rekap Kas Kelas")
df_display = st.session_state.data_siswa.T
st.dataframe(df_display, use_container_width=True, height=600)

# Download gambar
def dataframe_to_image(df):
    df_vis = df.fillna("").astype(str)
    n_rows, n_cols = df_vis.shape
    fig, ax = plt.subplots(figsize=(1.5 + n_cols, 0.4 + n_rows * 0.4))

    def cell_color(val):
        if val.upper() == "TRUE":
            return "#d4edda"
        elif val.strip().isdigit() or val.replace('.', '', 1).isdigit():
            return "#cce5ff"
        else:
            return "#ffffff"

    cell_colors = [[cell_color(val) for val in row] for row in df_vis.values]

    table = ax.table(cellText=df_vis.values,
                     rowLabels=df_vis.index,
                     colLabels=df_vis.columns,
                     cellColours=cell_colors,
                     loc='center',
                     cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)
    ax.axis('off')
    plt.title("Rekap Kas Kelas VII SMPI Al-HAYYAN", fontsize=14, weight='bold', pad=20)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    plt.close()
    buf.seek(0)
    return buf

img_buf = dataframe_to_image(df_display)
st.image(img_buf, caption="Rekap Kas Kelas (Gambar)")

st.download_button(
    label="🖼️ Download Rekap Kas sebagai Gambar (PNG)",
    data=img_buf,
    file_name="rekap_kas_kelas_vii.png",
    mime="image/png"
)

# Download Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True, sheet_name='Kas Siswa')
    return output.getvalue()

excel_data = to_excel(df_display)
st.download_button(
    label="📥 Download sebagai Excel",
    data=excel_data,
    file_name='kas_kelas_vii_smpi_alhayyan.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
