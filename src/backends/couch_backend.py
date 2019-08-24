import uuid
from src.backends import BaseCollectionsBackend
try:
    import Couch
except ImportError:
    pass


class CouchCollectionsBackend(BaseCollectionsBackend):

    _db_name_prefix = "couch_collections_db"

    def __init__(self, host='localhost', port=6379, db=0, profiling_level=0):

        from couchdb import Server
        self.server = Server()

        self.db_name = "{}_{}".format(self._db_name_prefix, uuid.uuid4().hex)
        self.db = self.server.create(self.db_name)

        self.doc_index_id = {}

    def __del__(self):

        del self.server[self.db_name]

    def __delitem__(self, index):

        obj = self[index]
        #self.db.delete_one({"index": index })
        #self.db.update_many({"index": {"$gt": index }}, {"$inc": {"index": -1 }})

    def _get(self, index):

        doc_id = self.doc_index_id[index]
        obj = self.db.get(doc_id)
        return obj

    def __getitem__(self, index):

        obj = self._get(index)
        if obj is None:
            raise IndexError

        return obj["value"]

    def __iter__(self):

        for obj in self.db.view('_all_docs'):
            yield self.db.get(obj.id)["value"]

    def _slice(self, index):

        indices = index.indices(len(self))
        start, stop, step = indices
        indices_numbers = range(start, stop, step)

        #objs = (obj["value"] for obj in self.db.find({"index": {"$in": indices_numbers }}))
        #return objs
        return []

    def _save(self, index, value):

        doc_id, rev = self.db.save({"value": value, "index": index })
        self.doc_index_id[index] = doc_id

    def __setitem__(self, index, value):

        obj = self._get(index)
        obj["value"] = value
        self.db.save(obj)

    def __len__(self):

        return self.db.info()["doc_count"]

    def insert(self, index, value):

        self._save(index, value)

    def extend(self, iterable):

        length = len(self)
        for index, value in enumerate(iterable):
            self.insert(index + length, value)
