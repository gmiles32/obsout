from dotenv import load_dotenv
import yaml

from outline.outline import *
from outline.constants import *
from outline.artifacts import *

def status(local: LocalClient, sync_type: SyncType):
    print("Missing collections:")
    missing = local._get_missing_items(item=OutlineItems.COLLECTIONS, sync_type=sync_type)
    for collection in missing:
        print("     {}".format(collection.name))

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

    client._create_client_collection(local._get_missing_items(OutlineItems.COLLECTIONS, SyncType.REMOTE))
    status(local=local, sync_type=SyncType.LOCAL)

if __name__ == "__main__":
    main()