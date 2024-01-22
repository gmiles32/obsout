import json
import os
import datetime
import shutil
import sys

from ..console import console,logger
from .client import RemoteClient, LocalClient
from .constants import *
from .artifacts import *
from .utils import *

class OutlineClient(RemoteClient):
    """ Remote Outline Client """
    def __init__(self, verbose: bool) -> None:
        super().__init__(verbose)
        if self.verbose:
            self.log.info("Building remote client")
        self.__set_library()

    def __set_library(self) -> None:
        self.collections = self._get_client_collections()
        self._get_client_documents()

    def _refresh_client(self) -> None:
        if self.verbose:
            self.log.info("Refreshed remote client")
        self.__set_library()

    def _get_client_collections(self) -> List[Collection]:
        """ Get collections in wiki """

        json_data = {
        'offset': 0,
        'limit': 100,
        }

        data = json.loads(self._make_request(RequestType.LIST_COLLECTIONS, json_data=json_data).text)
        try:
            collections = [Collection(id=collection['id'],name=collection['name'],documents=[]) for collection in data['data']]
        except KeyError:
            # log.exception("Invalid API Key!")
            sys.exit(1)

        return collections
    
    def _get_client_documents(self) -> List[Document]:
        """ Get documents in wiki """

        for collection in self.collections:
            json_data = {
            'offset': 0,
            'limit': 100, # Need to figure out how to get around this limit
            "sort": "updatedAt",
            "direction": "DESC",
            "collectionId": collection.id,
            }

            data = json.loads(self._make_request(RequestType.LIST_DOCUMENTS, json_data=json_data).text)['data']

            for document in data:
                new_doc = Document(id=document['id'], name=document['title'], parent_collection=collection, mod_date=document['updatedAt'])
                collection.documents.append(new_doc)

    def _get_client_document_mod_date(self, document: Document) -> datetime.datetime:
        """ Get the most current modification date of document on client """
        json_data = {
                "id": document.id
            }

        data = json.loads(self._make_request(RequestType.RETRIEVE_DOCUMENT, json_data=json_data).text)['data']
        mod_date = datetime.datetime.strptime(data['updatedAt'],"%Y-%m-%dT%H:%M:%S.%fZ")
        return mod_date


class Outline(LocalClient):
    """ Local Outline Notes """
    def __init__(self, client: RemoteClient, excluded: List[str], path: str, verbose: bool) -> None:
        super().__init__(verbose)
        if self.verbose:
            self.log.info("Building local client")
        self.client = client
        self.path = path
        self.excluded = excluded
        self.__set_library()

    def __set_library(self) -> None:
        self.collections = self._get_local_collections()
        self._get_local_documents()

    def _refresh_local(self) -> None:
        if self.verbose:
            self.log.info("Refreshing local client")
        self.__set_library()

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
                document = Document(id='',name=os.path.splitext(filename)[0],parent_collection=collection,mod_date='')
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
                missing_documents = [document for document in local_collection.documents if document.name in missing]
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
                if len(missing) <= 0:
                    continue
                missing_documents = [document for document in client_collection.documents if document.name in missing]
                missing_items.append(Collection(id=local_collection.id,name=local_collection.name,documents=missing_documents))

     
        return missing_items
    
    def _get_old_items(self, sync_type: SyncType) -> List[Collection]:
        """ Get list of documents to update based on modification date and sync direction """

        old_items = []
        for collection in self.client.collections:
            old_documents = []
            for document in collection.documents:
                client_mod_date = self.client._get_client_document_mod_date(document)
                local_filename = os.path.join(self.path,collection.name,document.name + '.md')
                if os.path.exists(local_filename):
                    local_mod_date = local_datetime(os.path.join(self.path,collection.name,document.name + '.md'))
                else:
                    continue

                if sync_type == SyncType.REMOTE and client_mod_date < local_mod_date: # older documents in client are wanted
                    diff = local_mod_date - client_mod_date
                    if divmod(diff.days * 86400 + diff.seconds, 60)[1] > 15:
                        old_documents.append(document)
                if sync_type == SyncType.LOCAL and local_mod_date < client_mod_date: # older documents in local repo wanted
                    diff = client_mod_date - local_mod_date
                    if divmod(diff.days * 86400 + diff.seconds, 60)[1] > 15:
                        old_documents.append(document)
            if len(old_documents) > 0:
                old_items.append(Collection(id=collection.id,name=collection.name,documents=old_documents))

        return old_items

    def _create_client_collections(self, collections: List[Collection]) -> None:
        """ Create collection in wiki """
        if os.getenv("COLLECTION_COLOR"):
            color = os.getenv("COLLECTION_COLOR")
        else:
            color = "#FFFFFF"

        client_collection_names = [collection.name for collection in self.client.collections]
        for collection in collections:
            if collection.name in client_collection_names:
                continue
            else:
                json_data = {
                "name": collection.name,
                "description": "",
                "permission": "read_write",
                "color": color,
                "private": False
                }

                self.client._make_request(RequestType.CREATE_COLLECTION, json_data=json_data)

        self.client._refresh_client()

    def _create_client_documents(self, local_collection: Collection) -> None:
        """ Create all documents in a collection based on local documents """

        for document in local_collection.documents:
            file = open(os.path.join(self.path,local_collection.name, document.name + '.md'))

            json_data = {
                "title": document.name,
                "collectionId": [client_collection.id for client_collection in self.client.collections if client_collection.name == local_collection.name][0],
                "text": file.read(),
                "publish": True
            }

            self.client._make_request(RequestType.CREATE_DOCUMENT, json_data=json_data)
        
        self.client._refresh_client()

    def _create_local_collections(self, collections: List[Collection]) -> None:
        """ Create missing client collections in vault """
        for collection in collections:
            try:
                os.mkdir(os.path.join(self.path,collection.name))
            except OSError as error:
                pass
        self._refresh_local()
        

    def _create_local_documents(self, client_collection: Collection) -> None:
        """ Create local documents based on remote collection """

        for document in client_collection.documents:
            json_data = {
                "id": document.id
            }

            data = json.loads(self.client._make_request(RequestType.RETRIEVE_DOCUMENT, json_data=json_data).text)['data']
            file = open(os.path.join(self.path,client_collection.name,document.name + '.md'), 'w')
            file.write(data['text'])
            file.close()

        self._refresh_local()

    def _delete_client_collection(self, collection: Collection) -> None:
        """ Delete specified collections """
        json_data = {
            "id": collection.id,
        }

        self.client._make_request(RequestType.DELETE_COLLECTION, json_data=json_data)

        self.client._refresh_client()

    def _delete_local_collection(self, collection: Collection) -> None:
        """ Delete a collection from local vault """
        try:
            shutil.rmtree(os.path.join(self.path,collection.name))
        except:
            console.log("[bold red]Could not remove local collection {}".format(collection.name))

        self._refresh_local()

    def _delete_client_documents(self, collection: Collection) -> None:
        """ Delete documents in collection on outline client """
        for document in collection.documents:
            json_data = {
                "id": document.id,
                "permanent": False,
            }

            self.client._make_request(RequestType.DELETE_DOCUMENT, json_data=json_data)

        self.client._refresh_client()

    def _delete_local_documents(self, collection: Collection) -> None:
        """ Delete documents in local vault """
        for document in collection.documents:
            try:
                os.remove(os.path.join(self.path,collection.name,document.name + '.md'))
            except OSError as error:
                pass

        self._refresh_local()

    def _update_client_documents(self, collection: Collection) -> None:
        """ Update documents in client """
        for document in collection.documents:
            file = open(os.path.join(self.path,collection.name,document.name + '.md'), 'r')
            json_data = {
                "id": document.id,
                "title": document.name,
                "text": file.read(),
                "append": False,
                "publish": True,
            }

            self.client._make_request(RequestType.UPDATE_DOCUMENT, json_data=json_data)
        
        self.client._refresh_client()

    def _update_local_documents(self, collection: Collection) -> None:
        """ Update local documents based on wiki documents """
        self._create_local_documents(collection) # Does the same thing

    def _find_document(self, collection_name: str, document_name: str) -> Collection:
        """ Find a document with a specified collection and name """
        collection = [collection for collection in self.client.collections if collection.name == collection_name]
        if len(collection) == 0:
            return None
        document = [document for document in collection[0].documents if document.name == document_name]
        
        return Collection(id=collection[0].id,name=collection[0].name,documents=document)

    def sync(self, sync_type: SyncType) -> None:
        """ Create and delete collections/documents depending on status """
        missing_items = self._get_missing_items(sync_type=sync_type)
        if sync_type == SyncType.REMOTE:
            self._create_client_collections(missing_items)
            console.print("Created missing collections in Outline")
            for collection in missing_items:
                self._create_client_documents(collection)
            console.print("Created missing documents in Outline")
            old_items = self._get_old_items(sync_type=sync_type)
            for collection in old_items:
                self._update_client_documents(collection)
            console.print("Updated documents in Outline")

        elif sync_type == SyncType.LOCAL:
            self._create_local_collections(missing_items)
            console.print("Created missing collections in vault")
            for collection in missing_items:
                self._create_local_documents(collection)
            console.print("Created missing documents in vault")
            old_items = self._get_old_items(sync_type=sync_type)
            for collection in old_items:
                self._update_local_documents(collection)
            console.print("Updated documents in vault")

    def delete(self, collection_name: str, document_name: str, all: bool):
        """ Delete a document from Outline client and local vault """
        collection = self._find_document(collection_name=collection_name,document_name=document_name)

        if collection is None:
            console.print("[bold red]Unable to find {}/{}, check collection/document name and try again".format(collection_name,document_name))
            return
        if all:
            self._delete_client_collection(collection)
            console.print("[bold blue]Deleted collection '{}' from client".format(collection_name))
            self._delete_local_collection(collection)
            console.print("[bold blue]Deleted collection '{}' from vault".format(collection_name))
        else:
            self._delete_client_documents(collection)
            console.print("[bold blue]Deleted document '{}/{}' from client".format(collection_name,document_name))
            self._delete_local_documents(collection)
            console.print("[bold blue]Deleted document '{}/{}' from vault".format(collection_name,document_name))

