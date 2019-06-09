import database as db
from datetime import datetime


# 重設資料庫
print('Recreate the database with dummies:', db.recreate_database(dummy=True))

# 查詢腳踏車編號
print('Is b04106021 a bicycle:', db.valid_bicycle('b04106021'))
print('Is b04106021-01 a bicycle:', db.valid_bicycle('b04106021-01'))

# 正常新增
with open('bicycle_example.jpg', 'rb') as image:
    print('Add a new violation:', db.add_violation('b04106021-01', '亂停車',
        datetime(2019, 6, 8, 12, 0, 0), '管院門口', image.read()))

# 分步驟新增
# step 1
user_id = 'a123'
data_tuple = ('b04106021-01', '亂停車', datetime(2019, 6, 8, 12, 0, 0), '管院門口')

cur_step = db.check_step(user_id)  # 0
if cur_step == 0:
    step = 1
    data_list = list(data_tuple)
    db.save_step(user_id, step, data_list)

# step 2
user_id = 'a123'
with open('bicycle_example.jpg', 'rb') as image:
    image_data = image.read()

cur_step = db.check_step(user_id)
if cur_step == 1:
    data_list = db.load_step(user_id)[1]
    data_list.append(image_data)
    print('Add a new violation with list:', db.add_violation_with_list(data_list))
    db.clear_step(user_id)

print('Get b04106021-01 violation:', db.get_violation_by_bicycle('b04106021-01'))
