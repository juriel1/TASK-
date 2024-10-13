import flet as ft
from dataController import DController

def main_main(page: ft.Page,user,mail):
    current_theme = ""
    controller = DController(user)
    
    page.title = "TASK!"
    page.scroll = "auto"
    page.padding = 10
        
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
                content=ft.Container(
                    content=theme_button,
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),
                elevation=2
            )
            theme_list.controls.append(theme_card)
            page.update() 
            theme_input.value = "" 
            theme_input.focus()  

    def add_task(e):
        task_text = task_input.value 
        if task_text and current_theme: 
            print(f"Tema de la tarea: {current_theme}")
            controller.add_task_db(current_theme, task_text)
            task_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(task_text),
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),
                elevation=2
            )
            task_list[current_theme].controls.append(task_card)
            curren_task_list.controls.append(task_card)
            page.update()
            task_input.value = "" 
            task_input.focus()            

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
                content=ft.Container(
                    content=theme_button,
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),
                elevation=2
            )
            theme_list.controls.append(theme_card)
            page.update() 

    def add_task_load(task_text):
        if task_text and current_theme: 
            print(f"Tema de la tarea cargada: {current_theme} - Tarea: {task_text}")
            task_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(task_text),
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),
                elevation=2
            )
            task_list[current_theme].controls.append(task_card)
            curren_task_list.controls.append(task_card)
            page.update()    

    def load_to_db(e=None):
        print("Cargando datos desde la base de datos...")
        try:
            data = controller.read_doc_to_user()  
            print("Datos obtenidos de la base de datos:", data) 

            i = 1
            while True:
                theme_key = f"Theme{i}"  
                task_key = f"Task{i}"  

                theme_value = data.get(theme_key)  
                tasks_value = data.get(task_key, [])  

                if theme_value is None:  
                    break

                if theme_value:  
                    add_theme_load(None, theme_value)  
                    for task in tasks_value:
                        add_task_load(task)  

                i += 1  

            page.update()
            print("Carga desde la base de datos completada.")
        except Exception as e:
            print(f"Ocurrió un error al cargar desde la base de datos: {e}")
    #-----------------------------------------------------
    user_txt = ft.Text(
        value=f"{user}: \n {mail}",
        size=10,        
    )    
    theme_input = ft.TextField(
        label="Agregar Tema",
        width=300
    )
    add_theme_button = ft.ElevatedButton(
        text="Agregar tema",
        on_click=add_theme
    )     
    task_input = ft.TextField(
        label="Agregar Tarea",
        width=300
    )    
    add_task_button = ft.ElevatedButton(
        text="Agregar tarea",
        on_click=add_task
    )                
    #-----------------------------------------------------
    page.add(
        ft.Container(
        content=user_txt,
        alignment=ft.alignment.top_right,
        padding=10,
        ),
        ft.Row([theme_input, add_theme_button]),
        theme_list,
        ft.Row([task_input, add_task_button]),
        curren_task_list
    )
    load_to_db()
