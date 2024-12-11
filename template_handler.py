import os
import pandas as pd
import time

def read_template_to_dict(file_path):
    sheet_name = 'evaluation_detail'
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=2)
    results_dict = {}
    current_time = time.strftime("%d/%m/%Y (%H:%M:%S)")
    results_dict["time_of_evaluation"] = current_time 
    messages = {
        "Review the rulesets order": {
            "cons_message": "Incomplete or improperly ordered rulesets, allowing suspicious traffic.",
            "pros_message": "Rulesets follow best practices: anti-spoofing, permit, deny & log."
        },
        "Stateful inspection": {
            "cons_message": "Long timeouts, no MAC or URL filtering, allowing harmful scripts.",
            "pros_message": "Appropriate timeouts, MAC filtering, URL/script filtering applied."
        },
        "Logging": {
            "cons_message": "Logs disabled or ignored, missing critical attack indicators.",
            "pros_message": "Logs are enabled, monitored, and analyzed for attack patterns."
        },
        "Patches and updates": {
            "cons_message": "Outdated software with unpatched vulnerabilities.",
            "pros_message": "Latest patches tested and applied from trusted sources."
        },
        "Vulnerability assessments/Testing": {
            "cons_message": "Open ports remain untested, leading to potential misconfigurations.",
            "pros_message": "Regular port scans and ruleset validations performed."
        },
        "Compliance with security policy": {
            "cons_message": "Rulesets contradict or fail to enforce security policies.",
            "pros_message": "Rulesets align with organizational security requirements."
        },
        "Block spoofed, private, and illegal IPs": {
            "cons_message": "Spoofed or illegal traffic is not filtered, posing security risks.",
            "pros_message": "RFC 1918 and illegal addresses are blocked and logged."
        },
        "Port restrictions": {
            "cons_message": "Open or unnecessary ports exposed to exploitation.",
            "pros_message": "Unused and critical ports are blocked according to policy."
        },
        "Remote access": {
            "cons_message": "Telnet or other insecure protocols are allowed.",
            "pros_message": "Secure access (e.g., SSH) is enforced for remote connections."
        },
        "File transfers": {
            "cons_message": "FTP is enabled within the internal network without safeguards.",
            "pros_message": "FTP servers are isolated from protected internal networks."
        },
        "ICMP": {
            "cons_message": "ICMP traffic is unrestricted, allowing potential reconnaissance.",
            "pros_message": "Echo requests and other unnecessary ICMP types are blocked."
        },
        "Egress filtering": {
            "cons_message": "Outbound traffic is unrestricted, allowing spoofed traffic to exit.",
            "pros_message": "Only internal IP traffic is allowed to leave the network."
        },
        "Firewall redundancy": {
            "cons_message": "No redundancy, risking firewall downtime during failures.",
            "pros_message": "Hot standby is configured for firewall redundancy."
        },
    }
    current_criteria = None
    for index, row in df.iterrows():
        criteria = row['Unnamed: 0']
        step = row['Unnamed: 1']
        check = row['Unnamed: 2']
        score = row['Unnamed: 3'] if 'Unnamed: 3' in row else None
        if criteria == "Criteria" or step == "Step":
            continue
        if pd.notna(criteria):
            current_criteria = criteria.strip()
            if current_criteria not in results_dict:
                results_dict[current_criteria] = {"steps": {}, "score": 0}
            if pd.notna(score):
                results_dict[current_criteria]["score"] = score
                if current_criteria in messages:
                    if int(score) <= 2:
                        results_dict[current_criteria]["cons_message"] = messages[current_criteria]["cons_message"]
                        
                    elif int(score) >= 3:
                        results_dict[current_criteria]["pros_message"] = messages[current_criteria]["pros_message"]
        if not current_criteria:
            continue
        if pd.notna(step) and pd.notna(check):
            step = step.strip()
            check_value = True if str(check).strip().upper() == 'TRUE' else False
            results_dict[current_criteria]["steps"][step] = check_value
    return results_dict
def check_template_exists(profile_dir, template_name="evaluation_detail_template.xlsx"):
    template_path = os.path.join(profile_dir, template_name)
    return os.path.exists(template_path), template_path
