import streamlit as st
import pandas as pd
import sqlite3
import datetime

# ----------------------------------------------------
# 1. TETAPAN HALAMAN STREAMLIT
# ----------------------------------------------------
st.set_page_config(
    page_title="Sistem Jadual Penugasan SBCC IPK Selangor",
    page_icon="📅",
    layout="wide"
)

DB_FILE = "jadual_penugasan.db"

# ----------------------------------------------------
# 2. FUNGSI PANGKALAN DATA (SQLITE)
# ----------------------------------------------------
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
            jenis_tugasan TEXT,
            nama_pegawai TEXT,
            no_tel_pegawai TEXT,
            bhg_pegawai TEXT,
            nama_penolong TEXT,
            no_tel_penolong TEXT,
            bhg_penolong TEXT,
            tarikh_disahkan TEXT
        )
    ''')
    
    # Semak dan tambah lajur jika belum wujud
    c.execute("PRAGMA table_info(rekod_jadual)")
    columns = [col[1] for col in c.fetchall()]
    if 'bhg_pegawai' not in columns:
        c.execute("ALTER TABLE rekod_jadual ADD COLUMN bhg_pegawai TEXT DEFAULT 'E8'")
    if 'bhg_penolong' not in columns:
        c.execute("ALTER TABLE rekod_jadual ADD COLUMN bhg_penolong TEXT DEFAULT 'E2'")
    if 'jenis_tugasan' not in columns:
        c.execute("ALTER TABLE rekod_jadual ADD COLUMN jenis_tugasan TEXT DEFAULT 'Rutin SBCC'")
        
    conn.commit()
    conn.close()

def simpan_jadual_db(bulan, tahun, df_jadual):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Padam rekod sedia ada bagi bulan dan tahun tersebut
    c.execute("DELETE FROM rekod_jadual WHERE bulan = ? AND tahun = ?", (bulan, tahun))
    conn.commit()
    
    df_to_save = df_jadual.copy()
    
    if 'Jenis Tugasan' not in df_to_save.columns: df_to_save['Jenis Tugasan'] = 'Rutin SBCC'
    if 'Bhg Pegawai' not in df_to_save.columns: df_to_save['Bhg Pegawai'] = 'E8'
    if 'Bhg Penolong' not in df_to_save.columns: df_to_save['Bhg Penolong'] = 'E2'
    
    df_to_save['bulan'] = bulan
    df_to_save['tahun'] = tahun
    df_to_save['tarikh_disahkan'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    df_to_save = df_to_save.rename(columns={
        'Tarikh': 'tarikh',
        'Hari': 'hari',
        'Syif / Masa': 'syif',
        'Jenis Tugasan': 'jenis_tugasan',
        'Nama Pegawai': 'nama_pegawai',
        'No. Tel Pegawai': 'no_tel_pegawai',
        'Bhg Pegawai': 'bhg_pegawai',
        'Nama Penolong': 'nama_penolong',
        'No. Tel Penolong': 'no_tel_penolong',
        'Bhg Penolong': 'bhg_penolong'
    })
    
    lajur_db = [
        'bulan', 'tahun', 'tarikh', 'hari', 'syif', 'jenis_tugasan',
        'nama_pegawai', 'no_tel_pegawai', 'bhg_pegawai',
        'nama_penolong', 'no_tel_penolong', 'bhg_penolong', 
        'tarikh_disahkan'
    ]
    
    df_to_save = df_to_save[lajur_db]
    df_to_save.to_sql('rekod_jadual', conn, if_exists='append', index=False)
    conn.close()

def ambil_jadual_db(bulan, tahun):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT * FROM rekod_jadual WHERE bulan = ? AND tahun = ? ORDER BY id ASC"
    df = pd.read_sql_query(query, conn, params=(bulan, tahun))
    conn.close()
    
    if not df.empty:
        df = df.rename(columns={
            'tarikh': 'Tarikh',
            'hari': 'Hari',
            'syif': 'Syif / Masa',
            'jenis_tugasan': 'Jenis Tugasan',
            'nama_pegawai': 'Nama Pegawai',
            'no_tel_pegawai': 'No. Tel Pegawai',
            'bhg_pegawai': 'Bhg Pegawai',
            'nama_penolong': 'Nama Penolong',
            'no_tel_penolong': 'No. Tel Penolong',
            'bhg_penolong': 'Bhg Penolong',
            'tarikh_disahkan': 'Tarikh Disahkan'
        })
    return df

def padam_jadual_db(bulan, tahun):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM rekod_jadual WHERE bulan = ? AND tahun = ?", (bulan, tahun))
    conn.commit()
    conn.close()

# ----------------------------------------------------
# 3. FUNGSI JANA DOKUMEN WORD (HTML/XML) LAMPIRAN 'A'
# ----------------------------------------------------
def jana_html_lampiran_a(df_jadual, bulan, tahun):
    nama_bulan_map = {
        1: "JAN", 2: "FEB", 3: "MAC", 4: "APR", 5: "MEI", 6: "JUN",
        7: "JUL", 8: "OGOS", 9: "SEP", 10: "OKT", 11: "NOV", 12: "DIS"
    }
    bln_str = nama_bulan_map.get(bulan, "SEP")
    
    html = f"""
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
    <meta charset="utf-8">
    <style>
        @page Section1 {{ size: 595.3pt 841.9pt; margin: 36.0pt 36.0pt 36.0pt 36.0pt; }}
        div.Section1 {{ page: Section1; }}
        body {{ font-family: Arial, sans-serif; font-size: 10pt; color: #000; line-height: 1.2; }}
        .lampiran {{ text-align: right; font-weight: bold; text-decoration: underline; font-size: 9pt; margin-bottom: 10px; }}
        .header {{ text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 10pt; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        th, td {{ border: 1px solid black; padding: 4px 5px; font-weight: bold; font-size: 8.5pt; vertical-align: middle; }}
        th {{ background-color: #d9d9d9; text-align: center; }}
        .text-center {{ text-align: center; }}
        .special-tag {{ color: #b30000; font-size: 7.5pt; font-style: italic; }}
    </style>
    </head>
    <body>
    <div class="Section1">
        <div class="lampiran">LAMPIRAN 'A'</div>
        <div class="header">
            JADUAL PEGAWAI / ANGGOTA BERTUGAS<br>
            SBCC IPK SELANGOR BAGI BULAN {bln_str} {tahun}
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 5%;">BIL</th>
                    <th style="width: 15%;">TKH/ MASA</th>
                    <th style="width: 12%;">HARI</th>
                    <th style="width: 46%;">NAMA PEGAWAI/ANGGOTA</th>
                    <th style="width: 15%;">NO TELEFON</th>
                    <th style="width: 7%;">BHG</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for idx, row in df_jadual.iterrows():
        bil = f"{idx+1:02d}."
        masa = "1700-0800"
        syif_val = str(row.get('Syif / Masa', ''))
        if "Siang" in syif_val: masa = "0800-2000"
        elif "Malam" in syif_val: masa = "2000-0800"
            
        tkh_masa = f"{row.get('Tarikh', '')}<br>{masa}"
        
        jenis_tugasan = str(row.get('Jenis Tugasan', 'Rutin SBCC'))
        tag_khas = ""
        if jenis_tugasan != "Rutin SBCC":
            tag_khas = f"<br><span class='special-tag'>[{jenis_tugasan}]</span>"
            
        hari = str(row.get('Hari', '')).upper()
        
        bhg_peg = str(row.get('Bhg Pegawai', 'E8') or 'E8')
        bhg_pen = str(row.get('Bhg Penolong', 'E2') or 'E2')
        
        tel_peg = str(row.get('No. Tel Pegawai', '') or '').strip()
        tel_pen = str(row.get('No. Tel Penolong', '') or '').strip()
        
        nama_peg = str(row.get('Nama Pegawai', ''))
        nama_pen = str(row.get('Nama Penolong', ''))
        
        html += f"""
            <tr>
                <td class="text-center">{bil}</td>
                <td class="text-center">{tkh_masa}{tag_khas}</td>
                <td class="text-center">{hari}</td>
                <td>{nama_peg}<br>{nama_pen}</td>
                <td class="text-center">({tel_peg})<br>({tel_pen})</td>
                <td class="text-center">{bhg_peg}<br>{bhg_pen}</td>
            </tr>
        """
        
    html += """
            </tbody>
        </table>
    </div>
    </body>
    </html>
    """
    return html

# ----------------------------------------------------
# 4. ANTARAMUKA UTAMA STREAMLIT
# ----------------------------------------------------
st.title("📅 Pengurusan Jadual Penugasan SBCC IPK Selangor")

tab1, tab2 = st.tabs(["📌 Jana / Kemas Kini Jadual", "📑 Semak & Muat Turun Jadual"])

SENARAI_JENIS_TUGASAN = [
    "Rutin SBCC",
    "Penugasan Khas / Event",
    "Kawalan Keselamatan",
    "Tugas Khas OCPD / CPO",
    "Operasi Khas / Ops SB",
    "Bilik Gerakan Utama (BGU)"
]

SENARAI_SYIF = [
    "Biasa (1700 - 0800)",
    "Siang (0800 - 2000)",
    "Malam (2000 - 0800)"
]

# ----------------------------------------------------
# TAB 1: JANA & SIMPAN JADUAL
# ----------------------------------------------------
with tab1:
    st.header("Jana Jadual Tugasan Bulanan")
    
    col_b, col_t = st.columns(2)
    with col_b:
        bulan_pilih = st.selectbox("Pilih Bulan", list(range(1, 13)), index=8, format_func=lambda x: f"Bulan {x}")
    with col_t:
        tahun_pilih = st.number_input("Pilih Tahun", min_value=2024, max_value=2035, value=2026)

    st.subheader("📋 Selenggara Jadual Penugasan & Special Assignments")
    
    data_sampel = [
        {
            "Tarikh": "01/09/2026", 
            "Hari": "Selasa", 
            "Syif / Masa": "Siang (0800 - 2000)", 
            "Jenis Tugasan": "Rutin SBCC",
            "Nama Pegawai": "INSP ROHAIZASHAFIKA BINTI MOHAMAD RADZALI", 
            "No. Tel Pegawai": "016-2448782", 
            "Bhg Pegawai": "E8", 
            "Nama Penolong": "SJN/D AHMAD ZAMANE BIN OMAR", 
            "No. Tel Penolong": "013-4939452", 
            "Bhg Penolong": "E2"
        },
        {
            "Tarikh": "01/09/2026", 
            "Hari": "Selasa", 
            "Syif / Masa": "Malam (2000 - 0800)", 
            "Jenis Tugasan": "Penugasan Khas / Event",
            "Nama Pegawai": "INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN", 
            "No. Tel Pegawai": "012-9212972", 
            "Bhg Pegawai": "E9", 
            "Nama Penolong": "SJN/D VASTERMORAILE ANAK MONDAY", 
            "No. Tel Penolong": "017-7058084", 
            "Bhg Penolong": "E6"
        },
        {
            "Tarikh": "02/09/2026", 
            "Hari": "Rabu", 
            "Syif / Masa": "Biasa (1700 - 0800)", 
            "Jenis Tugasan": "Rutin SBCC",
            "Nama Pegawai": "INSP MUHAMAD IQRAM BIN MOHAMAD BUKHARI", 
            "No. Tel Pegawai": "013-7044459", 
            "Bhg Pegawai": "E3", 
            "Nama Penolong": "SJN/D SHAHRUL IDHAM BIN MD SALIM", 
            "No. Tel Penolong": "014-2440181", 
            "Bhg Penolong": "E8"
        }
    ]

    df_editor = st.data_editor(
        pd.DataFrame(data_sampel),
        column_config={
            "Jenis Tugasan": st.column_config.SelectboxColumn(
                "Jenis Tugasan (Special Assignment)",
                help="Pilih jenis penugasan rutin atau Khas/Event",
                width="medium",
                options=SENARAI_JENIS_TUGASAN,
                required=True
            ),
            "Syif / Masa": st.column_config.SelectboxColumn(
                "Syif / Masa",
                options=SENARAI_SYIF,
                required=True
            )
        },
        num_rows="dynamic",
        use_container_width=True
    )

    # ----------------------------------------------------
    # SEMAKAN ATURAN TUGAS (1 KALI & 2 KALI)
    # ----------------------------------------------------
    st.markdown("---")
    st.subheader("📊 Semakan Otomatik Kekerapan Tugasan (Aturan 1 Kali / 2 Kali)")
    
    if not df_editor.empty:
        df_valid = df_editor.dropna(subset=['Nama Pegawai', 'Nama Penolong'], how='all')
        
        peg_counts = df_valid['Nama Pegawai'].value_counts()
        pen_counts = df_valid['Nama Penolong'].value_counts()
        
        col_k1, col_k2 = st.columns(2)
        
        with col_k1:
            st.write("**Statistik Pegawai Bertugas:**")
            st.dataframe(peg_counts.rename("Jumlah Syif"), use_container_width=True)
            
            # Semak pelanggaran aturan > 2 kali
            lebih_peg = peg_counts[peg_counts > 2]
            if not lebih_peg.empty:
                st.error(f"⚠️ **AMARAN (Lebih 2 Kali):** Pegawai berikut ditugaskan melebihi 2 kali: {', '.join(lebih_peg.index)}")
            else:
                st.success("✅ Semua pegawai mematuhi had maksimum 2 kali tugasan.")

        with col_k2:
            st.write("**Statistik Penolong Bertugas:**")
            st.dataframe(pen_counts.rename("Jumlah Syif"), use_container_width=True)
            
            # Semak pelanggaran aturan > 2 kali
            lebih_pen = pen_counts[pen_counts > 2]
            if not lebih_pen.empty:
                st.error(f"⚠️ **AMARAN (Lebih 2 Kali):** Penolong berikut ditugaskan melebihi 2 kali: {', '.join(lebih_pen.index)}")
            else:
                st.success("✅ Semua penolong mematuhi had maksimum 2 kali tugasan.")

    st.markdown("---")
    if st.button("🔒 Sahkan & Simpan Jadual Ini", type="primary"):
        if not df_editor.empty:
            simpan_jadual_db(bulan_pilih, tahun_pilih, df_editor)
            st.success(f"✅ Jadual bagi Bulan {bulan_pilih}/{tahun_pilih} berjaya disimpan ke dalam pangkalan data!")
        else:
            st.error("Jadual tidak boleh kosong!")

# ----------------------------------------------------
# TAB 2: SEMAK, PREVIEW & MUAT TURUN
# ----------------------------------------------------
with tab2:
    st.header("Carian & Muat Turun Jadual Disahkan")
    
    col_sb, col_st = st.columns(2)
    with col_sb:
        bulan_cari = st.selectbox("Pilih Bulan Carian", list(range(1, 13)), index=8, format_func=lambda x: f"Bulan {x}")
    with col_st:
        tahun_cari = st.number_input("Pilih Tahun Carian", min_value=2024, max_value=2035, value=2026, key="carian_tahun")

    df_rekod = ambil_jadual_db(bulan_cari, tahun_cari)

    if not df_rekod.empty:
        tkh_sah = df_rekod['Tarikh Disahkan'].iloc[0] if 'Tarikh Disahkan' in df_rekod.columns else 'Disahkan'
        st.success(f"📌 Rekod Ditemui. (Disahkan pada: {tkh_sah})")
        
        html_doc = jana_html_lampiran_a(df_rekod, bulan_cari, tahun_cari)
        
        col_dl1, col_dl2, col_del = st.columns([1.5, 1.5, 1])
        with col_dl1:
            st.download_button(
                label="📄 Muat Turun Format Word (.doc)",
                data=html_doc.encode('utf-8'),
                file_name=f"Jadual_SBCC_{bulan_cari}_{tahun_cari}.doc",
                mime="application/msword",
                use_container_width=True
            )
        with col_dl2:
            st.download_button(
                label="📥 Muat Turun Data (CSV)",
                data=df_rekod.to_csv(index=False).encode('utf-8'),
                file_name=f"Jadual_SBCC_{bulan_cari}_{tahun_cari}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_del:
            if st.button("🗑️ Padam Rekod", type="primary", use_container_width=True):
                padam_jadual_db(bulan_cari, tahun_cari)
                st.warning("Rekod telah dipadam dari pangkalan data.")
                st.rerun()

        st.markdown("---")
        st.subheader("📄 Pratonton Dokumen Cetakan (Lampiran 'A'):")
        st.components.v1.html(html_doc, height=650, scrolling=True)
    else:
        st.info("⚠️ Tiada rekod jadual ditemui bagi bulan dan tahun yang dipilih.")
