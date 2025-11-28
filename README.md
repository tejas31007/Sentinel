# Sentinel: AI-Powered Hybrid IDS 🛡️

Sentinel is a next-generation Intrusion Detection System (IDS) that combines high-performance C++ packet processing with a Machine Learning brain to detect and block network attacks in real-time.

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Language](https://img.shields.io/badge/Language-C%2B%2B%20%7C%20Python-blue)

## 🚀 Features
* **High-Performance Sniffer:** Custom C++ engine using `libpcap` and raw sockets.
* **AI Brain:** Embedded ONNX Runtime model (Random Forest) to detect malicious traffic patterns.
* **Active Defense:** Automatically updates Linux `iptables` firewall to block attacker IPs.
* **Real-Time Dashboard:** Live visualization of blocked threats using Python & Matplotlib.

## 🛠️ Architecture
1.  **Traffic Capture:** C++ Engine listens to the network interface.
2.  **Feature Extraction:** Parses TCP/IP headers to extract Packet Size, Ports, and Flags.
3.  **Inference:** Sends data to the `sentinel.onnx` model (inference time < 0.5ms).
4.  **Decision:** If malicious -> Executes `iptables` drop rule -> Logs to dashboard.

## 📦 Installation

### Prerequisites (Linux)
```bash
sudo apt install build-essential cmake libpcap-dev python3-pip python3-tk