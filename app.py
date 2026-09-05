def pilih_pegawai(is_wknd, elak_set, is_jumaat=False):
    calon = [p for p in senarai_aktif if p not in elak_set]
    PEGAWAI_BOCOR_KHAS = ["INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN"]

    # 1. Tapis Giliran Weekend
    if aktif_giliran_lelaki:
        if is_wknd:
            calon_we = [
                p for p in calon
                if is_pegawai_wanita(p) 
                or rekod_bulan_lepas.get(p, {}).get("WE", 0) == 0
                or p in PEGAWAI_BOCOR_KHAS
            ]
            if calon_we:
                calon = calon_we
        else:
            calon_wd = [
                p for p in calon
                if not is_pegawai_wanita(p) and rekod_bulan_lepas.get(p, {}).get("WE", 0) > 0
            ]
            if calon_wd:
                calon = calon_wd

    # 2. Penapisan Syarat Khas Insp Faiz
    if bulan == 10 and "INSP MOHD FAIZ BIN ESA" in calon:
        if is_wknd or tugas_wd.get("INSP MOHD FAIZ BIN ESA", 0) >= 1:
            if len(calon) > 1:
                calon = [p for p in calon if p != "INSP MOHD FAIZ BIN ESA"]

    # 3. Dynamic Cap (Had Tugas)
    def dapatkan_had_maksimum(nama_pegawai):
        rec_lepas = rekod_bulan_lepas.get(nama_pegawai, {"WD": 0, "WE": 0})
        jumlah_lepas = rec_lepas.get("WD", 0) + rec_lepas.get("WE", 0)
        return 1 if jumlah_lepas >= 2 else 2

    calon_cap = [
        p for p in calon 
        if (tugas_wd.get(p, 0) + tugas_we.get(p, 0)) < dapatkan_had_maksimum(p)
    ]
    if calon_cap:
        calon = calon_cap

    # 4. Penapisan Jumaat
    if is_wknd:
        calon_no_jumaat = [p for p in calon if p not in pegawai_tugas_jumaat]
        if calon_no_jumaat:
            calon = calon_no_jumaat

    # Safety Fallback jika senarai masih kosong
    if not calon:
        calon = [p for p in senarai_aktif if p not in elak_set] or senarai_aktif

    # 5. Skor & Pemilihan
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
