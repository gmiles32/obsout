import os
import json
import requests

from .constants import *

class RemoteClient():
    """ """
    def __init__(self) -> None:
        self.key = os.getenv("OUTLINE_API_KEY")
        self.base_url = os.getenv("OUTLINE_BASE_URL")
        self.headers = {'accept': 'application/json',}

    def make_request(self, request_type: RequestType):
        """ Make POST request to API """
        json_data = JSON_DATA[request_type]
        response = requests.post(self.base_url + request_type.value, headers=self.headers, json=json_data)
        return response