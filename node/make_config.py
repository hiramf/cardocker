import yaml
import os
from urllib import request

ENV_PREFIX = os.environ.get('ENV_PREFIX')
CONFIG_URL = os.environ.get('CONFIG')


with request.urlopen(CONFIG_URL) as response:
    config = yaml.load(response.read(), Loader=yaml.SafeLoader)

with request.urlopen('https://api.ipify.org') as response:
    PUBLIC_IP = response.read().decode('utf-8')


# Required
config['p2p']['listen_address'] = "/ip4/0.0.0.0/tcp/3000"
config['p2p']['public_address'] = f"/ip4/{PUBLIC_IP}/tcp/3000"
config['storage'] = "/mnt/storage/"

# Optional
config['p2p']['topics_of_interest']['blocks'] = "high"
config['p2p']['topics_of_interest']['messages'] = "high"

with open(f"{ENV_PREFIX}/bin/config.yaml", 'w') as file:
    documents = yaml.dump(config, file)