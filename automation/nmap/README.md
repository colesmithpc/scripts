# 🔍 Nmap Full-Scan Automation Script

A Bash script that performs a full-port **Nmap scan**, identifies **open ports**, then automatically runs **service/version detection**, **default scripts**, and **aggressive scanning** on the discovered ports.

This script saves results into timestamped output files and provides a quick summary at the end.

---

## 🚀 Features

- Full **0–65535** port scan  
- Automatic detection of open ports  
- **Service/version** scanning on discovered ports  
- Host availability check  
- Organized output stored in `nmap_scans/`  
- Human-readable summaries  
- Uses `tee` to show output while saving it

---

## 📌 Usage

```bash
./scan.sh <target_ip>
