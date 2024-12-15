import os
import json
import shutil 
import utils
import platform 
import subprocess  

PROFILES_DIR = utils.PROFILES_DIR
TEMPLATE_FILE = "evaluation_detail_template.xlsx"  
def load_profile_names():
    if not os.path.exists(PROFILES_DIR):
        return ""
    return [name for name in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, name))]

def create_profile(profile_name):
    if profile_name in load_profile_names():
        print(f"Profile '{profile_name}' already exist. please try again and choose different name.")
        return
    profile_path = os.path.join(PROFILES_DIR, profile_name)
    os.makedirs(profile_path, exist_ok= True)
    profile_data = {
        "name": profile_name,
    }
    with open(os.path.join(profile_path, "profile.json"), 'w', encoding='utf8') as f:
        json.dump(profile_data, f)
    template_path = os.path.join(os.getcwd(), TEMPLATE_FILE)
    destination_path = os.path.join(profile_path, TEMPLATE_FILE)
    if os.path.exists(template_path):
        shutil.copy(template_path, destination_path)
        print(f"Template '{TEMPLATE_FILE}' is created in {profile_path}")
        # print(f"Nhấn vào liên kết sau để mở file template: {destination_path}")
        open_file(destination_path)  
    else:
        print(f"checklist template file not found '{TEMPLATE_FILE}'.")

    print(f"Profile '{profile_name}' is created.")


def open_file(file_path):
    """Mở file bằng lệnh tương ứng với hệ điều hành."""
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)  # Windows
        elif platform.system() == "Darwin":
            subprocess.run(["open", file_path])  # MacOS
        else:
            subprocess.run(["xdg-open", file_path])  # Linux
    except Exception as e:
        print(f"Can't open file: {e}")


def load_profile_data(profile_names_para):
    profile_path = os.path.join(PROFILES_DIR, profile_names_para, "profile.json")

    # Kiểm tra nếu file profile.json tồn tại
    if not os.path.isfile(profile_path):
        print(f"Profile '{profile_names_para}' not exist.")
        return None

    # Mở và load dữ liệu từ file profile.json
    with open(profile_path, 'r', encoding='utf8') as f:
        profile_data = json.load(f)

    return profile_data
