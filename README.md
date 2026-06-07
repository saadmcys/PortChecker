# Network Inventory Scanner

![Network Scanner Tool](https://raw.githubusercontent.com/your-username/your-repo/main/assets/banner.png)

A powerful Python-based network scanning tool designed to discover devices in a local network, analyze open ports, and calculate risk levels for each host using Nmap and psutil.

---

## 🔍 Overview

This tool performs advanced local network analysis by:

- Detecting active devices in the LAN
- Scanning open TCP ports on each host
- Evaluating security risk based on exposed services
- Displaying results in a clean terminal UI using Rich

---

## ⚡ Features

- Automatic network interface detection
- LAN host discovery using Nmap
- Open port scanning for each device
- Smart risk scoring system (0–100%)
- Risk classification:
  - LOW
  - MEDIUM
  - HIGH
  - CRITICAL
- Beautiful CLI output with Rich tables
- Cross-platform support (Windows / Linux)

---

## 📦 Requirements

Install dependencies using:

```bash
pip install python-nmap psutil rich
```

### System Requirement

You must also install **Nmap**:

- https://nmap.org/download.html

Make sure `nmap.exe` path is correctly set in the script if you're using Windows:

```python
NMAP_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"
```

---

## 🚀 Usage

Run the tool with:

```bash
python main.py
```

⚠️ Run as Administrator / Root for best results.

---

## 🧠 How It Works

1. Detects active network interfaces
2. Selects a valid IPv4 interface
3. Generates local subnet (e.g., /24)
4. Performs host discovery using ping scan (-sn)
5. Scans common ports:
   21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 5900, 8080
6. Calculates risk score based on exposed services
7. Displays structured scan results in terminal

---

## 📊 Risk Scoring System

- LOW: 0 - 19
- MEDIUM: 20 - 49
- HIGH: 50 - 79
- CRITICAL: 80 - 100

Risk is calculated based on exposed services such as SSH, RDP, SMB, databases, and remote access ports.

---

## ⚠️ Legal Disclaimer

This tool is intended for educational purposes and authorized security testing only.

Unauthorized scanning of networks you do not own or have permission to test is illegal.

---

## 👨‍💻 Author

Developed using Python, Nmap, psutil, and Rich for cybersecurity and network analysis purposes.
