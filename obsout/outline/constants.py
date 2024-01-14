from enum import Enum
import os

class RequestType(Enum):
    LIST_COLLECTIONS = "/api/collections.list"
    CREATE_COLLECTION = "/api/collections.create"

JSON_DATA = {
    RequestType.LIST_COLLECTIONS: {
        'token': os.getenv("OUTLINE_API_KEY"),
        'offset': 0,
        'limit': 25,
    },
}

