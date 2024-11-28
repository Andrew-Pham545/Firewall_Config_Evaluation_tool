from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.piecharts import Pie
import utils
import os


def create_firewall_report(data_dict, profile_name, output_filename="firewall_report.pdf", ai_message=''):
    """
    Create a comprehensive firewall configuration report PDF from a dictionary.
    Includes a cover page, report summary, explanation of criteria, and evaluation details.
    """
    
    profile_dir = os.path.join(utils.PROFILES_DIR, profile_name)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir, exist_ok=True)

    output_filepath = os.path.join(profile_dir, output_filename)

    
    
    # Lấy thông tin từ dictionary
    name = data_dict.get("name", "N/A")
    evaluation_result = data_dict.get("evaluation_result", {})
    # print(evaluation_result)
    time_of_evaluation = evaluation_result.get("time_of_evaluation", "N/A")
    
    scanner_result = data_dict.get("scan_result", {})
    
    print(scanner_result)
    
    # Tách các tiêu chí và kết quả
    criteria = {k: v for k, v in evaluation_result.items() if k != "time_of_evaluation"}
    # print("Criteria:", criteria)

    # Tính tổng điểm từ các tiêu chí
    # print(f'item["score"]: {item["score"]}')
    total_score = sum(int(item["score"]) for item in criteria.values())
    print("Total Score:", total_score)
    max_score = len(criteria) * 5 

       # Mapping tiêu chí
    criteria_mapping = {
        "criteria_1": "Review the ruleset order",
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
        "criteria_13": "Firewall redundancy"
    }

    
    # Khởi tạo PDF
    doc = SimpleDocTemplate(output_filepath, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    
    title_style = ParagraphStyle(
        name="CustomTitle",
        fontName="Helvetica-Bold",
        fontSize=65,  # Chỉnh cỡ chữ cho tiêu đề lớn
        leading=70,   # Khoảng cách giữa các dòng
        alignment=0,  # Căn giữa
        textColor=colors.darkblue,
    )

    subtitle_style = ParagraphStyle(
        name="CustomSubtitle",
        fontName="Helvetica",
        fontSize=18,  # Chỉnh cỡ chữ nhỏ hơn
        leading=24,
        alignment=0,  # Căn giữa
        textColor=colors.black,
    )

    date_style = ParagraphStyle(
        name="CustomDate",
        fontName="Helvetica-Oblique",
        fontSize=14,  # Cỡ chữ nhỏ nhất
        leading=20,
        alignment=0,  # Căn giữa
        textColor=colors.grey,
    )    
    
    main_point_style = ParagraphStyle(
        name="CustomMainPoint",
        fontName="Helvetica-Bold",
        fontSize=30,  # Cỡ chữ nhỏ nhất
        leading=20,
        alignment=0,  # Căn giữa
        textColor=colors.black,
    )    
    
    # 1. Cover Page
    cover_title_1 = Paragraph("Firewall", title_style)
    cover_title_2 = Paragraph("Configuration", title_style)
    cover_title_3 = Paragraph("Assessment", title_style)
    cover_title_4 = Paragraph("Report", title_style)
    cover_subtitle = Paragraph(f"{name}", subtitle_style)
    cover_date = Paragraph(f"Date of Assessment: {time_of_evaluation}", date_style)
    
    elements.append(Spacer(1, 100))  # Khoảng cách lớn trên trang bìa
    elements.append(cover_title_1)
    elements.append(cover_title_2)
    elements.append(cover_title_3)
    elements.append(cover_title_4)
    elements.append(Spacer(1, 20))
    elements.append(cover_subtitle)
    elements.append(Spacer(1, 7))
    elements.append(cover_date)
    elements.append(PageBreak())  # Chuyển sang trang mới

    # 2. Report Summary
    elements.append(Paragraph("1. Report Summary", main_point_style))
    elements.append(Spacer(1, 30))
    
    elements.append(Paragraph(f"Overall Score: {total_score}/{max_score} ({(total_score/max_score)*100:.2f}%)", styles['Heading3']))
    # progress_bar = add_progress_bar(total_score, max_score)
    progress_bar = add_progress_bar(
    value=total_score,
    max_value=max_score,
    width=400,
    height=20,
    border_color="#4A90E2",  # Màu xanh nhạt
    fill_color="#50E3C2"    # Màu xanh lá nhạt
    )
    elements.append(progress_bar)
    elements.append(Spacer(1, 30))
    
    # summary_data = [
    #     ["Assessment Date", time_of_evaluation],
    #     ["Firewall Name/Model", name],
    #     ["Overall Score", "Pass"]  # Có thể tính toán từ dict
    # ]
    # summary_table = Table(summary_data, colWidths=[100, 350]) # width va 
    # summary_table.setStyle(TableStyle([
    #     ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    #     ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
    #     ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    # ]))
    # elements.append(summary_table)
    
    pros_cons_style = ParagraphStyle(
        name="CustomProsCons",
        fontName="Helvetica-Bold",
        fontSize=24,  # Cỡ chữ nhỏ nhất
        leading=20,
        alignment=0,  # Căn giữa
        textColor=colors.black,
        leftIndent=10
    )    
    # Custom style for bullet points
    bullet_style = ParagraphStyle(
        name="BulletPoints",
        fontName="Helvetica",
        fontSize=12,  # Font size for bullet points
        leading=16,
        leftIndent=20,  # Indentation for bullets
        bulletIndent=10,  # Indentation for the bullet itself
        bulletFontName="Helvetica-Bold",  # Font for bullets
        textColor=colors.black,
    )


    pros_list = [v["pros_message"] for v in criteria.values() if "pros_message" in v]
    cons_list = [v["cons_message"] for v in criteria.values() if "cons_message" in v]
    # print(cons_list)
    # Add "Pros" heading
    if pros_list != []:
        elements.append(Paragraph("Pros:", pros_cons_style))
        
    elements.append(Spacer(1, 15))  # Add a bit of space after the heading

    # Add bullet points under "Pros"
    # pros_list = [
    #     "Comprehensive firewall functionality meeting security needs.",
    #     "Extensive logging for detailed monitoring.",
    #     "Secure remote access for management interfaces.",
    #     "Strict control over external service ports."
    # ]
    for item in pros_list:
        elements.append(Paragraph(f"• {item}", bullet_style))
        elements.append(Spacer(1, 7))  # Space before the next section
    elements.append(Spacer(1, 20))  # Space before the next section

    # Add "Cons" heading
    if cons_list != []:
        elements.append(Paragraph("Cons:", pros_cons_style))
        
    elements.append(Spacer(1, 15))  # Add a bit of space after the heading

    # Add bullet points under "Cons"
    # cons_list = [
    #     "Limited protection against specific vulnerabilities like DDoS.",
    #     "HTTP access from external sources is restricted.",
    #     "Missing a built-in alerting mechanism for threats."
    # ]
    for item in cons_list:
        elements.append(Paragraph(f"• {item}", bullet_style))
        elements.append(Spacer(1, 7))  # Space before the next section

    elements.append(Spacer(1, 20))  # Space after the "Cons" section
    # elements.append(Paragraph("2. Explanation of Criteria", main_point_style))

    
    
    
    elements.append(Spacer(1, 20))

   
    elements.append(PageBreak())  # Chuyển sang trang mới
    # 3. Criteria and Evaluation
    elements.append(Paragraph("2. Evaluation Details", main_point_style))
    elements.append(Spacer(1, 30))

    elements.append(Paragraph('Score detail', styles['Heading3']))

    # Create table headers
    criteria_data = [["No.", "Criteria", "Score", "Passed Steps/Total Steps"]]  # Thêm cột 'Passed Steps / Total Steps'

    # Populate table rows with "No.", "Criteria", "Score", and "Passed Steps / Total Steps"
    for idx, (key, value) in enumerate(criteria.items(), start=1):
        criteria_name = criteria_mapping.get(key, key)  # Lấy tên tiêu chí từ mapping
        score = value.get("score", "N/A")  # Lấy điểm số
        passed_steps = sum(1 for step, passed in value['steps'].items() if passed)
        total_steps = len(value['steps'])
        passed_steps_info = f"{passed_steps} / {total_steps}"  # Tính toán và thêm thông tin "Passed Steps / Total Steps"
        
        criteria_data.append([idx, criteria_name, score, passed_steps_info])  # Thêm dòng vào bảng

    # Create the table
    criteria_table = Table(criteria_data, colWidths=[50, 300, 50, 150])
    criteria_table.setStyle(TableStyle([
        # Header row style
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        # Row styles
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),

        # Align "No." column to the center
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),

        # Align "Score" and "Passed Steps / Total Steps" columns to the center
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),

        # Grid lines
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(criteria_table)
    elements.append(Spacer(1, 20))
    

    #pie chart
    pie_chart = create_pie_chart_from_criteria(criteria)
    elements.append(pie_chart)

    # elements.append(Spacer(1, 30))
    
    failed_steps_data = [["No.", "Criterion", "Failed Step"]]  # Header của bảng

    # Duyệt qua các tiêu chí và tìm các bước không đạt
    for idx, (criterion_key, criterion_value) in enumerate(criteria.items(), start=1):
        criteria_name = criteria_mapping.get(criterion_key, criterion_key)
        for step_description, step_passed in criterion_value['steps'].items():
            if not step_passed:  # Nếu bước không đạt
                # Chuyển nội dung thành Paragraph để hỗ trợ wrap
                failed_steps_data.append([
                    idx,
                    Paragraph(criteria_name, styles["Normal"]),
                    Paragraph(step_description, styles["Normal"])
                ])

# Nếu có bước không đạt thì thêm bảng vào báo cáo
    if len(failed_steps_data) > 1:  # Kiểm tra xem có bước nào không đạt không
        elements.append(PageBreak())  # Bắt đầu trang mới cho bảng các bước không đạt
        elements.append(Paragraph('Failed steps', styles['Heading2']))

        # Create the failed steps table
        failed_steps_table = Table(failed_steps_data, colWidths=[50, 200, 300])
        failed_steps_table.setStyle(TableStyle([
            # Header row style
            ('BACKGROUND', (0, 0), (-1, 0), colors.red),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            # Row styles
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),

            # Align "No." column to the center
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),

            # Grid lines
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(failed_steps_table)
        elements.append(Spacer(1, 20))
    
    normal_style = ParagraphStyle(
    name="normalStyle",
    fontName="Helvetica",
    fontSize=12,  # Font size for bullet points
    leading=16,
    leftIndent=35,  # Indentation for bullets
    bulletIndent=10,  # Indentation for the bullet itself
    bulletFontName="Helvetica-Bold",  # Font for bullets
    textColor=colors.black,
    )
    
    
    # Scan Result - Nếu có
    if len(scanner_result) > 0:  
        elements.append(Paragraph("Scan Result", styles['Heading2']))
        
        # elements.append(Spacer(1, 30))

        # Định nghĩa dữ liệu scan để hiển thị
        target = scanner_result.get("target", "N/A")
        elements.append(Paragraph(f"• The IP of external side: {target}", bullet_style))
        elements.append(Spacer(1, 10))
        
        protocols = scanner_result.get("protocols", {})
        
        for protocol, ports in protocols.items():
            elements.append(Paragraph(f"• {protocol.upper()}:", bullet_style))
            for port_info in ports:
                port = port_info.get("port", "N/A")
                elements.append(Paragraph(f"+  Port {port} (open)", normal_style))
            elements.append(Spacer(1, 10))
        
        icmp_state = scanner_result.get("icmp", "N/A")
        elements.append(Paragraph(f"• The ICMP rule on the external side of the firewall is: {icmp_state}", bullet_style))
        elements.append(Spacer(1, 20))
    
        
        
    elements.append(PageBreak())
    # 4. Summary and Recommendations
    elements.append(Paragraph("3. Recommendations", main_point_style))
    elements.append(Spacer(1, 30))

    recommendations = []

    failed_step_count = len(failed_steps_data) - 1
    
    # Nếu có hơn 5 bước không đạt, thêm dòng cảnh báo
    if failed_step_count  > 5:
        recommendations.append(f"There are {failed_step_count} steps that are not passing. The admin should review these step and make change if it meet the requirement of the network.")
    
    
    # Hiển thị đề xuất trong báo cáo
    if recommendations:
        elements.append(Spacer(1, 15))
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", bullet_style))
    else:
        elements.append(Paragraph("All criteria are satisfactory. No specific recommendations for this network", bullet_style))

    elements.append(Spacer(1, 20))



    # Kế hoạch hành động
    action_plan = []

    # 1. Kích hoạt logging nếu chưa bật
    if "Logging" in evaluation_result and evaluation_result["Logging"]["score"] == 0:
        action_plan.append("Enable logging immediately and configure periodic log reviews.")

    # 2. Thay thế Telnet bằng SSH
    if "Remote access" in evaluation_result and evaluation_result["Remote access"]["score"] == 0:
        action_plan.append("Replace insecure remote access protocols (e.g., Telnet) with secure options like SSH.")

    # 3. Áp dụng các bản vá và cập nhật
    if "Patches and updates" in evaluation_result and evaluation_result["Patches and updates"]["score"] == 0:
        action_plan.append("Apply the latest firewall patches and ensure reliable download sources.")

    # 4. Chặn các địa chỉ IP bất hợp pháp và spoofing
    if "Block spoofed, private, and illegal IPs" in evaluation_result:
        failed_steps = [step for step, passed in evaluation_result["Block spoofed, private, and illegal IPs"]["steps"].items() if not passed]
        if failed_steps:
            action_plan.append("Review and block the following illegal or spoofed IP addresses:")
            for step in failed_steps:
                action_plan.append(f"---{step}")

    # 5. Kiểm tra và bảo vệ các cổng mở
    tcp_open_ports = [p["port"] for p in scanner_result["protocols"]["tcp"] if p["state"] == "open"]
    udp_open_ports = [p["port"] for p in scanner_result["protocols"]["udp"] if p["state"] == "open"]

    if tcp_open_ports or udp_open_ports:
        action_plan.append("Review and secure the following open ports:")
        if tcp_open_ports:
            action_plan.append(f"--- TCP: {', '.join(map(str, tcp_open_ports))}")
        if udp_open_ports:
            action_plan.append(f"--- UDP: {', '.join(map(str, udp_open_ports))}")

    # 6. Kiểm tra ICMP
    if scanner_result.get("icmp") == "open":
        action_plan.append("Block unnecessary ICMP traffic to reduce the risk of reconnaissance attacks.")

    # 7. Tối ưu hóa các bộ quy tắc (ruleset)
    if "Review the rulesets order (in the following order)" in evaluation_result:
        failed_steps = [step for step, passed in evaluation_result["Review the rulesets order (in the following order)"]["steps"].items() if not passed]
        if failed_steps:
            action_plan.append("Optimize firewall ruleset order to minimize conflicts and improve performance:")
            for step in failed_steps:
                action_plan.append(f"--- {step}")

    # 8. Khuyến nghị về đánh giá lỗ hổng
    if "Vulnerability assessments/Testing" in evaluation_result:
        failed_steps = [step for step, passed in evaluation_result["Vulnerability assessments/Testing"]["steps"].items() if not passed]
        if failed_steps:
            action_plan.append("Perform regular vulnerability assessments using tools like nmap to identify open ports and vulnerabilities:")
            for step in failed_steps:
                action_plan.append(f"--- {step}")

    # 9. Xác nhận thời gian quét
    if "completed_at" in scanner_result:
        action_plan.append(f"Ensure periodic scans like the one completed on {scanner_result['completed_at']}.")

    elements.append(Paragraph("Action Plan:", styles["Heading3"]))
    elements.append(Spacer(1, 10))

    for action in action_plan:
        elements.append(Paragraph(f"• {action}", bullet_style))
        elements.append(Spacer(1, 3))

    if ai_message != '':
            # Split the AI message into bullet points based on '•'
        bullet_points = [f"• {point.strip()}" for point in ai_message.split("•") if point.strip()]

        # Add AI evaluation heading
        elements.append(Paragraph("AI Evaluation:", styles["Heading3"]))
        elements.append(Spacer(1, 10))

        # Add each bullet point as a paragraph
        for point in bullet_points:
            elements.append(Paragraph(point, bullet_style))
            elements.append(Spacer(1, 10))  # Add space between bullet points

        
    elements.append(Spacer(1, 20))
        
    
    
    
    elements.append(PageBreak())
     # 5. Explanation of Criteria
    elements.append(Paragraph("4. APPENDIX", main_point_style))
    elements.append(Spacer(1, 30))
    
    
    elements.append(Paragraph("The criterias", styles['Heading3']))
    elements.append(Paragraph("This criteria is a smaller version of SANS firewall checklist. Our team has custom it to fit with the definition and pratical use case of small network. You can check the full version here: https://www.sans.org/media/score/checklists/FirewallChecklist.pdf ", bullet_style))
    
    explanation_data = [
        ["No.", "Criteria", "Definition"],
        [1, "Review the rulesets order", 
        """Review the rulesets to ensure that they follow the order as follows:
• anti-spoofing filters (blocked private addresses, internal addresses
        appearing from the outside)
• User permit rules (e.g. allow HTTP to public webserver)
• Management permit rules (e.g. SNMP traps to network management server)
• Noise drops (e.g. discard OSPF and HSRP chatter)
• Deny and Alert (alert systems administrator about traffic
that is suspicious)
• Deny and log (log remaining traffic for analysis)

• Firewalls operate on a first match basis, thus the above structure is
important to ensure that suspicious traffic is kept out 
instead of inadvertently allowing them in by not
following the proper order."""],
        [2, "Stateful inspection", '''Stateful inspection
Review the state tables to ensure that appropriate rules are set up in terms of
source and destination IP’s, source and destination ports and timeouts.
Ensure that the timeouts are appropriate so as not to give the hacker too much
time to launch a successful attack.
For URL’s
• If a URL filtering server is used, ensure that it is appropriately
defined in the firewall software. If the filtering server is external to
the organisation ensure that it is a trusted source.
• If the URL is from a file, ensure that there is adequate protection
for this file to ensure no unauthorised modifications.
Ensure that specific traffic containing scripts; ActiveX and java are striped prior
to being allowed into the internal network.
If filtering on MAC addresses is allowed, review the filters to ensure that it is
restricted to the appropriate MAC’s as defined in the security policy'''],
        [3, "Logging", '''Ensure that logging is enabled and that the logs are reviewed to identify any
potential patterns that could indicate an attack.'''],
        [4, "Patches and updates", '''Ensure that the latest patches and updates relating to your firewall product is
tested and installed.
If patches and updates are automatically downloaded from the vendors’
websites, ensure that the update is received from a trusted site.
Page 4 of 6
In the event that patches and updates are e-mailed to the systems
administrator ensure that digital signatures are used to verify the vendor and
ensure that the information has not been modified en-route.'''],
        [5, "Vulnerability assessments/Testing", '''Ascertain if there is a procedure to test for open ports using nmap and whether
unnecessary ports are closed.
Ensure that there is a procedure to test the rulesets when established or
changed so as not to create a denial of service on the organisation or allow
any weaknesses to continue undetected.'''],
        [6, "Compliance with security policy", '''Ensure that the ruleset complies with the organisation security policy.'''],
        [7, "Block spoofed, private, and illegal IPs", '''Ensure that the following spoofed, private (RFC 1918) and illegal addresses
are blocked:
Standard unroutables
• 255.255.255.255
• 127.0.0.0
Private (RFC 1918) addresses
• 10.0.0.0 – 10.255.255.255
• 172.16.0.0 – 172.31.255.255
• 192.168.0.0 - 192.168.255.255
Reserved addresses
• 240.0.0.0
Illegal addresses
• 0.0.0.0
UDP echo
ICMP broadcast (RFC 2644)
Ensure that traffic from the above addresses is not transmitted by the
interface.'''],
        [8, "Port restrictions", '''The following ports should blocked: 
TCP:
20, 21, 22, 23, 25, 37, 53, 80, 87, 109, 110, 111, 119, 123, 135, 139,
143, 161, 162, 179, 389, 443, 445, 512, 513, 514, 515, 540, 1080, 2000,
2001, 2049, 4001, 4045, 6000, 6001, 8000, 8080, 8888

UDP:
20, 37, 53, 69, 111, 123, 135, 137, 138, 161, 162, 389, 445, 514,
2000, 2049, 4045, 6000'''],
        [9, "Remote access", '''If remote access is to be used, ensure that the SSH protocol (port 22) is used
instead of Telnet.'''],
        [10, "File transfers", '''If FTP is a requirement, ensure that the server, which supports FTP, is placed
in a different subnet than the internal protected network.'''],
        [11, "ICMP", '''Ensure that there is a rule blocking ICMP echo requests and replies.'''],
        [12, "Egress filtering", '''Ensure that there is a rule specifying that only traffic originating from IP’s
within the internal network be allowed. Traffic with IP’s other than from the
Internal network are to be dropped.
Ensure that any traffic originating from IP’s other than from the internal
network are logged.'''],
        [13, "Firewall redundancy", '''Ensure that there is a hot standby for the primary firewall.''']
    ]
    explanation_table = Table(explanation_data, colWidths=[50, 180, 370])
    explanation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 1), (1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(explanation_table)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Scoring criteria", styles['Heading3']))
    # elements.append(Paragraph("This criteria is a smaller version of SANS firewall checklist. Our team has custom it to fit with the definition and pratical use case of small network. You can check the full version here: https://www.sans.org/media/score/checklists/FirewallChecklist.pdf ", bullet_style))
    scoring_explanation_data = [["Score's definition", "Rating", "Score"],
                                ["20%", "Failure", "1"],
                                ["40%", "Bad", "2"],
                                ["60%", "Fair", "3"],
                                ["80%", "Good", "4"],
                                ["100%", "Very well", "5"],
                                ]
    scoring_explanation_table = Table(scoring_explanation_data, colWidths=[100, 100, 100])
    scoring_explanation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(scoring_explanation_table)
    elements.append(Spacer(1, 20))
    
  
    
    # Xuất PDF
    doc.build(elements)
    print(f"PDF created: {output_filename}")
    
def add_progress_bar(value, max_value=100, width=400, height=20, border_color="#D3D3D3", fill_color="#ADFF2F", border_width=1):
    """
    Create a progress bar with a border and a filled section, allowing custom hex colors.
    :param value: Current progress value.
    :param max_value: Maximum value of the progress bar.
    :param width: Width of the progress bar.
    :param height: Height of the progress bar.
    :param border_color: Hex code or color for the border.
    :param fill_color: Hex code or color for the filled portion.
    :param border_width: Width of the border.
    :return: A Drawing object containing the styled progress bar.
    """
    # Convert hex colors to HexColor objects
    border_color = colors.HexColor(border_color)
    fill_color = colors.HexColor(fill_color)

    # Calculate percentage
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    filled_width = (percentage / 100) * width

    # Create a drawing
    drawing = Drawing(width, height + 10)

    # Background with border
    drawing.add(Rect(0, 0, width, height, fillColor=colors.white, strokeColor=border_color, strokeWidth=border_width))

    # Filled portion
    drawing.add(Rect(0, 0, filled_width, height, fillColor=fill_color, strokeColor=None))

    return drawing

def create_pie_chart_from_criteria(criteria):
    """
    Tạo biểu đồ hình tròn (pie chart) chuyên nghiệp từ dữ liệu tiêu chí đánh giá firewall.
    
    :param criteria: Dictionary chứa tiêu chí và điểm số của mỗi tiêu chí.
    :return: Drawing object chứa biểu đồ hình tròn.
    """
    # Đếm số lượng các tiêu chí theo điểm
    score_counts = {
        "5 (Excellent)": sum(1 for value in criteria.values() if value.get("score") == 5),
        "3-4 (Average)": sum(1 for value in criteria.values() if 3 <= value.get("score", 0) <= 4),
        "1-2 (Needs Improvement)": sum(1 for value in criteria.values() if value.get("score", 0) < 3)
    }

    # Kiểm tra nếu tất cả giá trị đều bằng 0
    if sum(score_counts.values()) == 0:
        print("No valid data for pie chart. Skipping chart creation.")
        return Spacer(1, 20)  # Trả về khoảng trắng nếu không có dữ liệu

    # Tạo biểu đồ hình tròn
    drawing = Drawing(500, 250)
    pie = Pie()
    pie.x = 100
    pie.y = 30
    pie.width = 150
    pie.height = 150
    pie.data = list(score_counts.values())
    pie.labels = list(score_counts.keys())
    pie.slices.strokeWidth = 0.5

    # Tùy chỉnh màu sắc cho từng phần của biểu đồ
    pie.slices[0].fillColor = colors.HexColor("#4A90E2")  # Xanh dương
    pie.slices[1].fillColor = colors.HexColor("#F5A623")  # Cam
    pie.slices[2].fillColor = colors.HexColor("#D0021B")  # Đỏ

    # Thêm ghi chú (legend)
    legend_x = 300
    legend_y = 170
    label_offset = 20

    for i, label in enumerate(pie.labels):
        color = pie.slices[i].fillColor
        drawing.add(String(legend_x, legend_y - (i * label_offset), label, fontSize=12, fillColor=colors.black))
        drawing.add(Line(legend_x - 15, legend_y - (i * label_offset) + 5, legend_x - 5, legend_y - (i * label_offset) + 5, strokeColor=color, strokeWidth=10))

    # Điều chỉnh kiểu của nhãn
    pie.sideLabels = True  # Đặt nhãn ở bên ngoài lát cắt
    pie.simpleLabels = False
    pie.pointerLabelMode = 'LeftRight'  # Nhãn sẽ được đặt ở hai bên để không che lấp nhau
    pie.slices.labelRadius = 1.3  # Tăng khoảng cách giữa nhãn và trung tâm biểu đồ

    drawing.add(pie)
    return drawing