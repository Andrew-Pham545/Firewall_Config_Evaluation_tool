import scanner
from colorama import Fore, init
import time

def firewall_checklist():
    print("\n--- Firewall Checklist ---")
    
    checklist = {
        "criteria_1": "Review the rulesets",
        "criteria_2": "Stateful inspection",
        "criteria_3": "Logging",
        "criteria_4": "Patches and updates",
        "criteria_5": "Vulnerability assessments/Testing",
        "criteria_6": "Compliance with security policy",
        "criteria_7": "Block spoofed, private, and illegal IPs",
        "criteria_8": "Port restrictions",
        "criteria_9": "Remote access",
        "criteria_10": "File transfers",
        "criteria_11": "ICMP",
        "criteria_12": "Egress filtering",
        "criteria_13": "Firewall redundancy",
    }

    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")
    
    pros_message = ''
    cons_message = ''
    
    results = {}  # Lưu kết quả với key ngắn gọn
    results["time_of_evaluation"] = current_time 
    for key, question in checklist.items():
        while True:  
            print(f"\nQuestion: {question}")
            
            if key == "criteria_1":
                print('nội dung: bla bla bla')
                pros_message = 'Rulesets follow best practices: anti-spoofing, permit, deny & log.'
                cons_message = 'Incomplete or improperly ordered rulesets, allowing suspicious traffic.'
                
                
            if key == "criteria_2":
                print('nội dung crit 2: bla bla bla')
                pros_message = 'Appropriate timeouts, MAC filtering, URL/script filtering applied.'
                cons_message = 'Long timeouts, no MAC or URL filtering, allowing harmful scripts.'
                
            if key == "criteria_3":
                print('nội dung: bla bla bla')
                pros_message = 'Logs are enabled, monitored, and analyzed for attack patterns.'
                cons_message = 'Logs disabled or ignored, missing critical attack indicators.'
                
            if key == "criteria_4":
                print('nội dung: bla bla bla')
                pros_message = 'Latest patches tested and applied from trusted sources.'
                cons_message = 'Outdated software with unpatched vulnerabilities.'
                
            if key == "criteria_5":
                pros_message = 'Regular port scans and ruleset validations performed.'
                cons_message = 'Open ports remain untested, leading to potential misconfigurations.'
                while True:
                    action = input("This criteria could require for port scan, do you want to scan the port (y/n): ")
                    if action in ["y", "n"]:
                        if action == "y":
                            target = input(f'\n{Fore.YELLOW + "Enter the firewall external IP:"} {Fore.RESET}')
                            scanner.scan_tcp_udp(target)
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                
            if key == "criteria_6":
                print('nội dung: bla bla bla')
                pros_message = 'Rulesets align with organizational security requirements.'
                cons_message = 'Rulesets contradict or fail to enforce security policies.'
                
            if key == "criteria_7":
                print('nội dung: bla bla bla')
                pros_message = 'RFC 1918 and illegal addresses are blocked and logged.'
                cons_message = 'Spoofed or illegal traffic is not filtered, posing security risks.'
                
            if key == "criteria_8":
                pros_message = 'Unused and critical ports are blocked according to policy.'
                cons_message = 'Open or unnecessary ports exposed to exploitation.'
                while True:
                    action = input("This criteria could require for port scan, do you want to scan the port (y/n): ")
                    if action in ["y", "n"]:
                        if action == "y":
                            target = input(f'\n{Fore.YELLOW + "Enter the firewall external IP:"} {Fore.RESET}')
                            scanner.port_restriction_scan(target)
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                        
            if key == "criteria_9":
                print('nội dung: bla bla bla')
                pros_message = 'Secure access (e.g., SSH) is enforced for remote connections.'
                cons_message = 'Telnet or other insecure protocols are allowed.'
                
            if key == "criteria_10":
                print('nội dung: bla bla bla')
                pros_message = 'FTP servers are isolated from protected internal networks.'
                cons_message = 'FTP is enabled within the internal network without safeguards.'
                
            if key == "criteria_11":
                pros_message = 'Echo requests and other unnecessary ICMP types are blocked.'
                cons_message = 'ICMP traffic is unrestricted, allowing potential reconnaissance.'
                while True:
                    action = input("This criteria will require for a ICMP scan, do you want to proceed (y/n): ")
                    if action in ["y", "n"]:
                        if action == "y":
                            target = input(f'\n{Fore.YELLOW + "Enter the firewall external IP:"} {Fore.RESET}')
                            scanner.scan_icmp_restrictions(target)
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                
            if key == "criteria_12":
                print('nội dung: bla bla bla')
                pros_message = 'Only internal IP traffic is allowed to leave the network.'
                cons_message = 'Outbound traffic is unrestricted, allowing spoofed traffic to exit.'
                
            if key == "criteria_13":
                print('nội dung: bla bla bla')                        
                pros_message = 'Hot standby is configured for firewall redundancy.'
                cons_message = 'No redundancy, risking firewall downtime during failures.'

            
            answer = input("Score this Criteria (1 - 5): ")
            if answer.isdigit() and 1 <= int(answer) <= 5:
                results[key] = {}
                results[key]["score"] = int(answer) 
                if int(answer) <= 2:
                    results[key]["cons_message"] = cons_message
                elif int(answer) >= 3:
                    results[key]["pros_message"] = pros_message
                break  
            else:
                print("Invalid input. Please enter a score between 1 and 5.")                
                
            
                
                
    
    print("\nYou have completed the checklist.")
    return results
