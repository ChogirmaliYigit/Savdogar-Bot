import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
        """
        self.execute(sql, commit=True)

    def create_table_category(self):
        sql = """
        CREATE TABLE Category (
            id INTEGER PRIMARY KEY,
            title VARCHAR(50) NOT NULL UNIQUE,
            desc TEXT,
            image TEXT
        );
        """
        self.execute(sql=sql, commit=True)
    
    def create_product_table(self):
        sql = """
        CREATE TABLE Product (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            desc TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL,
            cat_id INTEGER NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)

    def create_user_cart(self):
        sql = """
        CREATE TABLE Cart (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)

    def create_order_table(self):
        sql = """
        CREATE TABLE OrderProduct (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            phone VARCHAR(50) NOT NULL,
            address TEXT,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            paid INTEGER DEFAULT 0 NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)

    def create_order_item_table(self):
        sql = """
        CREATE TABLE OrderItem (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_id INTEGER NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)

    def create_payment_providers(self):
        sql = """
        CREATE TABLE Payment (
            id INTEGER PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            token TEXT NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)

    def add_product_to_cart(self, user_id, product_id, quantity):
        sql = """
        INSERT INTO Cart (user_id, product_id, quantity) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, product_id, quantity), commit=True)

    def add_order_product(self, user_id, phone, address, lat, lon, paid):
        sql = """INSERT INTO OrderProduct (user_id, phone, address, lat, lon, paid) VALUES(?, ?, ?, ?, ?, ?);"""
        self.execute(sql, parameters=(user_id, phone, address, lat, lon, paid), commit=True)

    def add_order_item(self, product_id, quantity, order_id):
        sql = """INSERT INTO OrderItem (product_id, quantity, order_id) VALUES (?, ?, ?);"""
        self.execute(sql=sql, parameters=(product_id, quantity, order_id), commit=True)

    def select_order_item(self, **kwargs):
        sql = """SELECT * FROM OrderItem WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_order_products(self, **kwargs):
        sql = """SELECT * FROM OrderProduct WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def update_order_paid(self, paid, user_id, id):
        sql = """
        UPDATE OrderProduct SET paid=? WHERE user_id=? AND id=?
        """
        self.execute(sql=sql, parameters=(paid, user_id, id), commit=True)

    def add_payment_provider(self, title, token):
        sql = """
        INSERT INTO Payment (title, token) VALUES (?, ?);
        """
        self.execute(sql=sql, parameters=(title, token), commit=True)

    def select_all_provider(self):
        sql = """
        SELECT * FROM Payment;
        """
        return self.execute(sql=sql, fetchall=True)

    def select_provider(self, **kwargs):
        sql = """SELECT * FROM Payment WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user_products(self, **kwargs):
        sql = """SELECT * FROM Cart WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_cart_product(self, **kwargs):
        sql = """SELECT * FROM Cart WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_cart_product(self, user_id, product_id, quantity):
        sql = """
        UPDATE Cart SET quantity=? WHERE user_id=? AND product_id=?
        """
        self.execute(sql=sql, parameters=(quantity, user_id, product_id), commit=True)

    def select_cats(self):
        sql = """SELECT * FROM Category;"""
        return self.execute(sql=sql, fetchall=True)

    def select_products(self, **kwargs):
        sql = """SELECT * FROM Product WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_cat(self, **kwargs):
        sql = """SELECT * FROM Category WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_product(self, **kwargs):
        sql = """SELECT * FROM Product WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def clear_cart(self, **kwargs):
        sql = """DELETE FROM Cart WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        self.execute(sql=sql, parameters=parameters, commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
