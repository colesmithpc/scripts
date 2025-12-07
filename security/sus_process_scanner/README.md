# 🕵️ Suspicious Process Scanner

A lightweight, beginner-friendly Python script that scans for potentially suspicious or malicious processes running on your system. This tool is designed to be simple, readable, and easy to extend — perfect for learning, experimentation, or adding to a security-focused GitHub portfolio.

---

## 🚀 Features

- Scans all running processes using `psutil`
- Matches process names and command-line arguments against a suspicious keyword list
- Displays clear, minimal, and well-formatted alerts
- Skips inaccessible processes quietly (no messy errors)
- Easy to customize: just edit the keyword list

---

## 🧩 How It Works

The script:

1. Iterates through all running processes  
2. Pulls process name, PID, and command line  
3. Converts everything to lowercase  
4. Checks if any suspicious keyword is present  
5. Prints clean, readable alerts for anything that matches

Suspicious keywords are defined in:

```python
SUSPICIOUS = [
    "mimikatz",
    "cobalt",
    "meterpreter",
    "powersploit",
    "unknown",
    "cmd.exe /c whoami",
]
