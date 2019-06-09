"""
資料庫的 api。

函式:
    recreate_database()
    add_bicycle()
    add_violation()
    valid_bicycle()
    get_violation_by_date()
    get_violation_by_bicycle()
    check_step()
    save_step()
    load_step()
    clear_step()
"""


import pickle

import _database_back as db
from _database_back import OperationalError, handle_err


def recreate_database(dummy=False, debug=False):
    """
    如果資料庫不存在的話，重新建立資料庫。

    傳入: dummy: bool = False (是否新增假資料)
          debug: bool = False (是否印出 debug 資訊)

    回傳: True (成功) 或 False (失敗)
    """
    try:
        db.initialize(debug=debug)
        if dummy:
            db.add_dummies(debug=debug)
        return True
    except OperationalError as err:
        handle_err(err)
        return False


def add_bicycle(bicycle_id, student_name, student_id, student_department):
    """
    新增腳踏車編號、學生姓名、學號、系級。

    傳入: bicycle_id: str
          student_name: str
          student_id: str
          student_department: str

    回傳: True (成功) 或 False (失敗)
    """
    data_tuple = (bicycle_id.upper(), student_name,
                  student_id.upper(), student_department)

    if any(data == None for data in data_tuple):
        return False

    try:
        conn = db.connect()
        conn.execute("""
            INSERT OR REPLACE INTO BICYCLE (bicycle_id, student_name,
                                            student_id, student_department)
            VALUES('%s', '%s', '%s', '%s')""" % data_tuple)

        conn.commit()
        conn.close()

        return True
    except OperationalError as err:
        handle_err(err)
        return False
    return False


def add_violation_with_list(li):
    """
    新增一筆違規紀錄，回傳違規編號。
    如果資料錯誤，會產生 AttributeError；新增失敗則會回傳空字串。

    傳入: list，內含：[bicycle_id: str (腳踏車編號),
                      violation: str (違規事件),
                      datetime: datetime.datetime (日期時間),
                      place: str (地點),
                      photo: bytes (照片)]

    回傳: str (此筆資料的違規編號)
    """
    if any(x is None for x in li) or len(li) != 5:
        raise AttributeError
    return add_violation(*li)

def add_violation(bicycle_id, violation, datetime, place, photo):
    """
    新增一筆違規紀錄，回傳違規編號。
    如果資料錯誤，會產生 AttributeError；如果新增失敗則會回傳空字串。

    傳入: bicycle_id: str (腳踏車編號)
          violation: str (違規事件)
          datetime: datetime.datetime (日期時間)
          place: str (地點)
          photo: bytes (照片)

    回傳: str (此筆資料的違規編號)
    """
    data_tuple = (bicycle_id.upper(), violation, datetime, place, photo)

    if any(data == None for data in data_tuple):
        raise AttributeError

    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT serial_count FROM VIOLATION_SERIAL
            WHERE violation_date LIKE '%s'""" % datetime.strftime('%Y%m%d'))
        count = cursor.fetchall()
    except OperationalError as err:
        handle_err(err)

    if len(count) == 0:
        count = 0
    else:
        count = count[0][0]
    count += 1

    serial = datetime.strftime('%Y%m%d') + "%04i" % count
    data_tuple = (serial, *data_tuple)

    try:
        conn = db.connect()
        conn.execute("""
            INSERT OR REPLACE INTO VIOLATION_RECORD
                (record_id, bicycle_id, violation, record_datetime,
                 record_place, photo)
            VALUES('%s', '%s', '%s', '%s', '%s', ?)""" % data_tuple[:-1], (photo,))
        conn.execute("""
            INSERT OR REPLACE INTO VIOLATION_SERIAL
                (violation_date, serial_count)
            VALUES('%s', '%i')""" % (datetime.strftime('%Y%m%d'), count))

        conn.commit()
        conn.close()

        return serial
    except OperationalError as err:
        handle_err(err)
        return ''
    return ''


def valid_bicycle(bicycle_id):
    """
    查腳踏車id是否有在資料庫內。

    傳入: bicycle_id: str (腳踏車編號)

    回傳: True 或 False
    """
    if bicycle_id is None:
        return False
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT bicycle_id FROM BICYCLE
                          WHERE bicycle_id = '%s'""" % bicycle_id.upper())
        data = cursor.fetchall()
    except OperationalError as err:
        db.handle_err(err)
    if len(data) == 0:
        return False
    else:
        return True
    return False


def get_violation_by_date(record_date):
    """
    用 datetime.date 查詢當天違規紀錄 (list)。
    如果當天沒有違規，回傳空list。

    傳入: record_datetime: datetime.date (日期)

    回傳: list，內含 tuple(record_datetime: str,
                          record_id: int,
                          bicycle_id: str,
                          violation: str)
    """
    conn = db.connect()
    try:
        cursor = conn.execute("""
            SELECT RECORD_DATETIME, RECORD_ID, BICYCLE_ID, VIOLATION
            FROM VIOLATION_RECORD""")
        date_violation_record = list()
        for row in cursor:
            date_violation_record.append((str(row[0]), int(row[1]),
                                          str(row[2]), str(row[3])))
    except OperationalError as err:
        db.handle_err(err)
    return date_violation_record


def get_violation_by_bicycle(bicycle_id):
    """
    用腳踏車 id 查詢違規紀錄 (list)。
    如果查無 id，會回傳 None；如果有 id 但沒有紀錄，回傳空 list。

    傳入: bicycle_id: str (腳踏車編號)

    回傳: list，內含 record_id: int
    """
    if bicycle_id is None:
        return None
    if not valid_bicycle(bicycle_id):
        return None
    conn = db.connect()
    try:
        cursor = conn.execute("""
            SELECT record_id FROM VIOLATION_RECORD
            WHERE bicycle_id LIKE '%s'""" % bicycle_id.upper())
        bicycle_violation_record = list()
        for row in cursor:
            bicycle_violation_record.append(int(row[0]))
        return bicycle_violation_record
    except OperationalError as err:
        handle_err(err)


def check_step(user_id):
    """
    用使用者 id 查詢進度(step, data)。
    如果查無進度，會回傳 0；如果發生錯誤，會回傳 -1。

    傳入: user_id: str (使用者編號)

    回傳: int
    """
    if user_id is None:
        return -1

    conn = db.connect()

    try:
        cursor = conn.execute("""
            SELECT step FROM USER_STEP
            WHERE user_id LIKE '%s'""" % user_id)

        steps = cursor.fetchall()
        if len(steps) == 0:
            return 0

        step = steps[-1][0]
        return step

    except OperationalError as err:
        handle_err(err)
        return -1

    return -1


def save_step(user_id, step, data):
    """
    儲存紀錄，如果已經有同一個 id 則會取代。
    如果儲存失敗則會回傳 False。

    傳入: user_id: str (使用者編號)
          step: int (步驟)
          data: 一個東西，比如 list

    回傳: True 或 False
    """
    if any(x is None for x in (user_id, step, data)):
        return None

    data_bin = pickle.dumps(data)

    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO USER_STEP (user_id, step, user_data)
            VALUES('%s', '%s', ?)""" % (user_id, step), (data_bin,))

        conn.commit()
        conn.close()

        return True

    except OperationalError as err:
        db.handle_err(err)
        return False

    return False


def load_step(user_id):
    """
    用使用者 id 查詢進度(step, data)。
    如果查無 id，會回傳 None。

    傳入: user_id: str (腳踏車編號)

    回傳: 一個 tuple，內含 int (step) 和 data
    """
    if user_id is None:
        return None

    conn = db.connect()

    try:
        cursor = conn.execute("""
            SELECT step, user_data FROM USER_STEP
            WHERE user_id LIKE '%s'""" % user_id)

        datas = cursor.fetchall()
        if len(datas) == 0:
            return 0

        step, data_bin = datas[-1]
        data = pickle.loads(data_bin)

        return step, data

    except OperationalError as err:
        handle_err(err)
        return None

    return None



def clear_step(user_id):
    """
    用使用者 id 清除進度(step, data)。
    如果發生錯誤，會回傳 False。

    傳入: user_id: str (使用者編號)

    回傳: True 或 False
    """
    if user_id is None:
        return False

    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM USER_STEP
                          WHERE user_id = '%s'""" % (user_id,))

        conn.commit()
        conn.close()

        return True

    except OperationalError as err:
        db.handle_err(err)
        return False

    return False