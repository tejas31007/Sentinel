import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter

fig, ax = plt.subplots()

def animate(i):
    try:
        with open("dashboard_data.txt", "r") as f:
            ips = f.readlines()
        
        ips = [ip.strip() for ip in ips]
        counts = Counter(ips)
        
        ax.clear()
        if counts:
            ax.bar(counts.keys(), counts.values(), color='red')
            ax.set_title("Sentinel Active Defense: Real-Time Blocks")
            ax.set_ylabel("Packets Dropped")
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
    except FileNotFoundError:
        pass

ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
plt.show()