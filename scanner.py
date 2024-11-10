import nmap
import subprocess
import re

def scan_network(target, side):
    nm = nmap.PortScanner()
    
    #các loại scan
    udp_scan  = "-sU --top-ports 1000"  # Quét TCP và UDP tất cả các cổng
    # criteria_7_11_12_and_version_detection = "-sV -sS -sU  --script vulners --script-args mincvss=7 -p T:0-10000,U:0-10000"  # Quét TCP và UDP tất cả các cổng
    icmp_scan = "-sS -PE --disable-arp-ping"  #ICMP check 
    tcp_scan = "-sV --script vulners --script-args mincvss=8 --top-ports 1000"
    internal_network_discovery = '-sn'
    
    lite_tcp_scan = '-sS -sV --script vulners --script-args mincvss=8 --top-ports 100'
    lite_udp_scan = '-sU --top-ports 100'
    
    scan_results= {}
    
    
    
    if side == "external":
        
        # show và cho user chọn interface dùng để scan
        show_interface()
        scan_interface= input("\nChoose an interface to scan(default is eth3): ") or "eth3"
        # Thêm interface vào lệnh nmap nếu có
        interface_arg = f"-e {scan_interface}" 
        
        #khởi tạo dictionary
        # scan_results = {}
        tcp_port_number = 0
        tcp_port_service = ""
        udp_port_number = 0
        udp_port_service = ""
        vulner_number = 0
        vulnerability = ""
        
        
        
        
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
                print(f'''   Service: 
                      {port_info.get("name", "unknown")} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')})''')
                # print(f"this is port info: {port_info}")
                
                # In ra thông tin về các lỗ hổng từ script vulners (nếu có)
                if 'script' in port_info:
                    vulnerabilities = port_info['script']
                    if vulnerabilities:
                        print(f"   Vulnerabilities: ")
                        for vuln_name, vuln_description in vulnerabilities.items() :
                            if vuln_name == "fingerprint-strings":
                                break
                            vulner_number += 1
                            print(f"   - {vuln_name}: {vuln_description}")
                            vulnerability += f"{vuln_name}: {vuln_description}\n"
                    else:
                        print("   Vulnerabilities: No vulnerabilities found.")
                else:
                    print("   Vulnerabilities: No vulners data available.")
                scan_results["tcp"][port] = {
                    "state": port_info['state'],
                    "service": f'{port_info.get('name', 'unknown')} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')})',
                    "vulner": f'{vulnerability}'
                }
                
            
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

        print (f"\nScanning ICMP.....")
        # Quét với lệnh -sP (Ping Scan)
        scan_results["icmp"] = {}
        nm.scan(target, arguments=f"{interface_arg} {icmp_scan} -T 5")
        
        # print (f"this is scanstat: {nm.scanstats()}")
        # print (f"this is all host: {nm.all_hosts()}")
        
        
        icmp_result = nm.scanstats()
        
        print("\n=========Scanning Detail (ICMP)=========")
        
        
        if icmp_result["uphosts"] == "0":
            print("ICMP is blocked or filtered")
            scan_results["icmp"] = "ICMP is blocked or filtered"
            
        if icmp_result["uphosts"] == "1":
            print("ICMP is open")
            scan_results["icmp"] = "ICMP is open"
            
        # tcp_port_numbers = len(scan_results["tcp"]) if "tcp" in scan_results and len(scan_results["tcp"]) != 0 else 0
        # udp_port_numbers = len(scan_results["udp"])
            
        
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
        
        # if 'tcp' in nm[target] and 22 in nm[target]['tcp'] and nm[target]['tcp'][22]['state'] == 'open' :
        #     print(nm[target]['tcp'][22].get('name', 'unknown'))
        #     print("\n\nTELNET IS OPEN TO EXTERNAL NETWORK")
        
# ===============================================================================================================================================================
                
    if side == "internal":
        
        # show và cho user chọn interface dùng để scan
        show_interface()
        scan_interface= input("\nChoose an interface to scan(default is eth2): ") or "eth2"
        # Thêm interface vào lệnh nmap nếu có
        interface_arg = f"-e {scan_interface}" 
        
        #khởi tạo biến
        scan_results = {"have something in it"}
        target_range = target + "/24"
        
        
        #quét network dícovery
        print (f"\nScanning for host.....")
        nm.scan(target_range, arguments=f'{internal_network_discovery} -T 5')
        print("\n=========Scanning Detail (network discovery)=========")
        print(f'{len(nm.all_hosts())} host found')
        scan_results["host_number"] = f'{len(nm.all_hosts())}'
        for host in nm.all_hosts():
            print(f'this is host: {host}')
            print(f'this is nm[host]: {nm[host]}')
        
        #quét firewall
        # print (f"\nScanning internal firewall (TCP).....")
        # nm.scan(target, arguments=f'{tcp_scan} -T 5')
        
        # print(f'this is nm[target]: {nm[target]}')
        # if "tcp" in nm[target]:
        #     print("have tcp in the scan")
        # print("\n=========Scanning Detail of Internal firewall (TCP)=========")
        
        # print("\n=========Scanning Detail (network discovery)=========")
        
        
        
        
        #     # Quét TCP UDP
        # print (f"\nTiến hành scan TCP UDP.....")
        # nm.scan(target, arguments=f"{interface_arg} {internal_network_discovery} -T 5")
        # for host in nm.all_hosts():
        #     #khởi tạo dictionary
        #     scan_results["Host"] = {}
            
        #     print("\n=========Scanning result=========")
        #     if 'tcp' in nm[host]:
        #         scan_results["Ports"]["tcp"] = {}
        #         print("\nTCP\n")
        #         for port in nm[host]['tcp']:
        #             port_info = nm[host]['tcp'][port]
        #             print(f"Port: {port} ({port_info["state"]}):")
        #             print(f"   Service: {port_info.get("name", "unknown")}\n")
        #             scan_results["Ports"]["tcp"][port] = {
        #                 "state": port_info['state'],
        #                 "service": port_info.get('name', 'unknown')
        #             }
                    
                

        #     if 'udp' in nm[host]:
        #         print("\nUDP\n")
        #         scan_results["Ports"]["udp"] = {}
        #         for port in nm[host]['udp']:
        #             port_info = nm[host]['udp'][port]
        #             print(f"Port {port} ({port_info["state"]}):")
        #             print(f"   Service: {port_info.get("name", "unknown")}\n")
        #             scan_results["Ports"]["udp"][port] = {
        #                 "state": port_info['state'],
        #                 "service": port_info.get('name', 'unknown')
        #             }

        # # Quét với lệnh -sP (Ping Scan)
        # scan_results["ICMP"] = {}
        # nm.scan(target, arguments=f"{interface_arg} {icmp_scan} -T 5")
        # print("ICMP")
        # # print (f"this is scanstat: {nm.scanstats()}")
        # # print (f"this is all host: {nm.all_hosts()}")
        
        
        # icmp_result = nm.scanstats()
        
        # if icmp_result["uphosts"] == "0":
        #     print("ICMP is blocked or filtered")
        #     scan_results["ICMP"] = "ICMP is blocked or filtered"
            
        # if icmp_result["uphosts"] == "1":
        #     print("ICMP is open")
        #     scan_results["ICMP"] = "ICMP is open"
     

    
    return scan_results  # Trả về kết quả dưới dạng JSON


def show_interface():
    # Sử dụng subprocess để thực hiện lệnh nmap
    command = ["nmap", "--iflist"]  # -sn chỉ ping scan
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Biểu thức regex để tìm DEV và IP
    pattern = r"(\b\w+\d+\b) \(\w+\) +([\da-fA-F:.]+/\d+)"

    # Tìm tất cả các kết quả khớp với biểu thức regex và loại bỏ trùng lặp
    matches = set(re.findall(pattern, result.stdout))

    # Sắp xếp theo `dev` theo thứ tự tăng dần
    sorted_matches = sorted(matches, key=lambda x: x[0])

    # In danh sách các thiết bị và IP theo thứ tự tăng dần của `dev`
    print("Danh sách DEV và IP:")
    for dev, ip in sorted_matches:
        print(f"Interface {dev}: {ip}")