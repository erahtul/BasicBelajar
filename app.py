import streamlit as st
import pandas as pd
from io import BytesIO

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

# Inisialisasi session state
if "data_siswa" not in st.session_state:
    st.session_state.data_siswa = pd.DataFrame(index=bulan, columns=nama_siswa)
    st.session_state.data_siswa.fillna("", inplace=True)

# Layout input
st.markdown("### 🔄 Input Data Kas")
selected_bulan = st.selectbox("Pilih Bulan", bulan, index=0)
st.markdown(f"#### 📅 Input untuk Bulan **{selected_bulan}**")

st.markdown("#### 🧾 Formulir Input Kas")
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

    with col_status:
        status = st.selectbox(
            label="",
            options=["Belum Bayar", "Sudah Bayar", "Bayar Sebagian"],
            key=key_status
        )

    with col_nominal:
        if status == "Bayar Sebagian":
            nominal = st.text_input(label="", key=key_nominal)
            if nominal.strip().isdigit() or nominal.replace('.', '', 1).isdigit():
                st.session_state.data_siswa.loc[selected_bulan, siswa] = nominal.strip()
            else:
                st.warning(f"Nominal tidak valid untuk: {siswa}")
        elif status == "Sudah Bayar":
            st.session_state.data_siswa.loc[selected_bulan, siswa] = "TRUE"
        else:
            st.session_state.data_siswa.loc[selected_bulan, siswa] = ""

# Rekap dan Tabel
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io

# Fungsi untuk membuat gambar dari DataFrame
def dataframe_to_image(df):
    plt.figure(figsize=(20, len(df) * 0.5))
    sns.set(font_scale=0.8)
    sns.heatmap(df.isna(), cbar=False, cmap='Greys', linewidths=0.5, linecolor='gray')  # hanya untuk garis
    plt.title("Rekap Kas Kelas", fontsize=16)
    plt.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    plt.close()
    buf.seek(0)
    return buf

# Buat gambar dari DataFrame
st.markdown("---")
st.markdown("### 📊 Rekap Kas Kelas")
df_display = st.session_state.data_siswa.T  # Transpose supaya nama siswa di kiri
st.dataframe(df_display, use_container_width=True, height=600)

import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io

# Fungsi untuk membuat gambar dari DataFrame
def dataframe_to_image(df):
    # Menyalin dataframe agar tidak mengubah aslinya
    df_vis = df.copy()

    # Konversi ke string agar seaborn bisa menampilkannya sebagai teks
    df_vis = df_vis.fillna("").astype(str)

    # Ukuran gambar dinamis tergantung banyaknya siswa dan bulan
    n_rows, n_cols = df_vis.shape
    fig, ax = plt.subplots(figsize=(1.5 + n_cols, 0.4 + n_rows * 0.4))

    # Warna latar berdasarkan isi sel
    def cell_color(val):
        if val.upper() == "TRUE":
            return "#d4edda"  # hijau muda
        elif val.strip().isdigit() or val.replace('.', '', 1).isdigit():
            return "#cce5ff"  # biru muda
        else:
            return "#ffffff"  # putih

    # Buat grid berwarna
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

    # Simpan ke buffer gambar
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    plt.close()
    buf.seek(0)
    return buf

# Buat gambar dari DataFrame
img_buf = dataframe_to_image(df_display)

# Tampilkan gambar di Streamlit
st.image(img_buf, caption="Rekap Kas Kelas (Gambar)")

# Tombol download gambar
st.download_button(
    label="🖼️ Download Rekap Kas sebagai Gambar (PNG)",
    data=img_buf,
    file_name="rekap_kas_kelas_vii.png",
    mime="image/png"
)

# Download sebagai Excel
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