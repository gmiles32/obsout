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
    local._create_client_documents(local.collections[0])
    # client._create_client_collection(local._get_missing_items(SyncType.REMOTE))
    status(local=local, sync_type=SyncType.LOCAL)

if __name__ == "__main__":
    main()