from fpdf import FPDF
import os

def generate_report(profile_name):
    profile_path = os.path.join("profiles", profile_name)
    internal_results_file = os.path.join(profile_path, "internal_results.json")
    external_results_file = os.path.join(profile_path, "external_results.json")
    
    # Đọc kết quả từ file JSON
    with open(internal_results_file, 'r') as f:
        internal_results = f.read()
    
    with open(external_results_file, 'r') as f:
        external_results = f.read()

    # Tạo file PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Báo cáo quét mạng", ln=True, align='C')
    pdf.cell(200, 10, txt="Kết quả quét nội bộ: ", ln=True)
    pdf.multi_cell(0, 10, txt=internal_results)
    pdf.cell(200, 10, txt="Kết quả quét bên ngoài: ", ln=True)
    pdf.multi_cell(0, 10, txt=external_results)

    pdf_file_path = os.path.join(profile_path, "report.pdf")
    pdf.output(pdf_file_path)

    print(f"Báo cáo đã được tạo: {pdf_file_path}")
