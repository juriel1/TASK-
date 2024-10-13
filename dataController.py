import pymongo
import struct

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
                    valor = 1
                    with open('state.bin', 'wb') as file:
                        file.write(struct.pack('B', valor))
                    return ("OK",document.get('Name'))
                else:
                    print("User not exists")
                    return "NOK "
                
    def pre_login_db(self):
        with open('state.txt', 'r') as file:
            f_line = file.readline()        
            if f_line == "1"


        