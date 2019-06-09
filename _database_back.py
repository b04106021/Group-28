"""
資料庫後端程式碼。

函式：
    connect()
    handle_err(err)
    initialize()
    add_dummies()
"""


import sqlite3


DATABASE_FILE = 'bicycle.db'
OperationalError = sqlite3.OperationalError


def connect():
    """
    連接資料庫。

    回傳：一個 sqlite3 connect。
    """
    return sqlite3.connect(DATABASE_FILE)


def handle_err(err):
    """
    處理錯誤。
    """
    print(err)
    raise(err)


def initialize(debug=False):
    """
    初始化資料庫。
    如果資料庫已經存在，則不會做任何修改。
    如果過程沒有錯誤，則會回傳 True。

    傳入：debug: bool = False (是否印出 debug 資訊)

    回傳：True 或 False
    """
    try:
        conn = connect()
        if debug:
            print("Opened database successfully")
    except OperationalError as err:
        handle_err(err)
        return False

    #創建BICYCLE、VIOLATION_RECORD、PHOTO_RECORD表
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS BICYCLE
            (bicycle_id         TEXT PRIMARY KEY NOT NULL,
             student_name       TEXT             NOT NULL,
             student_id         TEXT             NOT NULL,
             student_department TEXT             NOT NULL);''')
        if debug:
            print("Table BICYCLE created successfully")
    except OperationalError as err:
        handle_err(err)
        return False


    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS VIOLATION_RECORD
            (record_id       INT  PRIMARY KEY NOT NULL,
             bicycle_id      TEXT             NOT NULL,
             violation       TEXT             NOT NULL,
             record_datetime TEXT             NOT NULL,
             record_place    TEXT             NOT NULL,
             photo           BLOB             NOT NULL,
             FOREIGN KEY(bicycle_id) REFERENCES BICYCLE(bicycle_id));''')
        if debug:
            print("Table VIOLATION_RECORD created successfully")
    except OperationalError as err:
        handle_err(err)
        return False

    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS VIOLATION_SERIAL
            (violation_date TEXT PRIMARY KEY NOT NULL,
             serial_count   INT              NOT NULL);''')
        if debug:
            print("Table VIOLATION_SERIAL created successfully")
    except OperationalError as err:
        handle_err(err)
        return False

    # try:
    #     conn.execute('''CREATE TABLE IF NOT EXISTS PHOTO_RECORD
    #         (photo_id   INT  PRIMARY KEY NOT NULL,
    #          record_id  INT  PRIMARY KEY NOT NULL,
    #          photo_path TEXT             NOT NULL,
    #          FOREIGN KEY(record_id) REFERENCES VIOLATION_RECORD(record_id));''')
    #     if debug:
    #         print("Table PHOTO_RECORD created successfully")
    # except OperationalError as err:
    #     handle_err(err)
    #     return False

    return True


def add_dummies(debug=False):
    """
    為資料庫新增一些假資料。
    如果過程沒有錯誤，則會回傳 True。

    傳入：debug: bool = False (是否印出 debug 資訊)

    回傳：True 或 False
    """
    try:
        conn = connect()
        conn.execute("""
            INSERT OR IGNORE INTO BICYCLE (bicycle_id, student_name,
                                 student_id, student_department)
            VALUES('B04106021-01', '林怡岑', 'B04106021', '圖資四')""")

        conn.execute("""
            INSERT OR IGNORE INTO VIOLATION_RECORD (record_id, bicycle_id, violation,
                                          record_datetime, record_place)
            VALUES(1, 'B04106021-01', '未停在停車格內',
                   '2019-06-07 20:10:20', '圖資系館')""")

        conn.commit()
        if debug:
            print("Dummy records created successfully")
        conn.close()

        return True
    except OperationalError as err:
        handle_err(err)
        return False
    return False
