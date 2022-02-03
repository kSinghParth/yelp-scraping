import mysql.connector
from mysql.connector import Error
import yaml
import argparse

from util import *

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
    
    def clean_db(self):
        print('Cleaning')
        sql = "DELETE FROM yelp_business"

        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

    def enter_business_record(self, business):
        sql = 'INSERT INTO yelp_business ( business_id, business_name, review_count, star_rating,'\
            ' zip, city, state, country, business_url, latitude, longitude, address, price_range, '\
            'open, phone, categories, alias, cover_img_url, transactions ) '\
            'VALUE ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
        
        val = [business['id'], business['name'], business['review_count'], 
            business['rating'], business['zip_code'], business['city'], 
            business['state'], business['country'], business['url'],
            business['latitude'], business['longitude'],
            business['address'], business['price'], business['open'], 
            business['phone'], business['categories_str'], business['alias'],
            business['image_url'], business['transactions_str']
            ]

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


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete', dest='delete', default=False,
                        type=bool, help='Delete the db entries')
    input_values = parser.parse_args()

    connector = Connector()

    if input_values.delete:
        connector.clean_db()
