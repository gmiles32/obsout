import json
import os
import sys
from dotenv import load_dotenv
import yaml

from .console import console,logger

JSON_FILENAME = "conf.json"

def load_vars(env: str, config:str, verbose: bool):
    """ Load env and configuration from file paths """

    if verbose:
        log = logger()

    # Test if config file exists
    config_dir = "/home/{}/.config/obsout".format(os.environ.get("USER"))
   
    if os.path.exists(os.path.join(config_dir,JSON_FILENAME)):
        with open(os.path.join(config_dir,JSON_FILENAME),'r') as config_file:
            config_json = json.loads(config_file.read())
            if verbose:
                log.info("Loaded previous configuration")
    else:
        if verbose:
            log.warning("File {} does not exist".format(os.path.join(config_dir,JSON_FILENAME)))
            log.info("Creating config directory at {}".format(config_dir))
        try:
            os.mkdir(config_dir)
        except OSError as error:
            if verbose:
                log.warning("Config directory {} already exists".format(config_dir))
            pass
        config_json = {
            "env_path": "",
            "conf_path": "",
            "from_file": False
        }
        
    # Load environment
    if env:
        ENV_FILE = os.path.expanduser(env) # get rid of ~/
    else:
        ENV_FILE = config_json['env_path'] or '.env' # use saved path or default to current directory

    if not load_dotenv(ENV_FILE):
        if verbose:
            log.critical("Unable to load .env file: {}".format(ENV_FILE))
        console.print("[bold red]Unable to load .env file at path {}, check that path is correct".format(ENV_FILE))
        sys.exit(1) # Convert stuff to rich logging

    # Load config yaml file
    if config:
        CONF_FILE = os.path.expanduser(config)
    else:
        CONF_FILE = config_json['conf_path'] or 'conf.yml' # use saved path or default to current directory
    
    try:
        with open(CONF_FILE, 'r') as file:
            yml = yaml.safe_load(file)
    except OSError:
        if verbose:
            log.critical("Unable to load conf file: {}".format(CONF_FILE))
        console.print("[bold red]Unable to load conf.yml file at path {}: File does not exist".format(CONF_FILE))
        sys.exit(1)


    if verbose:
        log.info("Found env file at {}".format(ENV_FILE))
        log.info("Found conf.yml file at {}".format(CONF_FILE))

    # Save paths
    if not config_json["from_file"]:
        config_json["env_path"] = ENV_FILE
        config_json["conf_path"] = CONF_FILE
        config_json["from_file"] = True
        contents = json.dumps(config_json)
        file = open(os.path.join(config_dir,JSON_FILENAME),'w')
        file.write(contents)
        file.close()
        if verbose:
            log.info("Saved configuration to {}".format(os.path.join(config_dir,JSON_FILENAME)))

    return yml