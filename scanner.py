import subprocess
import json

def scan_network(target, scan_type):
    command = f"nmap -sP {target}" if scan_type == 'internal' else f"nmap -sS {target}"
    print(f"Đang quét {target} với lệnh: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
