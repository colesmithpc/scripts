# **Network Discovery & Port Scanning Tool**

A multithreaded Python tool for discovering devices on a local network, identifying hostnames, retrieving MAC addresses, and scanning for open ports.  
This utility is useful for **network auditing**, **pentesting practice**, **home lab management**, and **general recon**.

The script automatically detects your local IP and subnet, pings every host, looks up hostnames, retrieves MAC addresses through ARP, and checks common or custom-defined ports.

---

## **Features**

- ✅ Automatically detects local IP & subnet  
- ✅ Scans entire networks (default `/24`)  
- ✅ Retrieves **hostname** and **MAC address**  
- ✅ Multithreaded for fast scanning (50 workers)  
- ✅ Supports **custom port lists**  
- ✅ Saves a timestamped scan report to file  
- ✅ Works on **Windows**, **Linux**, and **macOS**  

---

## **Usage**

### **Run the script**
```bash
python network_scan.py
```

### **Recommended (Linux/macOS)**
```bash
sudo python network_scan.py
```
*Some ARP lookups require elevated privileges.*

---

## **Custom Options**

### **Specify a network**
Example:
```
192.168.1.0/24
```

### **Scan custom ports**
Provide comma-separated values:
```
22, 80, 443, 8080
```

### Defaults if left empty:
- Default network → detected automatically  
- Default ports → FTP, SSH, Telnet, SMTP, HTTP, HTTPS, MySQL, RDP, SMB, 8080  

---

## **Output Example**

```
Found: 192.168.1.12 - raspberrypi (B8:27:EB:xx:xx:xx)
Found: 192.168.1.35 - Unknown (N/A)
```

Results are saved as:
```
network_scan_YYYYMMDD_HHMMSS.txt
```

---

## **Requirements**

- Python **3.6+**
- Standard library only (no external modules)

---
