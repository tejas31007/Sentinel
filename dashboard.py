import matplotlib
matplotlib.use('TkAgg') # <--- 1. FORCE THE WINDOW TO OPEN
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter

fig, ax = plt.subplots()

def animate(i):
    try:
        # Read the log file
        with open("dashboard_data.txt", "r") as f:
            ips = f.readlines()
        
        # Count attacks
        ips = [ip.strip() for ip in ips]
        counts = Counter(ips)
        
        # Draw
        ax.clear()
        if counts:
            ax.bar(counts.keys(), counts.values(), color='red')
            ax.set_title("Sentinel Active Defense: Real-Time Blocks")
            ax.set_ylabel("Packets Dropped")
            
            # Make it look cool (rotate IP addresses so they don't overlap)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
    except FileNotFoundError:
        pass

# <--- 2. ADDED 'cache_frame_data=False' TO FIX THE WARNING
ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
plt.show()