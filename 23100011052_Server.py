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
udp_istemciler = {}

# kullanıcı adlarını tutmak için küme olacak, benzersiz oldukları için
kullanici_adlari = set()

# thread çakışmalarını önlemek için lock yani kilit gerekiyor
lock = threading.Lock()


def tcp_istemci_mesajlarini_dinle(istemci_soketi, kullanici_adi):

    while True:
        try:
            # TCP istemcisinden mesaj alınacak.
            mesaj = istemci_soketi.recv(BUFFER_SIZE).decode("utf-8")

            # Boş mesajlar yayınlanmayacak.
            if mesaj.strip() == "":
                continue

            if mesaj:
                print(f"{kullanici_adi} [TCP]: {mesaj}")

                # mesaj diğer TCP istemcilerine gönderilecek.
                genel_mesaj_broadcast(f"{kullanici_adi} [TCP]: {mesaj}","TCP", istemci_soketi)
            else:
                # Bağlantı kapatıldıysa döngüden çıkılır
                break
        except:
            break

    with lock:
        # İstemci bağlantısı kapatıldığında, kullanıcı adı ve soket listelerinden çıkarılır.
        for istemci in tcp_istemciler:
            if istemci["soket"] == istemci_soketi:
                tcp_istemciler.remove(istemci)
                kullanici_adlari.remove(kullanici_adi.lower())
                print(f"{kullanici_adi} [TCP] sohbet odasından ayrıldı.")
                break

    ayrilma_mesaji = f"{kullanici_adi} - [TCP] sohbet odasından ayrıldı."

    genel_mesaj_broadcast(ayrilma_mesaji, "TCP", istemci_soketi)

    istemci_soketi.close()


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

                    tcp_istemci_thread = threading.Thread(
                        target=tcp_istemci_mesajlarini_dinle,
                        args=(istemci_soketi, kullanici_adi)
                    )

                    tcp_istemci_thread.start()

                    break
          

def genel_mesaj_broadcast(mesaj, gonderen_tur, gonderen_bilgi):

    with lock:

        # Mesaj tüm TCP istemcilere gönderilir
        for istemci in tcp_istemciler:

            # Eğer gönderen TCP ise, kendi soketine geri gönderilmez
            if gonderen_tur == "TCP" and istemci["soket"] == gonderen_bilgi:
                continue

            try:
                istemci["soket"].send(mesaj.encode("utf-8"))
            except:
                pass

        # Mesaj tüm UDP istemcilere gönderilir
        for adres in udp_istemciler:

            # Eğer gönderen UDP ise, kendi adresine geri gönderilmez
            if gonderen_tur == "UDP" and adres == gonderen_bilgi:
                continue

            try:
                udp_sunucu.sendto(mesaj.encode("utf-8"), adres)
            except:
                pass


# UDP mesajlarını dinleyen fonksiyon
def udp_dinle():

    while True:

        # UDP istemcisinden veri alınır
        veri, adres = udp_sunucu.recvfrom(BUFFER_SIZE)

        # Gelen veri metne çevrilir
        mesaj = veri.decode("utf-8")

        # Eğer bu adres daha önce kayıtlı değilse, gelen ilk mesaj kullanıcı adı kabul edilir
        if adres not in udp_istemciler:

            kullanici_adi = mesaj
            kullanici_adi_kontrol = kullanici_adi.lower()

            with lock:

                # Aynı kullanıcı adı TCP veya UDP tarafında varsa kabul edilmez
                if kullanici_adi_kontrol in kullanici_adlari:

                    udp_sunucu.sendto(
                        "Bu kullanıcı adı zaten alınmış, lütfen başka bir tane deneyin.".encode("utf-8"),
                        adres
                    )

                else:

                    # Kullanıcı adı uygun ise kullanıcı sisteme eklenir
                    kullanici_adlari.add(kullanici_adi_kontrol)

                    udp_istemciler[adres] = kullanici_adi

                    udp_sunucu.sendto(
                        f"Hoşgeldiniz {kullanici_adi}, [UDP] ile bağlısınız!".encode("utf-8"),
                        adres
                    )

                    print(f"{kullanici_adi} - [UDP] ile sohbet odasına katıldı.")

        else:
            kullanici_adi = udp_istemciler[adres]

            # UDP istemcisi tam olarak "Gorusuruz" yazarsa sohbet odasından ayrılacak
            if mesaj == "Gorusuruz":

                with lock:
                    del udp_istemciler[adres]
                    kullanici_adlari.remove(kullanici_adi.lower())

                ayrilma_mesaji = f"{kullanici_adi} - [UDP] sohbet odasından ayrıldı."

                print(ayrilma_mesaji)

                genel_mesaj_broadcast(ayrilma_mesaji, "UDP", adres)

                continue

            # Boş UDP mesajları yayınlanmaz
            if mesaj.strip() == "":
                continue

            print(f"{kullanici_adi} [UDP]: {mesaj}")

            genel_mesaj_broadcast(
                f"{kullanici_adi} [UDP]: {mesaj}",
                "UDP",
                adres
            )
            


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

# Ana programın hemen kapanmaması için thread'ler beklenecek.
tcp_thread.join()
udp_thread.join()
# join sayesinde server çalışmaya devam eder, TCP ve UDP thread'leri açık kalır.