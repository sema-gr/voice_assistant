import os, platform, subprocess, winreg

def find_in_path(app_name: str):
    try:
        cmd = ["where", app_name] if platform.system() == "Windows" else ["which", app_name]
        result = subprocess.run(cmd, capture_output = True, text = True)
        if result.returncode == 0:
            return result.stdout.splitlines()[0]
    except Exception as error:
        print(error)

def main():
    path = find_in_path("Telegram")
    if path:
        return path