import pymongo
import os

class DController():
    def __init__(self,user):
        self.client = "mongodb://localhost:27017/"
        self.db = "TASKs"
        self.collection_task = "tasks"
        self.current_user = user

    def add_theme_db_FIRST(self, theme):
        client = pymongo.MongoClient(self.client)
        db = client[self.db]
        coleccion = db[self.collection_task]

        data = {
            "User": self.current_user,
            "Theme1": theme,
            "Task1": []
        }
        coleccion.insert_one(data)
        print(f"Insert FIRST theme {theme} OK")

    def add_theme_db(self, theme):
        client = pymongo.MongoClient(self.client)
        db = client[self.db]
        coleccion = db[self.collection_task]

        filter = {"User": self.current_user}
        document = coleccion.find_one(filter)

        if document:
            theme_count = sum(1 for key in document if key.startswith("Theme"))
            new_theme_key = f"Theme{theme_count + 1}"
            new_tasks_key = f"Task{theme_count + 1}"

            update_data = {
                "$set": {
                    new_theme_key: theme,
                    new_tasks_key: []
                }
            }
            res = coleccion.update_one(filter, update_data)

            if res.modified_count > 0:
                print(f"new THEME {theme} in User {self.current_user} OK")
            else:
                print(f"new THEME {theme} in User {self.current_user} NOK")
        else:
            print("First theme")
            self.add_theme_db_FIRST(theme)

    def add_task_db(self, theme_father, task):
        client = pymongo.MongoClient(self.client)
        db = client[self.db]
        coleccion = db[self.collection_task]

        filter = {"User": self.current_user}
        document = coleccion.find_one(filter)

        if document:
            for field, field_value in document.items():
                if field_value == theme_father:
                    task_number = str(field)[-1]
                    task_name = "Task" + task_number
                    update_data = {"$push": {task_name: task}}
                    res = coleccion.update_one(filter, update_data)

                    if res.modified_count > 0:
                        print(f"new TASK {task} in Theme {theme_father} in User {self.current_user} OK")
                    else:
                        print(f"new TASK {task} in Theme {theme_father} in User {self.current_user} NOK")

    def delete_task_db(self,theme_father,task):
        client = pymongo.MongoClient(self.client)
        db = client[self.db]
        coleccion = db[self.collection_task]

        filter = {"User": self.current_user}
        document = coleccion.find_one(filter)

        try:
            if document:
                for field,field_value in document.items():
                    if field_value == theme_father:
                        task_name = f"Task{field[-1]}"
                        filter2 = {field:field_value}
                        update_data = {"$pull":{task_name:task}}
                        coleccion.update_one(filter2,update_data)        
        except Exception as e:
            print(f"Error: {e}")

    def delete_theme_db(self,theme_father):
        client = pymongo.MongoClient(self.client)
        db = client[self.db]
        coleccion = db[self.collection_task]

        filter = {"User": self.current_user}
        document = coleccion.find_one(filter)

        try:
            if document:
                for field,field_value in document.items():
                    if field_value == theme_father:
                        task_name = f"Task{field[-1]}"
                        update_data = {"$unset": {field: "",task_name: ""}}
                        coleccion.update_one(filter,update_data)        
        except Exception as e:
            print(f"Error: {e}")


    def read_doc_to_user(self):
        client = pymongo.MongoClient(self.client)
        db = client[self.db]
        coleccion = db[self.collection_task]

        filter = {"User": self.current_user}
        document = coleccion.find_one(filter)

        if document:
            print(f"Document found OK: {document}")
            return document
        else:
            print(f"Document not found for user {self.current_user}")

class SecionController():
    def __init__(self):
        self.client = "mongodb://localhost:27017/"
        self.db = "TASKs"
        self.collection_task = "users"
        self.path = r"C:\Program Files\TASKs"
        self.path_file = os.path.join(self.path, "state.txt")

    def siginup_db(self,name,mail,pass_,repass_):
        if name is not None and mail is not None or pass_ is not None and repass_ is not None:
            if pass_ == repass_:
                client = pymongo.MongoClient(self.client)
                db = client[self.db]
                coleccion = db[self.collection_task]

                filter = {"Mail":mail}
                document = coleccion.find_one(filter)

                if document:
                    print("User rigth exist")
                    return "NOK"
                else:
                    data = {
                    "Name":name,
                    "Mail":mail,
                    "Pass":pass_,
                    "State":False
                    }
                    coleccion.insert_one(data)
                    print(f"Create user{name} with mail {mail}")
                    return "OK"
            else:
                print("Password different")
                return "NOK"
        else:
            print("Empty fields")
            return "NOK"

    def login_db(self,mail,pass_):
        if mail is not None and pass_ is not None:
                client = pymongo.MongoClient(self.client)
                db = client[self.db]
                coleccion = db[self.collection_task]

                filter = {"Mail":mail, "Pass":pass_}
                document = coleccion.find_one(filter)

                if document:
                    print("User rigth exists")       
                    val = f"{document.get('Name')}${mail}${pass_}"
                    with open(self.path_file, 'w') as file:
                        file.write(val)
                    return ("OK",document.get('Name'),document.get('Mail'))
                else:
                    print("User not exists")
                    return "NOK "

    def logut_db(self):
        with open(self.path_file, 'w') as file:
            file.write("")
        return ("OK")

    def pre_login_db(self):
        with open(self.path_file, 'r') as file:
            f_line = file.readline()
            if f_line != "":
                data = f_line.split('$')
                return ("OK",data[0],data[1])
            else:
                return "NOK"



        