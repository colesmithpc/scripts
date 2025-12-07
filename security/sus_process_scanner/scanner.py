import psutil

SUSPICIOUS = [
    "mimikatz",
    "cobalt",
    "meterpreter",
    "powersploit",
    "unknown",
    "cmd.exe /c whoami",
]

def check_processes():
    print("\n[+] Scanning for suspicious processes...\n")

    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            name = proc.info["name"] or ""
            cmd = " ".join(proc.info["cmdline"] or [])
            combined = (name + " " + cmd).lower()

            if any(s in combined for s in SUSPICIOUS):
                print(" ⚠️  Suspicious process detected")
                print(f"     PID: {proc.info['pid']}")
                print(f"     Name: {name}")
                print(f"     Cmd:  {cmd}\n")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    print("[+] Scan complete.\n")

if __name__ == "__main__":
    check_processes()
