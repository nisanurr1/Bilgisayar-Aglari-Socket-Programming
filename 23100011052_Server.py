import socket
import threading

# Sunucunun çalışacağı IP adresi
HOST = '127.0.0.1'

# PDF'te verilen TCP ve UDP port numaraları

TCP_PORT = 12345
UDP_PORT = 12346

BUFFER_SIZE = 1024

# TCP istemcilerini tutmak için liste ve UDP istemcileri için sözlük olacak 
# çünkü UDP istemcileri sadece IP adresi ve port numarası ile tanımlanır
tcp_istemciler = []
udp_istemciler = []

# kullanıcı adlarını tutmak için küme olacak, benzersiz oldukları için
kullanici_adlari = set()

# thread çakışmalarını önlemek için lock yani kilit gerekiyor
lock = threading.Lock()


# TCP istemcilerini dinleyen fonksiyon
def tcp_dinle():

    while True:

        # Yeni bağlantı gelene kadar beklenecek.
        istemci_soketi, adres = tcp_sunucu.accept()

        print(f"Yeni TCP bağlantısı geldi -> {adres}")

        while True:

            # İstemciden kullanıcı adı alınır
            kullanici_adi = istemci_soketi.recv(BUFFER_SIZE).decode("utf-8")

            ## print(f"{kullanici_adi} [TCP] ile sohbet odasına katılmak istiyor.")
            # Burada kullanıcı adının benzersiz olup olmadığı kontrol edilecek.
            kullanici_adi_kontrol = kullanici_adi.lower()

            with lock:
                # Aynı ada sahip başka biri var mı kontrol edilecek.
                if kullanici_adi_kontrol in kullanici_adlari: 
                    istemci_soketi.send("Bu kullanıcı adı zaten alınmış, lütfen başka bir tane deneyin.".encode("utf-8"))
                
                # Kullanıcı adı kimsede yoksa, kullanici_adlarina eklenecek.
                else:
                    kullanici_adlari.add(kullanici_adi_kontrol)
                    tcp_istemciler.append({
                        "soket": istemci_soketi,
                        "kullanici_adi": kullanici_adi,
                        "protokol": "TCP"
                    })
                    # Kullanıcı eklenince, hoşgeldiniz mesajı gönderilecek ve sohbet odasına katıldığı bildirilecek.
                    istemci_soketi.send(
                        f"Hoşgeldiniz {kullanici_adi}, [TCP] ile bağlısınız!".encode("utf-8")
                    )

                    print(f"{kullanici_adi} - [TCP] ile sohbet odasına katıldı.")

                    break
                

# UDP mesajlarını dinleyen fonksiyon
def udp_dinle():

    while True:

        # UDP mesajı beklenir
        veri, adres = udp_sunucu.recvfrom(BUFFER_SIZE)

        print(f"UDP mesajı alındı -> {adres}")


# TCP ve UDP soketi oluşturulur
tcp_sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sunucu = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TCP soketi belirtilen IP ve porta bağlanır
tcp_sunucu.bind((HOST, TCP_PORT))

# UDP soketi belirtilen IP ve porta bağlanır, hostları aynı olacak aynı sunucu üzerinden çalışacakları için
udp_sunucu.bind((HOST, UDP_PORT))

# TCP bağlantıları dinlenmeye başlanacak.
tcp_sunucu.listen()

print("Sunucu başlatıldı.")
print(f"TCP -> {HOST}:{TCP_PORT}")
print(f"UDP -> {HOST}:{UDP_PORT}")


# TCP dinleme thread'i oluşturulur
tcp_thread = threading.Thread(target=tcp_dinle)

# UDP dinleme thread'i oluşturulur
udp_thread = threading.Thread(target=udp_dinle)

# Son kısımda tcp ve udp dinlemelerinde threading kullanmasaydık, sunucu sadece TCP veya sadece UDP'yi dinleyebilirdi, ikisini aynı anda dinleyemezdi. 
# Threading sayesinde her iki protokolü de aynı anda dinleyebiliriz.

# Thread'ler çalıştırılır
tcp_thread.start()
udp_thread.start()