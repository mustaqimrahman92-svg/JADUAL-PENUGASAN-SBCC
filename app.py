import streamlit as st
import pandas as pd

# Tetapan Halaman Streamlit
st.set_page_config(page_title="Sistem Jadual Penugasan SBCC IPK Selangor", layout="wide")

st.title("🛡️ CAWANGAN KHAS IPK SELANGOR")
st.subheader("Pangkalan Data & Sistem Jadual Penugasan Pegawai / Penolong Pegawai")

# ==========================================
# 1. PANGKALAN DATA PEGAWAI (INSP)
# ==========================================
data_pegawai = [
    {"Bil": 1, "Nama Pegawai": "INSP ADDLYZAN BIN ABD MANAP", "No. Telefon": "012-4739701", "Cawangan": "E2"},
    {"Bil": 2, "Nama Pegawai": "INSP FAIZ BIN BASAR", "No. Telefon": "017-9457941", "Cawangan": "E2"},
    {"Bil": 3, "Nama Pegawai": "INSP SABARI BIN BUJANG", "No. Telefon": "016-7135975", "Cawangan": "E2"},
    {"Bil": 4, "Nama Pegawai": "INSP KASHMINDEJRIT KAUR A/P CHARLES", "No. Telefon": "016-6738465", "Cawangan": "E2"},
    {"Bil": 5, "Nama Pegawai": "INSP SHURENDREN A/L JAYARAMAN", "No. Telefon": "019-2823312", "Cawangan": "E2"},
    {"Bil": 6, "Nama Pegawai": "INSP FARAH NADJWA BT MOHD LASA", "No. Telefon": "013-9195659", "Cawangan": "E2"},
    {"Bil": 7, "Nama Pegawai": "INSP NORAINUN MUBIN BT ANUAR", "No. Telefon": "012-7493780", "Cawangan": "E3"},
    {"Bil": 8, "Nama Pegawai": "INSP MUHAMAD IQRAM BIN MOHAMAD BUKHARI", "No. Telefon": "013-7044459", "Cawangan": "E3"},
    {"Bil": 9, "Nama Pegawai": "INSP MOHAMAD IQBAL IBRAHIM BIN DAUD", "No. Telefon": "012-6467775", "Cawangan": "E4"},
    {"Bil": 10, "Nama Pegawai": "INSP AMI RUSLAN BIN MOHD RUSLAN", "No. Telefon": "017-9501506", "Cawangan": "E4"},
    {"Bil": 11, "Nama Pegawai": "INSP MOHD RAZIF BIN ROSSMAN", "No. Telefon": "017-9196166", "Cawangan": "E4"},
    {"Bil": 12, "Nama Pegawai": "INSP AZFIZI BIN AZIZ", "No. Telefon": "014-8340944", "Cawangan": "E4"},
    {"Bil": 13, "Nama Pegawai": "INSP MUHAMAD ARIFF BIN ABD RAHIM", "No. Telefon": "010-4017822", "Cawangan": "E4"},
    {"Bil": 14, "Nama Pegawai": "INSP MOHD RUSDI BIN HASSAN", "No. Telefon": "010-4535060", "Cawangan": "E4"},
    {"Bil": 15, "Nama Pegawai": "INSP ABDUL MUIN BIN AB AZIZ", "No. Telefon": "019-4494500", "Cawangan": "E5"},
    {"Bil": 16, "Nama Pegawai": "INSP MOHD SHAHRIL BIN MOHAMED RESALI", "No. Telefon": "012-9096486", "Cawangan": "E5"},
    {"Bil": 17, "Nama Pegawai": "INSP NOR HAIZAH BINTI YACOB", "No. Telefon": "012-9979790", "Cawangan": "E5"},
    {"Bil": 18, "Nama Pegawai": "INSP KUKENDRAN A/L YOGENDRAN", "No. Telefon": "012-9062264", "Cawangan": "E6"},
    {"Bil": 19, "Nama Pegawai": "INSP MUHAMMAD NOR QHAIREIL BIN NOR AZMI", "No. Telefon": "011-16554250", "Cawangan": "E6"},
    {"Bil": 20, "Nama Pegawai": "INSP KHAIRUL HAFIZ BIN SHAFFIE AHMED", "No. Telefon": "017-4308434", "Cawangan": "E6"},
    {"Bil": 21, "Nama Pegawai": "INSP EZYANTI BT MUHAMAD", "No. Telefon": "019-9241360", "Cawangan": "E6"},
    {"Bil": 22, "Nama Pegawai": "INSP MOHAMAD SYARUL FADLI BIN MAT HUSAIN", "No. Telefon": "011-10042323", "Cawangan": "E6"},
    {"Bil": 23, "Nama Pegawai": "INSP MUHAMMAD AFIQ BIN NORDIN", "No. Telefon": "010-4641637", "Cawangan": "E7"},
    {"Bil": 24, "Nama Pegawai": "INSP MOHD JEFFERE BIN ALI", "No. Telefon": "014-2348186", "Cawangan": "E7"},
    {"Bil": 25, "Nama Pegawai": "INSP NUR AADILA BINTI ABDUL MALEK", "No. Telefon": "014-3383604", "Cawangan": "E7"},
    {"Bil": 26, "Nama Pegawai": "INSP MOHD SHAHRILBUN BIN AMDAN", "No. Telefon": "017-5800578", "Cawangan": "E8"},
    {"Bil": 27, "Nama Pegawai": "INSP MOHD FAIZ BIN ESA", "No. Telefon": "010-7978603", "Cawangan": "E8"},
    {"Bil": 28, "Nama Pegawai": "INSP ROHAIZASHAFIKA BINTI MOHAMAD RADZALI", "No. Telefon": "016-2448782", "Cawangan": "E8"},
    {"Bil": 29, "Nama Pegawai": "INSP DZUL FADHLI BIN ABDUL HALIM", "No. Telefon": "014-6689803", "Cawangan": "E9"},
    {"Bil": 30, "Nama Pegawai": "INSP NORHAZIERAM BINTI ZAKARIA", "No. Telefon": "014-9207312", "Cawangan": "E9"},
    {"Bil": 31, "Nama Pegawai": "INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN", "No. Telefon": "012-9212972", "Cawangan": "E9"}
]

# ==========================================
# 2. PANGKALAN DATA PENOLONG PEGAWAI
# ==========================================
data_penolong = [
    {"Bil": 1, "Nama Penolong Pegawai": "SJN/D ONG WEI TAU", "No. Telefon": "012-8121981", "Cawangan": "E2"},
    {"Bil": 2, "Nama Penolong Pegawai": "KPL/D MOHD FAIZAL BIN TIMAN", "No. Telefon": "017-7455348", "Cawangan": "E2"},
    {"Bil": 3, "Nama Penolong Pegawai": "KPL/D MUHAMMAD AZRUL SHAFIQ BIN ISMAN", "No. Telefon": "019-5898658", "Cawangan": "E2"},
    {"Bil": 4, "Nama Penolong Pegawai": "KPL/D FARIEZUL NAIM BIN MOHD SANI", "No. Telefon": "013-6399275", "Cawangan": "E2"},
    {"Bil": 5, "Nama Penolong Pegawai": "SJN/D SUYANI BINTI MAT SAAD", "No. Telefon": "012-3405606", "Cawangan": "E2"},
    {"Bil": 6, "Nama Penolong Pegawai": "SJN/D MOHD JURAIDI BIN SAMSUDIN", "No. Telefon": "012-6769745", "Cawangan": "E2"},
    {"Bil": 7, "Nama Penolong Pegawai": "L/KPL/D NURHIDAYAH BINTI SUHAMI", "No. Telefon": "017-7011952", "Cawangan": "E2"},
    {"Bil": 8, "Nama Penolong Pegawai": "KONS NUR AMIERA BINTI MOHAMAD ALI AHAN", "No. Telefon": "017-6723075", "Cawangan": "E2"},
    {"Bil": 9, "Nama Penolong Pegawai": "L/KPL ATHIRAH NABILA BINTI SAEDIN", "No. Telefon": "018-3166724", "Cawangan": "E2"},
    {"Bil": 10, "Nama Penolong Pegawai": "L/KPL/D HANA LYDIA BINTI LIERON", "No. Telefon": "018-8709538", "Cawangan": "E2"},
    {"Bil": 11, "Nama Penolong Pegawai": "SJN/D HAFIZATUL AMIRA BT ADBUL MANAF", "No. Telefon": "019-5493007", "Cawangan": "E3"},
    {"Bil": 12, "Nama Penolong Pegawai": "KPL/D JEEVAN A/L VADIAHLAGAN", "No. Telefon": "013-5638303", "Cawangan": "E3"},
    {"Bil": 13, "Nama Penolong Pegawai": "L/KPL/D MOHAMMAD ARRYAN JUING BIN ABDULLAH", "No. Telefon": "019-4334734", "Cawangan": "E3"},
    {"Bil": 14, "Nama Penolong Pegawai": "SJN/D VASTERMORAILE ANAK MONDAY", "No. Telefon": "017-7058084", "Cawangan": "E3"},
    {"Bil": 15, "Nama Penolong Pegawai": "L/KPL AHMAD HELMI HARIRI BIN SALVEHUJRAIE", "No. Telefon": "011-166522645", "Cawangan": "E3"},
    {"Bil": 16, "Nama Penolong Pegawai": "SJN/D SHAHRUL IDHAM BIN MD SALIM", "No. Telefon": "014-2440181", "Cawangan": "E3"},
    {"Bil": 17, "Nama Penolong Pegawai": "SJN/D ZAMRI BIN BAKARI", "No. Telefon": "013-2893878", "Cawangan": "E3A"},
    {"Bil": 18, "Nama Penolong Pegawai": "SJN/D AHMAD ZAMANE BIN OMAR", "No. Telefon": "013-4939452", "Cawangan": "E4"},
    {"Bil": 19, "Nama Penolong Pegawai": "KPL/D MOHD SYAIFUL AZHAR BIN MOHD HANAFIAH", "No. Telefon": "011-51105497", "Cawangan": "E4"},
    {"Bil": 20, "Nama Penolong Pegawai": "SJN/D HAFENDI BIN HANAFIAH", "No. Telefon": "012-3784305", "Cawangan": "E4"},
    {"Bil": 21, "Nama Penolong Pegawai": "KPL/D LO YEE TYNG", "No. Telefon": "016-8374537", "Cawangan": "E4"},
    {"Bil": 22, "Nama Penolong Pegawai": "SJN/D JAAFAR BIN MA HASAN", "No. Telefon": "011-11474013", "Cawangan": "E4"},
    {"Bil": 23, "Nama Penolong Pegawai": "KPL/D MOHD KHAIROL IZDZUAN BIN MOHAMAD ZAHARI", "No. Telefon": "012-2796394", "Cawangan": "E4"},
    {"Bil": 24, "Nama Penolong Pegawai": "KPL/D MUHAMMAD AZKA FATIN BIN MOHD NORDIN", "No. Telefon": "016-2198068", "Cawangan": "E5"},
    {"Bil": 25, "Nama Penolong Pegawai": "SJN/D SYEAFUUL AZNRY BIN ZAMBRI", "No. Telefon": "012-7637889", "Cawangan": "E5"},
    {"Bil": 26, "Nama Penolong Pegawai": "SJN/D EFFARINA BIN AHMAD SUHAIMI", "No. Telefon": "018-9154504", "Cawangan": "E5"},
    {"Bil": 27, "Nama Penolong Pegawai": "KPL/D MUHAMMAD SYUKRI BIN ZULKIFLI", "No. Telefon": "012-6196573", "Cawangan": "E5"},
    {"Bil": 28, "Nama Penolong Pegawai": "P/SJN/D ASRUL AZWANDI BIN AHMAD", "No. Telefon": "019-4636430", "Cawangan": "E5"},
    {"Bil": 29, "Nama Penolong Pegawai": "KPL/D SUFIAN BIN ISMAIL", "No. Telefon": "017-6217662", "Cawangan": "E5"},
    {"Bil": 30, "Nama Penolong Pegawai": "KPL/D MUHAMMAD ZULFFY BIN RASHID", "No. Telefon": "013-4080883", "Cawangan": "E6"},
    {"Bil": 31, "Nama Penolong Pegawai": "SJN/D ZAMZUHAIRI BIN TOMIRAN", "No. Telefon": "012-2712700", "Cawangan": "E6"},
    {"Bil": 32, "Nama Penolong Pegawai": "KPL/D NOOR HAZWANI BINTI MUHAMAD RUSLI", "No. Telefon": "019-2217116", "Cawangan": "E6"},
    {"Bil": 33, "Nama Penolong Pegawai": "KPL/D YVONNE KUA CHEE WEI", "No. Telefon": "011-10905627", "Cawangan": "E6"},
    {"Bil": 34, "Nama Penolong Pegawai": "KPL/D MOHD KHAIROL ANUAR BIN MOHAMED", "No. Telefon": "010-4358116", "Cawangan": "E6"},
    {"Bil": 35, "Nama Penolong Pegawai": "KPL/D NELSON ANAK NUING", "No. Telefon": "017-3655175", "Cawangan": "E6"},
    {"Bil": 36, "Nama Penolong Pegawai": "KPL/D MUHAMMAD FIRDAUS BIN AMRAN", "No. Telefon": "013-7783677", "Cawangan": "E7"},
    {"Bil": 37, "Nama Penolong Pegawai": "SJN/D YUSRI BIN WAHAB", "No. Telefon": "019-3876720", "Cawangan": "E7"},
    {"Bil": 38, "Nama Penolong Pegawai": "KPL/D WELLINGTON RICHARD ANAK SADOK", "No. Telefon": "011-29994591", "Cawangan": "E7"},
    {"Bil": 39, "Nama Penolong Pegawai": "KPL/D MOHAMAD PARIS BIN ROMELI", "No. Telefon": "017-3864533", "Cawangan": "E7"},
    {"Bil": 40, "Nama Penolong Pegawai": "KPL/D ABDUL HALIM BIN KAMARUDDIN", "No. Telefon": "013-2425850", "Cawangan": "E7"},
    {"Bil": 41, "Nama Penolong Pegawai": "KPL/D MOHAMAD HAFIS BIN SALLEH", "No. Telefon": "013-4928247", "Cawangan": "E7"},
    {"Bil": 42, "Nama Penolong Pegawai": "KPL/D HAZIZAT BIN ATTAN", "No. Telefon": "013-5744426", "Cawangan": "E8"},
    {"Bil": 43, "Nama Penolong Pegawai": "KPL/D MOHD YUSRI BIN ABU SEMAN", "No. Telefon": "017-9278564", "Cawangan": "E8"},
    {"Bil": 44, "Nama Penolong Pegawai": "SJN/D NOOR HAKIMI BIN ZULKIFLI", "No. Telefon": "012-6949107", "Cawangan": "E8"},
    {"Bil": 45, "Nama Penolong Pegawai": "KPL/D RIZQI ALFIAN BIN KOMIN", "No. Telefon": "011-23246744", "Cawangan": "E8"},
    {"Bil": 46, "Nama Penolong Pegawai": "L/KPL/D KOLOZUM SAFINAH BINTI VARUSAI", "No. Telefon": "011-65670875", "Cawangan": "E8"},
    {"Bil": 47, "Nama Penolong Pegawai": "L/KPL/D MUHAMMAD ABDUL WAFIE HAZIQ BIN HAMDAN", "No. Telefon": "017-5431206", "Cawangan": "E8"}
]

# Tab Menu
tab1, tab2 = st.tabs(["📊 Pangkalan Data Pegawai", "📅 Semakan / Penugasan"])

with tab1:
    st.header("1. Senarai Pegawai Bertugas (Insp)")
    df_pegawai = pd.DataFrame(data_pegawai)
    st.dataframe(df_pegawai, use_container_width=True, hide_index=True)

    st.write("---")
    st.header("2. Senarai Penolong Pegawai Bertugas (Sjn / Kpl / L/Kpl)")
    df_penolong = pd.DataFrame(data_penolong)
    st.dataframe(df_penolong, use_container_width=True, hide_index=True)

with tab2:
    st.header("Carian & Semakan Penugasan Harian")
    tarikh = st.date_input("Pilih Tarikh Penugasan")
    
    # Contoh Penjana Tugas Ringkas Berdasarkan Index Tarikh
    idx_p = tarikh.day % len(data_pegawai)
    idx_pen = tarikh.day % len(data_penolong)
    
    st.success(f"**Tarikh Selected:** {tarikh.strftime('%d-%m-%Y')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pegawai Bertugas (Insp)")
        peg = data_pegawai[idx_p]
        st.info(f"**Nama:** {peg['Nama Pegawai']}\n\n**Cawangan:** {peg['Cawangan']}\n\n**No Tel:** {peg['No. Telefon']}")
        
    with col2:
        st.subheader("Penolong Pegawai Bertugas")
        pen = data_penolong[idx_pen]
        st.warning(f"**Nama:** {pen['Nama Penolong Pegawai']}\n\n**Cawangan:** {pen['Cawangan']}\n\n**No Tel:** {pen['No. Telefon']}")
