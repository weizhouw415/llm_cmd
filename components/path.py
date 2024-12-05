import winreg as reg

def find_install_path(registry_path: str) -> str:
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, registry_path) as key:
            install_path, _ = reg.QueryValueEx(key, "InstallPath")
            # executable_name, _ = reg.QueryValueEx(key, "ExecutableName")
            return install_path
    except FileNotFoundError:
        return "The specified software is not installed or the registry key is missing."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    registry_path = r"Software\Tencent\WeChat"
    install_path = find_install_path(registry_path)
    print(f"Installation path: {install_path}")