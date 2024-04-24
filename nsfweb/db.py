import pymysql
from datetime import datetime


config = {
        'host': 'localhost',
        'user': 'root',
        'password': '1111',
        'db': 'smartfactory',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
}

# db connection
def get_db_connection():
    return pymysql.connect(**config)

def get_all_user():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "select * from users"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def get_current_product_index():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                select ProductClassificationLogID from ProductClassificationLog
                where status != 'F'
                order by ProductClassificationLogID desc
                limit 1;
            """

            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return result['ProductClassificationLogID']
            else:
                return None
    finally:
        connection.close()
    
def get_current_product():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT * FROM ProductClassificationLog
                WHERE status != 'F'
                ORDER BY ProductClassificationLogID DESC
                LIMIT 1;
            """

            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
    finally:
        connection.close()


# 제품분류 시작
def start_product_classification(goalRed, goalGreen, goalBlue, goalYellow):
    connection = get_db_connection()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current = get_current_product_index()
    
    try:
        with connection.cursor() as cursor:
            if current:
                # SQL 쿼리 준비
                sql = """
                UPDATE ProductClassificationLog
                SET Status = 'S',
                    GoalRedCnt = %s,
                    GoalGreenCnt = %s,
                    GoalBlueCnt = %s,
                    GoalYellowCnt = %s
                WHERE ProductClassificationLogID = %s;
                """
                # 쿼리 실행
                cursor.execute(sql, (goalRed, goalGreen, goalBlue, goalYellow, current))
            else:
                # SQL 쿼리 준비
                sql = """
                INSERT INTO ProductClassificationLog (
                    StartTime, PauseTime, Status, GoalRedCnt, GoalGreenCnt, GoalBlueCnt, GoalYellowCnt,
                    ProductRedCnt, ProductGreenCnt, ProductBlueCnt, ProductYellowCnt,
                    ErrorEdgeCnt, ErrorColorCnt, ErrorQrCnt, ErrorImageCnt
                ) VALUES (%s, %s, 'S', %s, %s, %s, %s, 0, 0, 0, 0, 0, 0, 0, 0);
                """
                # 쿼리 실행
                cursor.execute(sql, (current_time, current_time, goalRed, goalGreen, goalBlue, goalYellow))
            # 변경사항 커밋
            connection.commit()
    finally:
        # 데이터베이스 연결 닫기
        connection.close()
        
def pause_product_classification():
    connection = get_db_connection()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current = get_current_product_index()

    try:
        with connection.cursor() as cursor:
            if current:
                sql = """
                UPDATE ProductClassificationLog
                SET PauseTime = %s,
                    status = 'P'
                WHERE ProductClassificationLogID = %s;
                """
                cursor.execute(sql, (current_time, current))
                connection.commit()
    finally:
        # 데이터베이스 연결 닫기
        connection.close()

def finish_product_classification():
    connection = get_db_connection()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current = get_current_product_index()

    try:
        with connection.cursor() as cursor:
            if current:
                sql = """
                UPDATE ProductClassificationLog
                SET FinishTime = %s,
                    status = 'F'
                WHERE ProductClassificationLogID = %s;
                """
                cursor.execute(sql, (current_time, current))
                connection.commit()
    finally:
        # 데이터베이스 연결 닫기
        connection.close()


# 수량 업데이트(product, error) 
def update_product_count(columnName, count):
    connection = get_db_connection()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current = get_current_product_index()
    
    try:
        with connection.cursor() as cursor:
            if current:
                # SQL 쿼리 준비
                sql = f"""
                UPDATE ProductClassificationLog
                SET {columnName} = %s
                WHERE ProductClassificationLogID = %s;
                """
                # 쿼리 실행
                cursor.execute(sql, (count, current))
            # 변경사항 커밋
            connection.commit()
    finally:
        # 데이터베이스 연결 닫기
        connection.close()





