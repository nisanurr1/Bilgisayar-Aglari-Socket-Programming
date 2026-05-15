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

# Kullanıcıdan kullanıcı adı alınır
kullanici_adi = input("Kullanıcı adınızı giriniz: ")

# Kullanıcı adı sunucuya gönderilir
istemci_soketi.send(kullanici_adi.encode("utf-8"))

print("Kullanıcı adı sunucuya gönderildi.")