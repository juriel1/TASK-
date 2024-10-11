import flet as ft

def main(page: ft.Page):
    page.title = "TASK!"
    page.scroll = "auto"
    page.padding = 10
        
    theme_list = ft.Row()
    task_list = ft.Column()
    
    def add_theme(e):
        theme_text = theme_input.value 
        if theme_text: 
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

    def theme_clicked(e):
        print(f"Tema seleccionado: {e.control.text}")

    def add_task(e):
        task_text = task_input.value 
        if task_text: 
            task_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(task_text),
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),
                elevation=2
            )
            task_list.controls.append(task_card)
            page.update() 
            task_input.value = "" 
            task_input.focus()

    def add_task_load(e, task_text=None):
        if task_text:
            task_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(task_text),
                    padding=10,
                    bgcolor=ft.colors.BLACK87,
                    border_radius=10
                ),
                elevation=2
            )
            task_list.controls.append(task_card)
            page.update() 
            task_input.value = "" 
            task_input.focus()

    def save(e):
        data = ""
        for control in task_list.controls:
            data += str(control.content.content.value) + "\n"
        with open('data.txt','a') as file_:
            file_.writelines(data)

    def load(e=None):  # Ahora acepta un argumento opcional
        try:
            with open("data.txt", 'r') as file_:
                for line in file_:  # Iterar directamente sobre el archivo
                    add_task_load(None, line.strip())  # Pasar None como primer argumento
        except FileNotFoundError:
            print("El archivo data.txt no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error al cargar las tareas: {e}")


#-----------------------------------------------------
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
    save_button = ft.ElevatedButton(
        text="Guardar",
        on_click=save
    )  
    load_button = ft.ElevatedButton(
        text="Cargar",
        on_click=load
    )   
#-----------------------------------------------------
    page.add(
        ft.Row([theme_input, add_theme_button]),
        theme_list,
        ft.Row([task_input, add_task_button,save_button,load_button]),
        task_list
    )

ft.app(target=main)
