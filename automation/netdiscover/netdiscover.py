import socket
import ipaddress
import platform
import subprocess
import concurrent.futures
import re
from datetime import datetime

def get_local_network():
    # figure out local ip and network
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    
    # default to /24
    network = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
    return local_ip, network

def get_mac_address(ip):
    # try to grab mac address
    try:
        if platform.system().lower() == 'windows':
            output = subprocess.check_output(['arp', '-a', str(ip)], timeout=2).decode()
            mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
        else:
            output = subprocess.check_output(['arp', '-n', str(ip)], timeout=2).decode()
            mac_pattern = r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}'
        
        match = re.search(mac_pattern, output)
        return match.group(0) if match else 'N/A'
    except:
        return 'N/A'

def ping_host(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '1000', str(ip)]
    
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(str(ip))[0]
        return hostname
    except:
        return "Unknown"

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        return result == 0
    except:
        return False

def scan_device(ip, custom_ports=None):
    if ping_host(ip):
        hostname = get_hostname(ip)
        mac = get_mac_address(ip)
        
        # default ports or use custom ones
        if custom_ports:
            ports_to_check = {int(p): f"Port {p}" for p in custom_ports}
        else:
            ports_to_check = {
                21: 'FTP',
                22: 'SSH',
                23: 'Telnet',
                25: 'SMTP',
                80: 'HTTP',
                443: 'HTTPS',
                3306: 'MySQL',
                3389: 'RDP',
                445: 'SMB',
                8080: 'HTTP-Alt'
            }
        
        open_ports = []
        for port, service in ports_to_check.items():
            if scan_port(ip, port):
                open_ports.append(f"{port}/{service}")
        
        return {
            'ip': str(ip),
            'hostname': hostname,
            'mac': mac,
            'ports': open_ports if open_ports else ['None']
        }
    return None

def main():
    print("Network Discovery Tool")
    print("=" * 60)
    
    local_ip, network = get_local_network()
    
    # ask for custom network range
    custom_network = input(f"Network to scan (default: {network}): ").strip()
    if custom_network:
        network = custom_network
    
    # ask for custom ports
    custom_ports_input = input("Custom ports to scan (comma separated, leave empty for defaults): ").strip()
    custom_ports = [p.strip() for p in custom_ports_input.split(',')] if custom_ports_input else None
    
    print(f"\nLocal IP: {local_ip}")
    print(f"Scanning: {network}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nScanning... might take a bit\n")
    
    try:
        network_range = ipaddress.ip_network(network, strict=False)
    except ValueError:
        print("Invalid network format")
        return
    
    devices = []
    
    # multithread to speed it up
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_device, ip, custom_ports): ip for ip in network_range.hosts()}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                devices.append(result)
                print(f"Found: {result['ip']} - {result['hostname']} ({result['mac']})")
    
    print("\n" + "=" * 60)
    print(f"Done - Found {len(devices)} device(s)\n")
    
    # display results
    for device in devices:
        print(f"IP: {device['ip']}")
        print(f"Hostname: {device['hostname']}")
        print(f"MAC: {device['mac']}")
        print(f"Ports: {', '.join(device['ports'])}")
        print("-" * 60)
    
    # save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"network_scan_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Network Scan Report\n")
        f.write(f"Network: {network}\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Devices found: {len(devices)}\n\n")
        
        for device in devices:
            f.write(f"IP: {device['ip']}\n")
            f.write(f"Hostname: {device['hostname']}\n")
            f.write(f"MAC: {device['mac']}\n")
            f.write(f"Ports: {', '.join(device['ports'])}\n")
            f.write("-" * 60 + "\n")
    
    print(f"\nSaved to {filename}")

if __name__ == "__main__":
    main()
