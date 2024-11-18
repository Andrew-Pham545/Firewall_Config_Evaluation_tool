import nmap
import subprocess
import re
import google.generativeai as genai
# import ai_evaluation
import time

def scan_network(target, side):
    nm = nmap.PortScanner()
    
    #các loại scan
    udp_scan  = "-sU --top-ports 1000"  
    tcp_scan = "-sV --script vulners --script-args mincvss=8 --top-ports 1000"
    lite_tcp_scan = '-sS -sV --script vulners --script-args mincvss=8 --top-ports 100'
    lite_udp_scan = '-sU --top-ports 100'
    icmp_scan = "-sS -PE --disable-arp-ping"  
    internal_network_discovery = '-sn'
    
    
    
    scan_results= {}
    
    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")


    
    if side == "external":
        
    # show và cho user chọn interface dùng để scan
        show_interface()
        scan_interface= input("\nChoose an interface to scan(default is eth3): ") or "eth3"
        interface_arg = f"-e {scan_interface}" 
        
    #khởi tạo biến
        tcp_port_number = 0
        tcp_port_service = ""
        udp_port_number = 0
        udp_port_service = ""
        vulner_number = 0
        vulnerability = ""
        
    #ip của firewall
        scan_results["firewall_ip"] = target 
    
    #thoi gian bat dau scan
        current_time = time.strftime("%D (%H:%M:%S)")
        scan_results["time_of_scan"] = current_time
        print(f'\nthời gian bắt đầu scan {side}: {current_time}')
        
        
    # Quét TCP
        print (f"\nScanning TCP.....")
        nm.scan(target, arguments=f"{interface_arg} {tcp_scan} -T 5")
        print("\n=========Scanning Detail (TCP)=========\n")
        if 'tcp' in nm[target]:
            scan_results["tcp"] = {}
            for port in nm[target]['tcp']:
                port_info = nm[target]['tcp'][port]
                tcp_port_number += 1
                tcp_port_service += f"{port_info.get("name","unknow")} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')}), "
                
                print(f"Port: {port} ({port_info["state"]})")
                print(f'   Service: {port_info.get("name", "unknown")} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')})')
                
                if 'script' in port_info:
                    vulnerabilities = port_info['script']
                    if vulnerabilities:
                        
                        print('   vulnerbility: ', end= '')
                        for vuln_name, vuln_description in vulnerabilities.items() :
                            vulner_number += 1
                            if "fingerprint-strings" in vuln_name or "fingerprint-strings" in vuln_description:
                                print(f'{vuln_name}')
                                vulnerability = vuln_name
                                break
                            print(f"{vuln_description}")
                            vulnerability += f"{vuln_description}"
                            
                    
                    else:
                        print("   Vulnerabilities: No vulnerabilities found.")
                        vulnerability = 'no vulnerability found'
                else:
                    print("   Vulnerabilities: No vulners data available.")
                    vulnerability = 'no vulnerability in vulners database'
                    
                vulnerability = vulnerability.replace("\t", "  ")

                scan_results["tcp"][port] = {
                    "state": port_info['state'],
                    "service": f'{port_info.get("name", "unknown")} ({port_info.get("product","unknown")} {port_info.get("version","unknown")})',
                    "vulner": f'{vulnerability}'
                }                
                vulnerability = ''
        
                
    # Quét UDP
        print (f"\nScanning UDP.....")
        nm.scan(target, arguments=f"{interface_arg} {udp_scan} -T 5")
        print("\n=========Scanning Detail (UDP)=========\n")
        if 'udp' in nm[target]:
            scan_results["udp"] = {}
            for port in nm[target]['udp']:
                port_info = nm[target]['udp'][port]
                udp_port_number += 1
                udp_port_service += f"{port_info.get("name","unknow")}, "
                print(f"Port {port} ({port_info["state"]}):")
                print(f"   Service: {port_info.get("name", "unknown")}\n")
                scan_results["udp"][port] = {
                    "state": port_info['state'],
                    "service": port_info.get('name', 'unknown')
                }
        
            
    # Quét ICMP
        print (f"\nScanning ICMP.....")
        scan_results["icmp"] = {}
        nm.scan(target, arguments=f"{interface_arg} {icmp_scan} -T 5")     
        icmp_result = nm.scanstats()
        print("\n=========Scanning Detail (ICMP)=========")
        if icmp_result["uphosts"] == "0":
            print("ICMP is blocked or filtered")
            scan_results["icmp"] = "ICMP is blocked or filtered"
        if icmp_result["uphosts"] == "1":
            print("ICMP is open")
            scan_results["icmp"] = "ICMP is open"
        
    #general report
        print(f'''\n=========General scan report========= 
              * The external firewall have {tcp_port_number} tcp and {udp_port_number} udp port open
              * {tcp_port_service} {udp_port_service} are listening in the external ip
              * {scan_results["icmp"]} (ICMP packet to the external ip)
              * {f"there are vulnerability ({vulner_number}) from the service open to public" if vulner_number > 0 else "no vulnerability found"}
              ''')
        scan_results["summary"] = f'''\n=========General scan report========= 
              * The external firewall have {tcp_port_number} tcp and {udp_port_number} udp port open
              * {tcp_port_service} {udp_port_service} are listening in the external ip
              * {scan_results["icmp"]} (ICMP packet to the external ip)
              * {f"there are vulnerability ({vulner_number}) from the service open to public" if vulner_number > 0 else "no vulnerability found"}
              '''
        
# ===============================================================================================================================================================
                
    if side == "internal":
        
    # show và cho user chọn interface dùng để scan
        show_interface()
        scan_interface= input("\nChoose an interface to scan(default is eth2): ") or "eth2"
        interface_arg = f"-e {scan_interface}" 
        
    #khởi tạo biến
        scan_results = {}
        target_range = target + "/24"
        tcp_port_number = 0
        tcp_port_service = ""
        udp_port_number = 0
        udp_port_service = ""
        vulner_number = 0
        vulnerability = ""
        
    #thoi gian bat dau scan
        current_time = time.strftime("%D (%H:%M:%S)")
        scan_results["time_of_scan"] = current_time
        print(f'\nthời gian bắt đầu scan {side}: {current_time}')
        
        
    #quét network dícovery
        scan_results[f"host_discovery"] = {}
        print (f"\nScanning for host.....")
        nm.scan(target_range, arguments=f'{interface_arg} {internal_network_discovery} -T 5')
        print("\n=========Scanning Detail (network discovery)=========")
        print(f'{len(nm.all_hosts())} host found')
        for host in nm.all_hosts():
            vendor_name = next(iter(nm[host]["vendor"].values()), None) if "vendor" in nm[host] and nm[host]["vendor"] else "Unknown"
            print(f'{nm[host]["addresses"]["ipv4"]} | {nm[host]["addresses"]["mac"]} ({vendor_name})')
            scan_results["host_discovery"][host] = f'{nm[host]["addresses"]["ipv4"]} | {nm[host]["addresses"]["mac"]} ({vendor_name})'
        scan_results["host_discovery"]["host_number"] = f'{len(nm.all_hosts())}'
        
        
    # quét firewall (TCP)
        print (f"\nScanning internal firewall (TCP).....")
        scan_results[f"firewall"] = {}
        scan_results[f"firewall"]["ip"] = target
        nm.scan(target, arguments=f"{interface_arg} {lite_tcp_scan} -T 5")
        print("\n=========Scanning Internal Firewall (TCP)=========\n")
        if 'tcp' in nm[target]:
            scan_results["firewall"]["tcp"] = {}
            for port in nm[target]['tcp']:
                port_info = nm[target]['tcp'][port]
                tcp_port_number += 1
                tcp_port_service += f"{port_info.get("name","unknow")} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')}), "
                print(f"Port: {port} ({port_info["state"]})")
                print(f'''   Service: {port_info.get("name", "unknown")} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')})''')
                if 'script' in port_info:
                    vulnerabilities = port_info['script']
                    if vulnerabilities: 
                        print(f"   Vulnerabilities: ")
                        for vuln_name, vuln_description in vulnerabilities.items() :
                            vulner_number += 1
                            if vuln_name == "fingerprint-strings":
                                print(f"   - {vuln_name}: fingerprint-strings")
                                vulnerability += f"{vuln_name}: fingerprint-strings\n"                                
                                break
                            print(f"   - {vuln_name}: {vuln_description}")
                            vulnerability += f"{vuln_name}: {vuln_description}\n"
                    else:
                        print("   Vulnerabilities: No vulnerabilities found.")
                else:
                    print("   Vulnerabilities: No vulners data available.")
                scan_results["firewall"]["tcp"][port] = {
                    "state": port_info['state'],
                    "service": f'{port_info.get('name', 'unknown')} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')})',
                    "vulner": f'{vulnerability}'
                }
        else:
            print("no tcp port open")
            scan_results["firewall"]["tcp"] = 0
                
    # quét firewall (UDP)
        print (f"\nScanning UDP.....")
        nm.scan(target, arguments=f"{interface_arg} {lite_udp_scan} -T 5")
        print("\n=========Scanning Internal Firewall (UDP)=========\n")
        if 'udp' in nm[target]:
            scan_results["firewall"]["udp"] = {}
            for port in nm[target]['udp']:
                port_info = nm[target]['udp'][port]
                udp_port_number += 1
                udp_port_service += f"{port_info.get("name","unknow")}, "
                print(f"Port {port} ({port_info["state"]}):")
                print(f"   Service: {port_info.get("name", "unknown")}\n")
                scan_results["firewall"]["udp"][port] = {
                    "state": port_info['state'],
                    "service": port_info.get('name', 'unknown')
                }
        else:
            print("no udp port open")
            scan_results["firewall"]["udp"] = 0
            
    # quét firewall (ICMP)
        print (f"\nScanning ICMP.....")
        scan_results["firewall"]["icmp"] = {}
        nm.scan(target, arguments=f"{interface_arg} {icmp_scan} -T 5")
        icmp_result = nm.scanstats()
        print("\n=========Scanning Detail (ICMP)=========")
        if icmp_result["uphosts"] == "0":
            print("ICMP is blocked or filtered")
            scan_results["firewall"]["icmp"] = "ICMP is blocked or filtered"
        if icmp_result["uphosts"] == "1":
            print("ICMP is open")
            scan_results["firewall"]["icmp"] = "ICMP is open"
            

    #general report       
        if scan_results["firewall"]["tcp"] == 0 and scan_results["firewall"]["udp"] == 0:
            print(f'''\n=========General scan report========= 
              * The internal firewall have no tcp and udp port open
              * Admin GUI not accessible from the internal LAN 
              * {scan_results["firewall"]["icmp"]} (ICMP packet to the internal ip)
              * There are no vulnerability in term of service from the internal side of the firewall
              ''')
            scan_results["firewall"]["summary"] = f'''\n=========General scan report========= 
              * The internal firewall have no tcp and udp port open
              * Admin GUI not accessible from the internal LAN 
              * {scan_results["firewall"]["icmp"]} (ICMP packet to the internal ip)
              * There are no vulnerability in term of service from the internal side of the firewall
              '''
        else:
            print(f'''\n=========General scan report========= 
                * The internal firewall have {tcp_port_number} tcp and {udp_port_number} udp port open
                * {tcp_port_service} {udp_port_service} are listening in the internal ip
                * {scan_results["firewall"]["icmp"]} (ICMP packet to the internal ip)
                * {f"there are vulnerability ({vulner_number}) from the service open to public" if vulner_number > 0 else "no vulnerability found"}
                ''')
            scan_results["firewall"]["summary"] = f'''\n=========General scan report========= 
                * The internal firewall have {tcp_port_number} tcp and {udp_port_number} udp port open
                * {tcp_port_service} {udp_port_service} are listening in the external ip
                * {scan_results["firewall"]["icmp"]} (ICMP packet to the internal ip)
                * {f"there are vulnerability ({vulner_number}) from the service open to public" if vulner_number > 0 else "no vulnerability found"}
                '''    
                
    
    return scan_results  # Trả về kết quả dưới dạng JSON


def show_interface():
    
    command = ["nmap", "--iflist"]  
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Biểu thức regex để tìm DEV và IP
    pattern = r"(\b\w+\d+\b) \(\w+\) +([\da-fA-F:.]+/\d+)"

    # Tìm tất cả các kết quả khớp với biểu thức regex và loại bỏ trùng lặp
    matches = set(re.findall(pattern, result.stdout))

    # Sắp xếp theo `dev` theo thứ tự tăng dần
    sorted_matches = sorted(matches, key=lambda x: x[0])

    # In danh sách các thiết bị và IP theo thứ tự tăng dần của `dev`
    print("\nDanh sách DEV và IP:")
    for dev, ip in sorted_matches:
        print(f"Interface {dev}: {ip}")