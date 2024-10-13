import os
import sys
import ctypes
import flet as ft
from login import main_login

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main(page: ft.Page):
    path = r"C:\Program Files\TASKs"
    path_file = os.path.join(path, "state.txt")

    if not os.path.exists(path):
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
        else:
            os.makedirs(path, exist_ok=True)

    if not os.path.exists(path_file):
        with open(path_file, 'w') as archivo:
            archivo.write("")

    main_login(page)

if __name__ == "__main__":
    if is_admin() or os.path.exists(r"C:\Program Files\TASKs"):
        ft.app(target=main)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
