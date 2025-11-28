import time
from scapy.all import IP, TCP, send
import random

# Target: We send packets to a random Google server just to generate traffic
# We are NOT attacking Google, we are just sending data OUT of your interface
target_ip = "8.8.8.8" 

print("--- STARTING SIMULATED ATTACK ---")
print("Injecting Malicious Traffic (Small Packets, SYN Flags)...")

while True:
    # We fake the Source IP as "10.10.10.10" (The 'Bad Guy')
    # Warning: Some routers block spoofed IPs, but let's try.
    fake_ip = "10.10.10.10"
    
    packet = IP(src=fake_ip, dst=target_ip)/TCP(dport=80, flags="S")
    
    send(packet, verbose=False)
    print(f"Sent Spoofed Packet from {fake_ip}")
    
    time.sleep(1)