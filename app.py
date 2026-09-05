def pilih_pegawai(is_wknd, elak_set, is_jumaat=False):
    calon = [p for p in senarai_aktif if p not in elak_set]
    
    if is_wknd:
        calon_tanpa_jumaat = [p for p in calon if p not in pegawai_tugas_jumaat]
        if calon_tanpa_jumaat:
            calon = calon_tanpa_jumaat

    # PENAPISAN TEGAS (HARD CONSTRAINT) GILIRAN LELAKI
    if aktif_giliran_lelaki:
        if is_wknd:
            # Elakkan pegawai lelaki yang pernah bertugas WE bulan lepas daripada dipilah untuk WE bulan ini
            calon_elak_we = [
                p for p in calon 
                if is_pegawai_wanita(p) or rekod_bulan_lepas.get(p, {}).get("WE", 0) == 0
            ]
            if calon_elak_we:
                calon = calon_elak_we
        else:
            # Utamakan pegawai lelaki yang bertugas WE bulan lepas untuk mengambil WD bulan ini
            calon_keutamaan_wd = [
                p for p in calon 
                if not is_pegawai_wanita(p) and rekod_bulan_lepas.get(p, {}).get("WE", 0) > 0
            ]
            if calon_keutamaan_wd:
                calon = calon_keutamaan_wd

    # Syarat Khas Insp Faiz (Bulan Okt)
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

    if is_jumaat:
        pegawai_tugas_jumaat.add(pilihan)
        
    return pilihan
