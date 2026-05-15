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

# thread çakışmalarını önlemek için kilit gerekiyor
kilit = threading.Lock()


# TCP istemcilerini dinleyen fonksiyon
def tcp_dinle():

    while True:

        # Yeni bağlantı gelene kadar beklenecek.
        istemci_soketi, adres = tcp_sunucu.accept()

        print(f"Yeni TCP bağlantısı geldi -> {adres}")


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