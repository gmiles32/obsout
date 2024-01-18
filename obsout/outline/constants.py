from enum import Enum
import os

class RequestType(Enum):
    LIST_COLLECTIONS = "/api/collections.list"
    LIST_DOCUMENTS = "/api/documents.list"

    CREATE_COLLECTION = "/api/collections.create"
    DELETE_COLLECTION = "/api/collections.delete"
    
    EXPORT_COLLECTION = "/api/collections.export"

    CREATE_DOCUMENT = "/api/documents.create"
    RETRIEVE_DOCUMENT = "/api/documents.info"
    DELETE_DOCUMENT = "/api/documents.delete"
    ARCHIVE_DOCUMENT = "/api/documents.archive"
    UPDATE_DOCUMENT = "/api/documents.update"

class OutlineItems(Enum):
    COLLECTIONS = "collections"
    DOCUMENTS = "documents"

class SyncType(Enum):
    LOCAL = "local"
    REMOTE = "remote"