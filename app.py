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

# --- yardımcı fonksiyonlar (virgüllü giriş için) ---
def parse_number(value):
    try:
        return int(str(value).replace(",", "").replace(".", "").strip())
    except:
        return 0

def formatted_text_input(label, default_value, key):
    return parse_number(
        st.text_input(label, value=f"{default_value:,}", key=key)
    )

# =========================================================
# GELİR HESAPLAMA PANELİ
# =========================================================

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Gelir Hesaplama Paneli</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    insaat_firma_sayisi = formatted_text_input(
        "1. İnşaat Firması Sayısı (Yıllık Abone İnşaat Firması Sayısı)",
        1000,
        "insaat_firma_sayisi"
    )

with c2:
    insaat_sistem_bedeli = formatted_text_input(
        "2. İnşaat Firması Sistem Kullanım Bedeli",
        10000,
        "insaat_sistem_bedeli"
    )

yillik_kazanc_insaat = insaat_firma_sayisi * insaat_sistem_bedeli * 0.20

st.markdown(f"""
<div class="alt-box">
    3. Yıllık Kazanç (İnşaat Firması): {yillik_kazanc_insaat:,.0f} TL
</div>
""", unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    tedarikci_sayisi = formatted_text_input(
        "4. Tedarikçi Sayısı (Yıllık Abone Tedarikçi Sayısı)",
        5000,
        "tedarikci_sayisi"
    )

with c4:
    tedarikci_sistem_bedeli = formatted_text_input(
        "5. Tedarikçi Sistem Kullanım Bedeli",
        5000,
        "tedarikci_sistem_bedeli"
    )

yillik_kazanc_tedarikci = tedarikci_sayisi * tedarikci_sistem_bedeli * 0.20
toplam_kazanc = yillik_kazanc_insaat + yillik_kazanc_tedarikci

st.markdown(f"""
<div class="alt-box">
    6. Yıllık Kazanç (Tedarikçi): {yillik_kazanc_tedarikci:,.0f} TL
</div>

<div class="total-box">
    7. Toplam Kazanç: {toplam_kazanc:,.0f} TL
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
