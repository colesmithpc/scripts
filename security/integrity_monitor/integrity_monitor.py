```python
import os
import hashlib
import json
import time
from datetime import datetime

HASH_FILE = "file_hashes.json"

def get_file_hash(path):
    try:
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except Exception:
        return None

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    try:
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)

def scan_directory(target_dir):
    current = {}
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            path = os.path.join(root, file)
            file_hash = get_file_hash(path)
            if file_hash:
                current[path] = file_hash
    return current

def compare_hashes(old, new):
    changed = []
    added = []
    removed = []

    # changed or modified
    for path, file_hash in new.items():
        if path in old and old[path] != file_hash:
            changed.append(path)
        if path not in old:
            added.append(path)

    # missing files
    for path in old:
        if path not in new:
            removed.append(path)

    return changed, added, removed

def main():
    print("=" * 60)
    print("Local File Integrity Monitor")
    print("=" * 60)

    target_dir = input("Directory to monitor: ").strip()
    if not os.path.isdir(target_dir):
        print("Not a valid directory")
        return

    print("\nLoading existing hashes...")
    old_hashes = load_hashes()

    print("Scanning directory...")
    new_hashes = scan_directory(target_dir)

    print("\nComparing results...")
    changed, added, removed = compare_hashes(old_hashes, new_hashes)

    print("\n" + "=" * 60)
    print(f"Scan completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("\nModified files:")
    if changed:
        for f in changed:
            print(f"  - {f}")
    else:
        print("  None")

    print("\nNew files:")
    if added:
        for f in added:
            print(f"  - {f}")
    else:
        print("  None")

    print("\nRemoved files:")
    if removed:
        for f in removed:
            print(f"  - {f}")
    else:
        print("  None")

    print("\nSaving updated hashes...")
    save_hashes(new_hashes)

    print("\nDone")
    print("=" * 60)

if __name__ == "__main__":
    main()
```
