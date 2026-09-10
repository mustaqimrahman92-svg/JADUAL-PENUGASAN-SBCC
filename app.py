# ----------------------------------------------------
# FUNGSI LAMPIRAN 'A' (PEGAWAI ATAS, PENOLONG BAWAH)
# ----------------------------------------------------
def jana_html_lampiran_a(df_jadual, bulan, tahun):
    nama_bulan_map = {
        1: "JANUARY", 2: "FEBRUARY", 3: "MARCH", 4: "APRIL", 5: "MAY", 6: "JUNE",
        7: "JULY", 8: "AUGUST", 9: "SEPTEMBER", 10: "OCTOBER", 11: "NOVEMBER", 12: "DECEMBER"
    }
    bln_str = nama_bulan_map.get(bulan, "SEPTEMBER")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @page {{ size: A4 portrait; margin: 10mm; }}
        body {{ font-family: Arial, sans-serif; font-size: 10px; color: #000; line-height: 1.2; }}
        .header {{ text-align: center; font-weight: bold; margin-bottom: 12px; font-size: 11px; line-height: 1.4; }}
        .lampiran {{ float: right; font-weight: bold; text-decoration: underline; font-size: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; page-break-inside: auto; }}
        tr {{ page-break-inside: avoid; page-break-after: auto; }}
        th, td {{ border: 1px solid black; padding: 6px 8px; vertical-align: middle; }}
        th {{ background-color: #e0e0e0; font-weight: bold; font-size: 10px; text-align: center; }}
        .text-center {{ text-align: center; }}
        .jawatan {{ font-size: 8.5px; color: #444; font-style: italic; font-weight: normal; }}
        .sek-pegawai {{ margin-bottom: 4px; padding-bottom: 4px; border-bottom: 1px dashed #bbb; }}
        .sek-penolong {{ padding-top: 2px; }}
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
                    <th style="width: 6%;">BIL</th>
                    <th style="width: 20%;">TKH / MASA</th>
                    <th style="width: 14%;">HARI</th>
                    <th style="width: 60%;">PEGAWAI & PENOLONG PEGAWAI BERTUGAS</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for idx, row in df_jadual.iterrows():
        bil = f"{idx+1:02d}."
        masa = "1700 - 0800"
        if "Siang" in str(row['Syif / Masa']):
            masa = "0800 - 2000"
        elif "Malam" in str(row['Syif / Masa']):
            masa = "2000 - 0800"
            
        tkh_masa = f"{row['Tarikh']}<br><b>{masa}</b>"
        hari = str(row['Hari']).upper()
        
        petak_gabung = f"""
            <div class="sek-pegawai">
                <b>1. {row['Nama Pegawai']}</b> <span class="jawatan">(Pegawai Bertugas)</span><br>
                &nbsp;&nbsp;&nbsp;&nbsp;<b>No. Tel:</b> {row['No. Tel Pegawai']}
            </div>
            <div class="sek-penolong">
                <b>2. {row['Nama Penolong']}</b> <span class="jawatan">(Penolong Pegawai Bertugas)</span><br>
                &nbsp;&nbsp;&nbsp;&nbsp;<b>No. Tel:</b> {row['No. Tel Penolong']}
            </div>
        """
        
        html += f"""
            <tr>
                <td class="text-center">{bil}</td>
                <td class="text-center">{tkh_masa}</td>
                <td class="text-center">{hari}</td>
                <td>{petak_gabung}</td>
            </tr>
        """
        
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html
