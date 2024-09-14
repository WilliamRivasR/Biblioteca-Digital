import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='biblioteca_escolar',
                user='root',
                password='1234'
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def call_procedure(self, proc_name, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            if not self.cursor:
                self.cursor = self.connection.cursor()

            if params:
                self.cursor.callproc(proc_name, params)
            else:
                self.cursor.callproc(proc_name)

            # Fetch any result sets
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())

            self.connection.commit()
            return results
        except Error as e:
            print(f"Error calling procedure {proc_name}: {e}")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()