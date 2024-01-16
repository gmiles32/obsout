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
    local = Outline(client=client, path=wiki_path, excluded=excluded, verbose=False)

    for collection in client.collections:
        print("ID: {}\nName: {}\n".format(collection.id, collection.name))

    for collection in local.collections:
        print("Name: {}".format(collection.name))

    missing = local._get_missing_items(item=OutlineItems.COLLECTIONS, sync_type=SyncType.REMOTE)
    print(missing[0].name)

def status():
    pass

if __name__ == "__main__":
    main()