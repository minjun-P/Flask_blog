from os import stat
from flask_login import UserMixin
from db_model import mysql


class User(UserMixin):
    def __init__(self, user_id, user_email, blog_id):
        self.id = user_id
        self.user_email = user_email
        self.blog_id = blog_id

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        # DB의 데이터를 USER 클래스화 해서 반환
        mysql_db = mysql.conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID ='" + str(user_id) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
        return user

    @staticmethod
    def find(user_email):
        # DB의 데이터를 USER 클래스화 해서 반환
        mysql_db = mysql.conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_EMAIL ='" + str(user_email) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
        return user

    @staticmethod
    def create(user_email, blog_id):
        # db에 데이터 넣고 User 클래스화 해서 반환
        user = User.find(user_email)
        # 찾아와봤는데, 기존에 없다면 만들어야지!
        if user == None:
            mysql_db = mysql.conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_info (USER_EMAIL, BLOG_ID) VALUES ('%s', '%s')" % (
                str(user_email),
                str(blog_id),
            )
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_email)
        else:
            return user

    @staticmethod
    def delete(user_id):
        mysql_db = mysql.conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM user_info WHERE USER_ID = %d" % (user_id)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted
