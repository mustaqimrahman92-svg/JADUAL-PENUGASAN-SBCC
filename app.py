<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Jadual Tugasan Cawangan Khas IPK Selangor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f6f9;
            color: #333;
        }
        h2, h3 {
            text-align: center;
            color: #1a2b4c;
        }
        .container {
            max-width: 1200px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
            font-size: 14px;
        }
        th {
            background-color: #1a2b4c;
            color: white;
            text-align: center;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            color: white;
            font-size: 12px;
        }
        .e2 { background-color: #2b5c8f; }
        .e3 { background-color: #27ae60; }
        .e4 { background-color: #d35400; }
        .e5 { background-color: #8e44ad; }
        .e6 { background-color: #c0392b; }
        .e7 { background-color: #16a085; }
        .e8 { background-color: #f39c12; }
        .e9 { background-color: #34495e; }
    </style>
</head>
<body>

<div class="container">
    <h2>CAWANGAN KHAS IPK SELANGOR</h2>
    <h3>PANGKALAN DATA PEGAWAI & PENOLONG PEGAWAI BERTUGAS (TERKINI)</h3>

    <h3>1. SENARAI PEGAWAI BERTUGAS (INSP)</h3>
    <table id="jadualPegawai">
        <thead>
            <tr>
                <th style="width: 5%;">Bil</th>
                <th style="width: 45%;">Nama Pegawai</th>
                <th style="width: 25%;">No. Telefon</th>
                <th style="width: 25%;">Cawangan / Seksyen</th>
            </tr>
        </thead>
        <tbody>
            <!-- Didesain & Diisi oleh JavaScript -->
        </tbody>
    </table>

    <br><br>

    <h3>2. SENARAI PENOLONG PEGAWAI BERTUGAS (SJN / KPL / L/KPL)</h3>
    <table id="jadualPenolong">
        <thead>
            <tr>
                <th style="width: 5%;">Bil</th>
                <th style="width: 45%;">Nama Penolong Pegawai</th>
                <th style="width: 25%;">No. Telefon</th>
                <th style="width: 25%;">Cawangan / Seksyen</th>
            </tr>
        </thead>
        <tbody>
            <!-- Didesain & Diisi oleh JavaScript -->
        </tbody>
    </table>
</div>

<script>
// PANGKALAN DATA TERKINI (DATABASE)
const dataPegawai = [
    { nama: "INSP ADDLYZAN BIN ABD MANAP", tel: "012-4739701", cawangan: "E2" },
    { nama: "INSP FAIZ BIN BASAR", tel: "017-9457941", cawangan: "E2" },
    { nama: "INSP SABARI BIN BUJANG", tel: "016-7135975", cawangan: "E2" },
    { nama: "INSP KASHMINDEJRIT KAUR A/P CHARLES", tel: "016-6738465", cawangan: "E2" },
    { nama: "INSP SHURENDREN A/L JAYARAMAN", tel: "019-2823312", cawangan: "E2" },
    { nama: "INSP FARAH NADJWA BT MOHD LASA", tel: "013-9195659", cawangan: "E2" },
    { nama: "INSP NORAINUN MUBIN BT ANUAR", tel: "012-7493780", cawangan: "E3" },
    { nama: "INSP MUHAMAD IQRAM BIN MOHAMAD BUKHARI", tel: "013-7044459", cawangan: "E3" },
    { nama: "INSP MOHAMAD IQBAL IBRAHIM BIN DAUD", tel: "012-6467775", cawangan: "E4" },
    { nama: "INSP AMI RUSLAN BIN MOHD RUSLAN", tel: "017-9501506", cawangan: "E4" },
    { nama: "INSP MOHD RAZIF BIN ROSSMAN", tel: "017-9196166", cawangan: "E4" },
    { nama: "INSP AZFIZI BIN AZIZ", tel: "014-8340944", cawangan: "E4" },
    { nama: "INSP MUHAMAD ARIFF BIN ABD RAHIM", tel: "010-4017822", cawangan: "E4" },
    { nama: "INSP MOHD RUSDI BIN HASSAN", tel: "010-4535060", cawangan: "E4" },
    { nama: "INSP ABDUL MUIN BIN AB AZIZ", tel: "019-4494500", cawangan: "E5" },
    { nama: "INSP MOHD SHAHRIL BIN MOHAMED RESALI", tel: "012-9096486", cawangan: "E5" },
    { nama: "INSP NOR HAIZAH BINTI YACOB", tel: "012-9979790", cawangan: "E5" },
    { nama: "INSP KUKENDRAN A/L YOGENDRAN", tel: "012-9062264", cawangan: "E6" },
    { nama: "INSP MUHAMMAD NOR QHAIREIL BIN NOR AZMI", tel: "011-16554250", cawangan: "E6" },
    { nama: "INSP KHAIRUL HAFIZ BIN SHAFFIE AHMED", tel: "017-4308434", cawangan: "E6" },
    { nama: "INSP EZYANTI BT MUHAMAD", tel: "019-9241360", cawangan: "E6" },
    { nama: "INSP MOHAMAD SYARUL FADLI BIN MAT HUSAIN", tel: "011-10042323", cawangan: "E6" },
    { nama: "INSP MUHAMMAD AFIQ BIN NORDIN", tel: "010-4641637", cawangan: "E7" },
    { nama: "INSP MOHD JEFFERE BIN ALI", tel: "014-2348186", cawangan: "E7" },
    { nama: "INSP NUR AADILA BINTI ABDUL MALEK", tel: "014-3383604", cawangan: "E7" },
    { nama: "INSP MOHD SHAHRILBUN BIN AMDAN", tel: "017-5800578", cawangan: "E8" },
    { nama: "INSP MOHD FAIZ BIN ESA", tel: "010-7978603", cawangan: "E8" },
    { nama: "INSP ROHAIZASHAFIKA BINTI MOHAMAD RADZALI", tel: "016-2448782", cawangan: "E8" },
    { nama: "INSP DZUL FADHLI BIN ABDUL HALIM", tel: "014-6689803", cawangan: "E9" },
    { nama: "INSP NORHAZIERAM BINTI ZAKARIA", tel: "014-9207312", cawangan: "E9" },
    { nama: "INSP WAN MUHAMAD MUSTAQIM BIN ABDUL RAHMAN", tel: "012-9212972", cawangan: "E9" }
];

const dataPenolong = [
    { nama: "SJN/D ONG WEI TAU", tel: "012-8121981", cawangan: "E2" },
    { nama: "KPL/D MOHD FAIZAL BIN TIMAN", tel: "017-7455348", cawangan: "E2" },
    { nama: "KPL/D MUHAMMAD AZRUL SHAFIQ BIN ISMAN", tel: "019-5898658", cawangan: "E2" },
    { nama: "KPL/D FARIEZUL NAIM BIN MOHD SANI", tel: "013-6399275", cawangan: "E2" },
    { nama: "SJN/D SUYANI BINTI MAT SAAD", tel: "012-3405606", cawangan: "E2" },
    { nama: "SJN/D MOHD JURAIDI BIN SAMSUDIN", tel: "012-6769745", cawangan: "E2" },
    { nama: "L/KPL/D NURHIDAYAH BINTI SUHAMI", tel: "017-7011952", cawangan: "E2" },
    { nama: "KONS NUR AMIERA BINTI MOHAMAD ALI AHAN", tel: "017-6723075", cawangan: "E2" },
    { nama: "L/KPL ATHIRAH NABILA BINTI SAEDIN", tel: "018-3166724", cawangan: "E2" },
    { nama: "L/KPL/D HANA LYDIA BINTI LIERON", tel: "018-8709538", cawangan: "E2" },
    { nama: "SJN/D HAFIZATUL AMIRA BT ADBUL MANAF", tel: "019-5493007", cawangan: "E3" },
    { nama: "KPL/D JEEVAN A/L VADIAHLAGAN", tel: "013-5638303", cawangan: "E3" },
    { nama: "L/KPL/D MOHAMMAD ARRYAN JUING BIN ABDULLAH", tel: "019-4334734", cawangan: "E3" },
    { nama: "SJN/D VASTERMORAILE ANAK MONDAY", tel: "017-7058084", cawangan: "E3" },
    { nama: "L/KPL AHMAD HELMI HARIRI BIN SALVEHUJRAIE", tel: "011-166522645", cawangan: "E3" },
    { nama: "SJN/D SHAHRUL IDHAM BIN MD SALIM", tel: "014-2440181", cawangan: "E3" },
    { nama: "SJN/D ZAMRI BIN BAKARI", tel: "013-2893878", cawangan: "E3A" },
    { nama: "SJN/D AHMAD ZAMANE BIN OMAR", tel: "013-4939452", cawangan: "E4" },
    { nama: "KPL/D MOHD SYAIFUL AZHAR BIN MOHD HANAFIAH", tel: "011-51105497", cawangan: "E4" },
    { nama: "SJN/D HAFENDI BIN HANAFIAH", tel: "012-3784305", cawangan: "E4" },
    { nama: "KPL/D LO YEE TYNG", tel: "016-8374537", cawangan: "E4" },
    { nama: "SJN/D JAAFAR BIN MA HASAN", tel: "011-11474013", cawangan: "E4" },
    { nama: "KPL/D MOHD KHAIROL IZDZUAN BIN MOHAMAD ZAHARI", tel: "012-2796394", cawangan: "E4" },
    { nama: "KPL/D MUHAMMAD AZKA FATIN BIN MOHD NORDIN", tel: "016-2198068", cawangan: "E5" },
    { nama: "SJN/D SYEAFUUL AZNRY BIN ZAMBRI", tel: "012-7637889", cawangan: "E5" },
    { nama: "SJN/D EFFARINA BIN AHMAD SUHAIMI", tel: "018-9154504", cawangan: "E5" },
    { nama: "KPL/D MUHAMMAD SYUKRI BIN ZULKIFLI", tel: "012-6196573", cawangan: "E5" },
    { nama: "P/SJN/D ASRUL AZWANDI BIN AHMAD", tel: "019-4636430", cawangan: "E5" },
    { nama: "KPL/D SUFIAN BIN ISMAIL", tel: "017-6217662", cawangan: "E5" },
    { nama: "KPL/D MUHAMMAD ZULFFY BIN RASHID", tel: "013-4080883", cawangan: "E6" },
    { nama: "SJN/D ZAMZUHAIRI BIN TOMIRAN", tel: "012-2712700", cawangan: "E6" },
    { nama: "KPL/D NOOR HAZWANI BINTI MUHAMAD RUSLI", tel: "019-2217116", cawangan: "E6" },
    { nama: "KPL/D YVONNE KUA CHEE WEI", tel: "011-10905627", cawangan: "E6" },
    { nama: "KPL/D MOHD KHAIROL ANUAR BIN MOHAMED", tel: "010-4358116", cawangan: "E6" },
    { nama: "KPL/D NELSON ANAK NUING", tel: "017-3655175", cawangan: "E6" },
    { nama: "KPL/D MUHAMMAD FIRDAUS BIN AMRAN", tel: "013-7783677", cawangan: "E7" },
    { nama: "SJN/D YUSRI BIN WAHAB", tel: "019-3876720", cawangan: "E7" },
    { nama: "KPL/D WELLINGTON RICHARD ANAK SADOK", tel: "011-29994591", cawangan: "E7" },
    { nama: "KPL/D MOHAMAD PARIS BIN ROMELI", tel: "017-3864533", cawangan: "E7" },
    { nama: "KPL/D ABDUL HALIM BIN KAMARUDDIN", tel: "013-2425850", cawangan: "E7" },
    { nama: "KPL/D MOHAMAD HAFIS BIN SALLEH", tel: "013-4928247", cawangan: "E7" },
    { nama: "KPL/D HAZIZAT BIN ATTAN", tel: "013-5744426", cawangan: "E8" },
    { nama: "KPL/D MOHD YUSRI BIN ABU SEMAN", tel: "017-9278564", cawangan: "E8" },
    { nama: "SJN/D NOOR HAKIMI BIN ZULKIFLI", tel: "012-6949107", cawangan: "E8" },
    { nama: "KPL/D RIZQI ALFIAN BIN KOMIN", tel: "011-23246744", cawangan: "E8" },
    { nama: "L/KPL/D KOLOZUM SAFINAH BINTI VARUSAI", tel: "011-65670875", cawangan: "E8" },
    { nama: "L/KPL/D MUHAMMAD ABDUL WAFIE HAZIQ BIN HAMDAN", tel: "017-5431206", cawangan: "E8" }
];

// FUNGSI JANA JADUAL
function memuatkanJadual(idElemen, data) {
    const tbody = document.querySelector(`#${idElemen} tbody`);
    tbody.innerHTML = "";
    
    data.forEach((item, index) => {
        const row = document.createElement("tr");
        const kelasCawangan = item.cawangan.toLowerCase().replace('a', '');
        
        row.innerHTML = `
            <td style="text-align: center;">${index + 1}</td>
            <td><strong>${item.nama}</strong></td>
            <td>${item.tel}</td>
            <td><span class="badge ${kelasCawangan}">${item.cawangan}</span></td>
        `;
        tbody.appendChild(row);
    });
}

// JALANKAN APABILA HALAMAN DIMUATKAN
window.onload = function() {
    memuatkanJadual("jadualPegawai", dataPegawai);
    memuatkanJadual("jadualPenolong", dataPenolong);
};
</script>

</body>
</html>
