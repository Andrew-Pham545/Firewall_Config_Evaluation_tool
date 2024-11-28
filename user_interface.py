import os
from colorama import Fore, init
from profile_manager import load_profile_names, create_profile, load_profile_data
from scanner import scan_network
from report_generator import *
import utils
import json
import ai_evaluation
import manual_criteria
from template_handler import read_template_to_dict, check_template_exists
import scanner
from pprint import pprint


init(autoreset=True)

def main_menu():
    while True:
        print(Fore.CYAN + "\n--- Firewall Evaluation ---")
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
        print(f"{i}. {profile}")
    choice_of_profile = int(input(Fore.WHITE + "Choose profile: ")) - 1
    if 0 <= choice_of_profile < len(profile_names):
        profile_name = profile_names[choice_of_profile]
        profile_data = load_profile_data(profile_name)
        profile_path = os.path.join(utils.PROFILES_DIR, profile_name, "profile.json")
        profile_dir = os.path.join(utils.PROFILES_DIR, profile_name)
        
        print(Fore.CYAN + f"\n======================= {profile_data['name']} =======================")
        print(Fore.YELLOW + "- EVALUATION:")
        print('  1. Begin to Evaluate (Auto + Manual)')
        print('  2. port and icmp scanner (for evaluation purpose)')
        print('  3. Read data from template')  # Tuỳ chọn mới
        print(Fore.YELLOW + "- REPORT")
        print(f'  4. Generate {Fore.GREEN + "Full Report"}')
        action = input("Choose action: ")
        
        if action == '1':
            profile_data["evaluation_result"] = manual_criteria.firewall_checklist()
            with open(profile_path, 'w', encoding='utf8') as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"Result is written into: {profile_path}")
            
        elif action == '2':
            target = input(f'\n{Fore.YELLOW + "Enter the firewall external IP:"} {Fore.RESET}')
            profile_data["scan_result"] = scanner.port_restriction_and_icmp_restriction_scan(target)
            with open(profile_path, 'w', encoding='utf8') as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"Result is written into: {profile_path}")
        
        elif action == '3':  # Đọc từ file template
            template_exists, template_path = check_template_exists(profile_dir)
            if template_exists:
                profile_data["evaluation_result"] = read_template_to_dict(template_path)
                
                with open(profile_path, 'w', encoding='utf8') as f:
                    json.dump(profile_data, f, indent=4, ensure_ascii=False)
                print(Fore.GREEN + f"Data read from template and saved to: {profile_path}")
            else:
                print(Fore.RED + "Template file not found in the profile directory.")
        
        elif action == '4':
            print(Fore.YELLOW + "\nDo you want to include AI evaluation?")
            print("1. Yes, include AI evaluation.")
            print("2. No, only manual evaluation.")

            ai_choice = input(Fore.WHITE + "Choose an option (1 or 2): ")
            
            if ai_choice == '1':
                # Thực hiện AI evaluation và cập nhật dữ liệu vào profile
                print(Fore.CYAN + "Running AI evaluation...")
                ai_evaluation_result = ai_evaluation.evaluate_scan_result(profile_data)
                
                create_firewall_report(profile_data, profile_name, ai_message=ai_evaluation_result)
                print(Fore.GREEN + "AI evaluation included in the report.")

            elif ai_choice == '2':
                print(Fore.CYAN + "Generating report with only manual evaluation results.")
                create_firewall_report(profile_data, profile_name)

            # Gọi hàm tạo báo cáo
            

        
        
        
def create_profile_menu():
    profile_name = input(f'{Fore.GREEN + 'Enter new profile name:'} {Fore.RESET}')
    create_profile(profile_name)
