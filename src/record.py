import pickle
import os
from models.base import Event

BASE_DIR = os.getcwd()

class Record:
    def __init__(self):
        db = self.__load()
        if db:
            self.records = pickle.loads(db.read())
            db.close()
            print(self.records)
        else:
            self.records = dict()

    def __repr__(self) -> str:
        return "<class Record([{}])>".format(self.records)

    def create(self, id, structure):
        if not self.get(id):
            self.records[id] = structure
            self.__sync()
            return True

    def set_value(self, id, key, value):
        record = self.get(id)
        if record:
            try:
                record[key] = value
            except KeyError:
                return False
            return True

    def get(self, id):
        if id in self.records.keys():
            return self.records[id]

    def get_value(self, id, key):
        record = self.get(id)
        if record:
            try:
                record[key]
            except KeyError:
                return False
            return record[key]


    def get_many(self, *ids):
        records = dict()
        for id in ids:
            record = self.get(id)
            if record:
                records[id] = record
        self.__sync()
        return records

    def update(self, id, structure):
        if self.get(id):
            self.records[id] = structure
            self.__sync()
            return True

    def delete(self, id):
        if self.get(id):
            del self.records[id]
            self.__sync()
            return True
    def __sync(self):
        with open(BASE_DIR+'/redis.pkl', 'wb') as db:
            pickle.dump(self.records, db)

    def __load(self):
        db = None
        try:
            db = open(BASE_DIR+'/redis.pkl', 'rb')
        except IOError:
            return False
        return db

    def reset(self):
        self.records = dict()
        self.__sync()

    