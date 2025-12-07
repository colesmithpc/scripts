# Network Visibility Tool

Simple script that shows **all active network connections** on the system, including:

- local address + port  
- remote address + port  
- connection state  
- PID  
- process name  

Works on Linux, macOS, and Windows.

---

## Features

- Displays every active TCP/UDP connection
- Shows which process owns the connection
- Auto-refreshing live view
- No external dependencies (just `psutil`)
- Clean, simple output

---

## Install Requirements

```bash
pip install psutil
