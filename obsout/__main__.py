import click

# from outline.outline import *
# from outline.constants import *
# from config import load_vars
# from console import console,logger
from .outline import *
from .config import *
from .console import console, logger

@click.group("cli")
@click.option('-v','--verbose',is_flag=True,help="Show verbose logs")
@click.option('-c','--config',required=False,help="Specify config file, defaults to current directory")
@click.option('-e','--env',required=False,help="Specify .env file, defaults to current directory")
@click.pass_context
def cli(ctx,verbose,config="",env=""):

    yml = load_vars(env=env,config=config,verbose=verbose)

    wiki_path = yml['wiki']['path']
    excluded = yml['wiki']['exclude']
    if excluded is None:
        excluded = []

    # Build client and local objects
    client = OutlineClient(verbose=verbose)
    outline = Outline(client=client, path=wiki_path, excluded=excluded, verbose=verbose)

    ctx.obj = {'outline': outline,'verbose': verbose}

@click.command("status",help="View local sync status")
@click.option('--local',required=False,is_flag=True,default=False,help="Show status of local files compared to remote")
@click.pass_context
def status(ctx,local):
    verbose = ctx.obj.get('verbose')
    if verbose:
        log = logger()

    if local:
        sync_type = SyncType.LOCAL
    else:
        sync_type = SyncType.REMOTE

    outline = ctx.obj.get('outline')

    missing = outline._get_missing_items(sync_type=sync_type)
    old = outline._get_old_items(sync_type=sync_type)
    if not verbose:
        console.print("Status:")
    if len(missing) <= 0 and len(old) <= 0:
        if verbose:
            log.info("Wiki is up to date")
        else: 
            console.print(" [bold green]Up to date!")
    
    if len(missing) > 0:
        for collection in missing:
            collection_name = collection.name
            if len(collection.documents) <= 0:
                if verbose:
                    log.info("Missing collection {}".format(collection_name))
                else:
                    console.print(" [bold red]missing: {}".format(collection_name))
            else:
                for document in collection.documents:
                    if verbose:
                        log.info("Missing document {}/{}".format(collection_name, document.name))
                    else:
                        console.print(" [bold red]missing: {}/{}".format(collection_name, document.name))
    if len(old) > 0:
        for collection in old:
            for document in collection.documents:
                if verbose:
                    log.info("Document {}/{} out of sync".format(collection.name, document.name))
                else: 
                    console.print(" [dark_orange3]modified: {}/{}".format(collection.name, document.name))

@click.command("sync",help="Sync local and client markdown files")
@click.pass_context
def sync(ctx):
    outline = ctx.obj.get('outline')
    verbose = ctx.obj.get('verbose')
    if verbose:
        log = logger()
    with console.status("[bold green]Syncing...") as status:
        if verbose:
            log.info("Syncing Outline client")
        else: 
            console.print("[bold blue]Syncing Outline...")
        outline.sync(SyncType.REMOTE)
        if verbose:
            log.info("Syncing local Obsidian vault")
        else:
            console.print("[bold blue]Syncing vault...")
        outline.sync(SyncType.LOCAL)
    console.print("[bold green]Complete!")

@click.command("delete",help="Delete a document from vault and Outline")
@click.option('-c','--collection',required=True,help="Collection name")
@click.option('-d','--document',required=False,help="Document name, without '.md' extension")
@click.option('--all',is_flag=True,show_default=True,default=False,help="Delete entire collection")
@click.pass_context
def delete(ctx,collection,all,document=""):
    outline = ctx.obj.get('outline')
    outline.delete(collection_name=collection,document_name=document,all=all)

cli.add_command(status)
cli.add_command(sync)
cli.add_command(delete)

def main():
    verbose = False
    yml = load_vars(env="",config="",verbose=verbose)

    wiki_path = yml['wiki']['path']
    excluded = yml['wiki']['exclude']
    if excluded is None:
        excluded = []

    # Build client and local objects
    client = OutlineClient(verbose=verbose)
    outline = Outline(client=client, path=wiki_path, excluded=excluded, verbose=verbose)

    outline.sync(SyncType.REMOTE)

if __name__ == "__main__":
    cli()
    # main()