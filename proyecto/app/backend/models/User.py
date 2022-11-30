from pymongo import MongoClient
from pymongo.collation import Collation

db = MongoClient().test
collection = db.create_collection('User',
                                  collation=Collation({
                                    "nombre",
                                    "apellido", 
                                  }))
