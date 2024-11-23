import os
from fpdf import *
import utils

def generate_report(profile_data, choice, ai_message = ''):
    internal_result = profile_data.get("internal_result", {})
    external_result = profile_data.get("external_result", {})
    
    # Cons
    IR = "internal_result"
    ER = "external_result"
    ND = "Not defined!"
    FI = "firewall"

    
    report = f"Profile Name: {profile_data.get("name",ND)}\n"

    # Internal Scan
    if ((choice == 3) or (choice == 5)):
        report += "\n"
        report += "Internal Scan Results\n"
        
        if internal_result and (profile_data.get(IR) != "this is just a string for testing"):

            # Scanning Time
            report += f"Scanning Time: {profile_data.get(IR,ND).get("time_of_scan",ND)}\n"

            # IP Internal
            report += f"Internal Firewall IP: {profile_data.get(IR,ND).get("firewall",ND).get("ip",ND)}\n"
            
            # Host Numbers
            report += "\n"
            report += f"Number of Devices Found: {profile_data.get(IR,ND).get("host_discovery",ND).get("host_number",ND)}\n"

            host_dis = profile_data.get(IR,ND).get("host_discovery",ND)
            if (len(host_dis) > 0):
                for host_addr, host_info in host_dis.items():
                    if (host_addr != "host_number"):
                        report += f"{host_addr}: {host_info}\n"

            # ICMP
            report += "\n"
            report += f"ICMP:\n{profile_data.get(IR,ND).get(FI,ND).get("icmp",ND)}\n"

            # Ports TCP
            report += "\n"
            report += "Ports (TCP):\n"

            ports_tcp = profile_data.get(IR,ND).get(FI,ND).get("tcp",ND)
            
            if (ports_tcp == 0):
                report += "No TCP port information.\n"
            else:
                if (len(ports_tcp) > 0):
                    for port_number, info in ports_tcp.items():
                        report += f"Port {port_number}:\n"
                        for key, value in info.items():
                            report += f"{key}: {value} \n"

            
            # Ports UDP
            report += "\n"
            report += "Ports (UDP):\n"

            ports_udp = profile_data.get(IR,ND).get(FI,ND).get("udp",ND)
            if (ports_udp == 0):
                report += "No UDP port information.\n"
            else:
                if len(ports_udp) > 0:
                    for port_number, info in ports_udp.items():
                        report += f"Port {port_number}:\n"
                        for key, value in info.items():
                            report += f"{key}: {value} \n"
            
        else:
            report += "No internal scan results.\n"


    # External Scan
    if ((choice == 4) or (choice == 5)):
        report += "\n"
        report += "External Scan Results\n"
        
        if external_result and (profile_data.get("external_result") != "this is just a string for testing"):
            
            # Scanning Time
            report += f"Scanning Time: {profile_data.get(ER,ND).get("time_of_scan",ND)}\n"

            # IP External
            report += f"External Firewall IP: {profile_data.get(ER,ND).get("firewall_ip",ND)}\n"

            # ICMP
            report += "\n"
            report += f"ICMP:\n{profile_data.get(ER,ND).get("icmp",ND)}\n"

            # Ports TCP
            report += "\n"
            report += "Ports (TCP):\n"

            ports_tcp = profile_data.get(ER,ND).get("tcp",ND)
            print(f'this is ports_tcp: {ports_tcp}')
            if len(ports_tcp) > 0:
                for port_number, info in ports_tcp.items():
                    report += f"Port {port_number}:\n"
                    for key, value in info.items():
                        report += f"{key}: {value} \n"
            else:
                report += "No TCP port information.\n"
            
            # Ports UDP
            report += "\n"
            report += "Ports (UDP):\n"

            ports_udp = profile_data.get(ER,ND).get("udp",ND)
            if (ports_udp == 0):
                report += "No UDP port information.\n"
            else:
                if len(ports_udp) > 0:
                    for port_number, info in ports_udp.items():
                        report += f"Port {port_number}:\n"
                        for key, value in info.items():
                            report += f"{key}: {value} \n"
        else:
            report += "No external scan results.\n"
            
            
    report += f'\nThis is ai evaluation:\n {ai_message}'
    print(f'This is ai evaluation:\n {ai_message}')
    

    return report

def save_report_to_pdf(report, profile_name):

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_top_margin(20)
    
    pdf.add_page()
    pdf.add_font("Arial", "", "Arial.ttf", uni = True)
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style='B', size=40)
    pdf.multi_cell(0, 10, "_____________________")
    pdf.set_font("Arial", style='B', size=50)
    pdf.multi_cell(0, 40, "FIREWALL")
    pdf.multi_cell(0, 10, "REPORT")
    # pdf.ln(10)

    # Print report
    # check = 0
    ai_check = 0
    lines = report.split('\n')
    for line in lines:

        # Internal Scan
        if (line == "Internal Scan Results"):
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=40)
            pdf.multi_cell(0, 10, "_____________________")
            pdf.set_font("Arial", style='B', size=35)
            pdf.multi_cell(0, 30, "Internal Firewall")
            pdf.multi_cell(0, 10, "Scan Result")
            pdf.multi_cell(0, 15, "")

        # External Scan
        elif (line == "External Scan Results"):
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=40)
            pdf.multi_cell(0, 10, "_____________________")
            pdf.set_font("Arial", style='B', size=35)
            pdf.multi_cell(0, 30, "External Firewall")
            pdf.multi_cell(0, 10, "Scan Result")
            pdf.multi_cell(0, 15, "")

        # Profile Name
        elif ("Profile Name:" in line):
            pdf.set_font("Arial", style='B', size=20)
            pdf.multi_cell(0, 30, line)
        #     check = 1
        # elif (check == 1):
        #     check = 0
        #     pdf.set_font("Arial", size=20)
        #     pdf.multi_cell(0, 10, line)

        elif ("Scanning Time: " in line):
            pdf.set_font("Arial", style='B', size=13)
            pdf.multi_cell(0, 10, line)

        elif (("External Firewall IP:" in line) or ("Internal Firewall IP:" in line)):
            pdf.set_font("Arial", style='B', size=13)
            pdf.multi_cell(0, 10, line)

        elif ("Number of Devices Found:" in line):
            pdf.set_font("Arial", style='B', size=15)
            pdf.multi_cell(0, 10, line)

        elif ((line == "ICMP:") or (line == "Ports:") or (line == "Ports (TCP):") or (line  == "Ports (UDP):")):
            pdf.set_font("Arial", style='B', size=15)
            pdf.multi_cell(0, 10, line)


        elif (("Port" in line) and (ai_check == 0)):
            pdf.set_font("Arial", style='B', size=13)
            pdf.multi_cell(0, 10, line)

        # AI Evaluation
        elif ("This is ai evaluation:" in line):
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=40)
            pdf.multi_cell(0, 10, "_____________________")
            pdf.set_font("Arial", style='B', size=35)
            pdf.multi_cell(0, 30, "AI")
            pdf.multi_cell(0, 10, "Evaluation")
            pdf.multi_cell(0, 15, "")
            ai_check = 1

        elif (("1. Evaluate Firewall Configuration:" in line) or ("2. Risks of Firewall Configuration:" in line) or ("3. Solutions:" in line)):
            pdf.set_font("Arial", style='B', size=15)
            pdf.multi_cell(0, 10, line)

        else:
            pdf.set_font("Arial", size=13)
            pdf.multi_cell(0, 10, line)


    # File PDF Path
    report_filename = os.path.join(utils.PROFILES_DIR, profile_name, f"{profile_name}_firewall_report.pdf")
    
    # Save file PDF
    pdf.output(report_filename)
    print(f"Report has been saved to: {report_filename}")
