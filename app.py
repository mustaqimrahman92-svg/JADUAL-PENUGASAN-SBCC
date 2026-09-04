
import streamlit as st
import pandas as pd
import datetime
import calendar

st.set_page_config(page_title="Sistem Penugasan Cawangan Khas IPK Selangor", layout="wide")

st.title("📅 Sistem Penugasan Pegawai (Kalendar Malaysia)")
st.write("Sistem automatik penjanaan jadual penugasan mengikut syarat syif hari bekerja, hujung minggu, cuti umum, serta penugasan khas.")

# --- SENARAI 31 PEGAWAI DARI DOKUMEN ---
SENARAI_PEGAWAI = [
    "INSP ADDLYZAN BIN ABD MANAP (012-4739701)",
    "INSP FAIZ BIN BASAR (017-9457941)",
    "INSP MOHD SHAHRILBUN BIN AMDAN (017-5800578)",
    "INSP FARAH NADJWA BT MOHD LASA (013-9195659)",
    "INSP SABARI BIN BUJANG (016-7135975)",
    "INSP KASHMINDEJRIT KAUR A/P CHARLES (016-6738465)",
    "INSP NORAINUN MUBIN BT ANUAR (012-7493780)",
    "INSP MUHAMAD IQRAM BIN MOHAMAD BUKHARI (013-7044459)",
    "INSP MOHAMAD IQBAL IBRAHIM BIN DAUD (012-6467775)",
    "INSP AMI RUSLAN BIN MOHD RUSLAN (017-9501506)",
    "INSP MOHD RAZIF BIN ROSSMAN (017-9196166)",
    "INSP AZFIZI BIN AZIZ (014-8340944)",
    "INSP MUHAMAD ARIFF BIN ABD RAHIM (010-4017822)",
    "INSP MOHD RUSDI BIN HASSAN (010-4535060)",
    "INSP ABDUL MUIN BIN AB AZIZ (019-4494500)",
    "INSP MOHD SHAHRIL BIN MOHAMED RESALI (012-9096486)",
    "INSP NOR HAIZAH BINTI YACOB (012-9979790)",
    "INSP KUKENDRAN A/L YOGENDRAN (012-9062264)",
    "INSP MUHAMMAD NOR QHAIREIL BIN NOR AZMI (011-16554250)",
    "INSP KHAIRUL HAFIZ BIN SHAFFIE AHMED (017-4308434)",
    "INSP EZYANTI BT MUHAMAD (019-9241360)",
    "INSP MOHAMAD SYARUL FADLI BIN MAT HUSAIN (011-10042323)",
    "INSP MUHAMMAD AFIQ BIN NORDIN (010-4641637)",
    "INSP MOHD JEFFERE BIN ALI (014-2348186)",
    "INSP NUR AADILA BINTI ABDUL MALEK (014-3383604)",
    "INSP SHURENDREN A/L JAYARAMAN (019-2823312)",
    "INSP MOHD FAIZ BIN ESA (010-7978603)",
    "INSP ROHAIZASHAFIKA BINTI MOHAMAD RADZALI (016-2448782)",
    "INSP DZUL FADHLI BIN ABDUL HALIM (014-6689803)",
    "INSP NORHAZIERAM BINTI ZAKARIA (014-9207312)",
    "INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN (012-9212972)"
]

# --- SIDEBAR: Tetapan Utama ---
st.sidebar.header("⚙️ Tetapan Penugasan")

tahun = st.sidebar.number_input("Tahun", min_value=2024, max_value=2030, value=datetime.datetime.now().year)
bulan = st.sidebar.selectbox("Bulan", range(1, 13), index=datetime.datetime.now().month - 1)

st.sidebar.subheader("👥 Bilangan Staf Per Syif")
staf_weekdays = st.sidebar.number_input("Isnin-Jumaat (1700-0800)", min_value=1, value=1)
staf_weekend_siang = st.sidebar.number_input("Sabtu/Ahad/Cuti (0800-2000)", min_value=1, value=1)
staf_weekend_malam = st.sidebar.number_input("Sabtu/Ahad/Cuti (2000-0800)", min_value=1, value=1)

st.sidebar.subheader("🇲🇾 Tarikh Cuti Umum")
cuti_input = st.sidebar.text_input("Masukkan Tarikh Cuti (Contoh: 1, 16, 31)", "")
tarikh_cuti_umum = []
if cuti_input:
    try:
        tarikh_cuti_umum = [int(x.strip()) for x in cuti_input.split(",") if x.strip().isdigit()]
    except ValueError:
        st.sidebar.error("Sila masukkan nombor tarikh yang sah dipisahkan dengan koma.")

# --- UTILITY FUNCTIONS ---
num_days = calendar.monthrange(tahun, bulan)[1]
tarikh_senarai = [datetime.date(tahun, bulan, day) for day in range(1, num_days + 1)]

def get_shift_type(dt, cuti_list):
    is_weekend = dt.weekday() in [5, 6] # 5 = Sabtu, 6 = Ahad
    is_holiday = dt.day in cuti_list
    return "WEEKEND_HOLIDAY" if (is_weekend or is_holiday) else "WEEKDAY"

# --- RUANGAN TUGAS KHAS (MANUAL SELECTION) ---
st.subheader("📌 Tetapan Tugas Khas (Pilihan Manual)")
st.caption("Pilih pegawai tertentu untuk tarikh dan syif khusus. Baki syif lain akan diisi secara automatik.")

if "tugas_khas" not in st.session_state:
    st.session_state.tugas_khas = []

col_khas1, col_khas2, col_khas3, col_khas4 = st.columns([2, 1, 1.5, 1])

with col_khas1:
    pegawai_pilihan = st.selectbox("Pilih Pegawai", SENARAI_PEGAWAI, key="khas_pegawai")
with col_khas2:
    hari_pilihan = st.selectbox("Tarikh (Hari)", range(1, num_days + 1), key="khas_hari")
with col_khas3:
    dt_temp = datetime.date(tahun, bulan, hari_pilihan)
    s_type = get_shift_type(dt_temp, tarikh_cuti_umum)
    pilihan_syif = ["1700-0800"] if s_type == "WEEKDAY" else ["0800-2000", "2000-0800"]
    syif_pilihan = st.selectbox("Pilih Syif", pilihan_syif, key="khas_syif")
with col_khas4:
    st.write("") # Spacing
    st.write("")
    if st.button("➕ Tambah", use_container_width=True):
        st.session_state.tugas_khas.append({
            "pegawai": pegawai_pilihan,
            "hari": hari_pilihan,
            "syif": syif_pilihan
        })
        st.success(f"Tugas khas ditambah untuk {pegawai_pilihan[:15]}... pada hari ke-{hari_pilihan}")

# Papar senarai tugas khas yang dimasukkan
if st.session_state.tugas_khas:
    st.write("**Senarai Tugas Khas Ditetapkan:**")
    df_khas = pd.DataFrame(st.session_state.tugas_khas)
    st.dataframe(df_khas, height=120)
    if st.button("🗑️ Padam Semua Tugas Khas"):
        st.session_state.tugas_khas = []
        st.rerun()

st.markdown("---")

# --- PROSES JANA JADUAL AUTOMATIK ---
if st.button("🚀 Jana Jadual Penugasan", type="primary", use_container_width=True):
    
    jadual = {pegawai: ["OFF" for _ in range(num_days)] for pegawai in SENARAI_PEGAWAI}
    counts = {pegawai: 0 for pegawai in SENARAI_PEGAWAI}

    # 1. Masukkan Tugas Khas Terlebih Dahulu
    for khas in st.session_state.tugas_khas:
        peg = khas["pegawai"]
        h_idx = khas["hari"] - 1
        syf = khas["syif"]
        
        if jadual[peg][h_idx] == "OFF":
            jadual[peg][h_idx] = f"{syf} (KHAS)"
            counts[peg] += 1

    # 2. Isi Baki Syif Secara Automatik
    for day_idx, dt in enumerate(tarikh_senarai):
        shift_type = get_shift_type(dt, tarikh_cuti_umum)
        
        if shift_type == "WEEKDAY":
            # Semak berapa slot 1700-0800 yang sudah diisi oleh Tugas Khas
            existing_assigned = [p for p in SENARAI_PEGAWAI if "1700-0800" in jadual[p][day_idx]]
            needed = staf_weekdays - len(existing_assigned)
            
            if needed > 0:
                # Baki pegawai yang tiada tugasan hari tersebut
                available = [p for p in SENARAI_PEGAWAI if jadual[p][day_idx] == "OFF"]
                available = sorted(available, key=lambda s: counts[s])
                for s in available[:needed]:
                    jadual[s][day_idx] = "1700-0800"
                    counts[s] += 1
                    
        else: # WEEKEND_HOLIDAY
            # Syif Siang (0800-2000)
            existing_siang = [p for p in SENARAI_PEGAWAI if "0800-2000" in jadual[p][day_idx]]
            needed_siang = staf_weekend_siang - len(existing_siang)
            
            # Syif Malam (2000-0800)
            existing_malam = [p for p in SENARAI_PEGAWAI if "2000-0800" in jadual[p][day_idx]]
            needed_malam = staf_weekend_malam - len(existing_malam)
            
            available = [p for p in SENARAI_PEGAWAI if jadual[p][day_idx] == "OFF"]
            available = sorted(available, key=lambda s: counts[s])
            
            idx_tracker = 0
            if needed_siang > 0:
                for s in available[idx_tracker:idx_tracker + needed_siang]:
                    jadual[s][day_idx] = "0800-2000"
                    counts[s] += 1
                idx_tracker += needed_siang
                
            if needed_malam > 0:
                for s in available[idx_tracker:idx_tracker + needed_malam]:
                    jadual[s][day_idx] = "2000-0800"
                    counts[s] += 1

    # Bina DataFrame
    kolum_header = [f"{dt.strftime('%d/%m')}\n({dt.strftime('%a')})" for dt in tarikh_senarai]
    df = pd.DataFrame.from_dict(jadual, orient='index', columns=kolum_header)
    df["JUMLAH SYIF"] = [counts[s] for s in df.index]

    # Display Results
    st.success("Jadual penugasan pegawai berjaya dijana!")
    st.subheader("📋 Jadual Penugasan Bulanan")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Muat Turun Jadual (CSV/Excel)",
        data=csv_data,
        file_name=f'jadual_penugasan_{bulan}_{tahun}.csv',
        mime='text/csv',
    )
