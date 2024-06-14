import psycopg2

class MagazineSubscriptionService:
    def __init__(self, dbname, host, port, user, password):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port, user=self.user, password=self.password)
            self.cursor = self.connection.cursor()
            print("Connected successfully")
        except Exception as e:
            print(f"Connection refused: {e}")

    def create_user(self, table_name, **kwargs):
        columns = ', '.join(kwargs.get('columns', []))
        values = ', '.join([f"'{value}'" if isinstance(value, str) else f"{value}" for value in kwargs.get('values', [])])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as error:
            print(f"Something went wrong: {error}")

    def create_magazine(self, table_name, **kwargs):
        columns = ', '.join(kwargs.get('columns', []))
        values = ', '.join([f"'{value}'" if isinstance(value, str) else f"{value}" for value in kwargs.get('values', [])])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as error:
            print(f"Something went wrong: {error}")

    def select(self, table_name, **kwargs):
        columns = ', '.join(kwargs.get('columns', [])) if kwargs.get('columns') else '*'
        query = f"SELECT {columns} FROM {table_name}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Something went wrong: {e}")

    def subscribe_user(self, user_id, magazine_id):
        query = "INSERT INTO subscriptions (user_id, magazine_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        try:
            self.cursor.execute(query, (user_id, magazine_id))
            self.connection.commit()
            print(f"User {user_id} subscribed to magazine {magazine_id}")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def unsubscribe_user(self, user_id, magazine_id):
        query = "DELETE FROM subscriptions WHERE user_id = %s AND magazine_id = %s"
        try:
            self.cursor.execute(query, (user_id, magazine_id))
            self.connection.commit()
            print(f"User {user_id} unsubscribed from magazine {magazine_id}")
        except Exception as e:
            print(f"Something went wrong: {e}")

def main():
    database = MagazineSubscriptionService('postgres', '127.0.0.1', 5432, user='postgres', password='123456')
    database.connect()

    while True:
        print("Welcome to our magazine subscription service. Please select an action:")
        task = int(input('1) Add User\n2) View Users\n3) Add Magazine\n4) View Magazines\n5) Subscribe User\n6) Unsubscribe User\n7) Exit\n: '))

        if task == 1:
            table_name = ('users')
            name = input("Enter name: ")
            email = input("Enter email: ")
            age = input("Enter age: ")
            database.create_user(table_name, columns=['name', 'email', 'age'], values=[name, email, age])
        elif task == 2:
            result_users = database.select("users")
            print(result_users)
        elif task == 3:
            table_name = ('magazines')
            title = input("Enter title: ")
            description = input("Enter description: ")
            database.create_magazine(table_name, columns=['title', 'description'], values=[title, description])
        elif task == 4:
            result_magazines = database.select("magazines")
            print(result_magazines)
        elif task == 5:
            user_id = int(input("Enter user ID: "))
            magazine_id = int(input("Enter magazine ID: "))
            database.subscribe_user(user_id, magazine_id)
        elif task == 6:
            user_id = int(input("Enter user ID: "))
            magazine_id = int(input("Enter magazine ID: "))
            database.unsubscribe_user(user_id, magazine_id)
        elif task == 7:
            print("Goodbye!")
            database.cursor.close()
            database.connection.close()
            return
        else:
            print('Choose only from 1 to 7!')

if __name__ == "__main__":
    main()