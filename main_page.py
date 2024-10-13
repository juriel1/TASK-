import flet as ft
from dataController import DController
from dataController import SecionController

def main_main(page: ft.Page,user,mail):
    current_theme = ""
    controller = DController(user)
    secion_controller = SecionController()
    
    page.title = "TASK!"
    page.scroll = "auto"
    page.padding = 10
    page.window_width = 1350
    page.window_height = 720
        
    theme_list = ft.Row()
    curren_task_list = ft.Column()
    task_list = {}
    
    def theme_clicked(e):
        nonlocal current_theme
        current_theme = str(e.control.text)
        curren_task_list.controls.clear()
        if current_theme in task_list:
            curren_task_list.controls.extend(task_list[current_theme].controls)
        page.update()
        print(f"Tema seleccionado: {current_theme}")

    def delete_theme(e,theme,theme_card):
        controller.delete_theme_db(theme)      
        theme_list.controls.remove(theme_card)
        if task_list[theme].controls[0] == curren_task_list.controls[0]:
            curren_task_list.controls.clear()
        task_list[theme].controls.clear()
        page.update()   


    def add_theme(e):
        nonlocal current_theme
        
        theme_text = theme_input.value 
        if theme_text: 
            controller.add_theme_db(theme_text)
            current_theme = theme_text            
            task_list[current_theme] = ft.Column()
            
            theme_button = ft.ElevatedButton(
                text=theme_text,
                on_click=theme_clicked
            )
            theme_card = ft.Card(
                content= ft.Column([
                    ft.Container(
                    content=theme_button,
                    padding=ft.padding.only(left=35, right=35,top=7, bottom=7),
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10),
                    ft.Container(
                        content = ft.Row([
                            ft.ElevatedButton(text=" ",icon=ft.icons.DELETE_OUTLINE,on_click=lambda e:delete_theme(e,theme_text,theme_card)),
                            ft.ElevatedButton(text=" ",icon=ft.icons.EDIT_OUTLINED)
                    ]))
                ]),elevation=2
            )
            theme_list.controls.append(theme_card)
            page.update() 
            theme_input.value = "" 
            theme_input.focus()  

    def add_theme_load(e, theme_text=None):        
        nonlocal current_theme
        if theme_text:
            current_theme = theme_text            
            task_list[current_theme] = ft.Column()
        
            theme_button = ft.ElevatedButton(
                text=theme_text,
                on_click=theme_clicked
            )
            theme_card = ft.Card(
                content= ft.Column([
                    ft.Container(
                    content=theme_button,
                    padding=ft.padding.only(left=35, right=35,top=7, bottom=7),
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10),
                    ft.Container(
                        content = ft.Row([
                            ft.ElevatedButton(text=" ",icon=ft.icons.DELETE_OUTLINE,on_click=lambda e:delete_theme(e,theme_text,theme_card)),
                            ft.ElevatedButton(text=" ",icon=ft.icons.EDIT_OUTLINED)
                    ]))
                ]),elevation=2
            )
            theme_list.controls.append(theme_card)
            page.update() 


    def delete_task(e = None,task = None,task_card = None):
        controller.delete_task_db(current_theme,task)
        task_list[current_theme].controls.remove(task_card)
        curren_task_list.controls.remove(task_card)
        page.update()

    def add_task(e):
        task_text = task_input.value 
        if task_text and current_theme: 
            print(f"Tema de la tarea: {current_theme}")
            controller.add_task_db(current_theme, task_text)
            task_card = ft.Row([
                ft.Card(
                content=ft.Container(
                    content=ft.Text(task_text),
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),elevation=2),
                ft.ElevatedButton(text=" ",icon=ft.icons.DELETE_OUTLINE,on_click=lambda e:delete_task(e,task_text,task_card)),
                ft.ElevatedButton(text=" ",icon=ft.icons.EDIT_OUTLINED)
                ])
            task_list[current_theme].controls.append(task_card)
            curren_task_list.controls.append(task_card)
            page.update()
            task_input.value = "" 
            task_input.focus()                

    def add_task_load(task_text):
        if task_text and current_theme: 
            print(f"Tema de la tarea cargada: {current_theme} - Tarea: {task_text}")
            task_card = ft.Row([
                ft.Card(
                content=ft.Container(
                    content=ft.Text(task_text),
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),elevation=2),
                ft.ElevatedButton(text=" ",icon=ft.icons.DELETE_OUTLINE,on_click=lambda e:delete_task(e,task_text,task_card)),
                ft.ElevatedButton(text=" ",icon=ft.icons.EDIT_OUTLINED)
                ])
            task_list[current_theme].controls.append(task_card)
            curren_task_list.controls.append(task_card)
            page.update()        

    def load_to_db(e=None):
        print("Cargando datos desde la base de datos...")
        try:
            data = controller.read_doc_to_user()  
            print("Datos obtenidos de la base de datos:", data) 

            themes = [key for key in data.keys() if key.startswith("Theme")]

            for theme_key in themes:
                theme_value = data.get(theme_key)  
                task_key = theme_key.replace("Theme", "Task")

                tasks_value = data.get(task_key, [])

                if theme_value:  
                    add_theme_load(None, theme_value)  
                    for task in tasks_value:
                        add_task_load(task)  

            page.update()
            print("Carga desde la base de datos completada.")
        except Exception as e:
            print(f"Ocurrió un error al cargar desde la base de datos: {e}")

    
    def logut_to_db(e):
        res = secion_controller.logut_db()
        if res == "OK":
            from login import main_login
            page.clean()
            main_login(page)

    #-----------------------------------------------------
    title_txt = ft.Text(
        value="TASKs!",
        size=50,        
    )  

    user_txt = ft.Text(
        value=f"{user}: \n {mail}",
        size=10,        
    )  

    logout_button = ft.ElevatedButton(
        text=" ",
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e:logut_to_db(e)
    ) 

    theme_input = ft.TextField(
        label="Theme",
        width=1100,        
    )

    add_theme_button = ft.ElevatedButton(
        text=" ",
        icon=ft.icons.ADD_CIRCLE_OUTLINE,
        on_click=lambda e:add_theme(e)
    )   

    task_input = ft.TextField(
        label="TASK!",
        width=1100
    )  

    add_task_button = ft.ElevatedButton(
        text=" ",
        icon=ft.icons.ADD_CIRCLE_OUTLINE,
        on_click=lambda e:add_task(e)
    )   
                 
    #-----------------------------------------------------
    page.add(
        ft.Row([
            ft.Container(
                content=title_txt,
                padding=ft.padding.only(left=500, right=305)),
            ft.Container(
                content=user_txt,
                padding=10),
            ft.Container(
                content=logout_button,
                padding=10,)
            ],alignment=ft.alignment.top_right),
            ft.Container(
                content = ft.Row([theme_input, add_theme_button]),
                padding=ft.padding.only(left=20, right=100)),
            ft.Container(
                content = theme_list,
                padding=ft.padding.only(left=20, right=100)),
            ft.Container(
                content = ft.Row([task_input, add_task_button]),
                padding=ft.padding.only(left=20, right=100)),
            ft.Container(
                content = curren_task_list,
                padding=ft.padding.only(left=20, right=100))
    )
    load_to_db()
