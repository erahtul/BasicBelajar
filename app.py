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

# Selamat Datang
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1 style="color:#4CAF50;">Welcome My Application</h1>
    <p style="font-size:14px; color:gray;">Created by <b>Bang Imat</b></p>
</div>
""", unsafe_allow_html=True)

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

# Load or initialize data
if os.path.exists(DATA_FILE):
    df_kas = pd.read_excel(DATA_FILE, index_col=0)
else:
    df_kas = pd.DataFrame(index=bulan, columns=nama_siswa).fillna("")

# Load or initialize pengeluaran data
if os.path.exists(PENGELUARAN_FILE):
    df_pengeluaran = pd.read_excel(PENGELUARAN_FILE)
else:
    df_pengeluaran = pd.DataFrame(columns=["Bulan", "Keterangan", "Nominal"])

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

    # Mengambil nilai sebelumnya dari DataFrame
    previous_value = df_kas.at[selected_bulan, siswa]

    # Menentukan default option dan previous nominal berdasarkan previous_value
    if previous_value == "TRUE":
        default_option = "Sudah Bayar"
        previous_nominal = "0"
    elif isinstance(previous_value, (int, float)):  # Cek jika previous_value adalah angka
        default_option = "Bayar Sebagian"
        previous_nominal = str(previous_value)
    elif isinstance(previous_value, str) and previous_value.strip().isdigit():
        default_option = "Bayar Sebagian"
        previous_nominal = previous_value.strip()
    else:
        default_option = "Belum Bayar"
        previous_nominal = ""

    with col_status:
        # Pilih status berdasarkan default_option
        status = st.selectbox(
            label="",
            options=["Belum Bayar", "Sudah Bayar", "Bayar Sebagian"],
            index=["Belum Bayar", "Sudah Bayar", "Bayar Sebagian"].index(default_option),
            key=key_status
        )

    with col_nominal:
        # Jika status adalah 'Sudah Bayar' atau 'Bayar Sebagian', input nominal
        if status in ["Sudah Bayar", "Bayar Sebagian"]:
            nominal = st.text_input(label="", key=key_nominal, value=previous_nominal)

            # Cek apakah nominal valid (angka atau format desimal)
            if nominal.strip().replace('.', '', 1).isdigit() and nominal.count('.') <= 1:
                # Jika valid, simpan sebagai angka di DataFrame
                df_kas.at[selected_bulan, siswa] = str(int(float(nominal.strip())))
            else:
                st.warning(f"Nominal tidak valid untuk: {siswa}")
        else:
            # Jika status 'Belum Bayar', kosongkan nilai nominal
            df_kas.at[selected_bulan, siswa] = ""

# Input pengeluaran
st.header("💸 Input Pengeluaran")
st.markdown("Masukkan pengeluaran untuk bulan ini:")

# Formulir untuk input pengeluaran utama
with st.form("form_pengeluaran"):
    col1, col2 = st.columns(2)
    with col1:
        keterangan = st.text_input("Keterangan")
    with col2:
        nominal_pengeluaran = st.number_input("Nominal", min_value=0, step=1000)
    
    submitted = st.form_submit_button("Simpan Pengeluaran")
    
    # Menyimpan pengeluaran jika sudah diinput
    if submitted and keterangan and nominal_pengeluaran > 0:
        new_row = {"Bulan": selected_bulan, "Keterangan": keterangan, "Nominal": int(nominal_pengeluaran)}
        df_pengeluaran = pd.concat([df_pengeluaran, pd.DataFrame([new_row])], ignore_index=True)
        df_pengeluaran.to_excel(PENGELUARAN_FILE, index=False)
        st.success("Pengeluaran berhasil disimpan!")

    # Tombol opsional untuk menambah tabel input pengeluaran tambahan
    add_table = st.checkbox("Tambahkan Pengeluaran Lainnya", value=False)
    
    if add_table:
        st.write("Masukkan pengeluaran tambahan di bawah ini:")
        # Membuat tabel pengeluaran tambahan
        num_rows = st.number_input("Berapa banyak baris yang ingin ditambahkan?", min_value=1, max_value=10, value=1, step=1)
        
        # List untuk menampung data input pengeluaran tambahan
        additional_data = []
    
        # Loop untuk input beberapa pengeluaran
        for i in range(num_rows):
            col1, col2 = st.columns(2)
            with col1:
                keterangan = st.text_input(f"Keterangan Pengeluaran {i+1}")
            with col2:
                nominal = st.number_input(f"Nominal Pengeluaran {i+1}", min_value=0, step=1000)
            
            if keterangan and nominal > 0:
                additional_data.append({"Bulan": selected_bulan, "Keterangan": keterangan, "Nominal": nominal})
        
        # Menampilkan tabel pengeluaran tambahan
        if additional_data:
            df_additional = pd.DataFrame(additional_data)
            st.dataframe(df_additional)
            
            # Tombol untuk menyimpan pengeluaran tambahan
            if st.button("Simpan Pengeluaran Tambahan"):
                df_pengeluaran = pd.concat([df_pengeluaran, df_additional], ignore_index=True)
                df_pengeluaran.to_excel(PENGELUARAN_FILE, index=False)
                st.success("Pengeluaran tambahan berhasil disimpan!")

# Tombol simpan
if st.button("💾 Simpan Kas Siswa"):
    df_kas.to_excel(DATA_FILE)
    st.success("Data kas siswa berhasil disimpan.")

# Rekap
st.header("📊 Rekap Kas")
df_display = df_kas.T
st.dataframe(df_display, use_container_width=True, height=600)

# Gambar
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
    plt.title("Rekap Kas Kelas VII SMPI Al-HAYYAN", fontsize=24, weight='bold', pad=20)

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
