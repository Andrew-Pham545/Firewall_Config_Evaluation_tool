from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.piecharts import Pie
import utils
import os


def create_firewall_report(data_dict, profile_name, output_filename="firewall_report.pdf", ai_message=''):
    profile_dir = os.path.join(utils.PROFILES_DIR, profile_name)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir, exist_ok=True)
    output_filepath = os.path.join(profile_dir, output_filename)
    name = data_dict.get("name", "N/A")
    evaluation_result = data_dict.get("evaluation_result", {})
    time_of_evaluation = evaluation_result.get("time_of_evaluation", "N/A")
    scanner_result = data_dict.get("scan_result", {})
    
    criteria = {k: v for k, v in evaluation_result.items() if k != "time_of_evaluation"}
    total_score = sum(int(item["score"]) for item in criteria.values())
    
    max_score = len(criteria) * 5 
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
    doc = SimpleDocTemplate(output_filepath, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="CustomTitle",
        fontName="Helvetica-Bold",
        fontSize=65, 
        leading=70,  
        alignment=0, 
        # textColor=colors.darkblue,
        textColor="#03045e",
    )
    subtitle_style = ParagraphStyle(
        name="CustomSubtitle",
        fontName="Helvetica",
        fontSize=18, 
        leading=24,
        alignment=0, 
        textColor=colors.black,
    )
    date_style = ParagraphStyle(
        name="CustomDate",
        fontName="Helvetica-Oblique",
        fontSize=14,
        leading=20,
        alignment=0,
        textColor=colors.grey,
    )    
    main_point_style = ParagraphStyle(
        name="CustomMainPoint",
        fontName="Helvetica-Bold",
        fontSize=30,
        leading=20,
        alignment=0,
        textColor=colors.black,
    )    
    cover_title_1 = Paragraph("Firewall", title_style)
    cover_title_2 = Paragraph("Configuration", title_style)
    cover_title_3 = Paragraph("Assessment", title_style)
    cover_title_4 = Paragraph("Report", title_style)
    cover_subtitle = Paragraph(f"{name}", subtitle_style)
    cover_date = Paragraph(f"Date of Assessment: {time_of_evaluation}", date_style)
    elements.append(Spacer(1, 100))  
    elements.append(cover_title_1)
    elements.append(cover_title_2)
    elements.append(cover_title_3)
    elements.append(cover_title_4)
    elements.append(Spacer(1, 20))
    elements.append(cover_subtitle)
    elements.append(Spacer(1, 7))
    elements.append(cover_date)
    elements.append(PageBreak()) 
    elements.append(Paragraph("1. Report Summary", main_point_style))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Overall Score: {total_score}/{max_score} ({(total_score/max_score)*100:.2f}%)", styles['Heading3']))
    progress_bar = add_progress_bar(
    value=total_score,
    max_value=max_score,
    width=400,
    height=20,
    border_color="#4A90E2",  
    fill_color="#50E3C2"    
    )
    elements.append(progress_bar)
    elements.append(Spacer(1, 30))
    pros_cons_style = ParagraphStyle(
        name="CustomProsCons",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=20,
        alignment=0,
        textColor=colors.black,
        leftIndent=10
    )    
    bullet_style = ParagraphStyle(
        name="BulletPoints",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        leftIndent=20,
        bulletIndent=10, 
        bulletFontName="Helvetica-Bold",
        textColor=colors.black,
    )
    action_plan_small_text = ParagraphStyle(
    name="ActionPlanSmallText",
    fontName="Helvetica",
    fontSize=12,
    leading=16,
    leftIndent=30,
    bulletIndent=10, 
    bulletFontName="Helvetica-Bold",
    textColor=colors.black,
)
    pros_list = [v["pros_message"] for v in criteria.values() if "pros_message" in v]
    cons_list = [v["cons_message"] for v in criteria.values() if "cons_message" in v]
    if pros_list != []:
        elements.append(Paragraph("Pros:", pros_cons_style))
    elements.append(Spacer(1, 15))  
    for item in pros_list:
        elements.append(Paragraph(f"• {item}", bullet_style))
        elements.append(Spacer(1, 7)) 
    elements.append(Spacer(1, 20)) 
    if cons_list != []:
        elements.append(Paragraph("Cons:", pros_cons_style))
    elements.append(Spacer(1, 15))  
    for item in cons_list:
        elements.append(Paragraph(f"• {item}", bullet_style))
        elements.append(Spacer(1, 7)) 
    elements.append(Spacer(1, 20)) 
    elements.append(Spacer(1, 20))
    

    
    elements.append(PageBreak())  
    wrapping_style = ParagraphStyle(
        name="WrappingStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=12,  # Khoảng cách dòng
        wordWrap='LTR',  # Tự động xuống dòng
    )

    # Tạo bảng dữ liệu với wrapping cho cột Criteria Detail
    criteria_data = [["Crit No.", "Criteria Detail", "Score", "Passed Steps/Total Steps"]]
    for idx, (key, value) in enumerate(criteria.items(), start=1):
        criteria_name = criteria_mapping.get(key, key)  
        score = value.get("score", "N/A")  
        passed_steps = sum(1 for step, passed in value['steps'].items() if passed)
        total_steps = len(value['steps'])
        passed_steps_info = f"{passed_steps} / {total_steps}"
        
        # Sử dụng Paragraph cho Criteria Detail
        wrapped_criteria_name = Paragraph(criteria_name, wrapping_style)
        criteria_data.append([idx, wrapped_criteria_name, score, passed_steps_info])

    # Tạo bảng với độ rộng cột cố định
    criteria_table = Table(criteria_data, colWidths=[70, 200, 50, 150])

    # Áp dụng style cho bảng
    criteria_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), "#2F3C7E"),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Align Crit No.
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Align Score
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Align Passed Steps
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Vertical alignment
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add grid lines
    ]))

    # Thêm bảng vào elements
    elements.append(Paragraph("2. Evaluation Details", main_point_style))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('Score detail', styles['Heading1']))
    elements.append(criteria_table)

    elements.append(Spacer(1, 20))
    pie_chart = create_pie_chart_from_criteria(criteria)
    elements.append(pie_chart)
    failed_steps_data = [["Crit No.", "Criteria Detail", "Failed Step"]]
    for idx, (criterion_key, criterion_value) in enumerate(criteria.items(), start=1):
        criteria_name = criteria_mapping.get(criterion_key, criterion_key)
        for step_description, step_passed in criterion_value['steps'].items():
            if not step_passed: 
                failed_steps_data.append([
                    idx,
                    Paragraph(criteria_name, styles["Normal"]),
                    Paragraph(step_description, styles["Normal"])
                ])
    if len(failed_steps_data) > 1:
        elements.append(PageBreak())
        elements.append(Paragraph('Failed steps', styles['Heading1']))
        failed_steps_table = Table(failed_steps_data, colWidths=[70, 200, 300])
        failed_steps_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.red),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), "#D9D9D9"),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(failed_steps_table)
        elements.append(Spacer(1, 20))
    normal_style = ParagraphStyle(
    name="normalStyle",
    fontName="Helvetica",
    fontSize=12,
    leading=16,
    leftIndent=35,
    bulletIndent=10,
    bulletFontName="Helvetica-Bold",
    textColor=colors.black,
    )
    if len(scanner_result) > 0:  
        elements.append(Paragraph("Scan Result", styles['Heading1']))
        target = scanner_result.get("target", "N/A")
        elements.append(Paragraph(f"• The IP of external side: {target}", bullet_style))
        elements.append(Spacer(1, 10))
        protocols = scanner_result.get("protocols", {})
        for protocol, ports in protocols.items():
            elements.append(Paragraph(f"• {protocol.upper()}:", bullet_style))
            for port_info in ports:
                port = port_info.get("port", "N/A")
                if port != 'N/A':
                    elements.append(Paragraph(f"+  Port {port} (open)", normal_style))
            elements.append(Spacer(1, 10))
        icmp_state = scanner_result.get("icmp", "N/A")
        elements.append(Paragraph(f"• The ICMP rule on the external side of the firewall is: {icmp_state}", bullet_style))
        elements.append(Spacer(1, 20))
    elements.append(Paragraph("3. Recommendations", main_point_style))
    elements.append(Spacer(1, 30))
    recommendations = []
    failed_step_count = len(failed_steps_data) - 1
    if failed_step_count  > 10:
        recommendations.append(f"There are {failed_step_count} steps that have not passed. The administrator should review these steps and make necessary adjustments to ensure they align with the network's requirements.")
    if recommendations:
        elements.append(Spacer(1, 15))
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", bullet_style))
    else:
        elements.append(Paragraph("Most criteria are chekced. Your firewall configuration can consider to be safe", bullet_style))
    elements.append(Spacer(1, 20))
    action_plan = []
    if "Logging" in evaluation_result and evaluation_result["Logging"]["score"] == 0:
        action_plan.append("• Enable logging immediately and configure periodic log reviews.")
    if "Remote access" in evaluation_result and evaluation_result["Remote access"]["score"] == 0:
        action_plan.append("• Replace insecure remote access protocols (e.g., Telnet) with secure options like SSH.")
    if "Patches and updates" in evaluation_result and evaluation_result["Patches and updates"]["score"] == 0:
        action_plan.append("• Apply the latest firewall patches and ensure reliable download sources.")
    if "Block spoofed, private, and illegal IPs" in evaluation_result:
        failed_steps = [step for step, passed in evaluation_result["Block spoofed, private, and illegal IPs"]["steps"].items() if not passed]
        if failed_steps:
            action_plan.append("• Review and block the following illegal or spoofed IP addresses:")
            for step in failed_steps:
                action_plan.append(f"+{step}")
                
    tcp_open_ports = [p["port"] for p in scanner_result["protocols"]["tcp"] if p["state"] == "open"]
    udp_open_ports = [p["port"] for p in scanner_result["protocols"]["udp"] if p["state"] == "open"]
    if tcp_open_ports or udp_open_ports:
        action_plan.append("• Review and secure the following open ports:")
        if tcp_open_ports:
            action_plan.append(f"+TCP: {', '.join(map(str, tcp_open_ports))}")
        if udp_open_ports:
            action_plan.append(f"+UDP: {', '.join(map(str, udp_open_ports))}")
    if scanner_result.get("icmp") == "open":
        action_plan.append("• Block unnecessary ICMP traffic to reduce the risk of reconnaissance attacks.")
    if "• Review the rulesets order (in the following order)" in evaluation_result:
        failed_steps = [step for step, passed in evaluation_result["Review the rulesets order (in the following order)"]["steps"].items() if not passed]
        if failed_steps:
            action_plan.append("• Optimize firewall ruleset order to minimize conflicts and improve performance:")
            for step in failed_steps:
                action_plan.append(f"+{step}")
    if "Vulnerability assessments/Testing" in evaluation_result:
        failed_steps = [step for step, passed in evaluation_result["Vulnerability assessments/Testing"]["steps"].items() if not passed]
        if failed_steps:
            action_plan.append("• Perform regular vulnerability assessments using tools like nmap to identify open ports and vulnerabilities:")
            for step in failed_steps:
                action_plan.append(f"+{step}")
    if "completed_at" in scanner_result:
        action_plan.append(f"• Ensure periodic scans like the one completed on {scanner_result['completed_at']}.")
    elements.append(Paragraph("Action Plan:", styles["Heading1"]))
    elements.append(Spacer(1, 10))
    for action in action_plan:
        if "+" in action:
            
            elements.append(Paragraph(f"{action}", action_plan_small_text)) 
            elements.append(Spacer(1, 3))
        else:
            elements.append(Paragraph(f"{action}", bullet_style))
            elements.append(Spacer(1, 3))
    if ai_message != '':
        bullet_points = [f"• {point.strip()}" for point in ai_message.split("•") if point.strip()]
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("AI Evaluation:", styles["Heading1"]))
        elements.append(Spacer(1, 10))
        for point in bullet_points:
            elements.append(Paragraph(point, bullet_style))
            elements.append(Spacer(1, 10))
    # elements.append(Spacer(1, 20))
    elements.append(PageBreak())
    elements.append(Paragraph("4. APPENDIX", main_point_style))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("The criterias", styles['Heading1']))
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
    explanation_table = Table(explanation_data, colWidths=[30, 180, 360])
    explanation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), "#205F3B"),
        # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        # ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('BACKGROUND', (0, 1), (-1, -1), "#EDF4F2"),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 1), (1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(Spacer(1, 20))
    elements.append(explanation_table)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Scoring criteria", styles['Heading1']))
    scoring_explanation_data = [["Score's definition", "Rating", "Score"],
                                ["20%", "Failure", "1"],
                                ["40%", "Bad", "2"],
                                ["60%", "Fair", "3"],
                                ["80%", "Good", "4"],
                                ["100%", "Very well", "5"],
                                ]
    scoring_explanation_table = Table(scoring_explanation_data, colWidths=[100, 100, 100])
    scoring_explanation_table.setStyle(TableStyle([
        # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), "#205F3B"),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        # ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('BACKGROUND', (0, 1), (-1, -1), "#EDF4F2"),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(Spacer(1, 20))
    elements.append(scoring_explanation_table)
    elements.append(Spacer(1, 20))
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
    border_color = colors.HexColor(border_color)
    fill_color = colors.HexColor(fill_color)
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    filled_width = (percentage / 100) * width
    drawing = Drawing(width, height + 10)
    drawing.add(Rect(0, 0, width, height, fillColor=colors.white, strokeColor=border_color, strokeWidth=border_width))
    drawing.add(Rect(0, 0, filled_width, height, fillColor=fill_color, strokeColor=None))
    return drawing


def create_pie_chart_from_criteria(criteria):
    """
    Tạo biểu đồ hình tròn (pie chart) chuyên nghiệp từ dữ liệu tiêu chí đánh giá firewall.

    :param criteria: Dictionary chứa tiêu chí và điểm số của mỗi tiêu chí.
    :return: Drawing object chứa biểu đồ hình tròn.
    """
    score_counts = {
        "5 (Excellent)": sum(1 for value in criteria.values() if value.get("score") == 5),
        "3-4 (Average)": sum(1 for value in criteria.values() if 3 <= value.get("score", 0) <= 4),
        "1-2 (Needs Improvement)": sum(1 for value in criteria.values() if value.get("score", 0) < 3)
    }
    total_scores = sum(score_counts.values())
    if total_scores == 0:
        print("No valid data for pie chart. Skipping chart creation.")
        return Spacer(1, 20)
    percentages = [(count / total_scores) * 100 for count in score_counts.values()]
    labels_with_percent = [
        f"{label} ({percentage:.1f}%)"
        for label, percentage in zip(score_counts.keys(), percentages)
    ]
    drawing = Drawing(500, 250)
    pie = Pie()
    pie.x = 100
    pie.y = 30
    pie.width = 150
    pie.height = 150
    pie.data = list(score_counts.values())
    pie.labels = labels_with_percent
    pie.slices.strokeWidth = 0.5
    pie.slices[0].fillColor = colors.HexColor("#4A90E2")  # Xanh dương
    pie.slices[1].fillColor = colors.HexColor("#F5A623")  # Cam
    pie.slices[2].fillColor = colors.HexColor("#D0021B")  # Đỏ
    # legend_x = 300
    # legend_y = 170
    # label_offset = 20
    # for i, label in enumerate(labels_with_percent):
    #     color = pie.slices[i].fillColor
    #     drawing.add(String(legend_x, legend_y - (i * label_offset), label, fontSize=12, fillColor=colors.black))
    #     drawing.add(Line(legend_x - 15, legend_y - (i * label_offset) + 5, legend_x - 5, legend_y - (i * label_offset) + 5, strokeColor=color, strokeWidth=10))
    pie.sideLabels = True  
    pie.simpleLabels = False
    pie.pointerLabelMode = 'LeftRight'
    pie.slices.labelRadius = 1.3 
    drawing.add(pie)
    return drawing