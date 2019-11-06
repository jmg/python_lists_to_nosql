import time
from src.backends import BaseCollectionsBackend
try:
    from pymongo import MongoClient
except ImportError:
    pass


class MongoCollectionsBackend(BaseCollectionsBackend):

    _db_name_name_prefix = "__mongo_collections_db"
    _collections_name = "__mongo_collections_collection"

    def __init__(self, profiling_level=0):

        super(MongoCollectionsBackend, self).__init__()

        db_name_sufix = "{:.5f}".format(time.time()).replace(".", "_")
        self.db_name = "{}_{}".format(self._db_name_name_prefix, db_name_sufix)

        self.mongo_client = MongoClient()
        self.db = self.mongo_client[self.db_name]
        self.db.set_profiling_level(profiling_level)

        self.db_collection = self.db[self._collections_name]

    def __del__(self):

        self.mongo_client.drop_database(self.db_name)

    def __delitem__(self, index):

        obj = self[index]
        self.db_collection.delete_one({"index": index })
        self.db_collection.update_many({"index": {"$gt": index }}, {"$inc": {"index": -1 }})

    def __getitem__(self, index):

        obj = self.db_collection.find_one({"index": index })
        if obj is None:
            raise IndexError

        return obj["value"]

    def __iter__(self):

        for obj in self.db_collection.find():
            yield obj["value"]

    def _slice(self, index):

        indices = index.indices(len(self))
        start, stop, step = indices
        indices_numbers = range(start, stop, step)

        objs = (obj["value"] for obj in self.db_collection.find({"index": {"$in": indices_numbers }}))
        return objs

    def __setitem__(self, index, value):

        obj = self[index]
        self.db_collection.update_one({"index": index }, {"$set": {"value": value}})

    def __len__(self):

        return self.db_collection.count()

    def insert(self, index, value):

        self.db_collection.insert_one({"value": value, "index": index })

    def extend(self, iterable):

        length = len(self)
        for index, value in enumerate(iterable):
            self.insert(index + length, value)
