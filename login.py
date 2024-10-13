import flet as ft
from dataController import SecionController
from sigin import main_sigin
from main_page import main_main

def main_login(page: ft.Page):
    
    page.title = "TASK! - Login"
    page.scroll = "auto"
    page.padding = 10

    controller = SecionController()

    def pre_login():
        controller.pre_login_db()
    def login(e):
        res = controller.login_db(user_input.value,pass_input.value)
        if res[0] == "OK":
            go_to_main(e,res[1])
    
    def go_to_sigin(e):
        page.clean()
        main_sigin(page)

    def go_to_main(e,name):
        page.clean()
        main_main(page,name,user_input.value)

    #-----------------------------------------------------

    title = ft.Text(
        value="TASKs!",
        size=50,        
    )
    
    user_input = ft.TextField(
        label="Usuario",   
        text_size=30        
    )
    
    pass_input = ft.TextField(
        label="Contraseña",        
        text_size=30,
        password=True
    )
    
    log_button = ft.ElevatedButton(
        text="Iniciar sesión",  
        width=300,
        height=75,    
        on_click=login,  
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=30),            
        )
    ) 
    
    sig_button = ft.ElevatedButton(
        text="Registrarte",
        width=200,
        height=75,
        on_click=go_to_sigin,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=30)
        )
    )

    #-----------------------------------------------------

    page.add(
        ft.Column(
        [
            ft.Container(
                content=title,
                alignment=ft.alignment.center,  
            ),
            ft.Container(
                content=user_input,
                alignment=ft.alignment.center, 
                padding=10,            
            ),
            ft.Container(
                content=pass_input,
                alignment=ft.alignment.center,
                padding=10
            ),
            ft.Container(
                content=log_button,
                alignment=ft.alignment.center,
                padding=30
            ),
            ft.Container(
                content=sig_button,
                alignment=ft.alignment.center,
                padding=20
            ),        
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    pre_login()
