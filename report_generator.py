import os
from fpdf import *
import utils

# Hàm tạo báo cáo văn bản từ dữ liệu profile
def generate_report(profile_data):
    internal_result = profile_data.get('internal_result', {})
    external_result = profile_data.get('external_result', {})
    
    report = f"============= Firewall Report =============\n"
    report += f"Profile Name: {profile_data.get('name', 'Not defined')}\n"
    report += f"=============================================\n"
    
    # Báo cáo về Internal Scan
    report += "\n--- Internal Scan Results ---\n"
    if internal_result:
        report += "ICMP: " + internal_result.get('ICMP', 'No ICMP results') + "\n"
        
        report += "\nPorts:\n"
        if 'Ports' in internal_result:
            if internal_result['Ports']:
                for port, details in internal_result['Ports'].items():
                    report += f"- {port}: {details}\n"
            else:
                report += "No open ports.\n"
        else:
            report += "No port information.\n"
    else:
        report += "No internal scan results.\n"

    # Báo cáo về External Scan
    report += "\n--- External Scan Results ---\n"
    if external_result:
        report += "ICMP: " + external_result.get('ICMP', 'No ICMP results') + "\n"
        
        report += "\nPorts (TCP):\n"
        if 'Ports' in external_result and 'tcp' in external_result['Ports']:
            for port, details in external_result['Ports']['tcp'].items():
                report += f"- {port}: {details['state']} ({details['service']})\n"
        else:
            report += "No TCP port information.\n"
        
        report += "\nPorts (UDP):\n"
        if 'Ports' in external_result and 'udp' in external_result['Ports']:
            for port, details in external_result['Ports']['udp'].items():
                report += f"- {port}: {details['state']} ({details['service']})\n"
        else:
            report += "No UDP port information.\n"
    else:
        report += "No external scan results.\n"

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
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, 'FIREWALL REPORT', ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    # In từng dòng báo cáo
    lines = report.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)



    # Đường dẫn đầy đủ đến file PDF
    report_filename = os.path.join(utils.PROFILES_DIR, profile_name, f"{profile_name}_firewall_report.pdf")
    
    # Lưu file PDF
    pdf.output(report_filename)
    print(f"Report has been saved to: {report_filename}")
