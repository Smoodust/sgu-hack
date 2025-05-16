from pymongo import MongoClient
from datetime import datetime


# Подключение к локальному серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['sgu_hack']
collection_name = 'logs'

if collection_name not in db.list_collection_names():
    db.create_collection(
        collection_name,
        validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['datetime', 'is_checked', 'is_worked'],
                'properties': {
                    'datetime': {
                        'bsonType': 'date',
                        'description': 'Дата и время, обязательное поле'
                    },
                    'json': {
                        'bsonType': 'object',
                        'description': 'JSON данные'
                    },
                    'is_checked': {
                        'bsonType': 'bool',
                        'description': 'Флаг проверки, обязательное поле'
                    },
                    'is_worked': {
                        'bsonType': 'bool',
                        'description': 'Флаг работы, обязательное поле'
                    }
                }
            }
        }
    )

collection = db['logs']
document = {
    'datetime': datetime.now(),  # Текущая дата и время
    'json': {'key': 'value', 'number': 42},  # Произвольные JSON данные
    'is_checked': True,
    'is_worked': False
}
print(client.list_database_names())