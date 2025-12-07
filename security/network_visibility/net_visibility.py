#!/usr/bin/env python3

# network visibility tool - lists active network connections + processes
# shows local/remote addr, ports, states, and owning process
# works on linux, mac, windows

import psutil
import platform
import os
import time
from datetime import datetime

def clear_screen():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')

def get_size(bytes):
    for unit in ['B','KB','MB','GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"

def get_connections():
    conns = psutil.net_connections()
    out = []

    for c in conns:
        laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
        raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "N/A"
        pid = c.pid if c.pid else "N/A"

        # try to get process name
        pname = "Unknown"
        if c.pid:
            try:
                pname = psutil.Process(c.pid).name()
            except:
                pass

        out.append({
            'local': laddr,
            'remote': raddr,
            'status': c.status,
            'pid': pid,
            'proc': pname
        })
    
    return out

def display(conns):
    clear_screen()
    
    print("=" * 70)
    print(f"Network Visibility Tool - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"OS: {platform.system()} {platform.release()}")
    print("=" * 70)

    for c in conns:
        print(f"Local:  {c['local']}")
        print(f"Remote: {c['remote']}")
        print(f"Status: {c['status']}")
        print(f"PID:    {c['pid']}")
        print(f"Process:{c['proc']}")
        print("-" * 70)

    print("Refreshing every 3s (Ctrl+C to exit)")

def main():
    print("Starting network visibility...")
    time.sleep(1)

    try:
        while True:
            connections = get_connections()
            display(connections)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
