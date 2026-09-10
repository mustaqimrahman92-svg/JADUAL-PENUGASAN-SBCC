import streamlit as st
import pandas as pd
import sqlite3
import datetime
import io
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# ----------------------------------------------------
# TETAPAN HALAMAN STREAMLIT
# ----------------------------------------------------
st.set_page_config(
    page_title="Sistem Jadual Penugasan SBCC",
    page_icon="📅",
    layout="wide"
)

DB_FILE = "jadual_penugasan.db"

# ----------------------------------------------------
# FUNGSI PANGKALAN DATA (SQLITE)
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
            nama_pegawai TEXT,
            no_tel_pegawai TEXT,
            bhg_pegawai TEXT,
            nama_penolong TEXT,
            no_tel_penolong TEXT,
            bhg_penolong TEXT,
            tarikh_disahkan TEXT
        )
    ''')
    
    # Semak dan tambah lajur bhg jika belum wujud dalam pangkalan data lama
    c.execute("PRAGMA table_info(rekod_jadual)")
    columns = [col[1] for col in c.fetchall()]
    if 'bhg_pegawai' not in columns:
        c.execute("ALTER TABLE rekod_jadual ADD COLUMN bhg_pegawai TEXT DEFAULT 'E8'")
    if 'bhg_penolong' not in columns:
        c.execute("ALTER TABLE rekod_jadual ADD COLUMN bhg_penolong TEXT DEFAULT 'E2'")
        
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
    
    # Pastikan lajur wajib wujud jika tidak diisi dalam data editor
    if 'Bhg Pegawai' not in df_to_save.columns: df_to_save['Bhg Pegawai'] = 'E8'
    if 'Bhg Penolong' not in df_to_save.columns: df_to_save['Bhg Penolong'] = 'E2'
    
    df_to_save['bulan'] = bulan
    df_to_save['tahun'] = tahun
    df_to_save['tarikh_disahkan'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Pemetaan lajur DataFrame ke nama lajur Pangkalan Data
    df_to_save = df_to_save.rename(columns={
        'Tarikh': 'tarikh',
        'Hari': 'hari',
        'Syif / Masa': 'syif',
        'Nama Pegawai': 'nama_pegawai',
        'No. Tel Pegawai': 'no_tel_pegawai',
        'Bhg Pegawai': 'bhg_pegawai',
        'Nama Penolong': 'nama_penolong',
        'No. Tel Penolong': 'no_tel_penolong',
        'Bhg Penolong': 'bhg_penolong'
    })
    
    lajur_db = [
        'bulan', 'tahun', 'tarikh', 'hari', 'syif', 
        'nama_pegawai', 'no_tel_pegawai', 'bhg_pegawai',
        'nama_penolong', 'no_tel_penolong', 'bhg_penolong', 
        'tarikh_disahkan'
    ]
    
    df_to_save = df_to_save[lajur_db]
    
    # Simpan menggunakan Pandas to_sql
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
# FUNGSI JANA FAIL WORD (.DOCX)
# ----------------------------------------------------
def jana_docx_lampiran_a(df_jadual, bulan, tahun):
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
    nama_bulan_map = {
        1: "JAN", 2: "FEB", 3: "MAC", 4: "APR", 5: "MEI", 6: "JUN",
        7: "JUL", 8: "OGOS", 9: "SEP", 10: "OKT", 11: "NOV", 12: "DIS"
    }
    bln_str = nama_bulan_map.get(bulan, "SEP")

    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_lamp = p_top.add_run("LAMPIRAN 'A'\n")
    r_lamp.bold = True
    r_lamp.underline = True
    r_lamp.font.size = Pt(9)
    r_lamp.font.name = 'Arial'

    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_head = p_head.add_run(f"JADUAL PEGAWAI / ANGGOTA BERTUGAS\nSBCC IPK SELANGOR BAGI BULAN {bln_str} {tahun}\n")
    r_head.bold = True
    r_head.font.size = Pt(10)
    r_head.font.name = 'Arial'

    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ['BIL', 'TKH/ MASA', 'HARI', 'NAMA PEGAWAI/ANGGOTA', 'NO TELEFON', 'BHG']
    widths = [Inches(0.5), Inches(1.1), Inches(0.9), Inches(3.3), Inches(1.3), Inches(0.5)]

    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        hdr_cells[i].width = widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(8.5)
            r.font.name = 'Arial'

    for idx, row in df_jadual.iterrows():
        row_cells = table.add_row().cells
        
        # 1. Bil
        row_cells[0].text = f"{idx+1:02d}."
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 2. Tkh / Masa
        masa = "1700-0800"
        syif_val = str(row.get('Syif / Masa', ''))
        if "Siang" in syif_val: masa = "0800-2000"
        elif "Malam" in syif_val: masa = "2000-0800"
        row_cells[1].text = f"{row.get('Tarikh', '')}\n{masa}"
        row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 3. Hari
        row_cells[2].text = str(row.get('Hari', '')).upper()
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 4. Nama Pegawai & Penolong
        nama_peg = str(row.get('Nama Pegawai', ''))
        nama_pen = str(row.get('Nama Penolong', ''))
        row_cells[3].text = f"{nama_peg}\n{nama_pen}"
        
        # 5. No Telefon
        tel_peg = str(row.get('No. Tel Pegawai', '') or '').strip()
        tel_pen = str(row.get('No. Tel Penolong', '') or '').strip()
        row_cells[4].text = f"({tel_peg})\n({tel_pen})"
        row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 6. Bahagian
        bhg_peg = str(row.get('Bhg Pegawai', 'E8') or 'E8')
        bhg_pen = str(row.get('Bhg Penolong', 'E2') or 'E2')
        row_cells[5].text = f"{bhg_peg}\n{bhg_pen}"
        row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        for i in range(6):
            row_cells[i].width = widths[i]
            for p in row_cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8)
                    r.font.name = 'Arial'
                    r.bold = True

    target_stream = io.BytesIO()
    doc.save(target_stream)
    target_stream.seek(0)
    return target_stream

# ----------------------------------------------------
# FUNGSI HTML PREVIEW (GAYA LAMPIRAN A)
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
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 11px; color: #000; line-height: 1.2; padding: 10px; }}
        .lampiran {{ float: right; font-weight: bold; text-decoration: underline; font-size: 10px; }}
        .header {{ text-align: center; font-weight: bold; margin: 15px 0; font-size: 11px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        th, td {{ border: 1px solid black; padding: 4px 5px; font-weight: bold; font-size: 10px; }}
        th {{ background-color: #d9d9d9; text-align: center; }}
        .text-center {{ text-align: center; }}
    </style>
    </head>
    <body>
        <div class="lampiran">LAMPIRAN 'A'</div>
        <div style="clear:both;"></div>
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
                    <th style="width: 45%;">NAMA PEGAWAI/ANGGOTA</th>
                    <th style="width: 16%;">NO TELEFON</th>
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
                <td class="text-center">{tkh_masa}</td>
                <td class="text-center">{hari}</td>
                <td>{nama_peg}<br>{nama_pen}</td>
                <td class="text-center">({tel_peg})<br>({tel_pen})</td>
                <td class="text-center">{bhg_peg}<br>{bhg_pen}</td>
            </tr>
        """
        
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html

# ----------------------------------------------------
# ANTARAMUKA UTAMA STREAMLIT
# ----------------------------------------------------
st.title("📅 Pengurusan Jadual Penugasan SBCC IPK Selangor")

tab1, tab2 = st.tabs(["📌 Jana / Kemas Kini Jadual", "📑 Semak & Muat Turun Jadual"])

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

    data_sampel = [
        {"Tarikh": "01/09/2026", "Hari": "Selasa", "Syif / Masa": "Siang (0800 - 2000)", "Nama Pegawai": "INSP ROHAIZASHAFIKA BINTI MOHAMAD RADZALI", "No. Tel Pegawai": "016-2448782", "Bhg Pegawai": "E8", "Nama Penolong": "SJN/D AHMAD ZAMANE BIN OMAR", "No. Tel Penolong": "013-4939452", "Bhg Penolong": "E2"},
        {"Tarikh": "01/09/2026", "Hari": "Selasa", "Syif / Masa": "Malam (2000 - 0800)", "Nama Pegawai": "INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN", "No. Tel Pegawai": "012-9212972", "Bhg Pegawai": "E9", "Nama Penolong": "SJN/D VASTERMORAILE ANAK MONDAY", "No. Tel Penolong": "017-7058084", "Bhg Penolong": "E6"},
        {"Tarikh": "02/09/2026", "Hari": "Rabu", "Syif / Masa": "Biasa (1700 - 0800)", "Nama Pegawai": "INSP MUHAMAD IQRAM BIN MOHAMAD BUKHARI", "No. Tel Pegawai": "013-7044459", "Bhg Pegawai": "E3", "Nama Penolong": "SJN/D SHAHRUL IDHAM BIN MD SALIM", "No. Tel Penolong": "014-2440181", "Bhg Penolong": "E8"}
    ]

    df_editor = st.data_editor(
        pd.DataFrame(data_sampel),
        num_rows="dynamic",
        use_container_width=True
    )

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
        
        docx_file = jana_docx_lampiran_a(df_rekod, bulan_cari, tahun_cari)
        html_preview = jana_html_lampiran_a(df_rekod, bulan_cari, tahun_cari)
        
        col_dl1, col_dl2, col_del = st.columns([1.5, 1.5, 1])
        with col_dl1:
            st.download_button(
                label="📄 Muat Turun Format Word (.docx)",
                data=docx_file,
                file_name=f"Jadual_SBCC_{bulan_cari}_{tahun_cari}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
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
        st.components.v1.html(html_preview, height=650, scrolling=True)
    else:
        st.info("⚠️ Tiada rekod jadual ditemui bagi bulan dan tahun yang dipilih.")
