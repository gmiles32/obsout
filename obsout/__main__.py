from dotenv import load_dotenv
import yaml

from outline.outline import *
from outline.constants import *
from outline.artifacts import *

def status(local, sync_type: SyncType):
    print("Missing:\n")
    missing = local._get_missing_items(sync_type=sync_type)
    for collection in missing:
        for document in collection.documents:
            print("{}/{}".format(collection.name, document.name))

def main():
    
    load_dotenv()
    with open("conf.yml", "r") as file:
        yml = yaml.safe_load(file)

    wiki_path = yml['wiki']['path']
    excluded = yml['exclude']['collections']


    client = OutlineClient(verbose=False)
    local = Outline(client=client, path=wiki_path, excluded=excluded, verbose=False)

    for collection in client.collections:
        print("ID: {}\nName: {}\n".format(collection.id, collection.name))

    for collection in local.collections:
        print("Name: {}".format(collection.name))

    client._refresh_client()
    missing_items = local._get_missing_items(sync_type=SyncType.REMOTE)
    local._create_client_collections(missing_items)
    for collection in missing_items:
        local._create_client_documents(collection)
    # client._create_client_collection(local._get_missing_items(SyncType.REMOTE))
    status(local=local, sync_type=SyncType.REMOTE)

if __name__ == "__main__":
    main()