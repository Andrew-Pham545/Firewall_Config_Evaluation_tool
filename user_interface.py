import os
from profile_manager import load_profile_names, create_profile, load_profile_data
from scanner import scan_network
from report_generator import *
import utils
import json
import ai_evaluation

def main_menu():
    while True:
        print("\n--- Network Scanner Tool ---")
        print("1. Chọn Profile")
        print("2. Tạo Profile Mới")
        print("3. Thoát")

        choice = input("Chọn một tùy chọn: ")

        if choice == '1':
            select_profile()
        elif choice == '2':
            create_profile_menu()
        elif choice == '3':
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

def select_profile():
    profile_names = load_profile_names()
    if not profile_names:
        print("Không có profile nào. Hãy tạo một profile mới.")
        return

    print("\n--- Chọn Profile ---")
    for i, profile in enumerate(profile_names, start=1):
        print(f"{i}. {profile}")
    choice_of_profile = int(input("Chọn profile: ")) - 1

    if 0 <= choice_of_profile < len(profile_names):
        profile_name = profile_names[choice_of_profile]
        profile_data = load_profile_data(profile_name)
        profile_path = os.path.join(utils.PROFILES_DIR, profile_name, "profile.json")
        # Hiển thị menu của profile
        print(f"\n============ {profile_data['name']} =============")
        print("Chọn hành động:")
        print("- SCAN:")
        
        # Kiểm tra nếu đã có kết quả scan nội bộ
        if profile_data.get("internal_result"):
            print("  1. Scan internal (đã có)")
        else:
            print("  1. Scan internal")
        
        # Kiểm tra nếu đã có kết quả scan bên ngoài
        if profile_data.get("external_result"):
            print("  2. Scan external (đã có)")
        else:
            print("  2. Scan external")
        
        # Hiển thị các tùy chọn báo cáo
        print("- REPORT")
        if profile_data.get("internal_result") != None:
            print(f"  3. Generate Partial Report (Internal)")
        if profile_data.get("external_result") != None:
            print("  4. Generate Partial Report (External)")
        if profile_data.get("internal_result") != None and profile_data.get("external_result") != None:
            print("  5. Generate Full Report")

        # Xử lý lựa chọn hành động của người dùng
        action = input("Chọn hành động: ")

        if action == '1':
            default_ip_internal = '10.10.10.15'
            target = input("enter internal IP (default is 10.10.10.15): ") or  default_ip_internal
    
            profile_data["internal_result"] = scan_network(target,"internal")
            print("\nScan internal hoàn tất.")
            
            # # In kết quả quét ra terminal
            # print("Kết quả quét internal:")
            # print(json.dumps(profile_data["internal_result"], indent=4))
            
            # Ghi lại profile_data vào profile.json
            with open(profile_path, 'w') as f:
                json.dump(profile_data, f, indent=4)
            print(f"Kết quả đã được ghi vào file: {profile_path}")

        elif action == '2':
            default_ip_external = '192.168.1.17'
            target = input("enter External IP (default is 192.168.1.17): ") or default_ip_external
            profile_data["external_result"] = scan_network(target, "external")
            print("\n=======================FINISH EXTERNAL SCAN=======================")
            
            # In kết quả quét ra terminal
            print("Kết quả quét external:")
            print(json.dumps(profile_data["external_result"], indent=4))
            
            # Ghi lại profile_data vào profile.json
            with open(profile_path, 'w') as f:
                json.dump(profile_data, f, indent=4)
            print(f"Kết quả đã được ghi vào file: {profile_path}")


        elif action == '3':
            print("Báo cáo Scan Nội Bộ:")

            ai_evaluation_message = ai_evaluation.evaluate_scan_result(profile_data)
            report = generate_report(profile_data, 3, ai_message= ai_evaluation_message)
            print(report)
            save_report_to_pdf(report, profile_data.get('name', 'profile'))
            
        elif action == '4':
            print("Báo cáo Scan Ngoài:")

            ai_evaluation_message = ai_evaluation.evaluate_scan_result(profile_data)
            report = generate_report(profile_data, 4, ai_message= ai_evaluation_message)
            print(report)
            save_report_to_pdf(report, profile_data.get('name', 'profile')) 

        elif action == '5':
            print("Báo cáo Toàn Bộ:")
            
            ai_evaluation_message = ai_evaluation.evaluate_scan_result(profile_data)
            report = generate_report(profile_data, 5, ai_message= ai_evaluation_message)
            print(report)
            save_report_to_pdf(report, profile_data.get('name', 'profile'))

        action = None
        

  


def create_profile_menu():
    profile_name = input("Nhập tên profile: ")
    create_profile(profile_name)

