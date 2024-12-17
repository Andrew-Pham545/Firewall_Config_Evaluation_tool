import nmap
import subprocess
import re
import time
from colorama import Fore

def scan_network(target):
    nm = nmap.PortScanner()

    udp_scan = "-sU --top-ports 500"  # Scan top 500 UDP ports
    tcp_scan = "-sS --top-ports 500"  # Standard SYN scan for top 500 TCP ports
    icmp_scan = "-sS -PE --disable-arp-ping"  # ICMP scan

    scan_results = {}
    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")

    show_interface()
    scan_interface = input(f'\n{Fore.YELLOW + "Choose an interface to scan (default is eth3):"} {Fore.RESET}') or 'eth3'
    interface_arg = f"-e {scan_interface}"

    tcp_port_number = 0
    udp_port_number = 0
    tcp_port_service = ""
    udp_port_service = ""

    scan_results["udp"] = {}
    scan_results["firewall_ip"] = target
    scan_results["time_of_scan"] = current_time
    print(f'\nScan external started at: {current_time}')

    # TCP Scan
    print("\nScanning TCP...")
    nm.scan(target, arguments=f"{interface_arg} {tcp_scan} -T 5")
    print(Fore.CYAN + '\n======================= Scanning Details (TCP) =======================\n')
    if 'tcp' in nm[target]:
        scan_results["tcp"] = {}
        for port in nm[target]['tcp']:
            port_info = nm[target]['tcp'][port]
            tcp_port_number += 1
            tcp_port_service += f"{port_info.get('name', 'unknown')} ({port_info.get('product', 'unknown')} {port_info.get('version', 'unknown')}), "
            print(f"Port: {port} ({port_info['state']})")
            print(f"   Service: {port_info.get('name', 'unknown')} ({port_info.get('product', 'unknown')} {port_info.get('version', 'unknown')})")
            scan_results["tcp"][port] = {
                "state": port_info['state'],
                "service": f"{port_info.get('name', 'unknown')} ({port_info.get('product', 'unknown')} {port_info.get('version', 'unknown')})"
            }
    else:
        print("No TCP ports open.")

    # UDP Scan
    print("\nScanning UDP...")
    nm.scan(target, arguments=f"{interface_arg} {udp_scan} -T 5")
    print(Fore.CYAN + '\n======================= Scanning Details (UDP) =======================\n')
    if 'udp' in nm[target]:
        for port in nm[target]['udp']:
            port_info = nm[target]['udp'][port]
            udp_port_number += 1
            udp_port_service += f"{port_info.get('name', 'unknown')}, "
            print(f"Port: {port} ({port_info['state']})")
            print(f"   Service: {port_info.get('name', 'unknown')}")
            scan_results["udp"][port] = {
                "state": port_info['state'],
                "service": port_info.get('name', 'unknown')
            }
    else:
        print("No UDP ports open.")

    # ICMP Scan
    print("\nScanning ICMP...")
    scan_results["icmp"] = {}
    nm.scan(target, arguments=f"{interface_arg} {icmp_scan} -T 5")
    icmp_result = nm.scanstats()
    print(Fore.CYAN + '\n======================= Scanning Details (ICMP) =======================\n')
    if icmp_result["uphosts"] == "0":
        print("ICMP is blocked or filtered")
        scan_results["icmp"] = "ICMP is blocked or filtered"
    elif icmp_result["uphosts"] == "1":
        print("ICMP is open")
        scan_results["icmp"] = "ICMP is open"

    # Summary
    print(f'''\n{Fore.CYAN +'======================= General Scan Report =======================' + Fore.RESET} 
    * External firewall has {tcp_port_number} TCP and {udp_port_number} UDP ports open.
    * {tcp_port_service} {udp_port_service} are listening on the external IP.
    * {scan_results["icmp"]} (ICMP packet to the external IP).
    ''')
    return scan_results

def scan_tcp_udp(target):
    show_interface()
    interface = input(f'\n{Fore.YELLOW + "Choose an interface to scan :"} {Fore.RESET}') 
    nm = nmap.PortScanner()

    tcp_scan = "-sS --top-ports 500"  # Scan top 500 TCP ports
    udp_scan = "-sU --top-ports 500"  # Scan top 500 UDP ports

    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")

    print(f"\n{Fore.GREEN}Starting scan on target: {target} at {current_time}{Fore.RESET}")
    print(f"Using interface: {interface}")

    # Scanning TCP ports
    print(f"\n{Fore.CYAN}Scanning TCP ports...{Fore.RESET}")
    nm.scan(target, arguments=f"-e {interface} {tcp_scan} -T 5")
    if 'tcp' in nm[target]:
        print(Fore.CYAN + '\n======================= TCP Scan Results =======================\n' + Fore.RESET)
        for port in nm[target]['tcp']:
            port_info = nm[target]['tcp'][port]
            print(f"Port: {port} ({port_info['state']})")
            print(f"   Service: {port_info.get('name', 'unknown')} ({port_info.get('product', 'unknown')} {port_info.get('version', 'unknown')})")
    else:
        print("No TCP ports open.")

    # Scanning UDP ports
    print(f"\n{Fore.CYAN}Scanning UDP ports...{Fore.RESET}")
    nm.scan(target, arguments=f"-e {interface} {udp_scan} -T 5")
    if 'udp' in nm[target]:
        print(Fore.CYAN + '\n======================= UDP Scan Results =======================\n' + Fore.RESET)
        for port in nm[target]['udp']:
            port_info = nm[target]['udp'][port]
            print(f"Port: {port} ({port_info['state']})")
            print(f"   Service: {port_info.get('name', 'unknown')}")
    else:
        print("No UDP ports open.")

    print(f"\n{Fore.GREEN}Scan complete for {target} at {time.strftime('%d/%m/%Y (%H:%M:%S)')}{Fore.RESET}")

def port_restriction_scan(target):
    
    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")
    

    # Danh sách dịch vụ và cổng cần kiểm tra (đơn giản hóa bằng cách liệt kê cổng trực tiếp)
    port_list = (
        "53,69,87,111,512-514,515,540,2000,2049,6000-6255,21,22,23,25,37,79,80,"
        "109-110,119,123,135,137-139,143,161-162,179,389,443,445,514,1080,2001,"
        "4001,4045,6001,8000,8080,8888"
    )
    show_interface()
    interface = input(f'\n{Fore.YELLOW + "Choose an interface to scan :"} {Fore.RESET}') 
    nm = nmap.PortScanner()
    print(f"{Fore.GREEN}Scanning target: {target}{Fore.RESET}")
    print(f"Checking ports: {port_list}\n")

    # Gộp cả TCP và UDP vào một lệnh nmap
    nm.scan(target, arguments=f"-e {interface} -p {port_list} -sS -sU -T4")

    print(f"{Fore.CYAN}Scan started at: {time.strftime('%Y-%m-%d %H:%M:%S')}{Fore.RESET}\n")
    print(f"{Fore.CYAN}======================= Open Ports ======================={Fore.RESET}")

    # Xử lý kết quả cho từng giao thức (TCP và UDP)
    for proto in nm[target].all_protocols():
        print(f"\n{Fore.BLUE}Protocol: {proto.upper()}{Fore.RESET}")
        for port in sorted(nm[target][proto].keys()):
            if nm[target][proto][port]['state'] == 'open':
                print(f"Port: {port} - {Fore.GREEN}Open{Fore.RESET}")

    print(f"\n{Fore.GREEN}Scan completed at: {current_time}{Fore.RESET}")
    
    


def scan_icmp_restrictions(target):
    """
    Perform an ICMP scan on the target and return the results.
    """
    nm = nmap.PortScanner()
    icmp_scan = "-PE --disable-arp-ping"  

    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")

    # Hiển thị danh sách giao diện
    show_interface()
    scan_interface = input(f'\n{Fore.YELLOW + "Choose an interface to scan (default is eth3):"} {Fore.RESET}') or 'eth3'
    interface_arg = f"-e {scan_interface}"

    print(f'\nScan ICMP started at: {current_time}')
    print("\nScanning ICMP...")
    nm.scan(target, arguments=f"{interface_arg} {icmp_scan} -T 5")
    icmp_result = nm.scanstats()
    print(Fore.CYAN + '\n======================= Scanning Details (ICMP) =======================\n')

    if icmp_result["uphosts"] == "0":
        print("ICMP is blocked or filtered")
    elif icmp_result["uphosts"] == "1":
        print("ICMP is open")


def port_restriction_and_icmp_restriction_scan(target):
    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")
    port_list = (
        "53,69,87,111,512-514,515,540,1194,2000,2049,6000-6255,21,22,23,25,37,79,80,"
        "109-110,119,123,135,137-139,143,161-162,179,389,443,445,514,1080,2001,"
        "4001,4045,6001,8000,8080,8888"
    )
    
    show_interface()
    interface = input(f'\n{Fore.YELLOW}Choose an interface to scan: {Fore.RESET}') 
    nm = nmap.PortScanner()

    # Port Scan
    print(f"{Fore.GREEN}Scanning target for open ports: {target}{Fore.RESET}")
    nm.scan(target, arguments=f"-e {interface} -p {port_list} -sS -sU -T4 -Pn")
    
    print(f"{Fore.CYAN}======================= Open Ports ======================={Fore.RESET}")
    scan_results = {"target": target, "protocols": {}}

    
    
    if target in nm.all_hosts():

        protocols_found = nm[target].all_protocols()


        for proto in protocols_found:
            print(f"\n{Fore.BLUE}Protocol: {proto.upper()}{Fore.RESET}")
            scan_results["protocols"][proto] = []


            for port in sorted(nm[target][proto].keys()):
                port_state = nm[target][proto][port]['state']
                if port_state == 'open':
                    print(f"Port: {port} - {Fore.GREEN}Open{Fore.RESET}")
                    scan_results["protocols"][proto].append({"port": port, "state": "open"})
                else:
                    print(f"Port: {port} - {Fore.RED}{port_state.capitalize()}{Fore.RESET}")
                    scan_results["protocols"][proto].append({"port": port, "state": port_state})

        
        if "udp" not in protocols_found:
            print("====================")
            print(f"\n{Fore.YELLOW}No UDP ports found.{Fore.RESET}")
            scan_results["protocols"]["udp"] = [{"state": "close"}]

        
        if "tcp" not in protocols_found:
            print(f"\n{Fore.YELLOW}No TCP ports found.{Fore.RESET}")
            scan_results["protocols"]["tcp"] = [{"state": "close"}]

    else:
        print(f"{Fore.RED}Target not found in scan results.{Fore.RESET}")
        scan_results = {"protocols": {"tcp": [{"state": "close"}], "udp": [{"state": "close"}]}}




    print(f"\n{Fore.GREEN}Scanning target for ICMP (ping): {target}{Fore.RESET}")
    nm.scan(target, arguments="-PE -sn --disable-arp-ping")
    
    print(f"{Fore.CYAN}======================= ICMP Results ======================={Fore.RESET}")
    if target in nm.all_hosts():
        print(f"{Fore.GREEN}ICMP is open on target: {target}{Fore.RESET}")
        scan_results["icmp"] = "open"
    else:
        print(f"{Fore.RED}ICMP is blocked or filtered on target: {target}{Fore.RESET}")
        scan_results["icmp"] = "blocked or filtered"

    # Finalizing Results
    scan_results["completed_at"] = current_time
    print(f"\n{Fore.GREEN}Scan completed at: {current_time}{Fore.RESET}")
    return scan_results

    




def show_interface():
    command = ["nmap", "--iflist"]
    result = subprocess.run(command, capture_output=True, text=True)
    pattern = r"(\b\w+\d+\b) \(\w+\) +([\da-fA-F:.]+/\d+)"
    matches = set(re.findall(pattern, result.stdout))
    sorted_matches = sorted(matches, key=lambda x: x[0])
    print(Fore.CYAN + "\n======================= Your Network Interface List =======================")
    for dev, ip in sorted_matches:
        print(f"Interface {dev}: {ip}")
