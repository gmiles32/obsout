from enum import Enum

class RequestType(Enum):
    LIST_COLLECTIONS = "/api/collections.list"
    LIST_DOCUMENTS = "/api/documents.list"

    CREATE_COLLECTION = "/api/collections.create"
    DELETE_COLLECTION = "/api/collections.delete"
    
    CREATE_DOCUMENT = "/api/documents.create"
    RETRIEVE_DOCUMENT = "/api/documents.info"
    DELETE_DOCUMENT = "/api/documents.delete"
    UPDATE_DOCUMENT = "/api/documents.update"

class SyncType(Enum):
    LOCAL = "local"
    REMOTE = "remote"