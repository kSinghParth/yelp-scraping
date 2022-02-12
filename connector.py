import mysql.connector
from mysql.connector import Error
import yaml
import argparse

from logger import logger


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
            logger.info("Connection to MySQL DB successful")
        except Error as e:
            logger.info(f"The error '{e}' occurred")
        return connection

    def close(self):
        self.connection.close()

    def clean_db(self):
        logger.info('Cleaning')

        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM yelp_business')
        cursor.execute('DELETE FROM coordinates')
        self.connection.commit()

    def clean_review_table(self):
        logger.info('Cleaning')

        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM yelp_reviews')
        self.connection.commit()

    def clean_user_table(self):
        logger.info('Cleaning')

        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM yelp_users')
        self.connection.commit()

    def enter_business_record(self, business):
        sql = 'INSERT INTO yelp_business ( business_id, business_name, review_count, star_rating, '\
            'zip, city, state, country, business_url, latitude, longitude, address, price_range, '\
            'open, phone, categories, cover_img_url, transactions ) '\
            'SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s AS tmp '\
            'WHERE NOT EXISTS (SELECT 1 FROM yelp_business WHERE business_id = %s) LIMIT 1;'

        val = [
            business['id'], business['name'], business['review_count'],
            business['rating'], business['zip_code'], business['city'],
            business['state'], business['country'], business['url'],
            business['latitude'], business['longitude'],
            business['address'], business['price'], business['open'],
            business['phone'], business['categories_str'],
            business['image_url'], business['transactions_str'],
            business['id']
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def enter_review_record(self, review):
        sql = 'INSERT INTO yelp_reviews ( review_id, business_id, user_id, review_text, review_rating, '\
            'language, review_date, useful_votes, cool_votes, funny_votes ) '\
            'SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s AS tmp '\
            'WHERE NOT EXISTS (SELECT 1 FROM yelp_reviews WHERE review_id = %s) LIMIT 1;'

        val = [
            review['id'], review['business_id'], review['user_id'],
            review['review_text'], review['rating'],
            review['language'], review['local_date'],
            review['useful'], review['cool'],
            review['funny'], review['id']
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def enter_user_record(self, user):
        sql = 'INSERT INTO yelp_users ( user_id, user_reviewCount, user_friendCount, user_photoCount, user_name, '\
            'feedback_counts_useful, feedback_counts_cool, feedback_counts_funny, user_link, user_userUrl,  '\
            'user_eliteYear, user_displayLocation, user_src, user_srcSet ) '\
            'SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s AS tmp '\
            'WHERE NOT EXISTS (SELECT 1 FROM yelp_users WHERE user_id = %s) LIMIT 1;'

        val = [
            user['id'], user['review_count'], user['friend_count'],
            user['photo_count'], user['user_name'], user['useful'],
            user['cool'], user['funny'], user['link'],
            user['user_url'], user['elite_year'], user['display_location'],
            user['src'], user['src_set'], user['id']
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def get_business_records(self):
        sql = "SELECT business_id, review_count FROM yelp_business"

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        businesses = cursor.fetchall()

        return businesses

    def enter_coordinate_record(self, latitude, longitude, radius, n_l, s_l, e_l, w_l, quantity, level):
        sql = 'INSERT INTO coordinates ( lat, lng, radius, north_lat, south_lat, east_lng, west_lng, quantity, level ) '\
            'SELECT  %s, %s, %s, %s, %s, %s, %s, %s, %s '
        val = [str(latitude), str(longitude), str(radius), str(n_l), str(s_l), str(e_l), str(w_l), quantity, level]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def does_coordinate_record_exist(self, latitude, longitude, radius):
        sql = "SELECT 1 FROM coordinates WHERE lat = %s AND lng = %s AND radius = %s"
        val = [latitude, longitude, radius]

        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        res = cursor.fetchone()
        if res:
            return res[0] == 1
        return False

    def execute_read_query(self):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute("SELECT * FROM yelp_business")
            result = cursor.fetchall()
            return result
        except Error as e:
            logger.info(f"The error '{e}' occurred")


connector = Connector()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean-db', dest='delete',
                        default=False, action="store_true",
                        help='Delete the db entrie')
    input_values = parser.parse_args()

    if input_values.delete:
        # connector.clean_db()
        connector.clean_user_table()
        connector.clean_review_table()
        print("Be extremely careful with the below query.")
