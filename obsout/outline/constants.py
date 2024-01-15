from enum import Enum
import os

class RequestType(Enum):
    LIST_COLLECTIONS = "/api/collections.list"
    LIST_DOCUMENTS = "/api/documents.list"

    CREATE_COLLECTION = "/api/collections.create"
    DELETE_COLLECTION = "/api/collections.delete"
    
    EXPORT_COLLECTION = "/api/collections.export"
    EXPORT_DOCUMENT = "/api/documents.export"
    IMPORT_DOCUMENT = "/api/documents.import"

    UPDATE_DOCUMENT = "/api/documents.update"

JSON_DATA = {
    RequestType.LIST_COLLECTIONS: {
        'token': os.getenv("OUTLINE_API_KEY"),
        'offset': 0,
        'limit': 25,
    },
}