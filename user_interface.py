import os
from profile_manager import load_profile_names, create_profile, load_profile_data
from scanner import scan_network
from report_generator import generate_report
import utils
import json

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
            print("  3. Generate Partial Report (Internal)")
        if profile_data.get("external_result") != None:
            print("  4. Generate Partial Report (External)")
        if profile_data.get("internal_result") != None and profile_data.get("external_result") != None:
            print("  5. Generate Full Report")

        # Xử lý lựa chọn hành động của người dùng
        action = input("Chọn hành động: ")

        if action == '1':
            profile_data["internal_result"] = scan_network("internal", profile_name)
            print("Scan internal hoàn tất.")
            # Ghi lại profile_data vào profile.json
            with open(profile_path, 'w') as f:
                json.dump(profile_data, f, indent=4)
                print(f"Kết quả đã được ghi vào file: {profile_path}")

        elif action == '2':
            profile_data["external_result"] = scan_network("external", profile_name)
            print("Scan external hoàn tất.")
            # Ghi lại profile_data vào profile.json
            with open(profile_path, 'w') as f:
                json.dump(profile_data, f, indent=4)
                print(f"Kết quả đã được ghi vào file: {profile_path}")

        elif action == '3':
            
            print("INTERNAL REPORT")
        elif action == '4':
            
            print("EXTERNAL REPORT")
        elif action == '5':
            print("FULL REPORT")
        else:
            print("Lựa chọn không hợp lệ.")
        action = None
        

  



    

def create_profile_menu():
    profile_name = input("Nhập tên profile: ")
    create_profile(profile_name)

def scan_or_report_menu(profile_name, scan_side):

    

    # Thực hiện kiểm tra dữ liệu và quét
    if scan_side == 1:
        scan_side = "Internal"
    if scan_side == 2:
        scan_side = "External"
    scan_side = "error"

    print(f"------{profile_name}----------------------------------SCANNING {scan_side}------------------------------------------") 
    print(f"Đang xử lý profile: {profile_name} ") 
    # (Thêm logic cho việc quét mạng và tạo báo cáo tại đây)
