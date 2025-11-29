Sentinel: AI-Powered Hybrid IDS 🛡️

Sentinel is a next-generation Intrusion Prevention System (IPS) that combines high-performance C++ packet processing with a Machine Learning brain to detect and block network attacks in real-time.

It features a Live Cyberpunk Dashboard to visualize threats as they are neutralized.

🚀 Features

High-Performance Sniffer: Custom C++ engine using libpcap and raw sockets for line-speed processing.

AI Brain: Embedded ONNX Runtime model (Random Forest) classifies packets (e.g., SYN Floods) in microseconds.

Active Defense: Automatically updates Linux iptables firewall rules to block malicious IPs immediately.

Visual Dashboard: Real-time web interface (Flask + Chart.js) displaying attack metrics and dropped packets.

🛠️ Architecture

Capture: C++ Engine listens to the Wi-Fi/Ethernet interface.

Analysis: Parses TCP/IP headers and extracts features (Size, Ports, Flags).

Inference: Data is fed into the sentinel.onnx AI model within the C++ runtime.

Defense:

If Malicious: Executes iptables DROP rule & logs to dashboard_data.txt.

If Safe: Traffic is allowed to pass.

Visualization: Python Flask server reads logs and updates the Web UI via AJAX.

📦 Installation

1. Prerequisites (Linux/Ubuntu)

sudo apt update
sudo apt install build-essential cmake libpcap-dev python3-pip python3-tk


2. Build the C++ Engine

cd cpp
# Compile with ONNX Runtime linking
g++ main.cpp -o sentinel -lpcap -I ../onnx_lib/include -L ../onnx_lib/lib -lonnxruntime


3. Setup Python Environment

# Go back to root
cd ..
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


⚡ Usage (Run in 3 Terminals)

Terminal 1: The Sentinel (Root required for Sniffing)

cd ~/Sentinel/cpp
sudo LD_LIBRARY_PATH=../onnx_lib/lib ./sentinel


Terminal 2: The Dashboard (Web Server)

cd ~/Sentinel
source venv/bin/activate
python3 server.py


View Dashboard at: http://127.0.0.1:5000

Terminal 3: Attack Simulation (Testing)

cd ~/Sentinel/model
source ../venv/bin/activate
sudo ../venv/bin/python3 attack.py


📂 Project Structure

Sentinel/
├── cpp/                 # C++ Source Code & Binary
│   ├── main.cpp         # Main Packet Inspection Engine
│   └── sentinel         # Compiled Executable
├── model/               # AI Training Lab
│   ├── generate_data.py # Synthetic Data Generator
│   ├── train_model.py   # Random Forest Trainer
│   └── attack.py        # Attack Simulator Script
├── templates/           # Web Frontend
│   └── index.html       # Cyberpunk Dashboard UI
├── onnx_lib/            # ONNX Runtime Libraries
├── dashboard_data.txt   # Live Log File
├── server.py            # Flask Backend
└── requirements.txt     # Python Dependencies


⚖️ License

MIT License - Educational Purpose Only.
Disclaimer: Do not use the