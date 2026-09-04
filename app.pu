import streamlit as st
import pandas as pd
import datetime
import calendar
import random

st.set_page_config(page_title="Sistem Penugasan SBCC IPK Selangor", layout="wide")

st.title("📋 Sistem Penugasan SBCC IPK Selangor")

# Senarai Pegawai Rasmi (31 Pegawai)
PEGAWAI = [
    {"nama": "INSP ADDLYZAN BIN ABD MANAP", "no_tel": "012-4739701"},
    {"nama": "INSP FAIZ BIN BASAR", "no_tel": "017-9457941"},
    {"nama": "INSP MOHD SHAHRILBUN BIN AMDAN", "no_tel": "017-5800578"},
    {"nama": "INSP FARAH NADJWA BT MOHD LASA", "no_tel": "013-9195659"},
    {"nama": "INSP SABARI BIN BUJANG", "no_tel": "016-7135975"},
    {"nama": "INSP KASHMINDEJRIT KAUR A/P CHARLES", "no_tel": "016-6738465"},
    {"nama": "INSP NORAINUN MUBIN BT ANUAR", "no_tel": "012-7493780"},
    {"nama": "INSP MUHAMAD IQRAM BIN MOHAMAD BUKHARI", "no_tel": "013-7044459"},
    {"nama": "INSP MOHAMAD IQBAL IBRAHIM BIN DAUD", "no_tel": "012-6467775"},
    {"nama": "INSP AMI RUSLAN BIN MOHD RUSLAN", "no_tel": "017-9501506"},
    {"nama": "INSP MOHD RAZIF BIN ROSSMAN", "no_tel": "017-9196166"},
    {"nama": "INSP AZFIZI BIN AZIZ", "no_tel": "014-8340944"},
    {"nama": "INSP MUHAMAD ARIFF BIN ABD RAHIM", "no_tel": "010-4017822"},
    {"nama": "INSP MOHD RUSDI BIN HASSAN", "no_tel": "010-4535060"},
    {"nama": "INSP ABDUL MUIN BIN AB AZIZ", "no_tel": "019-4494500"},
    {"nama": "INSP MOHD SHAHRIL BIN MOHAMED RESALI", "no_tel": "012-9096486"},
    {"nama": "INSP NOR HAIZAH BINTI YACOB", "no_tel": "012-9979790"},
    {"nama": "INSP KUKENDRAN A/L YOGENDRAN", "no_tel": "012-9062264"},
    {"nama": "INSP MUHAMMAD NOR QHAIREIL BIN NOR AZMI", "no_tel": "011-16554250"},
    {"nama": "INSP KHAIRUL HAFIZ BIN SHAFFIE AHMED", "no_tel": "017-4308434"},
    {"nama": "INSP EZYANTI BT MUHAMAD", "no_tel": "019-9241360"},
    {"nama": "INSP MOHAMAD SYARUL FADLI BIN MAT HUSAIN", "no_tel": "011-10042323"},
    {"nama": "INSP MUHAMMAD AFIQ BIN NORDIN", "no_tel": "010-4641637"},
    {"nama": "INSP MOHD JEFFERE BIN ALI", "no_tel": "014-2348186"},
    {"nama": "INSP NUR AADILA BINTI ABDUL MALEK", "no_tel": "014-3383604"},
    {"nama": "INSP SHURENDREN A/L JAYARAMAN", "no_tel": "019-2823312"},
    {"nama": "INSP MOHD FAIZ BIN ESA", "no_tel": "010-7978603"},
    {"nama": "INSP ROHAIZASHAFIKA BINTI MOHAMAD RADZALI", "no_tel": "016-2448782"},
    {"nama": "INSP DZUL FADHLI BIN ABDUL HALIM", "no_tel": "014-6689803"},
    {"nama": "INSP NORHAZIERAM BINTI ZAKARIA", "no_tel": "014-9207312"},
    {"nama": "INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN", "no_tel": "012-9212972"}
]

# Tetapan Bulan & Tahun
col1, col2 = st.columns(2)
with col1:
    bulan = st.selectbox("Pilih Bulan", list(range(1, 13)), index=datetime.datetime.now().month - 1)
with col2:
    tahun = st.number_input("Tahun", min_value=2024, max_value=2030, value=datetime.datetime.now().year)

num_days = calendar.monthrange(tahun, bulan)[1]
senarai_tarikh = [datetime.date(tahun, bulan, d) for d in range(1, num_days + 1)]

# Sidebar 1: Pengecualian Penugasan
st.sidebar.header("🚫 Pengecualian Penugasan (Cuti/Kursus)")
pegawai_dikecualikan = st.sidebar.multiselect(
    "Pilih pegawai yang DIKECUALIKAN bulan ini:",
    [p["nama"] for p in PEGAWAI]
)

# Sidebar 2: Special Assignment (Manual Override)
st.sidebar.header("📌 Special Assignment (Manual Override)")
override_dict = {}
senarai_aktif = [p["nama"] for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan]

for dt in senarai_tarikh:
    is_weekend = dt.weekday() in [5, 6]
    nama_hari = dt.strftime("%A")
    tkh_str = dt.strftime("%d/%m/%Y")
    
    if is_weekend:
        sel_s = st.sidebar.selectbox(f"{tkh_str} ({nama_hari}) - Siang", ["- Auto -"] + senarai_aktif, key=f"{tkh_str}_S")
        if sel_s != "- Auto -":
            override_dict[f"{tkh_str}_Siang"] = sel_s
            
        sel_m = st.sidebar.selectbox(f"{tkh_str} ({nama_hari}) - Malam", ["- Auto -"] + senarai_aktif, key=f"{tkh_str}_M")
        if sel_m != "- Auto -":
            override_dict[f"{tkh_str}_Malam"] = sel_m
    else:
        sel_b = st.sidebar.selectbox(f"{tkh_str} ({nama_hari}) - Biasa", ["- Auto -"] + senarai_aktif, key=f"{tkh_str}_B")
        if sel_b != "- Auto -":
            override_dict[f"{tkh_str}_Biasa"] = sel_b

# Logik Penjanaan Jadual
if st.button("🚀 Jana Jadual Penugasan", type="primary"):
    # Rekod pengiraan
    tugas_wd = {p["nama"]: 0 for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan}
    tugas_we = {p["nama"]: 0 for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan}
    pegawai_hari_sebelumnya = set()
    jadual = []

    # Ambil kira manual override
    for k, val in override_dict.items():
        if "_Siang" in k or "_Malam" in k:
            tugas_we[val] += 1
        else:
            tugas_wd[val] += 1

    def pilih_pegawai(is_wknd, elak_set):
        calon = [p for p in senarai_aktif if p not in elak_set]
        if not calon:
            calon = [p for p in senarai_aktif] # Fail-safe jika semua sedang bertugas
            
        # Utamakan pengagihan seimbang mengikut jenis hari (Weekdays/Weekends)
        if is_wknd:
            min_we = min([tugas_we[c] for c in calon])
            layak = [c for c in calon if tugas_we[c] == min_we]
            min_tot = min([tugas_wd[c] + tugas_we[c] for c in layak])
            final = [c for c in layak if (tugas_wd[c] + tugas_we[c]) == min_tot]
            pilihan = random.choice(final)
            tugas_we[pilihan] += 1
        else:
            min_wd = min([tugas_wd[c] for c in calon])
            layak = [c for c in calon if tugas_wd[c] == min_wd]
            min_tot = min([tugas_wd[c] + tugas_we[c] for c in layak])
            final = [c for c in layak if (tugas_wd[c] + tugas_we[c]) == min_tot]
            pilihan = random.choice(final)
            tugas_wd[pilihan] += 1
            
        return pilihan

    for dt in senarai_tarikh:
        is_weekend = dt.weekday() in [5, 6]
        tkh_str = dt.strftime("%d/%m/%Y")
        hari_str = dt.strftime("%A")
        pegawai_hari_ini = set()

        if is_weekend:
            # Syif Siang
            k_s = f"{tkh_str}_Siang"
            p_s = override_dict[k_s] if k_s in override_dict else pilih_pegawai(True, pegawai_hari_sebelumnya)
            pegawai_hari_ini.add(p_s)
            tel_s = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_s)
            jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Siang (0800 - 2000)", "Nama Pegawai": p_s, "No. Telefon": tel_s})

            # Syif Malam
            k_m = f"{tkh_str}_Malam"
            p_m = override_dict[k_m] if k_m in override_dict else pilih_pegawai(True, pegawai_hari_sebelumnya.union(pegawai_hari_ini))
            pegawai_hari_ini.add(p_m)
            tel_m = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_m)
            jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Malam (2000 - 0800)", "Nama Pegawai": p_m, "No. Telefon": tel_m})

        else:
            # Syif Biasa
            k_b = f"{tkh_str}_Biasa"
            p_b = override_dict[k_b] if k_b in override_dict else pilih_pegawai(False, pegawai_hari_sebelumnya)
            pegawai_hari_ini.add(p_b)
            tel_b = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_b)
            jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Biasa (1700 - 0800)", "Nama Pegawai": p_b, "No. Telefon": tel_b})

        pegawai_hari_sebelumnya = pegawai_hari_ini

    df_jadual = pd.DataFrame(jadual)
    
    st.subheader("📅 Jadual Penugasan")
    st.dataframe(df_jadual, use_container_width=True)

    # Ringkasan Pengagihan Tugas
    st.subheader("📊 Ringkasan Jumlah Tugas Setiap Pegawai")
    ringkasan_list = []
    for p in PEGAWAI:
        nama = p["nama"]
        if nama in pegawai_dikecualikan:
            ringkasan_list.append({"Nama Pegawai": nama, "Hari Biasa": 0, "Hujung Minggu": 0, "Jumlah Syif": 0, "Status": "DIKECUALIKAN"})
        else:
            wd = tugas_wd[nama]
            we = tugas_we[nama]
            ringkasan_list.append({"Nama Pegawai": nama, "Hari Biasa": wd, "Hujung Minggu": we, "Jumlah Syif": wd + we, "Status": "AKTIF"})
            
    df_ringkasan = pd.DataFrame(ringkasan_list)
    st.dataframe(df_ringkasan, use_container_width=True)
