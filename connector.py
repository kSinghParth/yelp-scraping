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
            logger.info("The error " + str(e) + " occurred")
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

    def enter_zip_code(self, zip_code, city, state):
        sql = 'INSERT INTO zip_code ( zipcode, city, state ) SELECT %s, %s, %s as tmp '\
            'WHERE NOT EXISTS (SELECT 1 FROM zip_code WHERE zipcode = %s) LIMIT 1;'

        val = [
            zip_code, city, state, zip_code
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def update_zip_code_counts(self, zip_code, total, checked):
        sql = 'update zip_code set total = %s, checked = %s where zipcode = %s'

        val = [
            total, checked, zip_code
        ]

        self.connection.cursor().execute(sql, val)
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

    def enter_review_record(self, review, business_id):
        sql = 'INSERT INTO yelp_reviews ( review_id, business_id, user_id, review_text, review_rating, '\
            'language, review_date, useful_votes, cool_votes, funny_votes, response_body, total_photos, photos_url, check_in, response_comment_id ) '\
            'SELECT  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 3, %s as tmp '
#            'WHERE NOT EXISTS (SELECT 1 FROM yelp_reviews WHERE review_id = %s) LIMIT 1'

        val = [
            review['id'], business_id, review['user_id'],
            review['review_text'], review['rating'],
            review['language'], review['local_date'],
            review['useful'], review['cool'],
            review['funny'], review['response_body'],
            review['total_photos'], review['photos_url'],
            review['response_comment_id']
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

    def add_updated_yelp_business_ids(self, new_business_id, old_business_id):
        sql = 'INSERT INTO `yelp_updated_business_ids` (`old_business_id`, `new_business_id`) select %s,%s as TMP '\
            'WHERE NOT EXISTS (SELECT 1 FROM `yelp_updated_business_ids` where `old_business_id`=%s and `new_business_id` = %s)'
        val = [
            old_business_id, new_business_id, old_business_id, new_business_id
        ]

        self.connection.cursor().execute(sql, val)
        sql = 'update yelp_reviews set business_id = %s where business_id = %s'
        val = [
            new_business_id, old_business_id
        ]
        self.connection.cursor().execute(sql, val)
        self.connection.commit()

        sql = "SELECT count(*) from yelp_reviews where business_id = %s"

        cursor = self.connection.cursor()
        cursor.execute(sql, [new_business_id])

        rv_ct = cursor.fetchall()[0][0]

        return rv_ct

    def get_business_id_for_review(self, review_id):
        sql = "SELECT business_id from yelp_reviews where review_id = %s"

        cursor = self.connection.cursor()
        cursor.execute(sql, [review_id])

        business_id = cursor.fetchall()[0][0]
        return business_id

    def update_review_photo_completeion(self, review_id):
        sql = 'UPDATE yelp_reviews set check_in = 4 where review_id = %s'
        val = [review_id]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def enter_photo_record(self, photo):
        sql = 'INSERT INTO yelp_photos ( image_id, review_id, caption, image_url, web_url, '\
            'alt_text, width, height, image_date, src_set) '\
            'values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'

        val = [
            photo['id'], photo['review_id'], photo['caption'],
            photo['image_url'], photo['web_url'], photo['alt_text'],
            photo['width'], photo['height'], photo['image_date'],
            photo['src_set']
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def add_total_photos(self, review_id, total_photos):
        sql = 'UPDATE yelp_reviews set total_photos = %s where review_id = %s'

        val = [total_photos, review_id]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def update_business_flag(self, business_id):
        sql = 'UPDATE yelp_business set flag = 1 where business_id = %s'
        val = [business_id]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def update_total_reviews(self, business_id, total_reviews):
        sql = 'UPDATE yelp_business set review_count = %s where business_id = %s'
        val = [total_reviews, business_id]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def update_reviews_for_html_decode(self, review_id, review_text):
        sql = 'UPDATE yelp_reviews set review_text = %s, check_in = 1 where review_id = %s'
        val = [review_text, review_id]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def get_business_records_for_reviews(self):
        # sql = 'SELECT business_url, review_count, business_id, 0 from `yelp_business`  '\
        #     ' where review_count!= 0 and business_id not in (select distinct(business_id) from `yelp_reviews`)'

        sql = 'SELECT b.business_url, b.review_count, b.business_id,  count(r.review_id) '\
            ' FROM yelp_business b left join `yelp_reviews` r '\
            ' on r.business_id = b.business_id '\
            ' where flag is Null '\
            ' group by b.`business_id` limit 100'

        # sql = 'SELECT business_url, review_count, business_id, tmp.r_counted from `yelp_business` b '\
        #     ' LEFT JOIN (SELECT b.business_id b_id, count(r.review_id) r_counted, b.review_count r_total '\
        #     ' FROM yelp_business b inner join `yelp_reviews` r on r.business_id = b.business_id '\
        #     ' INNER JOIN yelp_users u on u.user_id = r.user_id group by b.`business_id`) as tmp on tmp.b_id = b.business_id '\
        #     ' WHERE review_count>0 and (tmp.r_counted is null or tmp.r_counted < review_count) '
        #     ' WHERE review_count>0 and (tmp.r_counted is null or tmp.r_counted < review_count ) order by business_id desc'

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        businesses = cursor.fetchall()

        # print(len(businesses))

        return businesses

    def get_business_records(self):
        sql = "SELECT business_url, review_count FROM yelp_business"

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        businesses = cursor.fetchall()

        return businesses

    def get_zip_codes(self):
        sql = "SELECT zipcode, city, state, total, checked FROM zip_code WHERE total is Null OR checked = Null or (checked < total and checked < 900)"

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        zip_codes = cursor.fetchall()
        print(len(zip_codes))

        return zip_codes

    def get_select_cities(self):
        sql = "select distinct(city) from zip_code"

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        cities = cursor.fetchall()
        print(len(cities))

        return cities

    def get_review_photo_info(self):
        sql = 'SELECT review_id, total_photos, response_body, review_date from `yelp_reviews`  '\
            ' where total_photos != 0 and check_in = 3 limit 100000'

        # sql = 'SELECT review_id, total_photos, response_body, review_date from `yelp_reviews`  '\
        #     ' where total_photos != 0 and review_id not in (select distinct(review_id) from `yelp_photos`)'

        # sql = 'SELECT review_id, total_photos, response_body, review_date from `yelp_reviews` yr '\
        #     ' LEFT JOIN (SELECT p.review_id r_id, count(p.image_id) p_counted, r.total_photos p_total '\
        #     ' FROM yelp_photos p inner join `yelp_reviews` r on r.review_id = p.review_id '\
        #     ' group by p.review_id) as tmp on tmp.r_id =  yr.review_id '\
        #     ' WHERE (tmp.p_counted is null or tmp.p_counted < tmp.p_total) and  total_photos>0 '\
        #     ' and yr.response_body is not null'

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        reviews = cursor.fetchall()
        print(len(reviews))

        return reviews

    def get_reviews_for_html_decode(self):
        sql = 'SELECT review_id, review_text from yelp_reviews where check_in is null limit 100'

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        reviews = cursor.fetchall()
        print(len(reviews))

        return reviews

    def update_empty_owner_response(self, review_id):
        sql = 'UPDATE yelp_reviews set check_in = 0 where review_id = %s'

        val = [
            review_id
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    # Coming form the fix script
    def update_owner_response(self, review_id, response):
        sql = 'UPDATE yelp_reviews set response_comment_id=%s, check_in = 0 where review_id = %s'

        val = [
            response['response_id'], review_id
        ]

        self.connection.cursor().execute(sql, val)

        sql = 'INSERT into yelp_reviews_response (response_id, owner_id, response_comment, response_date,'\
              'response_display_name, response_owner_role, owner_src) '\
              'SELECT %s, %s, %s, %s, %s, %s, %s'

        val = [
            response['response_id'], response['owner_id'],
            response['response_comment'], response['response_date'],
            response['response_display_name'], response['response_owner_role'],
            response['owner_src']
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    # Comign from the main fetch_review script
    def add_owner_response(self, response):
        sql = 'INSERT into yelp_reviews_response (response_id, owner_id, response_comment, response_date,'\
              'response_display_name, response_owner_role, owner_src) '\
              'SELECT %s, %s, %s, %s, %s, %s, %s'

        val = [
            response['response_id'], response['owner_id'],
            response['response_comment'], response['response_date'],
            response['response_display_name'], response['response_owner_role'],
            response['owner_src']
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def get_reviews_for_owner_response(self):
        sql = 'SELECT review_id, response_body from yelp_reviews where check_in = 1 limit 1000000'

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        reviews = cursor.fetchall()
        print(len(reviews))

        return reviews

    def get_missed_reviews(self):
        sql = 'SELECT review_id, response_body from yelp_reviews where check_in=2 and review_text is null limit 10000'

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        reviews = cursor.fetchall()
        print(len(reviews))

        return reviews

    def update_missed_reviews(self, review_id, review_text):
        sql = 'update yelp_reviews set review_text = %s, check_in = 1 where review_id = %s'

        val = [
            review_text, review_id
        ]

        self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def get_review_info_for_backlog(self):
        sql = 'SELECT review_id, response_body from yelp_reviews where response_body is not null'

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        reviews = cursor.fetchall()
        print(len(reviews))

        return reviews

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

    def get_all_business_zip(self):
        sql = "SELECT distinct zip FROM yelp_business where zip is not null and zip != '' and primary_city is NULL"

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        zip = cursor.fetchall()
        return zip

    def get_primary_city_for_zip(self):
        sql = "SELECT zipcode, primary_city FROM dp_city_zipcode"

        cursor = self.connection.cursor()
        cursor.execute(sql, [])

        zip = cursor.fetchall()
        return zip

    def update_primary_city(self, cities):
        for city in cities:
            sql = 'update yelp_business set primary_city = %s where zip = %s'

            val = [
                city[1], city[0]
            ]

            self.connection.cursor().execute(sql, val)
        self.connection.commit()

    def execute_read_query(self):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute("SELECT * FROM yelp_business")
            result = cursor.fetchall()
            return result
        except Error as e:
            logger.info("The error " + str(e) + " occurred")


def get_connector():
    return Connector()


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
