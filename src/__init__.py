from src.client import BaseClientIterator
from src.backends.mongo_backend import MongoCollectionsBackend
from src.backends.couch_backend import CouchCollectionsBackend


class MongoDBList(BaseClientIterator):

    backend_class = MongoCollectionsBackend


class CouchDBList(BaseClientIterator):

    backend_class = CouchCollectionsBackend