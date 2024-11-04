import os
import json

PROFILES_DIR = "profiles/"

def load_profile_names():
    return [name for name in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, name))]

def create_profile(profile_name):
    profile_path = os.path.join(PROFILES_DIR, profile_name)
    os.makedirs(profile_path, exist_ok=True)

    profile_data = {
        "name": profile_name,
        "internal_results": None,
        "external_results": None
    }

    with open(os.path.join(profile_path, "profile.json"), 'w') as f:
        json.dump(profile_data, f)
    
    print(f"Profile '{profile_name}' đã được tạo.")
