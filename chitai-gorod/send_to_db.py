from pymongo.mongo_client import MongoClient
import datetime

url = 'mongodb://localhost:27017'

client = MongoClient(url)
db = client['chitaigoroddb']
collection_products = db['products']
collection_date = db['dates']

# Бля, мне впадлу объянсять это

def get_dates():
    return [date for date in collection_date.find({})]

def get_last_date():
    return collection_date.find_one(sort=[('_id', -1)])

def get_products_by_number(parsing_number):
    return [product for product in collection_products.find({ 'parsing_number': parsing_number })]

def send_to_db(items):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_parsing = get_last_date()

    if last_parsing:
        parsing_number = last_parsing['parsing_number'] + 1
    else:
        parsing_number = 1

    collection_date.insert_one({ 
        'date': date, 
        'parsing_number': parsing_number,
        'numb_of_products': len(items)
    })

    for item in items:
        item['parsing_number'] = parsing_number

    collection_products.insert_many(items)
        