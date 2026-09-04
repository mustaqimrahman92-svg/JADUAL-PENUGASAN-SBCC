import streamlit as st
import pandas as pd
import datetime
import calendar
import random
import sqlite3

st.set_page_config(page_title="Sistem Penugasan SBCC IPK Selangor", layout="wide")

# ==========================================
# FUNKSI PANGKALAN DATA (SQLITE)
# ==========================================
DB_FILE = "jadual_penugasan.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rekod_jadual (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bulan INTEGER,
            tahun INTEGER,
            tarikh TEXT,
            hari TEXT,
            syif TEXT,
            nama_pegawai TEXT,
            no_tel TEXT,
            tarikh_disahkan TEXT
        )
    ''')
    conn.commit()
    conn.close()

def simpan_jadual_db(bulan, tahun, df_jadual):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Padam rekod bulan/tahun tersebut jika pernah disimpan sebelum ini (re-write/update)
    c.execute("DELETE FROM rekod_jadual WHERE bulan = ? AND tahun = ?", (bulan, tahun))
    
    tarikh_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for _, row in df_jadual.iterrows():
        c.execute('''
            INSERT INTO rekod_jadual (bulan, tahun, tarikh, hari, syif, nama_pegawai, no_tel, tarikh_disahkan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bulan, tahun, row['Tarikh'], row['Hari'], row['Syif / Masa'], row['Nama Pegawai'], row['No. Telefon'], tarikh_sekarang))
    
    conn.commit()
    conn.close()

def ambil_jadual_db(bulan, tahun):
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT tarikh AS Tarikh, hari AS Hari, syif AS 'Syif / Masa', nama_pegawai AS 'Nama Pegawai', no_tel AS 'No. Telefon', tarikh_disahkan AS 'Tarikh Disahkan' FROM rekod_jadual WHERE bulan = ? AND tahun = ?"
    df = pd.read_sql_query(query, conn, params=(bulan, tahun))
    conn.close()
    return df

# Inisialisasi DB
init_db()

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

REKOD_SEP_2026 = {
    "INSP ROHAIZASHAFIKA BINTI MOHAMAD RADZALI": {"WD": 2, "WE": 0},
    "INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN": {"WD": 1, "WE": 1},
    "INSP MUHAMAD IQRAM BIN MOHAMAD BUKHARI": {"WD": 1, "WE": 0},
    "INSP ADDLYZAN BIN ABD MANAP": {"WD": 1, "WE": 0},
    "INSP SHURENDREN A/L JAYARAMAN": {"WD": 2, "WE": 0},
    "INSP SABARI BIN BUJANG": {"WD": 0, "WE": 1},
    "INSP MUHAMMAD AFIQ BIN NORDIN": {"WD": 1, "WE": 1},
    "INSP KHAIRUL HAFIZ BIN SHAFFIE AHMED": {"WD": 1, "WE": 1},
    "INSP DZUL FADHLI BIN ABDUL HALIM": {"WD": 0, "WE": 1},
    "INSP MOHAMAD IQBAL IBRAHIM BIN DAUD": {"WD": 1, "WE": 0},
    "INSP ABDUL MUIN BIN AB AZIZ": {"WD": 1, "WE": 1},
    "INSP AZFIZI BIN AZIZ": {"WD": 2, "WE": 0},
    "INSP AMI RUSLAN BIN MOHD RUSLAN": {"WD": 2, "WE": 0},
    "INSP FARAH NADJWA BT MOHD LASA": {"WD": 0, "WE": 2},
    "INSP MOHD JEFFERE BIN ALI": {"WD": 1, "WE": 1},
    "INSP NUR AADILA BINTI ABDUL MALEK": {"WD": 0, "WE": 1},
    "INSP EZYANTI BT MUHAMAD": {"WD": 1, "WE": 1},
    "INSP MOHD FAIZ BIN ESA": {"WD": 2, "WE": 0},
    "INSP KASHMINDEJRIT KAUR A/P CHARLES": {"WD": 0, "WE": 1},
    "INSP FAIZ BIN BASAR": {"WD": 0, "WE": 1},
    "INSP MOHAMAD SYARUL FADLI BIN MAT HUSAIN": {"WD": 1, "WE": 0},
    "INSP NOR HAIZAH BINTI YACOB": {"WD": 0, "WE": 1},
    "INSP MOHD RAZIF BIN ROSSMAN": {"WD": 0, "WE": 1},
    "INSP NORAINUN MUBIN BT ANUAR": {"WD": 0, "WE": 1},
    "INSP KUKENDRAN A/L YOGENDRAN": {"WD": 0, "WE": 1},
    "INSP MOHD SHAHRIL BIN MOHAMED RESALI": {"WD": 0, "WE": 1},
    "INSP MOHD SHAHRILBUN BIN AMDAN": {"WD": 1, "WE": 0},
    "INSP MOHD RUSDI BIN HASSAN": {"WD": 1, "WE": 0},
    "INSP MUHAMAD ARIFF BIN ABD RAHIM": {"WD": 0, "WE": 0},
    "INSP MUHAMMAD NOR QHAIREIL BIN NOR AZMI": {"WD": 0, "WE": 0},
    "INSP NORHAZIERAM BINTI ZAKARIA": {"WD": 0, "WE": 0}
}

# Pembahagian Tab
tab1, tab2 = st.tabs(["⚙️ Penjanaan Jadual Baru", "📜 Rekod Sejarah Penugasan"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        bulan = st.selectbox("Pilih Bulan", list(range(1, 13)), index=9)
    with col2:
        tahun = st.number_input("Tahun", min_value=2024, max_value=2030, value=datetime.datetime.now().year)

    num_days = calendar.monthrange(tahun, bulan)[1]
    senarai_tarikh = [datetime.date(tahun, bulan, d) for d in range(1, num_days + 1)]

    st.sidebar.header("🚫 Pengecualian Penugasan")
    pegawai_dikecualikan = st.sidebar.multiselect("Dikecualikan bulan ini:", [p["nama"] for p in PEGAWAI])

    st.sidebar.header("🎉 Tetapan Cuti Umum")
    tarikh_cuti_umum = st.sidebar.multiselect(
        "Pilih tarikh Cuti Umum:",
        options=senarai_tarikh,
        format_func=lambda d: d.strftime("%d/%m/%Y (%A)")
    )

    st.sidebar.header("📌 Special Assignment (Manual Override)")
    override_dict = {}
    senarai_aktif = [p["nama"] for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan]

    for dt in senarai_tarikh:
        is_weekend = dt.weekday() in [5, 6] or dt in tarikh_cuti_umum
        nama_hari = dt.strftime("%A")
        tkh_str = dt.strftime("%d/%m/%Y")
        label_tambahan = " (Cuti Umum)" if dt in tarikh_cuti_umum else ""
        
        if is_weekend:
            sel_s = st.sidebar.selectbox(f"{tkh_str} ({nama_hari}){label_tambahan} - Siang", ["- Auto -"] + senarai_aktif, key=f"{tkh_str}_S")
            if sel_s != "- Auto -":
                override_dict[f"{tkh_str}_Siang"] = sel_s
                
            sel_m = st.sidebar.selectbox(f"{tkh_str} ({nama_hari}){label_tambahan} - Malam", ["- Auto -"] + senarai_aktif, key=f"{tkh_str}_M")
            if sel_m != "- Auto -":
                override_dict[f"{tkh_str}_Malam"] = sel_m
        else:
            sel_b = st.sidebar.selectbox(f"{tkh_str} ({nama_hari}) - Biasa", ["- Auto -"] + senarai_aktif, key=f"{tkh_str}_B")
            if sel_b != "- Auto -":
                override_dict[f"{tkh_str}_Biasa"] = sel_b

    if st.button("🚀 Jana Jadual Penugasan", type="primary"):
        tugas_wd = {p["nama"]: 0 for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan}
        tugas_we = {p["nama"]: 0 for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan}
        pegawai_hari_sebelumnya = set()
        jadual = []

        for k, val in override_dict.items():
            if "_Siang" in k or "_Malam" in k:
                tugas_we[val] += 1
            else:
                tugas_wd[val] += 1

        def pilih_pegawai(is_wknd, elak_set):
            calon = [p for p in senarai_aktif if p not in elak_set]
            
            if bulan == 10 and "INSP MOHD FAIZ BIN ESA" in calon:
                if is_wknd:
                    calon.remove("INSP MOHD FAIZ BIN ESA")
                elif tugas_wd.get("INSP MOHD FAIZ BIN ESA", 0) >= 1:
                    calon.remove("INSP MOHD FAIZ BIN ESA")

            if not calon:
                calon = [p for p in senarai_aktif if p not in elak_set]
                if not calon:
                    calon = [p for p in senarai_aktif]
                
            def dapatkan_skor(nama_pegawai):
                rec = REKOD_SEP_2026.get(nama_pegawai, {"WD": 0, "WE": 0})
                if is_wknd:
                    return (tugas_we[nama_pegawai] * 100) + (rec["WE"] * 10) + (tugas_wd[nama_pegawai] + tugas_we[nama_pegawai])
                else:
                    return (tugas_wd[nama_pegawai] * 100) + (rec["WD"] * 10) + (tugas_wd[nama_pegawai] + tugas_we[nama_pegawai])

            min_skor = min([dapatkan_skor(c) for c in calon])
            final = [c for c in calon if dapatkan_skor(c) == min_skor]
            pilihan = random.choice(final)
            
            if is_wknd:
                tugas_we[pilihan] += 1
            else:
                tugas_wd[pilihan] += 1
                
            return pilihan

        for dt in senarai_tarikh:
            is_weekend = dt.weekday() in [5, 6] or dt in tarikh_cuti_umum
            tkh_str = dt.strftime("%d/%m/%Y")
            hari_str = dt.strftime("%A") + (" (CUTI UMUM)" if dt in tarikh_cuti_umum else "")
            pegawai_hari_ini = set()

            if is_weekend:
                k_s = f"{tkh_str}_Siang"
                p_s = override_dict[k_s] if k_s in override_dict else pilih_pegawai(True, pegawai_hari_sebelumnya)
                pegawai_hari_ini.add(p_s)
                tel_s = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_s)
                jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Siang (0800 - 2000)", "Nama Pegawai": p_s, "No. Telefon": tel_s})

                k_m = f"{tkh_str}_Malam"
                p_m = override_dict[k_m] if k_m in override_dict else pilih_pegawai(True, pegawai_hari_sebelumnya.union(pegawai_hari_ini))
                pegawai_hari_ini.add(p_m)
                tel_m = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_m)
                jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Malam (2000 - 0800)", "Nama Pegawai": p_m, "No. Telefon": tel_m})

            else:
                k_b = f"{tkh_str}_Biasa"
                p_b = override_dict[k_b] if k_b in override_dict else pilih_pegawai(False, pegawai_hari_sebelumnya)
                pegawai_hari_ini.add(p_b)
                tel_b = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_b)
                jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Biasa (1700 - 0800)", "Nama Pegawai": p_b, "No. Telefon": tel_b})

            pegawai_hari_sebelumnya = pegawai_hari_ini

        st.session_state['df_jadual_temp'] = pd.DataFrame(jadual)
        st.session_state['bulan_temp'] = bulan
        st.session_state['tahun_temp'] = tahun

    # Paparan hasil jika sudah dijana
    if 'df_jadual_temp' in st.session_state and st.session_state['bulan_temp'] == bulan and st.session_state['tahun_temp'] == tahun:
        st.subheader(f"📅 Hasil Jadual Penugasan (Bulan {bulan}/{tahun})")
        df_j = st.session_state['df_jadual_temp']
        st.dataframe(df_j, use_container_width=True)

        # Butang Sahkan & Simpan Rekod
        if st.button("🔒 Sahkan & Simpan Jadual Ini", type="secondary"):
            simpan_jadual_db(bulan, tahun, df_j)
            st.success(f"✅ Jadual bagi Bulan {bulan}/{tahun} BERHASIL DISIMPAN ke dalam pangkalan data!")

with tab2:
    st.subheader("📜 Carian Rekod Jadual Yang telah Disahkan")
    col_a, col_b = st.columns(2)
    with col_a:
        bulan_cari = st.selectbox("Pilih Bulan Rekod", list(range(1, 13)), index=9, key="b_cari")
    with col_b:
        tahun_cari = st.number_input("Pilih Tahun Rekod", min_value=2024, max_value=2030, value=2026, key="t_cari")

    df_rekod = ambil_jadual_db(bulan_cari, tahun_cari)
    
    if not df_rekod.empty:
        st.info(f"Rekod Ditemui. Tarikh Disahkan: {df_rekod['Tarikh Disahkan'].iloc[0]}")
        st.dataframe(df_rekod.drop(columns=['Tarikh Disahkan']), use_container_width=True)
        
        # Function Muat Turun CSV
        csv_data = df_rekod.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun Jadual (CSV)",
            data=csv_data,
            file_name=f"Jadual_SBCC_{bulan_cari}_{tahun_cari}.csv",
            mime="text/csv"
        )
    else:
        st.warning(f"Tiada rekod jadual yang disahkan ditemui bagi Bulan {bulan_cari}/{tahun_cari}.")
