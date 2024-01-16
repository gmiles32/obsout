import requests
import json
import os
from .client import RemoteClient, LocalClient
from .constants import *
from .artifacts import *

class OutlineClient(RemoteClient):
    """ Remote Outline Client """
    def __init__(self, verbose: bool) -> None:
        super().__init__(verbose)
        self.__set_library()

    def __set_library(self) -> None:
        self.collections = self._get_client_collections()
        self.documents = self._get_client_documents()

    def _get_client_collections(self) -> List[Collection]:
        """ Get collections in wiki """

        json_data = {
        'token': os.getenv("OUTLINE_API_KEY"),
        'offset': 0,
        'limit': 0,
        }

        data = json.loads(self._make_request(RequestType.LIST_COLLECTIONS, json_data=json_data).text)

        collections = [Collection(id=collection['id'],name=collection['name'],documents=[],from_client=True) for collection in data['data']]
        return collections
    
    def _get_client_documents(self) -> List[Document]:
        """ Get documents in wiki """

        documents = []
        for collection in self.collections:
            json_data = {
            'token': os.getenv("OUTLINE_API_KEY"),
            'offset': 0,
            'limit': 0,
            "sort": "updatedAt",
            "direction": "DESC",
            "collectionId": collection.id,
            "template": True
            }

            data = json.loads(self._make_request(RequestType.LIST_DOCUMENTS, json_data=json_data).text)['data']
            for document in data:
                documents.append(Document(id=document['id'], name=document['title'], parent_id=['collectionId']))

        return documents
    
    def _create_client_collection(self, name: str, color="#FFFFFF"):
        """ Create collection in wiki """
        # This will produce duplicates of collections with unique IDs, I need a way of creating maps

        json_data = {
        "token": os.getenv("OUTLINE_API_KEY"),
        "name": name,
        "description": "",
        "permission": "read_write",
        "color": color,
        "private": "false"
        }

        data = json.loads(self._make_request(RequestType.CREATE_COLLECTION, json_data=json_data).text)
        return data

class Outline(LocalClient):
    """ Local Outline Notes """
    def __init__(self, client: RemoteClient, excluded: List[str], path: str, verbose: bool) -> None:
        super().__init__(verbose)
        self.client = client
        self.path = path
        self.excluded = excluded
        self.__set_library()

    def __set_library(self) -> None:
        self.collections = self._get_local_collections()

    def _get_local_collections(self) -> List[Collection]:
        """ List collections in vault """
        collections = []

        for collection in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path,collection)) and not collection.startswith('.'):
                if collection not in self.excluded:
                    collections.append(Collection(id='',name=collection,documents=[],from_client=False))

        return collections
    
    def _get_local_documents(self) -> List[Document]:
        pass

    def _get_missing_items(self, item: OutlineItems, sync_type: SyncType):
        """ Get a list of missing items depending on local or remote sync """
        local_items = getattr(self, item.value)
        client_items = getattr(self.client, item.value)

        local_item_names = set(item.name for item in local_items)
        client_item_names = set(item.name for item in client_items)

        if sync_type == SyncType.REMOTE:
            missing = local_item_names - client_item_names
            missing_items = [item for item in local_items if item.name in missing]
        else:
            missing = client_item_names - local_item_names
            missing_items = [item for item in client_items if item.name in missing]
        
        return missing_items

