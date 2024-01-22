import os
import requests

from abc import ABC, abstractmethod

from .constants import *

class Client(ABC):
    ...

class RemoteClient(Client):
    @abstractmethod
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.key = os.getenv("OUTLINE_API_KEY")
        self.base_url = os.getenv("OUTLINE_BASE_URL")
        self.headers = {
            'Authorization': 'Bearer ' + os.getenv('OUTLINE_API_KEY'),
            'accept': 'application/json',
        }

    def _make_request(self, request_type: RequestType, json_data: dict) -> requests.Response:
        """ Make POST request to API"""
        response = requests.post(self.base_url + request_type.value, headers=self.headers, json=json_data)
        return response
    
class LocalClient(Client):
    @abstractmethod
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose