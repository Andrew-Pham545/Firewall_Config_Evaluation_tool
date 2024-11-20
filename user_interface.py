import os
from colorama import Fore, init
from profile_manager import load_profile_names, create_profile, load_profile_data
from scanner import scan_network
from report_generator import *
import utils
import json
import ai_evaluation

# Initialize colorama
init(autoreset=True)

def main_menu():
    while True:
        print(Fore.CYAN + "\n--- Network Scanner Tool ---")
        print(Fore.GREEN + "1. Choose Profile")
        print(Fore.GREEN + "2. Create new Profile")
        print(Fore.RED + "3. Exit tool")

        choice = input(Fore.WHITE + "Choose an option: ")

        match choice:
            case '1':
                select_profile()
            case '2':
                create_profile_menu()
            case '3':
                print(Fore.RED)
                break
            case _:
                print(Fore.RED + 'Invalid choice. Please try again.')
                
def select_profile():
    profile_names = load_profile_names()
    if not profile_names:
        print(Fore.RED + "No profiles found. Please create a new profile.")
        return

    print(Fore.CYAN + "\n--- Select Profile ---")
    for i, profile in enumerate(profile_names, start=1):
        print( f"{i}. {profile}")
    choice_of_profile = int(input(Fore.WHITE + "Choose profile: ")) - 1

    if 0 <= choice_of_profile < len(profile_names):
        profile_name = profile_names[choice_of_profile]
        profile_data = load_profile_data(profile_name)
        profile_path = os.path.join(utils.PROFILES_DIR, profile_name, "profile.json")
        # Hiển thị menu của profile
        print(Fore.CYAN + f"\n======================= {profile_data['name']} =======================")
        # print("Choose action:")
        print(Fore.YELLOW + "- SCAN:")
        
        # Kiểm tra nếu đã có kết quả scan nội bộ
        if profile_data.get("internal_result"):
            print(f'  1. Scan internal {Fore.GREEN + '(already scan)'}')
        else:
            print("  1. Scan internal")
        
        # Kiểm tra nếu đã có kết quả scan bên ngoài
        if profile_data.get("external_result"):
            print(f'  2. Scan external {Fore.GREEN + '(already scan)'}')
        else:
            print( "  2. Scan external")
        
        # Hiển thị các tùy chọn báo cáo
        print(Fore.YELLOW + "- REPORT")
        if profile_data.get("internal_result") != None:
            print("  3. Generate Partial Report (Internal)")
        if profile_data.get("external_result") != None:
            print("  4. Generate Partial Report (External)")
        if profile_data.get("internal_result") != None and profile_data.get("external_result") != None:
            print(f'  5. Generate {Fore.GREEN + 'Full Report'}')

        # Xử lý lựa chọn hành động của người dùng
        action = input("Choose action: ")

        if action == '1':
            default_ip_internal = '10.10.10.15'
            target = input(f'\n{Fore.YELLOW + 'Enter internal IP (default is 10.10.10.15):'}{Fore.RESET} ') or default_ip_internal
    
            profile_data["internal_result"] = scan_network(target, "internal")
            print(Fore.CYAN + "\n======================= FINISH INTERNAL SCAN ========================")
            
            # Ghi lại profile_data vào profile.json
            with open(profile_path, 'w', encoding='utf8') as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"Result is written into: {profile_path}")

        elif action == '2':
            default_ip_external = '192.168.1.17'
            target = input(f'\n{Fore.YELLOW + 'Enter external IP (default is 192.168.1.17):'}{Fore.RESET} ') or default_ip_external
            profile_data["external_result"] = scan_network(target, "external")
            print(Fore.CYAN + "\n======================= FINISH EXTERNAL SCAN ========================")
            
            # Ghi lại profile_data vào profile.json
            with open(profile_path, 'w', encoding='utf8') as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"Result is written into: {profile_path}")

        elif action == '3':

            ai_evaluation_message = ai_evaluation.evaluate_scan_result(profile_data["internal_result"])
            report = generate_report(profile_data, 3, ai_message=ai_evaluation_message)
            # print(Fore.GREEN + report)
            save_report_to_pdf(report, profile_data.get('name', 'profile'))
            print(Fore.CYAN + "======================= Internal scan report is generated =======================")
            
        elif action == '4':
            

            ai_evaluation_message = ai_evaluation.evaluate_scan_result(profile_data["external_result"])
            report = generate_report(profile_data, 4, ai_message=ai_evaluation_message)
            # print(Fore.GREEN + report)
            save_report_to_pdf(report, profile_data.get('name', 'profile')) 
            print(Fore.CYAN + "======================= External scan report is generated =======================")
        elif action == '5':
            
            
            ai_evaluation_message = ai_evaluation.evaluate_scan_result(profile_data)
            report = generate_report(profile_data, 5, ai_message=ai_evaluation_message)
            # print(Fore.GREEN + report)
            save_report_to_pdf(report, profile_data.get('name', 'profile'))
            print(Fore.CYAN + "======================= Full scan report is generated =======================")
        action = None

def create_profile_menu():
    profile_name = input(f'{Fore.GREEN + 'Enter new profile name:'} {Fore.RESET}')
    create_profile(profile_name)
