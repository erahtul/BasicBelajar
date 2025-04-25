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

col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    for siswa in nama_siswa:
        val = st.text_input(f"{siswa}", value=st.session_state.data_siswa.loc[selected_bulan, siswa], key=f"{selected_bulan}_{siswa}")
        if val.lower() == "true":
            st.session_state.data_siswa.loc[selected_bulan, siswa] = "TRUE"
        else:
            try:
                nominal = float(val)
                st.session_state.data_siswa.loc[selected_bulan, siswa] = nominal
            except ValueError:
                st.warning(f"Isi angka atau 'True' untuk: {siswa}")

# Rekap dan Tabel
st.markdown("---")
st.markdown("### 📊 Rekap Kas Kelas")
df_display = st.session_state.data_siswa.T  # Transpose supaya nama siswa di kiri
st.dataframe(df_display, use_container_width=True, height=600)

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