from typing import Optional, Dict, Any, List, Tuple

import numpy as np
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


class DatabaseAPI(Database):
    """define the CURD operations for database"""

    def __init__(self, db_name: str, collection_name: str) -> None:
        super().__init__(db_name, collection_name)

    """
    write methods:
    
    write_table_obs_by_var : write obs_by_var data into database
    
    write_table_gene_by_var : write gene_by_var data into database
    
    write_metadata : write metadata into database
    """

    def write_table_obs_by_var(self,
                               matrix: np.ndarray,
                               overwrite: bool = False,
                               verbose: bool = True) -> Optional[str]:
        collection_name = "obs_by_var_table"
        if collection_name in self.db.list_collection_names() and not overwrite:
            alarming = "Collection already exists, to overwrite it please use overwrite = True"
            if verbose:
                print(alarming)
            return alarming
        if collection_name in self.db.list_collection_names() and overwrite:
            self.db.drop_collection(collection_name)

        self.collection = self.db[collection_name]
        documents = []
        num_of_documents = 0
        for i in range(matrix.shape[0]):
            document = {
                "obs_id": i,
                "obs_value": matrix[i].tolist(),
            }
            documents.append(document)
            num_of_documents += 1

        self.insert_many(documents)

        self.create_index([("obs_id", pymongo.ASCENDING)], unique=True)

        msg = f"{num_of_documents} documents already loaded in collection {collection_name}"
        return msg

    def write_table_gene_by_var(self,
                                matrix: np.ndarray,
                                overwrite: bool = False,
                                genes: List[Optional[str]] = [],
                                verbose: bool = True) -> Optional[str]:
        collection_name = "gene_by_var_table"
        if collection_name in self.db.list_collection_names() and not overwrite:
            alarming = "Collection already exists, to overwrite it please use overwrite = True"
            if verbose:
                print(alarming)
            return alarming
        if collection_name in self.db.list_collection_names() and overwrite:
            self.db.drop_collection(collection_name)

        self.collection = self.db[collection_name]
        documents = []
        num_of_documents = 0
        for i in range(matrix.shape[0]):
            document = {
                "gene_id": genes[i],
                "gene_value": matrix[i].tolist(),
            }
            documents.append(document)
            num_of_documents += 1

        self.insert_many(documents)

        self.create_index([("gene_id", pymongo.ASCENDING)], unique=True)

        msg = f"{num_of_documents} documents already loaded in collection {collection_name}"
        return msg

    # default write method is to append the metadata
    def write_metadata(self,
                       metadata: Optional[Dict[str, list]] = None,
                       metadata_name: str = "metadata",
                       overwrite: bool = False,
                       verbose: bool = True) -> Optional[str]:
        collection_name = metadata_name
        if collection_name in self.db.list_collection_names() and overwrite:
            self.db.drop_collection(collection_name)
            self.collection = self.db[collection_name]
        if collection_name in self.db.list_collection_names() and not overwrite:
            alarming = "Collection already exists, to overwrite it please use overwrite = True"
            if verbose:
                print(alarming)
            return alarming
        if collection_name not in self.db.list_collection_names():
            self.collection = self.db[collection_name]

        documents = []
        num_of_documents = 0
        for key, value in metadata.items():
            document = {
                'key': key,
                "value": value
            }
            documents.append(document)
            num_of_documents += 1

        self.insert_many(documents)

        msg = f"{num_of_documents} documents already loaded in collection {collection_name}"
        return msg

    """
    read methods: read one document at a time
    
    read_table_obs_by_var : read the obs_by_var table from the database.
    paras: obs_id : type of int
    
    read_table_gene_by_var : read the gene_by_var table from the database
    paras: gene_id : gene name.
    
    read_metadata : read the metadata table from the database.
    paras: key,
           metadata_name
    """

    def read_table_obs_by_var(self, obs_id: int) -> np.ndarray:
        collection_name = "obs_by_var_table"
        self.collection = self.db[collection_name]
        res = self.find_one({"obs_id": obs_id})
        return res['obs_value']

    def read_table_gene_by_var(self, gene_id: int) -> np.ndarray:
        collection_name = "gene_by_var_table"
        self.collection = self.db[collection_name]
        res = self.find_one({"gene_id": gene_id})
        return res["gene_value"]

    def read_metadata(self,
                      key: str,
                      metadata_name: str = "metadata",
                      ) -> list:
        collection_name = metadata_name
        self.collection = self.db[collection_name]
        res = self.find_one({"key":key})
        return res['value']


    """
    query methods: allow querying many documents at a time.
    
    query_table_obs_by_var: query the obs_by_var table from the database.
    
    query_table_gene_by_var: query the gene_by_var table from the database.
    
    query_metadata: query the metadata table from the database.
    :param keys: a list of keys to query
    """

    # accellerate the query process
    def query_table_obs_by_var(self,
                               obs_ids : List[int]) -> np.ndarray:
        collection_name = "obs_by_var_table"
        self.collection = self.db[collection_name]
        res = self.find_many({"obs_id": {"$in": obs_ids}})
        return np.array([r['obs_value'] for r in res])

    def query_table_gene_by_var(self,
                                gene_ids : List[str]) -> np.ndarray:
        collection_name = "gene_by_var_table"
        self.collection = self.db[collection_name]
        res = self.find_many({"gene_id": {"$in": gene_ids}})
        return np.array([r['gene_value'] for r in res])

    def query_metadata(self,
                       keys : List[str],
                       metadata_name: str = "metadata") -> Dict[str, list]:
        collection_name = metadata_name
        self.collection = self.db[collection_name]
        res = self.find_many({"key": {"$in": keys}})
        return {r['key']: r['value'] for r in res}

    def delete_table_obs_by_var(self, keys : List[int]):
        collection_name = "obs_by_var_table"
        self.collection = self.db[collection_name]
        self.delete_many({"obs_id": {"$in": keys}})
        msg = f"Documents with keys {keys} have been deleted"
        return msg

    def delete_table_gene_by_var(self, keys : List[str]):
        collection_name = "gene_by_var_table"
        self.collection = self.db[collection_name]
        self.delete_many({"gene_id": {"$in": keys}})
        msg = f"Documents with keys {keys} have been deleted"
        return msg


    def delete_metadata(self, keys : List[str], metadata_name: str = "metadata", all = False):
        if all:
            self.db.drop_collection(metadata_name)
            msg = f"Collection {metadata_name} has been deleted"
            return msg
        collection_name = metadata_name
        self.collection = self.db[collection_name]
        self.delete_many({"key": {"$in": keys}})
        msg = f"Documents with keys {keys} have been deleted"
        return msg

