import os
import base64
import streamlit as st

st.set_page_config(
    page_title="Türkiye İnşaat Tedarik Sınıflandırma Sistemi",
    page_icon="🏗️",
    layout="wide"
)

LOGO_PATH = "İNDER Logo.jpg"

DATA = {
"01 – Genel & Şantiye":{
"Genel & Şantiye":["Aydınlatma Sistemleri","Güvenlik Sistemleri","İskele Sistemleri","Şantiye Ekipmanları","Geçici Yapılar"],
"İş Güvenliği":["Acil Müdahale","Ekipman","Eğitim","Denetim","Yangın Güvenliği"],
"Lojistik & Depo":["Depolama","Nakliye","Yükleme","Stok Yönetimi","Elleçleme"],
"Şantiye Yönetimi":["Planlama","Raporlama","İş Takibi","Maliyet Kontrol","İnsan Kaynakları"],
"Geçici Sistemler":["Elektrik","Su","Kanalizasyon","Isıtma","Soğutma"]},

"02 – Zemin & Temel":{
"Kazı":["Kaya Kazısı","Genel Kazı","Makinalı Kazı","El Kazısı","Hafriyat"],
"Dolgu":["Sıkıştırılmış Dolgu","Kum Dolgu","Stabilize","Kırmataş","Granüler"],
"Zemin İyileştirme":["Enjeksiyon","Jet Grout","Fore Kazık","Mini Kazık","Derin Karıştırma"],
"Temel Sistemleri":["Radye Temel","Münferit Temel","Kazıklı Temel","Sürekli Temel","Temel Kirişi"],
"Drenaj":["Drenaj Boruları","Geotekstil","Drenaj Çakılı","Yüzey Drenajı","Yağmur Suyu"]},

"03 – Beton":{
"Hazır Beton":["C25","C30","C35","C40","C50"],
"Prekast":["Kiriş","Panel","Döşeme","Merdiven","Kolon"],
"Beton Katkıları":["Akışkanlaştırıcı","Priz Geciktirici","Hızlandırıcı","Su Yalıtım","Hava Sürükleyici"],
"Donatı Sistemleri":["Nervürlü Demir","Hasır Çelik","Kafes Sistem","Bağ Teli","Donatı Kafesi"],
"Kalıp Sistemleri":["Ahşap Kalıp","Metal Kalıp","Tünel Kalıp","Plywood","Perde Kalıp"]},

"04 – Duvar Sistemleri":{
"Tuğla":["Dolu Tuğla","Delikli Tuğla","Asmolen","Dekoratif Tuğla","Şömine Tuğlası"],
"Gazbeton":["Blok","Panel","Lento","Kaplama","Yapıştırıcı"],
"Taş":["Doğal Taş","Granit","Mermer","Bazalt","Traverten"],
"Harç & Bağlayıcı":["Çimento","Kireç","Hazır Harç","Yapıştırıcı","Derz Dolgu"],
"Duvar Sistemleri":["Perde Duvar","Bölme Duvar","Yük Taşıyıcı","Hafif Duvar","Kuru Duvar"]},

"05 – Metal & Çelik":{
"İnşaat Demiri":["B420C","B500C","Hasır Çelik","Nervürlü Demir","Çubuk Demir"],
"Profil Çelik":["HEA","HEB","IPE","Kutu Profil","L Profil"],
"Ankraj":["Kimyasal Ankraj","Mekanik Ankraj","Ağır Yük Ankrajı","Hafif Yük Ankrajı","Dübel"],
"Çelik Yapılar":["Çelik Kolon","Çelik Kiriş","Çelik Çatı","Platform","Merdiven"],
"Bağlantı Elemanları":["Cıvata","Somun","Rondela","Perçin","Kaynak"]},

"06 – Ahşap & Kompozit":{
"Ahşap Yapı":["Lamine Ahşap","Masif Ahşap","Çatı Kirişi","Döşeme","Kaplama"],
"MDF":["Ham MDF","Lamine MDF","Neme Dayanıklı MDF","Boyalı MDF","Firex MDF"],
"CLT":["CLT Panel","CLT Döşeme","CLT Duvar","CLT Çatı","CLT Kolon"],
"Kompozit":["WPC","Fiber Panel","Alüminyum Kompozit","FRP","GRP"],
"Ahşap Kaplama":["Laminat","Veneer","Doğal Kaplama","PVC Kaplama","Lake"]},

"07 – İzolasyon & Su Yalıtımı":{
"Membran":["PVC Membran","Bitümlü Membran","EPDM","TPO","SBS"],
"Poliüretan":["Sprey Köpük","Likit Membran","Dolgu Köpüğü","Yalıtım Paneli","Enjeksiyon"],
"Bitüm":["Sıcak Bitüm","Soğuk Bitüm","Bitümlü Bant","Astar","Emülsiyon"],
"Isı Yalıtımı":["XPS","EPS","Taş Yünü","Cam Yünü","PIR"],
"Su Yalıtımı":["Likit","Kristalize","Çimento Bazlı","Pozitif","Negatif"]},

"08 – Kapı & Pencere":{
"Alüminyum":["Doğrama","Sürme","Isı Yalıtımlı","Cephe","Kaplama"],
"PVC":["Pencere","Kapı","Sürme","Kasa","Profil"],
"Çelik Kapı":["Daire","Yangın","Villa","Güvenlik","Endüstriyel"],
"Cam Sistemleri":["Temperli","Lamine","Low-E","Reflekte","Akıllı Cam"],
"Aksesuarlar":["Kilit","Menteşe","Kol","Sızdırmazlık","Ray"]},

"09 – İç Kaplama":{
"Boya":["İç Cephe","Dış Cephe","Epoksi","Akrilik","Silikon"],
"Seramik":["Duvar","Zemin","Porselen","Mozaik","Dekor"],
"Parke":["Laminat","Lamine","Masif","Vinil","PVC"],
"Alçı Sistemleri":["Alçıpan","Alçı Sıva","Kartonpiyer","Asma Tavan","Derz"],
"Zemin Kaplama":["Halı","Epoksi","Beton Parlatma","PVC","LVT"]},

"10 – Sabit Donatılar":{
"Dolap":["Gömme","Vestiyer","Arşiv","Banyo","Mutfak"],
"Mutfak":["Dolap","Tezgah","Ankastre","Tezgah Üstü","Modül"],
"Banyo":["Lavabo","Duş","Rezervuar","Ayna","Dolap"],
"Sabit Donatı":["Raf","Banko","Masa","Tezgah","Panel"],
"Aksesuar":["Kulp","Ray","Menteşe","Kilit","Tutamak"]},

"11 – Özel Sistemler":{
"Asansör":["Yolcu Asansörü","Yük Asansörü","Panoramik Asansör","Hidrolik Asansör","Makine Dairesiz"],
"Yürüyen Sistemler":["Yürüyen Merdiven","Yürüyen Bant","Eğimli Bant","AVM Sistemleri","Dış Mekan"],
"Otomasyon":["Akıllı Bina","Kontrol Sistemleri","Sensör","SCADA","BMS"],
"Güvenlik Sistemleri":["Kartlı Geçiş","Bariyer","X-Ray","Alarm","Yangın Alarm"],
"Özel Sistemler":["Otopark","Döner Kapı","Hızlı Kapı","Turnike","Geçiş Kontrol"]},

"12 – Mobilya":{
"Ofis Mobilyası":["Masa","Sandalye","Dolap","Toplantı Masası","Seperatör"],
"Sabit Mobilya":["Resepsiyon","Tezgah","Raf","Vitrin","Panel"],
"Dekorasyon":["Ayna","Duvar Paneli","Süs Elemanları","Heykel","Tablo"],
"Soft Mobilya":["Koltuk","Kanepe","Puf","Berjer","Oturma Grubu"],
"Aksesuar":["Aydınlatma","Halı","Perde","Stor","Plise"]},

"13 – Endüstriyel Sistemler":{
"Fabrika Ekipmanları":["Konveyör","Raf Sistemleri","Makine Kaidesi","Vinç","Kaldırma"],
"Endüstriyel Hatlar":["Paketleme","Üretim Hattı","Otomasyon","Robotik","Kontrol"],
"Depolama Sistemleri":["Depo Rafı","Yük Rafı","ASRS","Palet Rafı","Kayar Raf"],
"İşleme Sistemleri":["CNC","Lazer Kesim","Plazma","Torna","Freze"],
"Endüstriyel Altyapı":["Hava Hatları","Gaz Hatları","Su Hatları","Drenaj","Kanal"]},

"14 – Dış Cephe":{
"Giydirme Cephe":["Stick Sistem","Panel Sistem","Spider Sistem","Silikon Cephe","Yarı Kapaklı"],
"Cam Sistemleri":["Temperli","Lamine","Low-E","Reflekte","Akıllı Cam"],
"Cephe Kaplama":["Alüminyum Kompozit","Seramik Cephe","Doğal Taş","Fiber Cement","HPL"],
"Yalıtım Cephe":["Mantolama","XPS","EPS","Taş Yünü","Cam Yünü"],
"Aksesuarlar":["Cephe Ankraj","Sızdırmazlık","Silikon","Fitil","Ray"]},

"15 – Mekanik HVAC":{
"Chiller":["Hava Soğutmalı","Su Soğutmalı","Scroll","Vidalı","Absorbsiyon"],
"VRF":["Heat Pump","Heat Recovery","Mini VRF","Multi Sistem","Tek Split"],
"Klima":["Split","Kaset Tipi","Salon Tipi","Duvar Tipi","Tavan Tipi"],
"Havalandırma":["Fan","Menfez","Kanal","Difüzör","Hava Perdesi"],
"Isıtma":["Kazan","Radyatör","Yerden Isıtma","Isı Pompası","Elektrikli Isıtma"]},

"16 – Tesisat":{
"Boru":["PPRC","Çelik","PE","PVC","HDPE"],
"Armatür":["Batarya","Vana","Mix","Termostatik","Duvar Tipi"],
"Yangın":["Sprinkler","Dolap","Pompa","Hidrant","Alarm"],
"Kanalizasyon":["PVC Boru","HDPE Boru","Rögar","Menhol","Kapak"],
"Temiz Su":["Depo","Hidrofor","Filtre","Arıtma","Sayaç"]},

"17 – Elektrik":{
"Kablo":["NYY","TTR","Data","Fiber","Koaksiyel"],
"Trafo":["Kuru Tip","Yağlı","Dağıtım","Güç","Modüler"],
"Pano":["Ana Pano","Kat Pano","Kompanzasyon","Dağıtım","Otomasyon"],
"Aydınlatma":["LED","Projektör","Acil","Sokak","Dekoratif"],
"Jeneratör":["Dizel","Gaz","Hibrit","Portatif","Endüstriyel"]},

"18 – Zayıf Akım & Dijital":{
"CCTV":["IP Kamera","NVR","PTZ","Dome","Bullet"],
"Fiber":["Kablo","ODF","Patch Panel","Konnektör","Ek"],
"IoT":["Sensör","Gateway","Sayaç","Kontrol","Veri"],
"Ağ Sistemleri":["Switch","Router","Firewall","Access Point","Kablo"],
"Yazılım":["BMS","SCADA","ERP","IoT Platform","Analitik"]},

"19 – Peyzaj & Altyapı":{
"Bordür":["Beton","Granit","Dekoratif","Plastik","Doğal Taş"],
"Sulama":["Damla","Sprink","Kontrol","Boru","Vana"],
"Kanalizasyon":["Koruge","Rögar","Kapak","Baca","Drenaj"],
"Peyzaj":["Ağaç","Çim","Bitki","Toprak","Gübre"],
"Yol Sistemleri":["Asfalt","Beton","Kilit Taşı","Kaplama","Yol Çizgi"]},

"20 – Enerji & Yeni Nesil":{
"Güneş":["PV Panel","İnverter","Konstrüksiyon","Kablo","SCADA"],
"Batarya":["LFP","MCAP","Lityum","Hibrit","Depolama"],
"Şarj":["AC","DC","Hızlı","İstasyon","Yönetim"],
"Hidrojen":["Elektroliz","Depolama","Taşıma","Kullanım","Altyapı"],
"Yeni Nesil Sistemler":["Akıllı Şebeke","Mikrogrid","Enerji Yönetimi","Karbon Takip","ESG"]}
}

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #f1f5f9;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1200px;
}

.header-box {
    background: white;
    border-radius: 18px;
    padding: 18px;
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 20px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
}

.header-box img {
    width: 145px;
    height: 105px;
    object-fit: contain;
}

.main-title {
    font-size: 26px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
}

.sub-title {
    font-size: 16px;
    color: #475569;
    margin-top: 6px;
}

.metric-box {
    background: white;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    margin-bottom: 18px;
    height: 78px;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
}

.metric-label {
    font-size: 14px;
    color: #0f172a;
}

.metric-value {
    font-size: 26px;
    font-weight: 800;
    color: #ef3340;
    line-height: 1.2;
}

.section-box {
    background: white;
    border-radius: 18px;
    padding: 18px;
    margin-top: 18px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 16px;
}

.stButton > button {
    width: 100%;
    height: 72px !important;
    min-height: 72px !important;
    max-height: 72px !important;

    border-radius: 12px;
    border: none;
    color: white;
    font-weight: 800;
    font-size: 15px;
    background: linear-gradient(135deg, #ef3340, #457b9d);

    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;

    padding: 10px 14px;
    white-space: normal;
    word-break: break-word;
    overflow: hidden;
    line-height: 1.2;
}

.stButton > button:hover {
    color: white;
    border: none;
    opacity: 0.92;
    transform: translateY(-1px);
}

div[data-testid="column"] {
    padding: 0 6px;
}

.alt-box {
    background: #f8fafc;
    border-left: 6px solid #ef3340;
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 10px;
}

input {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


def image_to_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_all_groups():
    groups = []
    for ana_grup in DATA:
        groups.extend(DATA[ana_grup].keys())
    return sorted(set(groups))


def get_all_alt_groups():
    alt_groups = []
    for ana_grup in DATA:
        for grup in DATA[ana_grup]:
            alt_groups.extend(DATA[ana_grup][grup])
    return sorted(set(alt_groups))


def filter_ana_gruplar(query):
    if not query:
        return list(DATA.keys())

    q = query.lower()
    result = []

    for ana_grup, gruplar in DATA.items():
        match = q in ana_grup.lower()

        for grup, altlar in gruplar.items():
            if q in grup.lower():
                match = True

            for alt in altlar:
                if q in alt.lower():
                    match = True

        if match:
            result.append(ana_grup)

    return result


logo_b64 = image_to_base64(LOGO_PATH)

if logo_b64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}">'
else:
    logo_html = '<div style="font-size:60px;">🏗️</div>'

st.markdown(
    f"""
    <div class="header-box">
        {logo_html}
        <div>
            <div class="main-title">Türkiye İnşaat Tedarik Sınıflandırma Sistemi</div>
            <div class="sub-title">(MasterFormat Tabanlı)</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if "secilen_ana_grup" not in st.session_state:
    st.session_state.secilen_ana_grup = None

if "secilen_grup" not in st.session_state:
    st.session_state.secilen_grup = None

ana_gruplar = list(DATA.keys())
gruplar = get_all_groups()
alt_gruplar = get_all_alt_groups()

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Ana Grup</div>
        <div class="metric-value">{len(ana_gruplar)}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Grup Sayısı</div>
        <div class="metric-value">{len(gruplar)}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Alt Grup Sayısı</div>
        <div class="metric-value">{len(alt_gruplar)}</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    secim = st.session_state.secilen_ana_grup or "-"
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Seçim</div>
        <div class="metric-value">{secim}</div>
    </div>
    """, unsafe_allow_html=True)

arama = st.text_input("Ara", placeholder="Beton, Demir, Kablo, Cephe...")

gosterilecek_ana_gruplar = filter_ana_gruplar(arama)

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">20 Ana Grup</div>', unsafe_allow_html=True)

for i in range(0, len(gosterilecek_ana_gruplar), 4):
    cols = st.columns(4)
    for j, ana_grup in enumerate(gosterilecek_ana_gruplar[i:i + 4]):
        with cols[j]:
            if st.button(ana_grup, key=f"ana_{ana_grup}"):
                st.session_state.secilen_ana_grup = ana_grup
                st.session_state.secilen_grup = None

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.secilen_ana_grup:
    secilen_gruplar = list(DATA[st.session_state.secilen_ana_grup].keys())

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-title">{st.session_state.secilen_ana_grup} İçindeki Gruplar</div>',
        unsafe_allow_html=True
    )

    for i in range(0, len(secilen_gruplar), 5):
        cols = st.columns(5)
        for j, grup in enumerate(secilen_gruplar[i:i + 5]):
            with cols[j]:
                if st.button(grup, key=f"grup_{st.session_state.secilen_ana_grup}_{grup}"):
                    st.session_state.secilen_grup = grup

    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.secilen_ana_grup and st.session_state.secilen_grup:
    secilen_alt_gruplar = DATA[st.session_state.secilen_ana_grup][st.session_state.secilen_grup]

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-title">{st.session_state.secilen_grup} İçindeki Alt Gruplar</div>',
        unsafe_allow_html=True
    )

    for alt_grup in secilen_alt_gruplar:
        st.markdown(f'<div class="alt-box">{alt_grup}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
