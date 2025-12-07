import platform
import subprocess
import sys

def check_admin():
    # see if we have admin/root
    try:
        if platform.system().lower() == 'windows':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            import os
            return os.geteuid() == 0
    except:
        return False

def flush_dns_windows():
    try:
        print("Flushing DNS on Windows...")
        result = subprocess.run(['ipconfig', '/flushdns'], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("Done! Cache cleared")
            print(result.stdout)
        else:
            print(f"Failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def flush_dns_linux():
    try:
        print("Flushing DNS on Linux...")
        
        # try common services
        services = [
            (['systemctl', 'restart', 'systemd-resolved'], 'systemd-resolved'),
            (['systemctl', 'restart', 'nscd'], 'nscd'),
            (['systemctl', 'restart', 'dnsmasq'], 'dnsmasq'),
            (['service', 'nscd', 'restart'], 'nscd (service)'),
        ]
        
        success = False
        for cmd, name in services:
            try:
                result = subprocess.run(cmd, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    print(f"Cleared using {name}")
                    success = True
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        if not success:
            print("No DNS cache service found")
            print("Your system might not cache DNS")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def flush_dns_mac():
    try:
        print("Flushing DNS on macOS...")
        
        # different versions use different commands
        commands = [
            ['dscacheutil', '-flushcache'],
            ['killall', '-HUP', 'mDNSResponder']
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    print(f"Success using {' '.join(cmd)}")
            except:
                continue
        
        print("Cache cleared")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 50)
    print("DNS Cache Flusher")
    print("=" * 50)
    
    system = platform.system().lower()
    print(f"OS: {platform.system()}")
    
    # check admin
    if not check_admin():
        print("\nNot running as admin/root - might fail")
        
        if system == 'windows':
            print("Run as Administrator")
        else:
            print("Use 'sudo'")
        print()
    
    # do the flush
    if system == 'windows':
        success = flush_dns_windows()
    elif system == 'linux':
        success = flush_dns_linux()
    elif system == 'darwin':
        success = flush_dns_mac()
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Done" if success else "Failed - check errors above")

if __name__ == "__main__":
    main()
