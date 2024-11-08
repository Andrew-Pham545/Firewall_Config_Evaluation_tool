import nmap
import json

def scan_network(target, side):
    nm = nmap.PortScanner()
    criteria_7_11_12 = "-sS -sU -p T:0-10000,U:0-10000"  # Quét TCP và UDP tất cả các cổng
    criteria_15 = "-sS -PE --disable-arp-ping"  #ICMP check 
    criteria_4_5_6 = "-sV"  # Quét phiên bản dịch vụ

    # Kết quả quét dưới dạng dictionary
    scan_results = {}

    if side == "external":
        
       # Quét TCP UDP
        print (f"\nTiến hành scan TCP UDP.....")
        nm.scan(target, arguments=f"{criteria_7_11_12} -T 5")
        warning_flag = False
        for host in nm.all_hosts():
            #khởi tạo dictionary
            scan_results["Ports"] = {}
            
            print("\n=========Scanning result=========")
            if 'tcp' in nm[host]:
                scan_results["Ports"]["tcp"] = {}
                print("\nTCP\n")
                for port in nm[host]['tcp']:
                    port_info = nm[host]['tcp'][port]
                    print(f"=Port: {port} ({port_info["state"]}):")
                    print("|")
                    print(f"==Service: {port_info.get("name", "unknown")}")
                    scan_results["Ports"]["tcp"][port] = {
                        "state": port_info['state'],
                        "service": port_info.get('name', 'unknown')
                    }
                    
                

            if 'udp' in nm[host]:
                print("\nUDP\n")
                scan_results["Ports"]["udp"] = {}
                for port in nm[host]['udp']:
                    port_info = nm[host]['udp'][port]
                    print(f"=Port {port} ({port_info["state"]}):")
                    print(f"==Service: {port_info.get("name", "unknown")}")
                    scan_results["Ports"]["udp"][port] = {
                        "state": port_info['state'],
                        "service": port_info.get('name', 'unknown')
                    }

        # Quét với lệnh -sP (Ping Scan)
        scan_results["ICMP"] = {}
        nm.scan(target, arguments=f"{criteria_15} -T 5")
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
            
            
        if warning_flag == True:
            if 'tcp' in nm[target] and 22 in nm[target]['tcp'] and nm[target]['tcp'][22]['state'] == 'open' :
                print(nm[target]['tcp'][22].get('name', 'unknown'))
                print("TELNET IS OPEN TO EXTERNAL NETWORK")

                
            

  
            
        if side == "external":
            print("placeholder")
     

    
    return scan_results  # Trả về kết quả dưới dạng JSON