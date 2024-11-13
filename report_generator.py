import os
from fpdf import *
import utils

# Hàm tạo báo cáo văn bản từ dữ liệu profile
def generate_report(profile_data, choice, ai_message = ''):
    internal_result = profile_data.get("internal_result", {})
    external_result = profile_data.get("external_result", {})
    # Hằng
    IR = "internal_result"
    ER = "external_result"
    ND = "Not defined!"
    FI = "firewall"

    
    report = f"Profile Name:\n{profile_data.get("name",ND)}\n"


    # Báo cáo về Internal Scan
    if ((choice == 3) or (choice == 5)):
        report += "\n"
        report += "--------- Internal Scan Results ---------\n"
        
        if internal_result and (profile_data.get("internal_result") != "this is just a string for testing"):

            # Host Numbers
            report += f"Host Numbers: {profile_data.get(IR,ND).get("host_number",ND)}\n"

            # ICMP
            report += f"ICMP:\n {profile_data.get(IR,ND).get(FI,ND).get("icmp",ND)}"

            # Ports TCP
            report += "\n"
            report += "Ports (TCP):\n"

            ports_tcp = profile_data.get(IR,ND).get(FI,ND).get("tcp",ND)
            if ports_tcp > 0:
                for port_number, info in ports_tcp.items():
                    report += f"Port {port_number}:\n"
                    for key, value in info.items():
                        report += f"{key}: {value} \n"
            else:
                report += "No TCP port information.\n"
            
            # Ports UDP
            report += "\n"
            report += "Ports (UDP):\n"

            ports_udp = profile_data.get(IR,ND).get(FI,ND).get("udp",ND)
            if ports_udp > 0:
                for port_number, info in ports_udp.items():
                    report += f"Port {port_number}:\n"
                    for key, value in info.items():
                        report += f"{key}: {value} \n"
            else:
                report += "No TCP port information.\n"
            
        else:
            report += "No internal scan results.\n"


    # Báo cáo về External Scan
    if ((choice == 4) or (choice == 5)):
        report += "\n"
        report += "--------- External Scan Results ---------\n"
        
        if external_result and (profile_data.get("external_result") != "this is just a string for testing"):
            
            # ICMP
            report += f"ICMP:\n {profile_data.get(ER,ND).get("icmp",ND)}"

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
            if len(ports_udp) > 0:
                for port_number, info in ports_udp.items():
                    report += f"Port {port_number}:\n"
                    for key, value in info.items():
                        report += f"{key}: {value} \n"
            else:
                report += "No TCP port information.\n"
        else:
            report += "No external scan results.\n"
            
    if choice == 5:
        report += f'\nthis is ai evaluation: {ai_message}'
        print(f'this is ai evaluation: {ai_message}')

    

    return report

# Hàm lưu báo cáo vào file PDF với đường dẫn tùy chỉnh
def save_report_to_pdf(report, profile_name):
    # Tạo đối tượng PDF mới
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_top_margin(20)
    
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Tiêu đề báo cáo
    pdf.set_font("Arial", style='B', size=40)
    pdf.cell(0, 10, "FIREWALL REPORT", ln=True, align="C")
    pdf.ln(10)

    # In từng dòng báo cáo
    check = 0
    lines = report.split('\n')
    for line in lines:
        if ((line == "--------- Internal Scan Results ---------") or (line == "--------- External Scan Results ---------")):
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=20)
            pdf.multi_cell(0, 15, line, align = "C")

        # Profile Name viết khác tí
        elif (line == "Profile Name:"):
            pdf.set_font("Arial", style='B', size=20)
            pdf.multi_cell(0, 10, line)
            check = 1
        elif (check == 1):
            check = 0
            pdf.set_font("Arial", size=20)
            pdf.multi_cell(0, 10, line)


        elif ((line == "ICMP:") or (line == "Ports:") or (line == "Ports (TCP):") or (line  == "Ports (UDP):")):
            pdf.set_font("Arial", style='B', size=15)
            pdf.multi_cell(0, 10, line)


        elif (("Port" in line)):
            pdf.set_font("Arial", style='B', size=13)
            pdf.multi_cell(0, 10, line)


        else:
            pdf.set_font("Arial", size=13)
            pdf.multi_cell(0, 10, line)


    # Đường dẫn đầy đủ đến file PDF
    report_filename = os.path.join(utils.PROFILES_DIR, profile_name, f"{profile_name}_firewall_report.pdf")
    
    # Lưu file PDF
    pdf.output(report_filename)
    print(f"Report has been saved to: {report_filename}")
