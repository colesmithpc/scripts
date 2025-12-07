import psutil
import time
import os
import platform
from datetime import datetime

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def get_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    
    return {
        'usage': cpu_percent,
        'cores': cpu_count,
        'threads': cpu_threads,
        'freq': cpu_freq.current if cpu_freq else 'N/A'
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        'total': get_size(mem.total),
        'used': get_size(mem.used),
        'available': get_size(mem.available),
        'percent': mem.percent,
        'swap_used': get_size(swap.used),
        'swap_total': get_size(swap.total),
        'swap_percent': swap.percent
    }

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = []
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': get_size(usage.total),
                'used': get_size(usage.used),
                'free': get_size(usage.free),
                'percent': usage.percent
            })
        except PermissionError:
            continue
    
    return disk_info

def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        'sent': get_size(net_io.bytes_sent),
        'received': get_size(net_io.bytes_recv)
    }

def display_stats():
    clear_screen()
    
    print("=" * 60)
    print(f"System Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"OS: {platform.system()} {platform.release()}")
    print("=" * 60)
    
    # cpu stuff
    cpu = get_cpu_info()
    print(f"\nCPU Usage: {cpu['usage']}%")
    print(f"Cores: {cpu['cores']} | Threads: {cpu['threads']}")
    if cpu['freq'] != 'N/A':
        print(f"Frequency: {cpu['freq']:.2f} MHz")
    
    # memory
    mem = get_memory_info()
    print(f"\nMemory Usage: {mem['percent']}%")
    print(f"Total: {mem['total']} | Used: {mem['used']} | Available: {mem['available']}")
    print(f"Swap: {mem['swap_percent']}% ({mem['swap_used']} / {mem['swap_total']})")
    
    # disks
    print(f"\nDisk Usage:")
    disks = get_disk_info()
    for disk in disks:
        print(f"  {disk['mountpoint']} ({disk['fstype']})")
        print(f"    Total: {disk['total']} | Used: {disk['used']} | Free: {disk['free']}")
        print(f"    Usage: {disk['percent']}%")
    
    # network
    net = get_network_info()
    print(f"\nNetwork I/O:")
    print(f"  Sent: {net['sent']} | Received: {net['received']}")
    
    print("\n" + "=" * 60)
    print("Press Ctrl+C to exit")

def main():
    print("Starting monitor...")
    time.sleep(2)
    
    try:
        while True:
            display_stats()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
