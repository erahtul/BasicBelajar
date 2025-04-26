import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO
import io

# Konfigurasi login admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Fungsi untuk login
def login():
    st.session_state.logged_in = False
    st.session_state.username = ""
    
    st.title("Login Admin")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login berhasil!")
        else:
            st.error("Username atau password salah!")

# Mengecek status login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
# Setup
st.set_page_config(page_title="Kas Kelas VII", layout="centered")  # Ganti layout menjadi centered untuk tampilan mobile yang lebih baik

# Welcome Header
st.markdown("<h1 style='text-align: center;'>Welcome to My Application</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Created by Bang Imat</p>", unsafe_allow_html=True)

# Judul
st.markdown("<h2 style='text-align: center;'>SMPI Al HAYYAN</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Kas Ortu/Wali Kelas VII</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Tahun Ajaran 2024/2025</h4>", unsafe_allow_html=True)
st.markdown("---")

# Data setup
nama_siswa = ["Afiqah Naura R.", "Ahdani Nurrohmah", "Ahmad Haikal Zufar", "Ahmad Zaki Alghifari", 
    "Annisa Mutia Azizah", "Aqilah Athaya Yuvita", "Aqila Qonita Mumtaza", "Bima Wahianto Sitepu", 
    "Bryan Keama Huda", "Darrel Muhammad Ziqrillah", "Falya Azqya Nadheera", "Herjuno Caesar Ali", 
    "Iksan Fahmi", "Kayla Julia Rahma", "Ladysha Qanita Wijaya", "Lakeisha Safilla Budiyanto", 
    "Muhammad Athar Rafianza", "Muhammad Dimas Prasetyo", "Muhammad Kresna Akbar S.", 
    "Muhammad Wijaya K.", "Najmi Al Irsyaq Nurhadi", "Rachel Kireina Axelle", "Ragil Albar Fahrezi", 
    "Rizqi Heriansyah", "Ruby Aqilah A.", "Salsabila Putri Kurniawan", "Yuko Haadi Pratama"]

bulan = ["Juli", "Agustus", "September", "Oktober", "November", "Desember", "Januari", "Febuari", 
         "Maret", "April", "Mei", "Juni"]

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

    # Tentukan status default berdasarkan data sebelumnya
    if str(previous_value).strip().isdigit():
        if int(previous_value) == 15000:
            default_option = "Sudah Bayar"
        else:
            default_option = "Bayar Sebagian"
        previous_nominal = str(previous_value)
    else:
        default_option = "Belum Bayar"
        previous_nominal = ""

    # Cek session state untuk mempertahankan input
    if key_status not in st.session_state:
        st.session_state[key_status] = default_option
    if key_nominal not in st.session_state:
        st.session_state[key_nominal] = previous_nominal

    with col_status:
        status = st.selectbox(
            label="",
            options=["Belum Bayar", "Sudah Bayar", "Bayar Sebagian"],
            index=["Belum Bayar", "Sudah Bayar", "Bayar Sebagian"].index(st.session_state[key_status]),
            key=key_status
        )

    with col_nominal:
        if status in ["Sudah Bayar", "Bayar Sebagian"]:
            nominal_display_partial = [f"Rp {x:,}".replace(",", ".") for x in range(5000, 20001, 5000)]
            if previous_nominal.isdigit():
                default_nominal = f"Rp {int(previous_nominal):,}".replace(",", ".")
            else:
                default_nominal = nominal_display_partial[0]

            try:
                default_index = nominal_display_partial.index(default_nominal) + 1
            except ValueError:
                default_index = 0

            nominal = st.selectbox(
                label="",
                options=[""] + nominal_display_partial,
                index=default_index,
                key=key_nominal
            )
        else:
            nominal = ""

    # Update session state dengan nilai yang dipilih
    st.session_state[key_status] = status
    st.session_state[key_nominal] = nominal

    # Simpan data status dan nominal ke DataFrame
    if status == "Belum Bayar":
        df_kas.at[selected_bulan, siswa] = ""
    elif status in ["Sudah Bayar", "Bayar Sebagian"]:
        if nominal and nominal in nominal_mapping:
            df_kas.at[selected_bulan, siswa] = str(nominal_mapping[nominal])
        else:
            df_kas.at[selected_bulan, siswa] = ""

# Setelah loop selesai, auto save
df_kas.to_excel(DATA_FILE)
st.success("✅ Data kas siswa otomatis tersimpan.")

# Input pengeluaran
st.header("💸 Input Pengeluaran")
st.markdown("Masukkan pengeluaran untuk bulan ini (nominal kelipatan Rp1.000):")

# Formulir input pengeluaran
with st.form("form_pengeluaran"):
    col1, col2 = st.columns(2)
    with col1:
        keterangan = st.text_input("Keterangan")
    with col2:
        nominal_pengeluaran = st.number_input(
            "Nominal (Rp)", min_value=0, step=1000, format="%d"
        )

    submitted = st.form_submit_button("Simpan Pengeluaran")

    if submitted:
        if keterangan and nominal_pengeluaran > 0:
            if nominal_pengeluaran % 1000 == 0:
                new_row = {"Bulan": selected_bulan, "Keterangan": keterangan, "Nominal": int(nominal_pengeluaran)}
                df_pengeluaran = pd.concat([df_pengeluaran, pd.DataFrame([new_row])], ignore_index=True)
                df_pengeluaran.to_excel(PENGELUARAN_FILE, index=False)
                st.success("Pengeluaran berhasil disimpan!")
            else:
                st.error("Nominal harus kelipatan Rp1.000.")

# Tampilkan tabel semua pengeluaran bulan ini
st.subheader(f"📄 Daftar Pengeluaran Bulan {selected_bulan}")
df_pengeluaran_bulan_ini = df_pengeluaran[df_pengeluaran['Bulan'] == selected_bulan]

if not df_pengeluaran_bulan_ini.empty:
    # Format nominal jadi format uang
    df_pengeluaran_bulan_ini_display = df_pengeluaran_bulan_ini.copy()
    df_pengeluaran_bulan_ini_display['Nominal'] = df_pengeluaran_bulan_ini_display['Nominal'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.'))

    # Tampilkan tabel lebih rapih
    st.dataframe(
        df_pengeluaran_bulan_ini_display.style
            .set_properties(**{
                'text-align': 'center',
                'background-color': '#f0f8ff',  # Soft light blue
                'font-weight': 'bold'
            })
            .set_table_styles([{
                'selector': 'thead th',
                'props': [('background-color', '#dbeafe'), ('font-weight', 'bold'), ('text-align', 'center')]
            }])
            .hide(axis="index")
    )
else:
    st.info("Belum ada pengeluaran tercatat untuk bulan ini.")

# --- Rekap Kas ---
st.header("📊 Rekap Kas")
df_display = df_kas.T
st.dataframe(df_display, use_container_width=True, height=600)

# Fungsi konversi dataframe ke gambar
def dataframe_to_image(df):
    df_vis = df.fillna("").astype(str)
    n_rows, n_cols = df_vis.shape
    fig, ax = plt.subplots(figsize=(1.5 + n_cols, 0.4 + n_rows * 0.4))

    def cell_color(val):
        if val.upper() == "TRUE":
            return "#d4edda"  # Hijau untuk 'Sudah Bayar'
        elif val.strip().isdigit() or val.replace('.', '', 1).isdigit():
            return "#fff3cd"  # Kuning untuk 'Bayar Sebagian'
        else:
            return "#ffffff"  # Tidak ada warna untuk 'Belum Bayar'

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
    plt.title("Rekap Kas Kelas VII SMPI Al-HAYYAN", fontsize=20, weight='bold', pad=0)  # Mengurangi jarak

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    plt.close()
    buf.seek(0)
    return buf

# Mengubah DataFrame menjadi gambar
img_buf = dataframe_to_image(df_display)

# Menampilkan gambar pada Streamlit
st.image(img_buf, caption="Rekap Kas Kelas (Gambar)", use_container_width=True)

# Menambahkan tombol untuk download gambar
st.download_button(
    label="🖼️ Download Rekap Kas sebagai Gambar (PNG)",
    data=img_buf,
    file_name="rekap_kas_kelas_vii.png",
    mime="image/png"
)

# Rekap Total
st.header("💰 Total Rekapitulasi")
total_masuk = 0
for val in df_kas.values.flatten():
    if str(val).strip().isdigit() or str(val).replace('.', '', 1).isdigit():
        total_masuk += int(float(val))

total_pengeluaran = df_pengeluaran[df_pengeluaran['Bulan'] == selected_bulan]['Nominal'].sum()
sisa_kas = total_masuk - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Kas Masuk", f"Rp {total_masuk:,}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,}")
col3.metric("Sisa Kas", f"Rp {sisa_kas:,}")

# --- DOWNLOAD & RESET SECTION ---

st.markdown("---")
st.header("📦 Download & Reset Data")

# Download Laporan Kas
st.subheader("📥 Download Laporan Kas")
with open(DATA_FILE, "rb") as f:
    st.download_button(
        label="Download Laporan Kas (Excel)",
        data=f,
        file_name="laporan_kas_kelas_vii.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Download Laporan Pengeluaran
st.subheader("📥 Download Laporan Pengeluaran")
with open(PENGELUARAN_FILE, "rb") as f:
    st.download_button(
        label="Download Laporan Pengeluaran (Excel)",
        data=f,
        file_name="laporan_pengeluaran_kelas_vii.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Reset Data Kas
st.subheader(f"♻️ Reset Data Kas Bulan {selected_bulan}")
if st.button(f"Reset Data Kas Bulan {selected_bulan}"):
    for siswa in nama_siswa:
        df_kas.at[selected_bulan, siswa] = ""
    df_kas.to_excel(DATA_FILE)
    st.success(f"✅ Data kas bulan {selected_bulan} berhasil di-reset!")

# Reset Data Pengeluaran
st.subheader(f"♻️ Reset Data Pengeluaran Bulan {selected_bulan}")
if st.button(f"Reset Data Pengeluaran Bulan {selected_bulan}"):
    df_pengeluaran = df_pengeluaran[df_pengeluaran['Bulan'] != selected_bulan]
    df_pengeluaran.to_excel(PENGELUARAN_FILE, index=False)
    st.success(f"✅ Data pengeluaran bulan {selected_bulan} berhasil di-reset!")