import os
from typing import Optional, Union, Dict, Any, List

import numpy as np
import pandas as pd
import pymongo

Document = Dict[str, Any]
Query = Dict[str, Any]
Update = Dict[str, Any]

class Database(object):
    def __init__(self, db_name: str, collection_name: str) -> None:
        self.client: pymongo.MongoClient = pymongo.MongoClient()
        self.db: pymongo.database.Database = self.client[db_name]
        self.collection: pymongo.collection.Collection = self.db[collection_name]

    def insert_one(self, document: Document) -> Any:
        return self.collection.insert_one(document)

    def insert_many(self, documents: List[Document]) -> Any:
        return self.collection.insert_many(documents)

    def find_one(self, query: Query, projection: Optional[Dict[str, Any]] = None) -> Optional[Document]:
        return self.collection.find_one(query, projection)

    def find_many(self, query: Query, projection: Optional[Dict[str, Any]] = None) -> List[Document]:
        return list(self.collection.find(query, projection))

    def update_one(self, query: Query, update: Update) -> Any:
        return self.collection.update_one(query, update)

    def update_many(self, query: Query, update: Update) -> Any:
        return self.collection.update_many(query, update)

    def delete_one(self, query: Query) -> Any:
        return self.collection.delete_one(query)

    def delete_many(self, query: Query) -> Any:
        return self.collection.delete_many(query)

    def count_documents(self, query: Query) -> int:
        return self.collection.count_documents(query)

    def create_index(self, keys: List[Tuple[str, int]], **kwargs: Any) -> str:
        return self.collection.create_index(keys, **kwargs)

    def drop_index(self, index_name: str) -> Any:
        return self.collection.drop_index(index_name)

    def list_indexes(self) -> Any:
        return self.collection.list_indexes()