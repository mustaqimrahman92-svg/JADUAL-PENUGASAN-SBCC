import streamlit as st
import pandas as pd
import datetime
import calendar
import random
import sqlite3

st.set_page_config(page_title="Sistem Penugasan SBCC IPK Selangor", layout="wide")

# ==========================================
# 1. FUNGSI PANGKALAN DATA (SQLITE)
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
    c.execute("DELETE FROM rekod_jadual WHERE bulan = ? AND tahun = ?", (bulan, tahun))
    
    tarikh_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for _, row in df_jadual.iterrows():
        c.execute('''
            INSERT INTO rekod_jadual (bulan, tahun, tarikh, hari, syif, nama_pegawai, no_tel, tarikh_disahkan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bulan, tahun, row['Tarikh'], row['Hari'], row['Syif / Masa'], row['Nama Pegawai'], row['No. Telefon'], tarikh_sekarang))
    
    conn.commit()
    conn.close()

def padam_jadual_db(bulan, tahun):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM rekod_jadual WHERE bulan = ? AND tahun = ?", (bulan, tahun))
    conn.commit()
    conn.close()

def ambil_jadual_db(bulan, tahun):
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT tarikh AS Tarikh, hari AS Hari, syif AS 'Syif / Masa', nama_pegawai AS 'Nama Pegawai', no_tel AS 'No. Telefon', tarikh_disahkan AS 'Tarikh Disahkan' FROM rekod_jadual WHERE bulan = ? AND tahun = ?"
    df = pd.read_sql_query(query, conn, params=(bulan, tahun))
    conn.close()
    return df

def is_pegawai_wanita(nama):
    nama_upper = nama.upper()
    kata_kunci_wanita = [" BINTI ", " BT ", " A/P ", " KAUR "]
    return any(k in f" {nama_upper} " for k in kata_kunci_wanita)

def jana_html_lampiran_a(df_jadual, bulan, tahun):
    nama_bulan_map = {
        1: "JAN", 2: "FEB", 3: "MAC", 4: "APR", 5: "MEI", 6: "JUN",
        7: "JUL", 8: "OGOS", 9: "SEP", 10: "OKT", 11: "NOV", 12: "DIS"
    }
    bln_str = nama_bulan_map.get(bulan, "SEP")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 11px; }}
        .header {{ text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 12px; }}
        .lampiran {{ float: right; font-weight: bold; text-decoration: underline; font-size: 11px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid black; padding: 4px 6px; text-align: center; }}
        th {{ background-color: #e0e0e0; font-weight: bold; }}
        .text-left {{ text-align: left; }}
    </style>
    </head>
    <body>
        <div class="lampiran">LAMPIRAN 'A'</div>
        <div style="clear:both;"></div>
        <div class="header">
            JADUAL PEGAWAI BERTUGAS<br>
            SBCC IPK SELANGOR BAGI BULAN {bln_str} {tahun}
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 4%;">BIL</th>
                    <th style="width: 16%;">TKH / MASA</th>
                    <th style="width: 12%;">HARI</th>
                    <th style="width: 48%;">NAMA PEGAWAI</th>
                    <th style="width: 20%;">NO TELEFON</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for idx, row in df_jadual.iterrows():
        bil = f"{idx+1:02d}."
        masa = "1700 - 0800"
        if "Siang" in row['Syif / Masa']:
            masa = "0800 - 2000"
        elif "Malam" in row['Syif / Masa']:
            masa = "2000 - 0800"
            
        tkh_masa = f"{row['Tarikh']}<br>{masa}"
        hari = row['Hari'].upper()
        nama = row['Nama Pegawai']
        no_tel = f"({row['No. Telefon']})"
        
        html += f"""
            <tr>
                <td>{bil}</td>
                <td>{tkh_masa}</td>
                <td>{hari}</td>
                <td class="text-left"><b>{nama}</b></td>
                <td>{no_tel}</td>
            </tr>
        """
        
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html

init_db()

# ==========================================
# 2. SENARAI PEGAWAI & REKOD SEJARAH (PDF TEPAT)
# ==========================================
st.title("📋 Sistem Penugasan SBCC IPK Selangor")

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

# REKOD SEPTEMBER 2026 TEPAT MENGIKUT DOKUMEN PDF
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
    "INSP KASHMINDEJRIT KAUR A/P CHARLES": {"WD": 1, "WE": 0},
    "INSP FAIZ BIN BASAR": {"WD": 1, "WE": 0},
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

# ==========================================
# 3. ANTARAMUKA STREAMLIT
# ==========================================
tab1, tab2 = st.tabs(["⚙️ Penjanaan Jadual Baru", "📜 Rekod Sejarah & Format Cetak"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        bulan = st.selectbox("Pilih Bulan", list(range(1, 13)), index=9)
    with col2:
        tahun = st.number_input("Tahun", min_value=2024, max_value=2030, value=datetime.datetime.now().year)

    num_days = calendar.monthrange(tahun, bulan)[1]
    senarai_tarikh = [datetime.date(tahun, bulan, d) for d in range(1, num_days + 1)]

    st.sidebar.header("🔄 Tetapan Giliran (Rotation)")
    aktif_giliran_lelaki = st.sidebar.checkbox("Aktifkan Giliran WE/WD Pegawai Lelaki", value=True)

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
        pegawai_tugas_jumaat = set()
        pegawai_hari_sebelumnya = set()
        jadual = []

        bulan_lepas = 12 if bulan == 1 else bulan - 1
        tahun_lepas = tahun - 1 if bulan == 1 else tahun
        
        rekod_bulan_lepas = {}
        if bulan_lepas == 9 and tahun_lepas == 2026:
            rekod_bulan_lepas = REKOD_SEP_2026
        else:
            df_bln_lepas = ambil_jadual_db(bulan_lepas, tahun_lepas)
            if not df_bln_lepas.empty:
                for p in PEGAWAI:
                    nm = p["nama"]
                    df_p = df_bln_lepas[df_bln_lepas['Nama Pegawai'] == nm]
                    wd_cnt = 0
                    we_cnt = 0
                    for _, r in df_p.iterrows():
                        if "Siang" in r['Syif / Masa'] or "Malam" in r['Syif / Masa'] or "CUTI UMUM" in r['Hari']:
                            we_cnt += 1
                        else:
                            wd_cnt += 1
                    rekod_bulan_lepas[nm] = {"WD": wd_cnt, "WE": we_cnt}

        # ----------------------------------------------------
        # FUNGSI PEMILIHAN PEGAWAI (BEBAS BUG DYNAMIC CAP)
        # ----------------------------------------------------
        def pilih_pegawai(is_wknd, elak_set, is_jumaat=False):
            calon = [p for p in senarai_aktif if p not in elak_set]

            # STEP 1: TAPIS HAD MAKSIMUM TUGASAN DINAMIK (MUTLAK)
            def dapatkan_had_maksimum(nama_pegawai):
                rec_lepas = rekod_bulan_lepas.get(nama_pegawai, {"WD": 0, "WE": 0})
                jumlah_lepas = rec_lepas.get("WD", 0) + rec_lepas.get("WE", 0)
                return 1 if jumlah_lepas >= 2 else 2

            calon_cap = [
                p for p in calon 
                if (tugas_wd.get(p, 0) + tugas_we.get(p, 0)) < dapatkan_had_maksimum(p)
            ]
            
            # Kekalkan HANYA calon yang belum capai had
            if calon_cap:
                calon = calon_cap

            # STEP 2: SEKATAN KHAS INSP FAIZ
            if bulan == 10 and "INSP MOHD FAIZ BIN ESA" in calon:
                if is_wknd or tugas_wd.get("INSP MOHD FAIZ BIN ESA", 0) >= 1:
                    if len(calon) > 1:
                        calon = [p for p in calon if p != "INSP MOHD FAIZ BIN ESA"]

            # STEP 3: PENAPISAN GILIRAN LELAKI WE/WD
            if aktif_giliran_lelaki:
                if is_wknd:
                    calon_sub = [
                        p for p in calon
                        if is_pegawai_wanita(p) or rekod_bulan_lepas.get(p, {}).get("WE", 0) == 0
                    ]
                else:
                    calon_sub = [
                        p for p in calon
                        if not is_pegawai_wanita(p) and rekod_bulan_lepas.get(p, {}).get("WE", 0) > 0
                    ]
                
                if calon_sub:
                    calon = calon_sub

            # STEP 4: PENAPISAN SYIF JUMAAT
            if is_wknd:
                calon_no_jumaat = [p for p in calon if p not in pegawai_tugas_jumaat]
                if calon_no_jumaat:
                    calon = calon_no_jumaat

            # FALLBACK KESELAMATAN (MENGELAKKAN SENARAI KOSONG)
            if not calon:
                calon = [p for p in senarai_aktif if p not in elak_set] or senarai_aktif

            # STEP 5: PENGIRAAN SKOR & PEMILIHAN PEGAWAI
            def dapatkan_skor(nama_pegawai):
                rec = rekod_bulan_lepas.get(nama_pegawai, {"WD": 0, "WE": 0})
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

            if is_jumaat:
                pegawai_tugas_jumaat.add(pilihan)

            return pilihan

        # ----------------------------------------------------
        # GELUNG UTAMA MENGIKUT KRONOLOGI TARIKH
        # ----------------------------------------------------
        for dt in senarai_tarikh:
            is_weekend = dt.weekday() in [5, 6] or dt in tarikh_cuti_umum
            is_jumaat = (dt.weekday() == 4 and dt not in tarikh_cuti_umum)
            tkh_str = dt.strftime("%d/%m/%Y")
            hari_str = dt.strftime("%A") + (" (CUTI UMUM)" if dt in tarikh_cuti_umum else "")
            pegawai_hari_ini = set()

            if is_weekend:
                # 1. Syif Siang
                k_s = f"{tkh_str}_Siang"
                if k_s in override_dict:
                    p_s = override_dict[k_s]
                    tugas_we[p_s] += 1  # Kemas kini kaunter terus secara rasmi
                else:
                    p_s = pilih_pegawai(True, pegawai_hari_sebelumnya)

                pegawai_hari_ini.add(p_s)
                tel_s = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_s)
                jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Siang (0800 - 2000)", "Nama Pegawai": p_s, "No. Telefon": tel_s})

                # 2. Syif Malam
                k_m = f"{tkh_str}_Malam"
                if k_m in override_dict:
                    p_m = override_dict[k_m]
                    tugas_we[p_m] += 1  # Kemas kini kaunter terus secara rasmi
                else:
                    p_m = pilih_pegawai(True, pegawai_hari_sebelumnya.union(pegawai_hari_ini))

                pegawai_hari_ini.add(p_m)
                tel_m = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_m)
                jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Malam (2000 - 0800)", "Nama Pegawai": p_m, "No. Telefon": tel_m})

            else:
                # 3. Syif Biasa (Weekday)
                k_b = f"{tkh_str}_Biasa"
                if k_b in override_dict:
                    p_b = override_dict[k_b]
                    tugas_wd[p_b] += 1  # Kemas kini kaunter terus secara rasmi
                    if is_jumaat:
                        pegawai_tugas_jumaat.add(p_b)
                else:
                    p_b = pilih_pegawai(False, pegawai_hari_sebelumnya, is_jumaat=is_jumaat)

                pegawai_hari_ini.add(p_b)
                tel_b = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_b)
                jadual.append({"Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Biasa (1700 - 0800)", "Nama Pegawai": p_b, "No. Telefon": tel_b})

            pegawai_hari_sebelumnya = pegawai_hari_ini

        st.session_state['df_jadual_temp'] = pd.DataFrame(jadual)
        st.session_state['bulan_temp'] = bulan
        st.session_state['tahun_temp'] = tahun

    if 'df_jadual_temp' in st.session_state and st.session_state['bulan_temp'] == bulan and st.session_state['tahun_temp'] == tahun:
        df_j = st.session_state['df_jadual_temp']
        
        st.subheader(f"📅 Hasil Jadual Penugasan (Bulan {bulan}/{tahun})")
        st.dataframe(df_j, use_container_width=True)

        if st.button("🔒 Sahkan & Simpan Jadual Ini", type="secondary"):
            simpan_jadual_db(bulan, tahun, df_j)
            st.success(f"✅ Jadual bagi Bulan {bulan}/{tahun} BERHASIL DISIMPAN ke dalam pangkalan data!")

with tab2:
    st.subheader("📜 Carian & Paparan Format Cetak (Lampiran 'A')")
    col_a, col_b = st.columns(2)
    with col_a:
        bulan_cari = st.selectbox("Pilih Bulan Rekod", list(range(1, 13)), index=8, key="b_cari")
    with col_b:
        tahun_cari = st.number_input("Pilih Tahun Rekod", min_value=2024, max_value=2030, value=2026, key="t_cari")

    df_rekod = ambil_jadual_db(bulan_cari, tahun_cari)
    
    if not df_rekod.empty:
        st.info(f"Rekod Ditemui. Tarikh Disahkan: {df_rekod['Tarikh Disahkan'].iloc[0]}")
        
        html_code = jana_html_lampiran_a(df_rekod, bulan_cari, tahun_cari)
        
        col_dl1, col_dl2, col_del = st.columns([1, 1, 1])
        with col_dl1:
            st.download_button(
                label="🖨️ Muat Turun Format Cetakan Lampiran 'A' (HTML)",
                data=html_code,
                file_name=f"Lampiran_A_SBCC_{bulan_cari}_{tahun_cari}.html",
                mime="text/html"
            )
        with col_dl2:
            csv_data = df_rekod.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Muat Turun Data Asal (CSV)",
                data=csv_data,
                file_name=f"Jadual_SBCC_{bulan_cari}_{tahun_cari}.csv",
                mime="text/csv"
            )
        with col_del:
            if st.button("🗑️ Padam Rekod Disahkan Ini", type="primary"):
                padam_jadual_db(bulan_cari, tahun_cari)
                st.success(f"🗑️ Rekod jadual bagi Bulan {bulan_cari}/{tahun_cari} telah dipadam daripada pangkalan data.")
                st.rerun()

        st.markdown("---")
        st.subheader(f"📊 Statistik Kekerapan Penugasan (Bulan {bulan_cari}/{tahun_cari})")
        
        stat_list = []
        for idx, p in enumerate(PEGAWAI, start=1):
            nama_p = p["nama"]
            df_p = df_rekod[df_rekod['Nama Pegawai'] == nama_p]
            
            wd_count = 0
            we_count = 0

            for _, r in df_p.iterrows():
                is_wk = ("Siang" in r['Syif / Masa'] or "Malam" in r['Syif / Masa'] or "CUTI UMUM" in r['Hari'])
                if is_wk:
                    we_count += 1
                else:
                    wd_count += 1

            if wd_count == 0 and we_count == 0 and bulan_cari == 9 and tahun_cari == 2026:
                rec_sep = REKOD_SEP_2026.get(nama_p, {"WD": 0, "WE": 0})
                wd_count = rec_sep["WD"]
                we_count = rec_sep["WE"]

            jantina = "Wanita" if is_pegawai_wanita(nama_p) else "Lelaki"

            stat_list.append({
                "BIL": f"{idx:02d}.",
                "NAMA PEGAWAI": nama_p,
                "JANTINA": jantina,
                "WEEKDAY (HARI BIASA)": wd_count,
                "WEEKEND / CUTI UMUM": we_count,
                "JUMLAH KEKERAPAN TUGAS": wd_count + we_count
            })

        df_stat = pd.DataFrame(stat_list)
        st.dataframe(df_stat, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("📄 Pratonton Dokumen Cetakan (Format Lampiran 'A'):")
        st.components.v1.html(html_code, height=600, scrolling=True)

    else:
        st.warning(f"Tiada rekod jadual yang disahkan ditemui bagi Bulan {bulan_cari}/{tahun_cari}.")
