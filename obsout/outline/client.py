import os
import requests

from abc import ABC, abstractmethod

from .constants import *

class Client(ABC):
    ...

class RemoteClient(Client):
    @abstractmethod
    def __init__(self) -> None:
        self.key = os.getenv("OUTLINE_API_KEY")
        self.base_url = os.getenv("OUTLINE_BASE_URL")
        self.headers = {'accept': 'application/json',}

    def _make_request(self, request_type: RequestType, json_data: dict) -> requests.Response:
        pass

class LocalClient(Client):
    @abstractmethod
    def __init__(self) -> None:
        pass