from typing import List

class Collection():
    def __init__(self,
                 id: str,
                 name: str
                 ) -> None:
        
        self.id = id
        self.name = name

class Document():
    def __init__(self,
                 id: str,
                 name: str
                 ) -> None:
        self.id = id
        self.name = name