import csv

# Tır sınıfı
class TIR:
    # Tır nesnesi oluşturulurken çalışacak fonksiyon
    def __init__(self, gelis_zamani, plaka, ulke, tonaj_20, tonaj_30, yuk_miktari, yuk_maliyeti): 
        self.bilgi = {
            'ulke': ulke,
            'tonaj_20_adet': tonaj_20,
            'tonaj_30_adet': tonaj_30,
            'yuk_miktari': yuk_miktari,
            'yuk_maliyeti': yuk_maliyeti
        }
        self.gelis_zamani = gelis_zamani 
        self.plaka = plaka 

# Gemi sınıfı
class Gemi:
    # Gemi nesnesi oluşturulurken çalışacak fonksiyon
    def __init__(self, gelis_zamani, gemi_numarasi, kapasite, gidilecek_ulke):
        self.bilgi = {
            'gidilecek_ulke': gidilecek_ulke,
            'tonaj_20_adet': 0, # Geminin 20 tonluk konteyner sayısı başta 0 olarak tanımlandı
            'tonaj_30_adet': 0, # Geminin 30 tonluk konteyner sayısı başta 0 olarak tanımlandı
            'yuk_miktari': 0, # Geminin yük miktarı başta 0 olarak tanımlandı
            'yuk_maliyeti': 0 # Geminin yük maliyeti başta 0 olarak tanımlandı
        }
        self.gelis_zamani = gelis_zamani
        self.gemi_numarasi = gemi_numarasi
        self.kapasite = kapasite

# İstif alanı sınıfı
class IstifAlani:
    # İstif alanı nesnesi oluşturulurken çalışacak fonksiyon
    def __init__(self, kapasite):
        self.kapasite = kapasite
        self.yukler = []

    # İstif alanına yük ekleme fonksiyonu
    def yuk_ekle(self, yuk):
        if sum(yuk['yuk_miktari'] for yuk in self.yukler) + yuk['yuk_miktari'] <= self.kapasite: # Eğer istif alanının kapasitesi yük miktarından büyükse
            self.yukler.append(yuk) # Yükü istif alanına ekle
            return True
        else:
            return False

            
# Simülasyon sınıfı
class Simulasyon:
    def __init__(self, tir_listesi, gemi_listesi, istif_alanlari): # Simülasyon nesnesi oluşturulurken çalışacak fonksiyon
        self.tir_listesi = tir_listesi
        self.gemi_listesi = gemi_listesi
        self.limandaki_gemiler = [] # Limandaki gemileri tutan liste
        self.istif_alanlari = istif_alanlari 
        self.vinc_kullanim_sayisi = 0  # Vincin kaç kere kullanıldığını tutan değişken
        self.t = 1 # Zamanı başlangıç değeri olarak 1 olarak tanımladık

    # Simülasyonu başlatan fonksiyon
    def simulate(self):
        while len(self.gemi_listesi) > 0 or len(self.limandaki_gemiler) > 0: # Eğer en az gelecek bir gemi ya da limanda bekleyen bir gemi varsa.
            print(f"\nT Zamanı: {self.t}")

            self.vinc_kullanim_sayisi = 0 # Vincin kullanım sayısını sıfırla
            if self.istif_alanlari[0].yukler or self.istif_alanlari[1].yukler: # Eğer istif alanlarında yük varsa
                self.yukle() # Yükleri gemilere yükle
                self.indir() # TIR'ları indir
                self.yukle() # Yükleri gemilere yükle
                # Burada iki kere yükleme yapmamızın sebebi tırların oluşturacağı kalabalığı engelleyerek gemilerin daha hızlı yüklenmesini sağlamak
                # Bunu yapmadığımızda istif alanları daha erken doluyor ve simülasyon daha erken bitmek zorunda kalıyor.
            else: # Eğer yük yoksa normal sırayla yapılabilir.
                self.indir() # TIR'ları indir
                self.yukle() # Yükleri gemilere yükle
            
            self.t += 1 # Zamanı ilerlet

    # TIR'ları indiren fonksiyon
    def indir(self):
        print("TIR'lar indiriliyor:")
        for tir in self.tir_listesi:
            if tir.gelis_zamani == self.t: # Eğer TIR'ın gelis_zamani şu anki zamana eşitse
                print(f"{tir.plaka} plakalı TIR indiriliyor. Ülke: {tir.bilgi['ulke']}") # TIR'ın ülkesini yazdır
                self.yukleriIstifAlanaEkle(tir) # TIR'ın yükünü istif alanına ekle
            elif tir.gelis_zamani > self.t: # Eğer TIR'ın gelis_zamani şu anki zamandan büyükse bitir (TIR'lar gelis_zamani'na göre sıralı olduğu için)
                break 

    # Yükleri gemilere yükleyen fonksiyon
    def yukle(self):
        print("Gemilere yükleniyor:")

        # Gelen gemileri kontrol et
        for gemi in self.gemi_listesi:
            if gemi.gelis_zamani == self.t: # Eğer geminin gelis_zamani şu anki zamana eşitse
                self.limandaki_gemiler.append(gemi) # Gemiyi limandaki gemilere ekle
                self.gemi_listesi.pop(0) # Gemiyi gemi listesinden çıkar
                print(f"{gemi.gemi_numarasi} numaralı gemi limana yanaştı.")
            elif gemi.gelis_zamani > self.t: # Eğer geminin gelis_zamani şu anki zamandan büyükse bitir (Gemiler gelis_zamani'na göre sıralı olduğu için)
                break
            
        self.yukleriGemilereEkle()

    def yukleriIstifAlanaEkle(self, tir):
        
        yuk = tir.bilgi # TIR'ın yükünü al
        istif_alani = self.istif_alanlari[0] # İstif alanını al
        
        if istif_alani.yuk_ekle(yuk):
            print(f"{tir.plaka} plakalı TIR, istif alanına eklendi.")

            gemi = None # Gemiyi tanımla
            if len(self.limandaki_gemiler) > 0: # Eğer limandaki gemi sayısı 0'dan büyükse
                gemi = self.limandaki_gemiler[0] # Gemiyi limandaki gemilerden al

            # Eğer gemi varsa ve geminin gidilecek ülkesi yükün ülkesine eşitse ve geminin kapasitesi yeterliyse
            if gemi is not None and \
                    self.limandaki_gemiler[0].bilgi['gidilecek_ulke'] == yuk['ulke'] and \
                    gemi.bilgi['yuk_miktari'] + yuk['yuk_miktari'] <= gemi.kapasite:
                
                istif_alani.yukler.pop(-1) # Yükü istif alanından çıkar
                # Yükü gemiye ekle
                gemi.bilgi['tonaj_20_adet'] += yuk['tonaj_20_adet'] 
                gemi.bilgi['tonaj_30_adet'] += yuk['tonaj_30_adet']
                gemi.bilgi['yuk_miktari'] += yuk['yuk_miktari']
                gemi.bilgi['yuk_maliyeti'] += yuk['yuk_maliyeti']
                self.vinc_kullanim_sayisi += 1 # Vincin kullanım sayısını 1 arttır
                
        else: # Eğer istif alanına yük eklenemediyse
            print(f"{tir.plaka} plakalı TIR için uygun istif alanı bulunamadı. Beklemeye devam ediyor.")
            tir.gelis_zamani += 1 # TIR'ın gelis_zamani'ni 1 arttırarak tırın beklemesini sağla.


    # Yükleri gemilere yükleyen fonksiyon
    def yukleriGemilereEkle(self):
        
        for istif_alani in self.istif_alanlari: # Her istif alanı için

            try:
                gemi = self.limandaki_gemiler[0] # Gemiyi limandaki gemilerden al
                print(f"{gemi.gemi_numarasi} numaralı gemiye yükleniyor. Gidilecek Ülke: {gemi.bilgi['gidilecek_ulke']}")
            except IndexError: # Eğer limandaki gemi sayısı 0 ise bitir
                break

            while self.vinc_kullanim_sayisi < 50: # Vinç kullanım limitine ulaşılmadığı sürece

                if not istif_alani.yukler: # Eğer istif alanında yük yoksa bitir
                    break

                yuk = istif_alani.yukler[-1] # Yükü al

                # Geminin doluluğunu kontrol et.
                if gemi.bilgi['yuk_miktari'] >= 0.95 * gemi.kapasite or gemi.kapasite - gemi.bilgi['yuk_miktari'] <= 20: 
                    print(f"{gemi.gemi_numarasi} numaralı gemi dolu. Limandan ayrılıyor.")
                    self.limandaki_gemiler.pop(0) # Gemiyi limandaki gemilerden çıkar
                    
                    # Yeni gemiyi al
                    try:
                        gemi = self.limandaki_gemiler[0]
                        print(f"{gemi.gemi_numarasi} numaralı gemiye yükleniyor. Gidilecek Ülke: {gemi.bilgi['gidilecek_ulke']}") # 
                    except IndexError:
                        break

                    # Bir sonraki vinç operasyonuna geç
                    continue
                    
                # Eğer yükün ülkesi geminin gidilecek ülkesine eşitse ve geminin kapasitesi yeterliyse
                if yuk['ulke'] == gemi.bilgi['gidilecek_ulke'] and gemi.bilgi['yuk_miktari'] + yuk['yuk_miktari'] <= gemi.kapasite:

                    istif_alani.yukler.pop(-1) # Yükü istif alanından çıkar
                    # Gemiye yükü ekle
                    gemi.bilgi['tonaj_20_adet'] += yuk['tonaj_20_adet']
                    gemi.bilgi['tonaj_30_adet'] += yuk['tonaj_30_adet']
                    gemi.bilgi['yuk_miktari'] += yuk['yuk_miktari']
                    gemi.bilgi['yuk_maliyeti'] += yuk['yuk_maliyeti']
                    
                else: # Eğer yükün ülkesi geminin gidilecek ülkesine eşit değilse
                    
                    other_istif_alani = next(ia for ia in self.istif_alanlari if ia != istif_alani) # Diğer istif alanını al
                    other_istif_alani.yuk_ekle(yuk) # Yükü diğer istif alanına ekle
                    istif_alani.yukler.pop(-1) # Yükü bu istif alanından çıkar

                self.vinc_kullanim_sayisi += 1 # Vincin kullanım sayısını 1 arttır
            


def main():
    tir_listesi = [] # TIR'ların tutulacağı liste
    gemi_listesi = [] # Gemilerin tutulacağı liste
    istif_alan1 = IstifAlani(kapasite=750) # İstif alanı 1
    istif_alan2 = IstifAlani(kapasite=750) # İstif alanı 2

    istif_alanlari = [istif_alan1, istif_alan2] # İstif alanlarının tutulacağı liste

    with open('olaylar.csv', newline='', encoding='utf-8', errors='replace') as csvfile: # Olaylar dosyasını oku
        olaylar_reader = csv.reader(csvfile)
        next(olaylar_reader)  # Başlık satırını atla
        for row in olaylar_reader: # Her satır için
            gelis_zamani, plaka, ulke, tonaj_20, tonaj_30, yuk_miktari, yuk_maliyeti = row # Satırı değişkenlere ata
            tir = TIR(int(gelis_zamani), plaka, ulke, int(tonaj_20), int(tonaj_30), int(yuk_miktari), float(yuk_maliyeti)) # TIR nesnesi oluştur
            tir_listesi.append(tir) # TIR'ı listeye ekle

    with open('gemiler.csv', newline='', encoding='utf-8', errors='replace') as csvfile: # Gemiler dosyasını oku
        gemiler_reader = csv.reader(csvfile)
        next(gemiler_reader)  # Başlık satırını atla
        for row in gemiler_reader: # Her satır için
            gelis_zamani, gemi_adi, kapasite, gidilecek_ulke = row # Satırı değişkenlere ata
            gemi = Gemi(int(gelis_zamani), gemi_adi, int(kapasite), gidilecek_ulke) # Gemi nesnesi oluştur
            gemi_listesi.append(gemi) # Gemi'yi listeye ekle

    simulasyon = Simulasyon(tir_listesi, gemi_listesi, istif_alanlari) # Simülasyon nesnesi oluştur
    simulasyon.simulate() # Simülasyonu başlat

if __name__ == "__main__":
    main()
    
