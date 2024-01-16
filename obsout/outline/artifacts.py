from typing import List
from .constants import *

class Document():
    def __init__(self,
                 id: str,
                 name: str,
                 parent_id: str,
                 ) -> None:
        self.id = id
        self.name = name
        self.parent_id = parent_id

class Collection():
    def __init__(self,
                 id: str,
                 name: str,
                 documents: List[Document],
                 from_client: bool
                ) -> None:
        
        self.id = id
        self.name = name
        self.documents = documents
        self.from_client = from_client