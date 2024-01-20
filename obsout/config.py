import json
import os
import sys
from dotenv import load_dotenv
import yaml

JSON_FILENAME = "conf.json"

def load_vars(env: str, config:str):
    """ Load env and configuration from file paths """

    # Test if config file exists
    config_dir = "/home/{}/.config/obsout".format(os.environ.get("USER"))
    if os.path.exists(os.path.join(config_dir,JSON_FILENAME)):
        with open(os.path.join(config_dir,JSON_FILENAME),'r') as config_file:
            config_json = json.loads(config_file.read())
    else:
        try:
            os.mkdir(config_dir)
        except OSError as error:
            pass
        config_json = {
            "env_path": "",
            "conf_path": ""
        }
        
    # Load environment
    if env:
        ENV_FILE = os.path.expanduser(env) # get rid of ~/
    else:
        ENV_FILE = config_json['env_path'] or '.env' # use saved path or default to current directory
    
    if not load_dotenv(ENV_FILE):
        sys.exit("Unable to load .env file: {}".format(ENV_FILE))

    # Load config yaml file
    if config:
        CONF_FILE = os.path.expanduser(config)
    else:
        CONF_FILE = config_json['conf_path'] or 'conf.yml' # use saved path or default to current directory

    try:
        with open(CONF_FILE, 'r') as file:
            yml = yaml.safe_load(file)
    except OSError:
        sys.exit("Unable to load conf.yml file at path {}: File does not exist".format(CONF_FILE))

    # Save paths
    config_json["env_path"] = ENV_FILE
    config_json["conf_path"] = CONF_FILE
    contents = json.dumps(config_json)
    file = open(os.path.join(config_dir,JSON_FILENAME),'w')
    file.write(contents)
    file.close()

    return yml