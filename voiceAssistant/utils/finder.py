import os, platform, subprocess, winreg

def find_in_path(app_name):
    try:
        cmd = ["where", app_name] if platform.system() == "Windows" else ["which", app_name]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.splitlines()[0]
    except Exception as error:
        print(error)
    return None

def find_in_registry(app_name):
    if platform.system() != "Windows":
        return None

    try:
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"
        ]

        for reg_path in reg_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                i = 0
                while True:
                    subkey_name = winreg.EnumKey(key, i)
                    if app_name.lower() in subkey_name.lower():
                        subkey = winreg.OpenKey(key, subkey_name)
                        value, _ = winreg.QueryValueEx(subkey, None)
                        return value
                    i += 1
            except:
                pass
    except:
        pass

    return None

def find_in_start_menu(app_name):
    if platform.system() != "Windows":
        return None

    start_paths = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs")
    ]

    for base in start_paths:
        if not os.path.exists(base): continue
        for root, _, files in os.walk(base):
            for file in files:
                if file.lower().startswith(app_name.lower()) and file.endswith(".lnk"):
                    return os.path.join(root, file)
    return None

def find_in_common_dirs(app_name):
    system = platform.system()
    if system == "Windows":
        base_dirs = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
            os.environ.get("LocalAppData", ""),
            os.environ.get("AppData", ""),
        ]

        for base in base_dirs:
            if not base or not os.path.exists(base): continue
            for root, dirs, files in os.walk(base):
                for file in files:
                    if file.lower() == app_name.lower() + ".exe":
                        return os.path.join(root, file)
                
                if root.count(os.sep) - base.count(os.sep) > 3:
                    dirs[:] = [] 
    else:

        base_dirs = [
            "/usr/bin",
            "/usr/local/bin",
            "/Applications",
            "/System/Applications",
            os.path.expanduser("~/Applications"),
        ]

        for base in base_dirs:
            if not os.path.exists(base):
                continue

            for item in os.listdir(base):
                if item.lower().startswith(app_name.lower()):
                    full_path = os.path.join(base, item)

                    if item.endswith(".app"):
                        exe_path = os.path.join(full_path, "Contents", "MacOS")
                        if os.path.exists(exe_path):
                            files = os.listdir(exe_path)
                            if files:
                                return os.path.join(exe_path, files[0])
                        return full_path

                    if os.path.isfile(full_path):
                        return full_path
    return None

def find_app_path(app_name: str):
    app_name_clean = app_name.lower().replace(".exe", "").replace(".app", "")


    path = find_in_path(app_name_clean)
    if path: return path

    path = find_in_registry(app_name_clean)
    if path: return path

    path = find_in_start_menu(app_name_clean)
    if path: return path

    path = find_in_common_dirs(app_name_clean)
    if path: return path

    return None

# test_apps = ["telegram"]

# for app in test_apps:
#     result = find_app_path(app)
#     print(f"{app}: {result}")