import nmap
import subprocess
import re

def scan_network(target, side):
    nm = nmap.PortScanner()
    
    scan_udp  = "-sU -p U:0-10000"  # Quét TCP và UDP tất cả các cổng
    criteria_7_11_12_and_version_detection = "-sV -sS -sU  --script vulners --script-args mincvss=7 -p T:0-10000,U:0-10000"  # Quét TCP và UDP tất cả các cổng
    # criteria_15 = "-sS -PE --disable-arp-ping"  #ICMP check 
    scan_tcp = "-sV --script vulners --script-args mincvss=7 -p T:0-10000"

    # Kết quả quét dưới dạng dictionary
    scan_results = {}
    
    
    # show và cho user chọn interface dùng để scan
    show_interface()
    scan_interface= input("\nChoose an interface to scan(default is eth5): ") or "eth5"
    
     # Thêm interface vào lệnh nmap nếu có
    interface_arg = f"-e {scan_interface}" 
    
    if side == "external":
        
       # Quét TCP UDP
        print (f"\nScanning TCP.....")
        nm.scan(target, arguments=f"{interface_arg} {scan_tcp} -T 5")
        print (f"\nScanning UDP.....")
        nm.scan(target, arguments=f"{interface_arg} {scan_udp} -T 5")
        for host in nm.all_hosts():
            #khởi tạo dictionary
            scan_results = {}
            tcp_port_number = 0
            tcp_port_service = ""
            udp_port_number = 0
            udp_port_service = ""
            
            
            
            print("\n=========Scanning Detail (TCP)=========")
            if 'tcp' in nm[host]:
                scan_results["tcp"] = {}
                print("\nTCP\n")
                for port in nm[host]['tcp']:
                    port_info = nm[host]['tcp'][port]
                    tcp_port_number += 1
                    tcp_port_service += f"{port_info.get("name","unknow")} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')}), "
                    
                    print(f"Port: {port} ({port_info["state"]})")
                    print(f"   Service: {port_info.get("name", "unknown")} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')})\n")
                    
                    scan_results["tcp"][port] = {
                        "state": port_info['state'],
                        "service": f'{port_info.get('name', 'unknown')} ({port_info.get("product",'unknown')} {port_info.get("version",'unknown')})'
                    }
                    
                

            print("\n=========Scanning Detail (UDP)=========")
            if 'udp' in nm[host]:
                print("\nUDP\n")
                scan_results["udp"] = {}
                for port in nm[host]['udp']:
                    port_info = nm[host]['udp'][port]
                    udp_port_number += 1
                    udp_port_service += f"{port_info.get("name","unknow")}/"
                    print(f"Port {port} ({port_info["state"]}):")
                    print(f"   Service: {port_info.get("name", "unknown")}\n")
                    scan_results["udp"][port] = {
                        "state": port_info['state'],
                        "service": port_info.get('name', 'unknown')
                    }

        print("\n=========Scanning Detail (UDP)=========")
        # Quét với lệnh -sP (Ping Scan)
        scan_results["ICMP"] = {}
        print (f"\nScanning ICMP.....")
        nm.scan(target, arguments=f"{interface_arg} {criteria_15} -T 5")
        print("ICMP")
        # print (f"this is scanstat: {nm.scanstats()}")
        # print (f"this is all host: {nm.all_hosts()}")
        
        
        icmp_result = nm.scanstats()
        
        print("\n=========Scanning Detail (ICMP)=========")
        
        if icmp_result["uphosts"] == "0":
            print("ICMP is blocked or filtered")
            scan_results["ICMP"] = "ICMP is blocked or filtered"
            
        if icmp_result["uphosts"] == "1":
            print("ICMP is open")
            scan_results["ICMP"] = "ICMP is open"
            
        # tcp_port_numbers = len(scan_results["tcp"]) if "tcp" in scan_results and len(scan_results["tcp"]) != 0 else 0
        # udp_port_numbers = len(scan_results["udp"])
            
        
        print(f'''\nGeneral scan report: 
              * The external firewall have {tcp_port_number} tcp and {udp_port_number} udp port open
              * {tcp_port_service} (TCP) and {udp_port_service} (UDP) are listening
              * {scan_results["ICMP"]}
              ''')
        
        # if 'tcp' in nm[target] and 22 in nm[target]['tcp'] and nm[target]['tcp'][22]['state'] == 'open' :
        #     print(nm[target]['tcp'][22].get('name', 'unknown'))
        #     print("\n\nTELNET IS OPEN TO EXTERNAL NETWORK")
        
# ===============================================================================================================================================================
                
    if side == "internal":
            # Quét TCP UDP
        print (f"\nTiến hành scan TCP UDP.....")
        nm.scan(target, arguments=f"{interface_arg} {criteria_7_11_12} -T 5")
        for host in nm.all_hosts():
            #khởi tạo dictionary
            scan_results["Ports"] = {}
            
            print("\n=========Scanning result=========")
            if 'tcp' in nm[host]:
                scan_results["Ports"]["tcp"] = {}
                print("\nTCP\n")
                for port in nm[host]['tcp']:
                    port_info = nm[host]['tcp'][port]
                    print(f"Port: {port} ({port_info["state"]}):")
                    print(f"   Service: {port_info.get("name", "unknown")}\n")
                    scan_results["Ports"]["tcp"][port] = {
                        "state": port_info['state'],
                        "service": port_info.get('name', 'unknown')
                    }
                    
                

            if 'udp' in nm[host]:
                print("\nUDP\n")
                scan_results["Ports"]["udp"] = {}
                for port in nm[host]['udp']:
                    port_info = nm[host]['udp'][port]
                    print(f"Port {port} ({port_info["state"]}):")
                    print(f"   Service: {port_info.get("name", "unknown")}\n")
                    scan_results["Ports"]["udp"][port] = {
                        "state": port_info['state'],
                        "service": port_info.get('name', 'unknown')
                    }

        # Quét với lệnh -sP (Ping Scan)
        scan_results["ICMP"] = {}
        nm.scan(target, arguments=f"{interface_arg} {criteria_15} -T 5")
        print("ICMP")
        # print (f"this is scanstat: {nm.scanstats()}")
        # print (f"this is all host: {nm.all_hosts()}")
        
        
        icmp_result = nm.scanstats()
        
        if icmp_result["uphosts"] == "0":
            print("ICMP is blocked or filtered")
            scan_results["ICMP"] = "ICMP is blocked or filtered"
            
        if icmp_result["uphosts"] == "1":
            print("ICMP is open")
            scan_results["ICMP"] = "ICMP is open"
     

    
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