import mysql.connector
from mysql.connector import Error
import yaml

class Connector():

    DB_SERVER = None
    USER_NAME = None
    USER_PASSWORD = None
    DB_NAME = None

    connection = None


    def __init__(self):
        with open("conf.yaml", 'r') as stream:
            yaml_loader = yaml.safe_load(stream)
            DB_SERVER = yaml_loader.get('db_server')
            USER_NAME = yaml_loader.get('user_name')
            USER_PASSWORD = yaml_loader.get('user_password')
            DB_NAME = yaml_loader.get('db_name')
        self.connection = self.create_connection(DB_SERVER, USER_NAME, USER_PASSWORD, DB_NAME)


    def create_connection(self, host_name, user_name, user_password, db_name):
        try:
            connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection


    def close(self):
        self.connection.close()
    

    def enter_business_record(self, business):
        print(business['name'])
        sql = "INSERT INTO yelp_business ( business_name ) VALUE ( %s )"
        val = [business["name"]]

        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        self.connection.commit()


    def execute_read_query(self):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute("SELECT * FROM yelp_business")
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
