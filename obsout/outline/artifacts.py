from typing import List
from .constants import *

class Document():
    def __init__(self,
                 id: str,
                 name: str,
                 parent_collection,
                 ) -> None:
        self.id = id
        self.name = name
        self.parent_collection = parent_collection

class Collection():
    def __init__(self,
                 id: str,
                 name: str,
                 documents: List[Document],
                ) -> None:
        
        self.id = id
        self.name = name
        self.documents = documents
