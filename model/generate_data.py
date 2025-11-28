import random
import pandas as pd
import numpy as np

NUM_SAMPLES = 5000
data = []

print("Generating synthetic network traffic...")

for _ in range(NUM_SAMPLES):
    if random.random() < 0.5:
        src_port = random.randint(1024, 65535)
        dst_port = random.choice([80, 443, 53, 8080])
        packet_size = random.randint(100, 1500)
        flags = 16
        label = 0 
    else:
        src_port = random.randint(1024, 65535)
        dst_port = random.choice([80, 443, 22, 21]) 
        packet_size = random.randint(40, 60) 
        flags = 2
        label = 1 

    data.append([src_port, dst_port, packet_size, flags, label])

df = pd.DataFrame(data, columns=["src_port", "dst_port", "packet_size", "flags", "label"])
df.to_csv("traffic_data.csv", index=False)
print(f"Success! {NUM_SAMPLES} packets saved to 'traffic_data.csv'.")