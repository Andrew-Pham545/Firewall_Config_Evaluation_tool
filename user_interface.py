import os
from profile_manager import load_profile_names, create_profile
from scanner import scan_network
from report_generator import generate_report

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
    profiles = load_profile_names()
    if not profiles:
        print("Không có profile nào. Hãy tạo một profile mới.")
        return

    print("\n--- Chọn Profile ---")
    for i, profile in enumerate(profiles, start=1):
        print(f"{i}. {profile}")
    choiceOfProfile = int(input("Chọn profile: ")) - 1

    print("\n--- Chọn Phía Scan ---")
    print("1. External side")
    print("2. Internal side")
    choiceOfScanSide = int(input("Chọn Phía Scan: ")) 

    if choiceOfScanSide != 1 or choiceOfScanSide != 2:
        print("lựa chọn không hợp lệ")


    if 0 <= choiceOfProfile < len(profiles):
        profile_name = profiles[choiceOfProfile]
        scan_or_report_menu(profile_name)
    else:
        print("Lựa chọn không hợp lệ.")

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
