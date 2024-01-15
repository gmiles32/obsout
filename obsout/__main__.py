import os
import json
import requests
from dotenv import load_dotenv
import yaml

from outline.outline import *
from outline.constants import *
from outline.artifacts import *

def main():
    
    load_dotenv()
    with open("conf.yml", "r") as file:
        yml = yaml.safe_load(file)

    wiki_path = yml['wiki']['path']
    excluded = yml['exclude']['collections']
    client = OutlineClient(verbose=False)
    local = Outline(path=wiki_path, excluded=excluded, verbose=False)
    local_collections = local.get_local_collections()
    remote_collections = client.get_remote_collections()
    for collection in remote_collections:
        print("ID: {}\nName: {}\n".format(collection.id, collection.name))

    for collection in local_collections:
        print("Name: {}".format(collection))

if __name__ == "__main__":
    main()