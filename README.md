# obsout
`obsout` is an [Obsidian](https://obsidian.md/) to [Outline Wiki](https://www.getoutline.com/) connector written in Python. It will sync local markdown files to Outline via API requests (and sync to local computer), show status of sync, and aid in deleting documents between both Outline and local Obsidian vault.

## Installation
`obsout` can be installed from `PyPI`:
```bash
pipx install obsout
```

## Vault Structure
```
- Collection1
    - Document1
    - Document2
    ...
- Collection2
```

Outline is relatively simple wiki, with only high level collections, which contain any number of documents. Outline also provides the functionality of nested documents, however I'm not sure how to implement this from the perspective of files/directories.

This structure means that any files found in the root directory will be ignored, so keep that in mind.

## Configuration
Use the provided `example.env` to make a `.env` file. Note the path to this file (I recommend placing it in your wiki directory, you won't be able to see it in Obsidian). In addition to the `.env` file, a `conf.yml` file is also needed - again, use the provided example. Private directories can be added as shown:
```yaml
wiki:
    path: "your path"
    exclude:
        - directory1
        - direcotry2
```

Once you have provided the path to the `.env` and `conf.yml` files, the paths will be stored in a json file at the path `/home/user/.config/obsout/conf.json`.

On the first run of `obsout`, use the following options to specify paths:
```
  -c, --config TEXT  Specify config file, defaults to current directory
  -e, --env TEXT     Specify .env file, defaults to current directory
```

Again, after first run these options are not necessary unless you have moved the path of the `.env` and `conf.yml` files.

## Commands

`status` will show modified/missing files by default compared to the local vault. Using the `--local` flag, you can see the status in the opposite direction (file missing from vault compared to Outline).

```
obsout status [OPTIONS]

  View local sync status

Options:
  --local  Show status of local files compared to remote
```

`sync` will sync files bi-directionally between Outline and the local Obsidian vault based on modification date (older files will be overwritten). No files will be deleted in the sync.

```
Usage: obsout sync [OPTIONS]

  Sync local and client markdown files
```

`delete` will delete a collection, or a document, based on the collection/document name provided. The entire collection will be deleted if the `--all` flag is provided.

```
Usage: obsout delete [OPTIONS]

  Delete a document from vault and Outline

Options:
  -c, --collection TEXT  Collection name  [required]
  -d, --document TEXT    Document name, without '.md' extension
  --all                  Delete entire collection
```

## Contributing
Pull requests are more than welcome. If you have major changes slated, please open an issue instead.

To set up a development environment with `poetry` (on Linux):
```bash
# Install poetry
pipx install poetry
# Create virtual environemnt
python -m venv venv
source venv/bin/activate
# Install dependencies
poetry install
```

For more information on working with Outline Wiki API, see [the documentation](https://github.com/openapi-generators/openapi-python-client)

## Credits
Thanks to jaypyles and his project [obsidian-to-bookstack](https://github.com/jaypyles/obsidian-to-bookstack) for the inspiration. His approach to syncing between obsidian and bookstack provided a lot of inspiration to my approach in this project.

## License
[GPL3](LICENSE.md)