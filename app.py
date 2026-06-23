import streamlit as st
import pandas as pd

# Sayfa Yapılandırması (Geniş Ekran)
st.set_page_config(layout="wide", page_title="Bio_Node Simülatörü", page_icon="🌿")
st.title("🌿 Bio_Node: Uçtan Uca Maliyet ve Deneyim Simülatörü")
st.divider()

# ==========================================
# 1. BÖLÜM: KULLANICI KONTROL PANELİ (Sol Menü)
# ==========================================
st.sidebar.header("📡 Anlık Sensör ve Tercihler")
sicaklik = st.sidebar.slider("Dış Ortam Sıcaklığı (°C)", min_value=0, max_value=45, value=38)

st.sidebar.divider()
st.sidebar.subheader("👤 Konut Sakini (Beyhan) Tercihi")
sadece_elektrik_modu = st.sidebar.checkbox("Sadece Soğutma (Elektrik) Modunu Kullan")

# ==========================================
# 2. BÖLÜM: MATEMATİKSEL HESAPLAMALAR
# ==========================================
baz_elektrik = 15000   
baz_su = 8000          
baz_dogalgaz = 5000    

# Site Geneli Hesaplamalar
if sicaklik >= 25:
    eski_elektrik = baz_elektrik + ((sicaklik - 25) * 1200)
    yeni_elektrik = eski_elektrik * 0.70
    yeni_su = baz_su * 0.85
    eski_dogalgaz = baz_dogalgaz   # <--- EKSİK OLAN SATIR EKLENDİ
    yeni_dogalgaz = baz_dogalgaz
    sistem_mesaji = "🟢 AKTİF (Optimum Soğutma Modu)"
    hissedilen = sicaklik - 4
else:
    eski_elektrik = baz_elektrik
    yeni_elektrik = eski_elektrik
    yeni_su = baz_su
    eski_dogalgaz = baz_dogalgaz + ((25 - sicaklik) * 1500) if sicaklik < 15 else baz_dogalgaz
    yeni_dogalgaz = eski_dogalgaz * 0.80 if sicaklik < 15 else eski_dogalgaz
    sistem_mesaji = "🔵 AKTİF (Kış/Yalıtım Modu)" if sicaklik < 15 else "⚪ PASİF (İdeal Sıcaklık)"
    hissedilen = sicaklik + 2 if sicaklik < 15 else sicaklik

# Beyhan'ın Kişisel Tasarruf Hesaplamaları (Seçime Göre Dinamik Değişir)
beyhan_elektrik_tasarruf = int((eski_elektrik - yeni_elektrik) / 50)

if sadece_elektrik_modu:
    beyhan_su_tasarruf = 0
    beyhan_dogalgaz_tasarruf = 0
    beyhan_bakim_payi = 100 
    paket_durumu = "Sadece Soğutma Paketi"
else:
    beyhan_su_tasarruf = 36 if sicaklik >= 25 else 0
    beyhan_dogalgaz_tasarruf = 80 if sicaklik < 15 else 0
    beyhan_bakim_payi = 156 
    paket_durumu = "Tam Entegrasyon"

beyhan_net_kazanc = beyhan_elektrik_tasarruf + beyhan_su_tasarruf + beyhan_dogalgaz_tasarruf - beyhan_bakim_payi

# ==========================================
# 3. BÖLÜM: GÖRSEL ARAYÜZ (Ekranı İkiye Bölme)
# ==========================================
col_mobil, col_panel = st.columns([1.5, 2.5])

# --- SOL TARAF: MOBİL UYGULAMA ---
with col_mobil:
    st.subheader("📱 Kullanıcı Deneyimi (Beyhan)")
    mobil_arayuz = f"""
_____________________________________________________________
|                                                             |
|  09:41  LTE 📶                                         🔋 %85 |
|                                                             |
|  👤 Merhaba Beyhan!                                           |
|  📍 Avrupa Konutları, C Blok, D.12                          |
| ___________________________________________________________ |
|                                                             |
|  🌿 SİSTEM: {sistem_mesaji}             |
|  📦 Paket: {paket_durumu}               |
|                                                             |
|  [ Dış Ortam ]         [ Bio_Node Etkisi ]                  |
|     {sicaklik}°C        ➡️           {hissedilen}°C                 |
| ___________________________________________________________ |
|                                                             |
|  💰 KİŞİSEL TASARRUF DETAYI (Bu Ay)                         |
|  -------------------------------------------                |
|  ⚡ Elektrik (Klima Azalması) :  +{beyhan_elektrik_tasarruf} TL                   |
|  💧 Su (Ortak Alan İndirimi)  :  +{beyhan_su_tasarruf} TL                   |
|  🔥 Doğalgaz (Yalıtım)        :  +{beyhan_dogalgaz_tasarruf} TL                   |
|  🛠️ Sistem Bakım Payı         :  -{beyhan_bakim_payi} TL                   |
|  -------------------------------------------                |
|  ✨ NET KAZANÇ  : +{beyhan_net_kazanc} TL                                 |
| ___________________________________________________________ |
|                                                             |
|        [ 🎛️ PAKETİ DEĞİŞTİR / AYARLAR ]                     |
| =========================================================== |
|     🏠          📊          🌿         ⚙️                 |
|  Ana Sayfa   Finans     Alg Durumu   Ayarlar              |
|_____________________________________________________________|
"""
    st.code(mobil_arayuz, language="text")

# --- SAĞ TARAF: YÖNETİM PANELİ ---
with col_panel:
    st.subheader("🏢 Emlak Konut Site Yönetimi Paneli")
    st.write("Sistem, kullanıcının abonelik paketine ve anlık sıcaklığa göre eşzamanlı optimize ediliyor.")
    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("⚡ ELEKTRİK (Toplam)", f"{int(yeni_elektrik):,} TL", f"- {int(eski_elektrik - yeni_elektrik):,} TL", delta_color="inverse")
    m2.metric("💧 SU (Toplam)", f"{int(yeni_su):,} TL", f"- {int(baz_su - yeni_su):,} TL", delta_color="inverse")
    m3.metric("🔥 DOĞALGAZ (Toplam)", f"{int(yeni_dogalgaz):,} TL", f"- {int(eski_dogalgaz - yeni_dogalgaz):,} TL", delta_color="inverse")
    
    toplam_tasarruf = (eski_elektrik - yeni_elektrik) + (baz_su - yeni_su) + (eski_dogalgaz - yeni_dogalgaz)
    st.success(f"### 💰 50 Konutluk Pilot Alanda Toplam Aylık Net Tasarruf: {int(toplam_tasarruf):,} TL")
    
    grafik_verisi = pd.DataFrame({
        'Fatura Kalemi': ['Elektrik', 'Elektrik', 'Su', 'Su', 'Doğalgaz', 'Doğalgaz'],
        'Durum': ['1. Geleneksel', '2. Bio_Node', '1. Geleneksel', '2. Bio_Node', '1. Geleneksel', '2. Bio_Node'],
        'Tutar (TL)': [eski_elektrik, yeni_elektrik, baz_su, yeni_su, eski_dogalgaz, yeni_dogalgaz]
    })
    st.bar_chart(grafik_verisi.pivot(index='Fatura Kalemi', columns='Durum', values='Tutar (TL)'))