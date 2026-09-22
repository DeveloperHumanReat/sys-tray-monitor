import os
import sys
import winreg

APP_NAME = "SysTrayMonitor"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

def is_autostart_enabled() -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Autostart kontrol hatası: {e}")
        return False

def set_autostart(enable: bool) -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
        
        if enable:
            # Derlenmiş .exe olarak mı yoksa .py betiği olarak mı çalışıyor kontrolü
            if getattr(sys, 'frozen', False):
                cmd = f'"{sys.executable}"'
            else:
                python_exe = sys.executable
                if python_exe.endswith("python.exe"):
                    python_exe = python_exe[:-10] + "pythonw.exe"
                main_script = os.path.abspath(sys.argv[0])
                cmd = f'"{python_exe}" "{main_script}"'
            
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass

        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Autostart ayarı değiştirilemedi: {e}")
        return False