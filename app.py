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
            no_tel_pegawai TEXT,
            nama_penolong TEXT,
            no_tel_penolong TEXT,
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
            INSERT INTO rekod_jadual (bulan, tahun, tarikh, hari, syif, nama_pegawai, no_tel_pegawai, nama_penolong, no_tel_penolong, tarikh_disahkan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bulan, tahun, row['Tarikh'], row['Hari'], row['Syif / Masa'], row['Nama Pegawai'], row['No. Tel Pegawai'], row['Nama Penolong'], row['No. Tel Penolong'], tarikh_sekarang))
    
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
    query = """
        SELECT tarikh AS Tarikh, hari AS Hari, syif AS 'Syif / Masa', 
               nama_pegawai AS 'Nama Pegawai', no_tel_pegawai AS 'No. Tel Pegawai',
               nama_penolong AS 'Nama Penolong', no_tel_penolong AS 'No. Tel Penolong',
               tarikh_disahkan AS 'Tarikh Disahkan' 
        FROM rekod_jadual WHERE bulan = ? AND tahun = ?
    """
    df = pd.read_sql_query(query, conn, params=(bulan, tahun))
    conn.close()
    return df

def is_pegawai_wanita(nama):
    nama_upper = nama.upper()
    kata_kunci_wanita = [" BINTI ", " BT ", " A/P ", " KAUR ", " LO YEE TYNG ", " YVONNE KUA "]
    return any(k in f" {nama_upper} " for k in kata_kunci_wanita)

# ----------------------------------------------------
# FUNGSI LAMPIRAN 'A' (VERSI GABUNG PEGAWAI & PENOLONG)
# ----------------------------------------------------
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
        @page {{ size: A4 portrait; margin: 10mm; }}
        body {{ font-family: Arial, sans-serif; font-size: 10px; color: #000; }}
        .header {{ text-align: center; font-weight: bold; margin-bottom: 12px; font-size: 11px; line-height: 1.3; }}
        .lampiran {{ float: right; font-weight: bold; text-decoration: underline; font-size: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; page-break-inside: auto; }}
        tr {{ page-break-inside: avoid; page-break-after: auto; }}
        th, td {{ border: 1px solid black; padding: 5px 6px; text-align: center; vertical-align: middle; }}
        th {{ background-color: #e0e0e0; font-weight: bold; font-size: 10px; }}
        .text-left {{ text-align: left; }}
        .jawatan {{ font-size: 9px; color: #333; font-style: italic; }}
    </style>
    </head>
    <body>
        <div class="lampiran">LAMPIRAN 'A'</div>
        <div style="clear:both;"></div>
        <div class="header">
            JADUAL PEGAWAI & PENOLONG PEGAWAI BERTUGAS<br>
            SBCC IPK SELANGOR BAGI BULAN {bln_str} {tahun}
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 5%;">BIL</th>
                    <th style="width: 18%;">TKH / MASA</th>
                    <th style="width: 12%;">HARI</th>
                    <th style="width: 65%;">PEGAWAI & PENOLONG PEGAWAI BERTUGAS</th>
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
        
        petak_gabung = f"""
            <b>1. {row['Nama Pegawai']}</b> <span class="jawatan">(Pegawai Bertugas)</span><br>
            &nbsp;&nbsp;&nbsp;&nbsp;<b>No. Tel:</b> {row['No. Tel Pegawai']}<br>
            <div style="margin-top:3px; border-top: 1px dotted #ccc; padding-top: 3px;">
            <b>2. {row['Nama Penolong']}</b> <span class="jawatan">(Penolong Pegawai Bertugas)</span><br>
            &nbsp;&nbsp;&nbsp;&nbsp;<b>No. Tel:</b> {row['No. Tel Penolong']}
            </div>
        """
        
        html += f"""
            <tr>
                <td>{bil}</td>
                <td>{tkh_masa}</td>
                <td>{hari}</td>
                <td class="text-left">{petak_gabung}</td>
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
# 2. SENARAI DATA PEGAWAI & PENOLONG PEGAWAI
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

PENOLONG_PEGAWAI = [
    {"nama": "SJN/D HAFIZATUL AMIRA BT ADBUL MANAF", "no_tel": "019-5493007"},
    {"nama": "SJN/D AHMAD ZAMANE BIN OMAR", "no_tel": "013-4939452"},
    {"nama": "SJN/D ZAMRI BIN BAKARI", "no_tel": "013-2893878"},
    {"nama": "KPL/D MUHAMMAD AZKA FATIN BIN MOHD NORDIN", "no_tel": "016-2198068"},
    {"nama": "KPL/D MUHAMMAD ZULFFY BIN RASHID", "no_tel": "013-4080883"},
    {"nama": "KPL/D MUHAMMAD FIRDAUS BIN AMRAN", "no_tel": "013-7783677"},
    {"nama": "KPL/D HAZIZAT BIN ATTAN", "no_tel": "013-5744426"},
    {"nama": "SJN/D ONG WEI TAU", "no_tel": "012-8121981"},
    {"nama": "KPL/D MOHD FAIZAL BIN TIMAN", "no_tel": "017-7455348"},
    {"nama": "KPL/D JEEVAN A/L VADIAHLAGAN", "no_tel": "013-5638303"},
    {"nama": "KPL/D MOHD SYAIFUL AZHAR BIN MOHD HANAFIAH", "no_tel": "011-51105497"},
    {"nama": "SJN/D SYEAFUUL AZNRY BIN ZAMBRI", "no_tel": "012-7637889"},
    {"nama": "SJN/D ZAMZUHAIRI BIN TOMIRAN", "no_tel": "012-2712700"},
    {"nama": "SJN/D YUSRI BIN WAHAB", "no_tel": "019-3876720"},
    {"nama": "KPL/D MOHD YUSRI BIN ABU SEMAN", "no_tel": "017-9278564"},
    {"nama": "KPL/D MUHAMMAD AZRUL SHAFIQ BIN ISMAN", "no_tel": "019-5898658"},
    {"nama": "KPL/D FARIEZUL NAIM BIN MOHD SANI", "no_tel": "013-6399275"},
    {"nama": "L/KPL/D MOHAMMAD ARRYAN JUING BIN ABDULLAH", "no_tel": "019-4334734"},
    {"nama": "SJN/D HAFENDI BIN HANAFIAH", "no_tel": "012-3784305"},
    {"nama": "SJN/D EFFARINA BIN AHMAD SUHAIMI", "no_tel": "018-9154504"},
    {"nama": "KPL/D NOOR HAZWANI BINTI MUHAMAD RUSLI", "no_tel": "019-2217116"},
    {"nama": "KPL/D WELLINGTON RICHARD ANAK SADOK", "no_tel": "011-29994591"},
    {"nama": "SJN/D NOOR HAKIMI BIN ZULKIFLI", "no_tel": "012-6949107"},
    {"nama": "SJN/D SUYANI BINTI MAT SAAD", "no_tel": "012-3405606"},
    {"nama": "SJN/D MOHD JURAIDI BIN SAMSUDIN", "no_tel": "012-6769745"},
    {"nama": "SJN/D VASTERMORAILE ANAK MONDAY", "no_tel": "017-7058084"},
    {"nama": "KPL/D LO YEE TYNG", "no_tel": "016-8374537"},
    {"nama": "KPL/D MUHAMMAD SYUKRI BIN ZULKIFLI", "no_tel": "012-6196573"},
    {"nama": "KPL/D YVONNE KUA CHEE WEI", "no_tel": "011-10905627"},
    {"nama": "KPL/D MOHAMAD PARIS BIN ROMELI", "no_tel": "017-3864533"},
    {"nama": "KPL/D RIZQI ALFIAN BIN KOMIN", "no_tel": "011-23246744"},
    {"nama": "L/KPL/D NURHIDAYAH BINTI SUHAMI", "no_tel": "017-7011952"},
    {"nama": "KONS NUR AMIERA BINTI MOHAMAD ALI AHAN", "no_tel": "017-6723075"},
    {"nama": "L/KPL AHMAD HELMI HARIRI BIN SALVEHUJRAIE", "no_tel": "0111-66522645"},
    {"nama": "SJN/D JAAFAR BIN MA HASAN", "no_tel": "011-11474013"},
    {"nama": "P/SJN/D ASRUL AZWANDI BIN AHMAD", "no_tel": "019-4636430"},
    {"nama": "KPL/D MOHD KHAIROL ANUAR BIN MOHAMED", "no_tel": "010-4358116"},
    {"nama": "KPL/D ABDUL HALIM BIN KAMARUDDIN", "no_tel": "013-2425850"},
    {"nama": "L/KPL/D KOLOZUM SAFINAH BINTI VARUSAI", "no_tel": "011-65670875"},
    {"nama": "L/KPL ATHIRAH NABILA BINTI SAEDIN", "no_tel": "018-3166724"},
    {"nama": "L/KPL/D HANA LYDIA BINTI LIERON", "no_tel": "018-8709538"},
    {"nama": "SJN/D SHAHRUL IDHAM BIN MD SALIM", "no_tel": "014-2440181"},
    {"nama": "KPL/D MOHD KHAIROL IZDZUAN BIN MOHAMAD ZAHARI", "no_tel": "012-2796394"},
    {"nama": "KPL/D SUFIAN BIN ISMAIL", "no_tel": "017-6217662"},
    {"nama": "KPL/D NELSON ANAK NUING", "no_tel": "017-3655175"},
    {"nama": "KPL/D MOHAMAD HAFIS BIN SALLEH", "no_tel": "013-4928247"},
    {"nama": "L/KPL/D MUHAMMAD ABDUL WAFIE HAZIQ BIN HAMDAN", "no_tel": "017-5431206"}
]

PENOLONG_DIKECUALIKAN_DEFAULT = [
    "KPL/D FITRI HAMIZAN BIN MOHD SHUKRI",
    "KPL/D MOHD AZHARI BIN ABD KARIM",
    "SJN/D MUHD FAIRUL BIN SIDI AHMAD",
    "KPL/D BENNY DENESIUS",
    "KPL/D MOHD TAUFIQ BIN NORHISHAM",
    "KPL/D MUHAMAD HANAFI BIN ZAINOL"
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

    st.sidebar.header("🔄 Tetapan Giliran")
    aktif_giliran_lelaki = st.sidebar.checkbox("Aktifkan Giliran WE/WD Pegawai Lelaki", value=True)

    st.sidebar.header("🚫 Pengecualian Tugas Pegawai (Insp)")
    pegawai_dikecualikan = st.sidebar.multiselect("Pegawai Dikecualikan:", [p["nama"] for p in PEGAWAI])

    st.sidebar.header("🚫 Pengecualian Tugas Penolong Pegawai")
    penolong_dikecualikan = st.sidebar.multiselect(
        "Penolong Pegawai Dikecualikan:",
        [p["nama"] for p in PENOLONG_PEGAWAI],
        default=[p for p in PENOLONG_DIKECUALIKAN_DEFAULT if any(x["nama"] == p for x in PENOLONG_PEGAWAI)]
    )

    st.sidebar.header("🎉 Tetapan Cuti Umum")
    tarikh_cuti_umum = st.sidebar.multiselect(
        "Pilih tarikh Cuti Umum:",
        options=senarai_tarikh,
        format_func=lambda d: d.strftime("%d/%m/%Y (%A)")
    )

    st.sidebar.header("📌 Special Assignment (Manual Override)")
    override_pegawai = {}
    override_penolong = {}
    
    senarai_pegawai_aktif = [p["nama"] for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan]
    senarai_penolong_aktif = [p["nama"] for p in PENOLONG_PEGAWAI if p["nama"] not in penolong_dikecualikan]

    with st.sidebar.expander("Tetapan Manual Override (Jika Ada)"):
        for dt in senarai_tarikh:
            is_weekend = dt.weekday() in [5, 6] or dt in tarikh_cuti_umum
            tkh_str = dt.strftime("%d/%m/%Y")
            
            if is_weekend:
                s_peg = st.selectbox(f"{tkh_str} (Siang) - Pegawai", ["- Auto -"] + senarai_pegawai_aktif, key=f"peg_{tkh_str}_S")
                if s_peg != "- Auto -": override_pegawai[f"{tkh_str}_Siang"] = s_peg
                
                s_pen = st.selectbox(f"{tkh_str} (Siang) - Penolong", ["- Auto -"] + senarai_penolong_aktif, key=f"pen_{tkh_str}_S")
                if s_pen != "- Auto -": override_penolong[f"{tkh_str}_Siang"] = s_pen

                m_peg = st.selectbox(f"{tkh_str} (Malam) - Pegawai", ["- Auto -"] + senarai_pegawai_aktif, key=f"peg_{tkh_str}_M")
                if m_peg != "- Auto -": override_pegawai[f"{tkh_str}_Malam"] = m_peg
                
                m_pen = st.selectbox(f"{tkh_str} (Malam) - Penolong", ["- Auto -"] + senarai_penolong_aktif, key=f"pen_{tkh_str}_M")
                if m_pen != "- Auto -": override_penolong[f"{tkh_str}_Malam"] = m_pen
            else:
                b_peg = st.selectbox(f"{tkh_str} (Biasa) - Pegawai", ["- Auto -"] + senarai_pegawai_aktif, key=f"peg_{tkh_str}_B")
                if b_peg != "- Auto -": override_pegawai[f"{tkh_str}_Biasa"] = b_peg
                
                b_pen = st.selectbox(f"{tkh_str} (Biasa) - Penolong", ["- Auto -"] + senarai_penolong_aktif, key=f"pen_{tkh_str}_B")
                if b_pen != "- Auto -": override_penolong[f"{tkh_str}_Biasa"] = b_pen

    if st.button("🚀 Jana Jadual Penugasan", type="primary"):
        tugas_wd_peg = {p["nama"]: 0 for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan}
        tugas_we_peg = {p["nama"]: 0 for p in PEGAWAI if p["nama"] not in pegawai_dikecualikan}
        
        tugas_penolong = {p["nama"]: 0 for p in PENOLONG_PEGAWAI if p["nama"] not in penolong_dikecualikan}

        pegawai_tugas_jumaat = set()
        pegawai_hari_sebelumnya = set()
        penolong_hari_sebelumnya = set()
        jadual = []

        bulan_lepas = 12 if bulan == 1 else bulan - 1
        tahun_lepas = tahun - 1 if bulan == 1 else tahun
        
        rekod_bulan_lepas = REKOD_SEP_2026 if (bulan_lepas == 9 and tahun_lepas == 2026) else {}

        # Pemilihan Pegawai (Insp)
        def pilih_pegawai(is_wknd, elak_set, is_jumaat=False):
            calon = [p for p in senarai_pegawai_aktif if p not in elak_set]

            def dapatkan_had_maksimum(nama_pegawai):
                rec_lepas = rekod_bulan_lepas.get(nama_pegawai, {"WD": 0, "WE": 0})
                jumlah_lepas = rec_lepas.get("WD", 0) + rec_lepas.get("WE", 0)
                return 1 if jumlah_lepas >= 2 else 2

            calon_cap = [p for p in calon if (tugas_wd_peg.get(p, 0) + tugas_we_peg.get(p, 0)) < dapatkan_had_maksimum(p)]
            if calon_cap: calon = calon_cap

            if bulan == 10 and "INSP MOHD FAIZ BIN ESA" in calon:
                if is_wknd or tugas_wd_peg.get("INSP MOHD FAIZ BIN ESA", 0) >= 1:
                    if len(calon) > 1: calon = [p for p in calon if p != "INSP MOHD FAIZ BIN ESA"]

            if aktif_giliran_lelaki:
                if is_wknd:
                    calon_we = []
                    for p in calon:
                        rec_we_lepas = rekod_bulan_lepas.get(p, {}).get("WE", 0)
                        sudah_we = tugas_we_peg.get(p, 0)
                        if is_pegawai_wanita(p):
                            if sudah_we < 1: calon_we.append(p)
                        else:
                            if rec_we_lepas == 0 and sudah_we < 1: calon_we.append(p)
                    if calon_we: calon = calon_we
                else:
                    calon_wd = [p for p in calon if not is_pegawai_wanita(p) and rekod_bulan_lepas.get(p, {}).get("WE", 0) > 0]
                    if len(calon_wd) >= 1: calon = calon_wd

            if is_wknd:
                calon_no_jumaat = [p for p in calon if p not in pegawai_tugas_jumaat]
                if calon_no_jumaat: calon = calon_no_jumaat

            if not calon: calon = [p for p in senarai_pegawai_aktif if p not in elak_set] or senarai_pegawai_aktif

            def dapatkan_skor(nama_pegawai):
                rec = rekod_bulan_lepas.get(nama_pegawai, {"WD": 0, "WE": 0})
                if is_wknd:
                    return (tugas_we_peg[nama_pegawai] * 100) + (rec["WE"] * 10) + (tugas_wd_peg[nama_pegawai] + tugas_we_peg[nama_pegawai])
                else:
                    return (tugas_wd_peg[nama_pegawai] * 100) + (rec["WD"] * 10) + (tugas_wd_peg[nama_pegawai] + tugas_we_peg[nama_pegawai])

            min_skor = min([dapatkan_skor(c) for c in calon])
            final = [c for c in calon if dapatkan_skor(c) == min_skor]
            pilihan = random.choice(final)

            if is_wknd: tugas_we_peg[pilihan] += 1
            else: tugas_wd_peg[pilihan] += 1

            if is_jumaat: pegawai_tugas_jumaat.add(pilihan)
            return pilihan

        # Pemilihan Penolong Pegawai (Had 1 Kali Sebulan)
        def pilih_penolong(elak_set):
            calon = [p for p in senarai_penolong_aktif if p not in elak_set]
            calon_1kali = [p for p in calon if tugas_penolong.get(p, 0) < 1]
            if calon_1kali: calon = calon_1kali
            if not calon: calon = [p for p in senarai_penolong_aktif if p not in elak_set] or senarai_penolong_aktif

            min_tugas = min([tugas_penolong[c] for c in calon])
            final = [c for c in calon if tugas_penolong[c] == min_tugas]
            pilihan = random.choice(final)
            tugas_penolong[pilihan] += 1
            return pilihan

        # Gelung Penjana Jadual
        for dt in senarai_tarikh:
            is_weekend = dt.weekday() in [5, 6] or dt in tarikh_cuti_umum
            is_jumaat = (dt.weekday() == 4 and dt not in tarikh_cuti_umum)
            tkh_str = dt.strftime("%d/%m/%Y")
            hari_str = dt.strftime("%A") + (" (CUTI UMUM)" if dt in tarikh_cuti_umum else "")
            
            pegawai_hari_ini = set()
            penolong_hari_ini = set()

            if is_weekend:
                # Syif Siang
                p_s = override_pegawai.get(f"{tkh_str}_Siang") or pilih_pegawai(True, pegawai_hari_sebelumnya)
                if f"{tkh_str}_Siang" in override_pegawai: tugas_we_peg[p_s] += 1
                pegawai_hari_ini.add(p_s)

                pen_s = override_penolong.get(f"{tkh_str}_Siang") or pilih_penolong(penolong_hari_sebelumnya)
                if f"{tkh_str}_Siang" in override_penolong: tugas_penolong[pen_s] += 1
                penolong_hari_ini.add(pen_s)

                tel_p_s = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_s)
                tel_pen_s = next(p["no_tel"] for p in PENOLONG_PEGAWAI if p["nama"] == pen_s)

                jadual.append({
                    "Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Siang (0800 - 2000)",
                    "Nama Pegawai": p_s, "No. Tel Pegawai": tel_p_s,
                    "Nama Penolong": pen_s, "No. Tel Penolong": tel_pen_s
                })

                # Syif Malam
                p_m = override_pegawai.get(f"{tkh_str}_Malam") or pilih_pegawai(True, pegawai_hari_sebelumnya.union(pegawai_hari_ini))
                if f"{tkh_str}_Malam" in override_pegawai: tugas_we_peg[p_m] += 1
                pegawai_hari_ini.add(p_m)

                pen_m = override_penolong.get(f"{tkh_str}_Malam") or pilih_penolong(penolong_hari_sebelumnya.union(penolong_hari_ini))
                if f"{tkh_str}_Malam" in override_penolong: tugas_penolong[pen_m] += 1
                penolong_hari_ini.add(pen_m)

                tel_p_m = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_m)
                tel_pen_m = next(p["no_tel"] for p in PENOLONG_PEGAWAI if p["nama"] == pen_m)

                jadual.append({
                    "Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Malam (2000 - 0800)",
                    "Nama Pegawai": p_m, "No. Tel Pegawai": tel_p_m,
                    "Nama Penolong": pen_m, "No. Tel Penolong": tel_pen_m
                })

            else:
                # Syif Biasa
                p_b = override_pegawai.get(f"{tkh_str}_Biasa") or pilih_pegawai(False, pegawai_hari_sebelumnya, is_jumaat=is_jumaat)
                if f"{tkh_str}_Biasa" in override_pegawai: 
                    tugas_wd_peg[p_b] += 1
                    if is_jumaat: pegawai_tugas_jumaat.add(p_b)
                pegawai_hari_ini.add(p_b)

                pen_b = override_penolong.get(f"{tkh_str}_Biasa") or pilih_penolong(penolong_hari_sebelumnya)
                if f"{tkh_str}_Biasa" in override_penolong: tugas_penolong[pen_b] += 1
                penolong_hari_ini.add(pen_b)

                tel_p_b = next(p["no_tel"] for p in PEGAWAI if p["nama"] == p_b)
                tel_pen_b = next(p["no_tel"] for p in PENOLONG_PEGAWAI if p["nama"] == pen_b)

                jadual.append({
                    "Tarikh": tkh_str, "Hari": hari_str, "Syif / Masa": "Biasa (1700 - 0800)",
                    "Nama Pegawai": p_b, "No. Tel Pegawai": tel_p_b,
                    "Nama Penolong": pen_b, "No. Tel Penolong": tel_pen_b
                })

            pegawai_hari_sebelumnya = pegawai_hari_ini
            penolong_hari_sebelumnya = penolong_hari_ini

        st.session_state['df_jadual_temp'] = pd.DataFrame(jadual)
        st.session_state['bulan_temp'] = bulan
        st.session_state['tahun_temp'] = tahun

    if 'df_jadual_temp' in st.session_state and st.session_state['bulan_temp'] == bulan and st.session_state['tahun_temp'] == tahun:
        df_j = st.session_state['df_jadual_temp']
        st.subheader(f"📅 Hasil Jadual Penugasan (Bulan {bulan}/{tahun})")
        st.dataframe(df_j, use_container_width=True)

        if st.button("🔒 Sahkan & Simpan Jadual Ini", type="secondary"):
            simpan_jadual_db(bulan, tahun, df_j)
            st.success(f"✅ Jadual bagi Bulan {bulan}/{tahun} BERHASIL DISIMPAN!")

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
            st.download_button("🖨️ Muat Turun Format Lampiran 'A' (HTML)", html_code, f"Lampiran_A_SBCC_{bulan_cari}_{tahun_cari}.html", "text/html")
        with col_dl2:
            st.download_button("📥 Muat Turun Data Asal (CSV)", df_rekod.to_csv(index=False).encode('utf-8'), f"Jadual_SBCC_{bulan_cari}_{tahun_cari}.csv", "text/csv")
        with col_del:
            if st.button("🗑️ Padam Rekod Disahkan Ini", type="primary"):
                padam_jadual_db(bulan_cari, tahun_cari)
                st.success("Rekod dipadam.")
                st.rerun()

        st.markdown("---")
        st.subheader("📄 Pratonton Dokumen Cetakan (Format Lampiran 'A'):")
        st.components.v1.html(html_code, height=600, scrolling=True)
    else:
        st.warning(f"Tiada rekod jadual yang disahkan ditemui bagi Bulan {bulan_cari}/{tahun_cari}.")
