#!/bin/bash

# nmap scanner - scans all ports and grabs service info

if [ $# -eq 0 ]; then
    echo "Usage: $0 <target_ip>"
    exit 1
fi

TARGET=$1
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="nmap_scans"
OUTPUT_FILE="${OUTPUT_DIR}/scan_${TARGET}_${TIMESTAMP}"

# make sure nmap exists
if ! command -v nmap &> /dev/null; then
    echo "nmap not installed, get it first"
    exit 1
fi

mkdir -p $OUTPUT_DIR

echo "Scanning $TARGET..."
echo "Saving to ${OUTPUT_FILE}.txt"
echo ""

# quick check if host is alive
echo "[*] Pinging host..."
if ! ping -c 1 -W 2 $TARGET &> /dev/null; then
    echo "Host might be down but trying anyway..."
fi

# scan everything - this is slow
echo "[*] Scanning all ports (this takes a while)..."
nmap -p- -T4 $TARGET -oN "${OUTPUT_FILE}_all_ports.txt" | tee /dev/tty

# grab just the open ports
OPEN_PORTS=$(grep "^[0-9]" "${OUTPUT_FILE}_all_ports.txt" | grep "open" | cut -d'/' -f1 | tr '\n' ',' | sed 's/,$//')

if [ -z "$OPEN_PORTS" ]; then
    echo "Nothing open, we're done"
    exit 0
fi

echo ""
echo "[*] Open ports: $OPEN_PORTS"
echo "[*] Getting service versions..."

# detailed scan on the open ones
nmap -p$OPEN_PORTS -sV -sC -A -T4 $TARGET -oN "${OUTPUT_FILE}_services.txt" | tee /dev/tty

echo ""
echo "Done. Check these files:"
echo "  ${OUTPUT_FILE}_all_ports.txt"
echo "  ${OUTPUT_FILE}_services.txt"

# quick summary
echo ""
echo "=== Open Ports ==="
grep "open" "${OUTPUT_FILE}_services.txt" | grep -v "Nmap"
