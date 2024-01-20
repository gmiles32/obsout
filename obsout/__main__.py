from dotenv import load_dotenv
import yaml
import click
from rich import print

from .outline import *
from .config import load_vars

@click.group("cli")
@click.option('-v','--verbose',is_flag=True,help="Show verbose logs")
@click.option('-c','--config',required=False,help="Specify config file, defaults to current directory")
@click.option('-e','--env',required=False,help="Specify .env file, defaults to current directory")
@click.pass_context
def cli(ctx,verbose,config="",env=""):
    
    yml = load_vars(env=env,config=config)

    wiki_path = yml['wiki']['path']
    excluded = yml['wiki']['exclude']
    if excluded is None:
        excluded = []

    # Build client and local objects
    client = OutlineClient(verbose=False)
    local = Outline(client=client, path=wiki_path, excluded=excluded, verbose=verbose)

    ctx.obj = {'outline': local}

@click.command("status")
@click.pass_context
def status(local, sync_type: SyncType):
    print("Missing:\n")
    missing = local._get_missing_items(sync_type=sync_type)
    for collection in missing:
        for document in collection.documents:
            print("{}/{}".format(collection.name, document.name))

@click.command("sync",help="Sync local and client markdown files")
@click.pass_context
def sync(ctx):
    local = ctx.obj.get('outline')
    local.sync(SyncType.REMOTE)
    local.sync(SyncType.LOCAL)
    pass

cli.add_command(sync)

# def main():
    
    # load_dotenv()
    # with open("conf.yml", "r") as file:
    #     yml = yaml.safe_load(file)

    # wiki_path = yml['wiki']['path']
    # excluded = yml['exclude']['collections']


    # client = OutlineClient(verbose=False)
    # local = Outline(client=client, path=wiki_path, excluded=excluded, verbose=False)

    # local._delete_client_documents(collection=[collection for collection in client.collections if collection.name == "OPNsense"][0])
    # # local._update_local_documents(collection=[collection for collection in client.collections if collection.name == "test"][0])
    # # local._get_old_items(sync_type=SyncType.REMOTE)
    # local.sync(SyncType.REMOTE)

    # load_vars(env="",conf="")

if __name__ == "__main__":
    cli()