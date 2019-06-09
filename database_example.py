import database as db
from datetime import datetime



print('Recreate the database with dummies', db.recreate_database(dummy=True))
print('Is b04106021 a bicycle:', db.valid_bicycle('b04106021'))
print('Is b04106021-01 a bicycle:', db.valid_bicycle('b04106021-01'))

with open('bicycle_example.jpg', 'rb') as image:
    print('Add a new violation:', db.add_violation('b04106021-01', '亂停車',
        datetime(2019, 6, 8, 12, 0, 0), '管院門口', image.read()))
print('Get b04106021-01 violation:', db.get_violation_by_bicycle('b04106021-01'))