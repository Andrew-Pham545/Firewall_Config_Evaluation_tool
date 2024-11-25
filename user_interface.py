import os
from colorama import Fore, init
from profile_manager import load_profile_names, create_profile, load_profile_data
from scanner import scan_network
from report_generator import *
import utils
import json
import ai_evaluation
import manual_criteria
# Initialize colorama
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
        print( f"{i}. {profile}")
    choice_of_profile = int(input(Fore.WHITE + "Choose profile: ")) - 1

    if 0 <= choice_of_profile < len(profile_names):
        profile_name = profile_names[choice_of_profile]
        profile_data = load_profile_data(profile_name)
        profile_path = os.path.join(utils.PROFILES_DIR, profile_name, "profile.json")
        # Hiển thị menu của profile
        print(Fore.CYAN + f"\n======================= {profile_data['name']} =======================")
        # print("Choose action:")
        print(Fore.YELLOW + "- EVALUATION:")
        
        # # Kiểm tra nếu đã có kết quả scan nội bộ
        # if profile_data.get("internal_result"):
        #     print(f'  1. Scan internal {Fore.GREEN + '(already scan)'}')
        # else:
        #     print("  1. Scan internal")
        
        # print( "  1. Criteria 5 + 7 + 11" + Fore.GREEN + ' (already scan)')
        # print( "  2. Criteria 1 ")
        # print( "  3. Criteria 2")
        # print( "  4. Criteria 3")
        # print( "  5. Criteria 4")
        # print( "  6. Criteria 6")
        # print( "  7. Criteria 8")
        # print( "  8. Criteria 9")
        # print( "  9. Criteria 10")
        # print( "  10. Criteria 12")
        # print( "  11. Criteria 13")
        # print( "  11. Criteria 13")
        
        print('  1. Begin to Eveluate (Auto + Manual)')
        print('  2. Eveluate a single criteria')
        
        
        
        
        
        # Hiển thị các tùy chọn báo cáo
        print(Fore.YELLOW + "- REPORT")
        print(f'  3. Generate {Fore.GREEN + 'Full Report'}')

        # if profile_data.get("internal_result") != None and profile_data.get("external_result") != None:
        #     print(f'  5. Generate {Fore.GREEN + 'Full Report'}')

        # Xử lý lựa chọn hành động của người dùng
        action = input("Choose action: ")

        if action == '1':
            profile_data = manual_criteria.firewall_checklist()
            target = input(f'\n{Fore.YELLOW + 'Enter the firewall external IP:'} {Fore.RESET} ')
            profile_data += scan_network(target, "external")
            profile_data["external_result"] = scan_network(target, "external")
            
            # print(Fore.CYAN + "\n======================= FINISH EXTERNAL SCAN ========================")
            
            # Ghi lại profile_data vào profile.json
            with open(profile_path, 'w', encoding='utf8') as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"Result is written into: {profile_path}")
            
        elif action == '2':
            #Eveluate a single criteria   
            print('do the firewall .... (ghi lý thuyết vào)')
            profile_data["criteria_1"] = input('do the firewall 1 ')  
            
            with open(profile_path, 'w', encoding='utf8') as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"Result is written into: {profile_path}")
         
        elif action == '3':
            print('criteria 2')   
            
            print('do the firewall .... (ghi lý thuyết vào)')
            profile_data["criteria_2"] = input('do the firewall ')  
            
            with open(profile_path, 'w', encoding='utf8') as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"Result is written into: {profile_path}")
        action = None


            
def create_profile_menu():
    profile_name = input(f'{Fore.GREEN + 'Enter new profile name:'} {Fore.RESET}')
    create_profile(profile_name)
