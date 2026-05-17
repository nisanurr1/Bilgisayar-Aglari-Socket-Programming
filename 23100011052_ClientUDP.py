import socket
import threading

# Sunucu bağlantı bilgileri
HOST = "127.0.0.1"
UDP_PORT = 12346
BUFFER_SIZE = 1024

# UDP istemci soketi oluşturulur
istemci_soketi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Sunucu adresi tanımlanır
# UDP'de server sadece IP ve port bilgilerini bilir, bağlantı kurulmaz.
sunucu_adresi = (HOST, UDP_PORT)

print("UDP istemcisi başlatıldı.")

def mesajlari_dinle():

    while True:
        try:
            # Sunucudan gelen UDP mesajı alınır
            veri, _ = istemci_soketi.recvfrom(BUFFER_SIZE)

            # Gelen veri metne çevrilir
            mesaj = veri.decode("utf-8")

            # Mesaj ekrana yazdırılır
            print("\n" + mesaj)

        except:
            print("Sunucu bağlantısı kesildi.")
            break

while True:

    # Kullanıcıdan kullanıcı adı alınır
    kullanici_adi = input("Kullanıcı adınızı giriniz: ")

    # UDP bağlantısız olduğu için kullanıcı adı ilk datagram olarak gönderilir
    istemci_soketi.sendto(kullanici_adi.encode("utf-8"), sunucu_adresi)

    # Sunucudan kullanıcı adı kabul/ret cevabı alınır
    cevap, _ = istemci_soketi.recvfrom(BUFFER_SIZE)

    # Gelen cevap metne çevrilir
    cevap = cevap.decode("utf-8")

    # Cevap ekrana yazdırılır
    print(cevap)

    # Kullanıcı adı kabul edildiyse döngüden çıkılır
    if cevap.startswith("Hoşgeldiniz"):
        break
dinleme_thread = threading.Thread(target=mesajlari_dinle, daemon=True)
dinleme_thread.start()

# Burada her veri paketi bağımsız olarak iletilir.
while True:

    # Kullanıcıdan mesaj alınır
    mesaj = input()

    # Mesaj sunucuya gönderilir
    istemci_soketi.sendto(
        mesaj.encode("utf-8"),
        sunucu_adresi
    )

    # Kullanıcı "Gorusuruz" yazarsa UDP istemcisi kapatılır
    if mesaj == "Gorusuruz":
        print("UDP sohbetinden ayrıldınız.")
        break

# UDP soketi kapatılır
istemci_soketi.close()