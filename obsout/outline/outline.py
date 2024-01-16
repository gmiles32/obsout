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
        self._get_client_documents()

    def _refresh_client(self) -> None:
        self.__set_library()

    def _get_client_collections(self) -> List[Collection]:
        """ Get collections in wiki """

        json_data = {
        'token': os.getenv("OUTLINE_API_KEY"),
        'offset': 0,
        'limit': 25,
        }

        data = json.loads(self._make_request(RequestType.LIST_COLLECTIONS, json_data=json_data).text)

        collections = [Collection(id=collection['id'],name=collection['name'],documents=[]) for collection in data['data']]
        return collections
    
    def _get_client_documents(self) -> List[Document]:
        """ Get documents in wiki """

        for collection in self.collections:
            json_data = {
            'token': os.getenv("OUTLINE_API_KEY"),
            'offset': 0,
            'limit': 25, # Need to figure out how to get around this limit
            "sort": "updatedAt",
            "direction": "DESC",
            "collectionId": collection.id,
            }

            data = json.loads(self._make_request(RequestType.LIST_DOCUMENTS, json_data=json_data).text)['data']

            for document in data:
                new_doc = Document(id=document['id'], name=document['title'], parent_collection=collection)
                collection.documents.append(new_doc)

    
    def _create_client_collection(self, collections: List[Collection], color="#FFFFFF"):
        """ Create collection in wiki """
        # This will produce duplicates of collections with unique IDs, I need a way of creating maps

        for collection in collections:
            json_data = {
            "token": os.getenv("OUTLINE_API_KEY"),
            "name": collection.name,
            "description": "",
            "permission": "read_write",
            "color": color,
            "private": "false"
            }

            # data = json.loads(self._make_request(RequestType.CREATE_COLLECTION, json_data=json_data).text)
            json.loads(self._make_request(RequestType.CREATE_COLLECTION, json_data=json_data).text)

    

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
        self._get_local_documents()

    def _get_local_collections(self) -> List[Collection]:
        """ List collections in vault """
        collections = []

        for collection in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path,collection)) and not collection.startswith('.'):
                if collection not in self.excluded:
                    collections.append(Collection(id='',name=collection,documents=[]))

        return collections
    
    def _get_local_documents(self) -> List[Document]:
        """ List documents in collections in vault """

        for collection in self.collections:
            for filename in os.listdir(os.path.join(self.path,collection.name)):
                document = Document(id='',name=os.path.splitext(filename)[0],parent_collection=collection)
                collection.documents.append(document)
    
    def _get_missing_items(self, sync_type: SyncType):
        """ Get a list of missing items depending on local or remote sync """

        local_collection_names = set(collections.name for collections in self.collections)
        client_collection_names = set(collections.name for collections in self.client.collections)

        if sync_type == SyncType.REMOTE:
            missing = local_collection_names - client_collection_names
            missing_items = [collection for collection in self.collections if collection.name in missing]
            present = local_collection_names - missing
            for collection_name in present:
                local_collection = [collection for collection in self.collections if collection.name == collection_name][0]
                client_collection = [collection for collection in self.client.collections if collection.name == collection_name][0]
                
                local_document_names = set(document.name for document in local_collection.documents)
                client_document_names = set(document.name for document in client_collection.documents)
                
                missing = local_document_names - client_document_names
                if len(missing) == 0:
                    continue
                missing_documents = [document for document in self.collections if document.name in missing]
                missing_items.append(Collection(id=local_collection.id,name=local_collection.name,documents=missing_documents))
        else:   
            missing = client_collection_names - local_collection_names # names of missing collections from local
            missing_items = [collection for collection in self.client.collections if collection.name in missing]
            present = client_collection_names - missing # names of collections only present on local (want present on both)
            for collection_name in present:
                local_collection = [collection for collection in self.collections if collection.name == collection_name][0]
                client_collection = [collection for collection in self.client.collections if collection.name == collection_name][0]
                
                local_document_names = set(document.name for document in local_collection.documents)
                client_document_names = set(document.name for document in client_collection.documents)
                
                missing = client_document_names - local_document_names
                if len(missing) == 0:
                    continue
                missing_documents = [document for document in self.client.collections if document.name in missing]
                missing_items.append(Collection(id=local_collection.id,name=local_collection.name,documents=missing_documents))

     
        return missing_items

