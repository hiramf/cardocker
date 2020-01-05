import os
import logging
import yaml

logging.basicConfig(level=logging.DEBUG,
                    # Use Jormungandr logging format
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%b %d %H:%M:%S',
                    )
logger = logging.getLogger(__file__)

def load_config():
    try:
        ENV_PREFIX = os.environ.get('ENV_PREFIX')       
        # Load Configuration
        with open(os.path.join(ENV_PREFIX, 'bin/config.yaml')) as file:
            return yaml.load(file, Loader=yaml.SafeLoader)
    except Exception as e:
        logger.exception(e)

CONFIG = load_config()

ACCOUNT_ADDRESS = os.environ.get("ACCOUNT_ADDRESS")