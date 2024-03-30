import mysql.connector

class DatabaseHandler:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            print("Connected to MySQL server")
        except mysql.connector.Error as error:
            print("Failed to connect to MySQL server:", error)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from MySQL server")

    def add_server(self, server_name, ip_address):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "INSERT INTO servers (name, ip_address) VALUES (%s, %s)"
                values = (server_name, ip_address)
                cursor.execute(query, values)
                self.connection.commit()
                print("Server added successfully")
            except mysql.connector.Error as error:
                print("Failed to add server:", error)
        else:
            print("Not connected to MySQL server")
    def list_tables(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    print(table[0])
            except mysql.connector.Error as error:
                print("Failed to list tables:", error)
        else:
            print("Not connected to MySQL server")

# Example usage:
db = DatabaseHandler("192.168.1.150", 1115,"boom", "BoomerangBS", "test")
db.connect()
print(db.list_tables())
db.disconnect()