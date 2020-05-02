import json

from datetime import date, datetime

with open('data/data_matter.json') as js:
    DATA = json.load(js)
    MATTERS = DATA.get('MATTERS')

with open('data/data_teacher.json') as js:
    DATA = json.load(js)
    TEACHERS = DATA.get('TEACHERS')

with open('data/data_class.json') as js:
    DATA = json.load(js)
    CLASS = DATA.get('CLASS')

# Script starts here
if __name__ == '__main__':
    pass

