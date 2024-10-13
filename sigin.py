import flet as ft
from dataController import SecionController

def main_sigin(page: ft.Page):
    
    page.title = "TASK! - Sigin"
    page.scroll = "auto"
    page.padding = 10

    controller = SecionController()

    def siginup(e):
        res = controller.siginup_db(name_input.value,mail_input.value,pass_input.value,re_pass_input.value)   
        if res == "OK":
            go_to_login(e)         

    def go_to_login(e):
        page.clean()
        from login import main_login
        main_login(page)



#-----------------------------------------------------

    title = ft.Text(
        value="Registrate!",
        size=50,        
    )
    
    name_input = ft.TextField(
        label="Nombre",   
        text_size=30        
    )

    mail_input = ft.TextField(
        label="Correo",   
        text_size=30        
    )
    
    pass_input = ft.TextField(
        label="Contraseña",        
        text_size=30,
        password=True
    )

    re_pass_input = ft.TextField(
        label="Confirma la contraseña",        
        text_size=30,
        password=True
    )
    
    sig_button = ft.ElevatedButton(
        text="Registrar",  
        width=300,
        height=75,  
        on_click=lambda e:siginup(e),   
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=30),            
        )
    ) 
    
    back_button = ft.ElevatedButton(
        text="Volver",
        width=200,
        height=75,
        on_click=lambda e:go_to_login(e),
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
            content=name_input,
            alignment=ft.alignment.center, 
            padding=10,            
        ),
        ft.Container(
            content=mail_input,
            alignment=ft.alignment.center,
            padding=10
        ),
        ft.Container(
            content=pass_input,
            alignment=ft.alignment.center,
            padding=10
        ),
        ft.Container(
            content=re_pass_input,
            alignment=ft.alignment.center,
            padding=10
        ),   
        ft.Container(
            content=sig_button,
            alignment=ft.alignment.center,
            padding=20
        ),
        ft.Container(
            content=back_button,
            alignment=ft.alignment.center,
            padding=20
        ),     
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        )
    )
