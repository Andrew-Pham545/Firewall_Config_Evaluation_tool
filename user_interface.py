import os
from profile_manager import load_profiles, create_profile
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
    profiles = load_profiles()
    if not profiles:
        print("Không có profile nào. Hãy tạo một profile mới.")
        return

    print("\n--- Chọn Profile ---")
    for i, profile in enumerate(profiles):
        print(f"{i + 1}. {profile}")
    choice = int(input("Chọn profile: ")) - 1

    if 0 <= choice < len(profiles):
        profile_name = profiles[choice]
        scan_or_report_menu(profile_name)
    else:
        print("Lựa chọn không hợp lệ.")

def create_profile_menu():
    profile_name = input("Nhập tên profile: ")
    create_profile(profile_name)

def scan_or_report_menu(profile_name):
    # Thực hiện kiểm tra dữ liệu và quét
    print(f"Đang xử lý profile: {profile_name}")
    # (Thêm logic cho việc quét mạng và tạo báo cáo tại đây)
