import socket
import threading

# Sunucu bağlantı bilgileri
HOST = "127.0.0.1"
TCP_PORT = 12345
BUFFER_SIZE = 1024

# TCP istemci soketi oluşturulur
istemci_soketi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# İstemci TCP sunucusuna bağlanır
istemci_soketi.connect((HOST, TCP_PORT))

print("TCP sunucusuna bağlantı kuruldu.")

# sunucudan gelen mesajlar dinlenecek ve ekrana yazdırılacak.
def mesajlari_dinle():
    while True:
        try:
            # sunucudan gelen mesaj alınacak
            mesaj = istemci_soketi.recv(BUFFER_SIZE).decode("utf-8")

            print("\n" + mesaj)
        except:
            print("Sunucu bağlantısı kesildi.")
            break


while True:
        
    # Kullanıcıdan kullanıcı adı alınır
    kullanici_adi = input("Kullanıcı adınızı giriniz: ")

    # Kullanıcı adı sunucuya gönderilir
    istemci_soketi.send(kullanici_adi.encode("utf-8"))

    # Sunucudan gelen kabul ya da red mesajı alınır
    cevap = istemci_soketi.recv(BUFFER_SIZE).decode("utf-8")
    print(f"Sunucudan gelen mesaj: {cevap}")

    # Kullanıcı adı kabul edildiyse döngüden çıkılacak.

    if cevap.startswith("Hoşgeldiniz"):
        break    

# Mesajları almak için ayrı thread başlatılacak.
dinleme_thread = threading.Thread(target=mesajlari_dinle)
dinleme_thread.start()

while True:

    # Kullanıcıdan sohbet mesajı alınır
    mesaj = input()

    # Mesaj sunucuya gönderilir
    istemci_soketi.send(mesaj.encode("utf-8"))
