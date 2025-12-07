# Local File Integrity Monitor

Simple file integrity checker that creates and stores SHA-256 hashes of files inside a directory.  
Useful for detecting tampering, unexpected changes, malware activity, or tracking system modifications.

This script fits well into security auditing, blue team workflows, and general system monitoring.

---

## 🔍 Features

- Generates SHA-256 hashes for every file in a directory  
- Saves all hashes to `file_hashes.json`  
- Detects:
  - **Modified files**
  - **New files**
  - **Deleted files**
- Clean terminal output  
- No external dependencies  
- Works on Windows, macOS, and Linux  

---

## ▶️ Usage

Run the script:

```bash
python integrity_monitor.py
```

Enter the directory you want to monitor:

```
Directory to monitor: /path/to/check
```

The script will:

- Scan all files  
- Compare hashes to previous runs  
- Show modifications  
- Save updated hashes  

---

## 📁 Hash Storage

The script automatically creates:

```
file_hashes.json
```

This file stores all previously known hashes so futures scans can compare against it.

---

## 🛡️ Why This Script Is Useful

- Detects tampering or malware changing files  
- Monitors config directories  
- Tracks changes in sensitive folders  
- Helps maintain system integrity across updates or incidents  

---

## ✔ Future Improvements (optional ideas)

- Email/Discord alerting  
- Scheduled scans  
- Hashing exclusions  
- Real-time monitoring (watchdog)  

---

Made for security auditing & monitoring.
