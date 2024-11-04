import os
import json
import utils
PROFILES_DIR = utils.PROFILES_DIR

# def load_profile_names():
#     return [name for name in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, name))]

def load_profile_names():
    # Kiểm tra xem thư mục PROFILES_DIR có tồn tại không
    if not os.path.exists(PROFILES_DIR):
        return ""
    
    # Nếu tồn tại, lấy danh sách thư mục con trong PROFILES_DIR
    return [name for name in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, name))]


def create_profile(profile_name):
    # Kiểm tra nếu profile đã tồn tại
    if profile_name in load_profile_names():
        print(f"Profile '{profile_name}' đã tồn tại. Vui lòng chọn tên khác.")
        return

    # Tạo thư mục và file profile mới
    profile_path = os.path.join(PROFILES_DIR, profile_name)
    os.makedirs(profile_path, exist_ok=True)

    profile_data = {
        "name": profile_name,
        "internal_result": None,
        "external_result": None
    }

    with open(os.path.join(profile_path, "profile.json"), 'w') as f:
        json.dump(profile_data, f)

    print(f"Profile '{profile_name}' đã được tạo.")



def load_profile_data(profile_names_para):
    profile_path = os.path.join(PROFILES_DIR, profile_names_para, "profile.json")
    
    # Kiểm tra nếu file profile.json tồn tại
    if not os.path.isfile(profile_path):
        print(f"Profile '{profile_names_para}' không tồn tại.")
        return None
    
    # Mở và load dữ liệu từ file profile.json
    with open(profile_path, 'r') as f:
        profile_data = json.load(f)
    
    return profile_data