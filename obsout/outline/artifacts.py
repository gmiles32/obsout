from typing import List
from .constants import *

class Document():
    def __init__(self,
                 id: str,
                 name: str,
                 parent_collection,
                 mod_date: str
                 ) -> None:
        self.id = id
        self.name = name
        self.parent_collection = parent_collection
        self.mod_date = mod_date

class Collection():
    def __init__(self,
                 id: str,
                 name: str,
                 documents: List[Document],
                ) -> None:
        
        self.id = id
        self.name = name
        self.documents = documents
