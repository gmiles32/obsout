import os
import json
import requests
from dotenv import load_dotenv

from outline.client import *
from outline.constants import *

def main():
    
    load_dotenv()
    
    # headers = {
    #     # Already added when you pass json=
    #     # 'content-type': 'application/json',
    #     'accept': 'application/json',
    # }

    # json_data = {
    #     'token': os.getenv("OUTLINE_API_KEY"),
    #     'offset': 0,
    #     'limit': 25,
    # }

    # response = requests.post('{}/api/collections.list'.format(os.getenv("OUTLINE_BASE_URL")), headers=headers, json=json_data)
    # print(response.text)

    client = RemoteClient()
    response = client.make_request(RequestType.LIST_COLLECTIONS)
    collections = json.loads(response.text)
    print("ID: {}\nName: {}".format(collections['data'][0]['id'], collections['data'][0]['name']))

if __name__ == "__main__":
    main()