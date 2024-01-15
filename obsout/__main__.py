import os
import json
import requests
from dotenv import load_dotenv

from outline.outline import *
from outline.constants import *
from outline.artifacts import *

def main():
    
    load_dotenv()

    client = OutlineClient(verbose=False)
    remote_collections = client.get_remote_collections()
    for collection in remote_collections:
        print("ID: {}\nName: {}\n".format(collection.id, collection.name))

if __name__ == "__main__":
    main()