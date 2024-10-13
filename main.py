import flet as ft
from login import main_login

def main(page: ft.Page):
    main_login(page)

if __name__ == "__main__":
    ft.app(target=main)