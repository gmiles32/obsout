import requests
import json
from .client import RemoteClient, LocalClient
from .constants import *
from .artifacts import *

class OutlineClient(RemoteClient):
    """ Remote Outline Client """
    def __init__(self, verbose: bool) -> None:
        super().__init__()
        self.verbose = verbose

    def _make_request(self, request_type: RequestType, json_data: dict) -> requests.Response:
        """ Make POST request to API"""
        json_data = JSON_DATA[request_type]
        response = requests.post(self.base_url + request_type.value, headers=self.headers, json=json_data)
        return response
    
    def get_remote_collections(self):
        """ Get collections in wiki """

        json_data = {
        'token': os.getenv("OUTLINE_API_KEY"),
        'offset': 0,
        'limit': 25,
        },

        data = json.loads(self._make_request(RequestType.LIST_COLLECTIONS, json_data=json_data).text)

        collections = [Collection(id=collection['id'],name=collection['name']) for collection in data['data']]
        return collections

class Outline(LocalClient):
    """ Local Outline Notes """
    def __init__(self, path , excluded, verbose: bool) -> None:
        super().__init__()
        self.path = path
        self.excluded = excluded
        self.verbose = verbose
