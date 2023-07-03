import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset =string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password
    
    
def insert_user(user_name, mail,password):
    sql = 'INSERT INTO quiz_user VALUES(default, %s, %s, %s, %s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name, mail, hashed_password, salt))
        count = cursor.rowcount #更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM quiz_user WHERE name = %s' #ユーザー名がに件取れる可能性があるから直すnmae=%sのとこ
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, ))
        user = cursor.fetchone()

        if user != None:
            salt = user[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally :
        cursor.close()
        connection.close()
    
    return flg

def insert_quiz(title,answer1,answer2,answer3,answer4,correctanswer):
    sql = 'INSERT INTO quiz VALUES(default, %s, %s, %s, %s,%s,%s)'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (title,answer1,answer2,answer3,answer4,correctanswer))
        count = cursor.rowcount #更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def de_quiz(quizid):
    sql = 'DELETE FROM quiz WHERE quizid = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (quizid,))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def edit_quiz(quizid, title,answer1,answer2,answer3,answer4,correctanswer):
    sql = 'UPDATE quiz SET Quizcontent=%s, Answer1=%s, Answer2=%s, Answer3=%s, Answer4=%s, Correctanswer=%s WHERE quizid=%s;'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (title,answer1,answer2,answer3,answer4,correctanswer,quizid))
        count = cursor.rowcount #更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count




def select_all_quiz():
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT quizid, quizcontent, answer1, answer2, answer3, answer4 FROM quiz'

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

