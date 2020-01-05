import logging
import os
import secrets
import socket
import sys
from timeit import default_timer as timer
from urllib import request

import yaml


logging.basicConfig(level=logging.DEBUG,
                    # Use Jormungandr logging format
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%b %d %H:%M:%S',
                    )
logger = logging.getLogger(__file__)

def tcpping(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s_start = timer()
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
    # Connection Timed Out
    except (socket.timeout, OSError):
        logging.error(f"Could not connect to {host}[{port}]")
    else:
        # Stop Timer
        s_stop = timer()
        s_runtime = "%.2f" % (1000 * (s_stop - s_start))
        logger.info(f"Connected to trusted peer {host}:{port} in {s_runtime} ms")
        return s_runtime

ENV_PREFIX = os.environ.get('ENV_PREFIX')
CONFIG_URL = os.environ.get('CONFIG')
LISTEN_PORT = os.environ.get('LISTEN_PORT', default=3000)
REST_PORT = os.environ.get('REST_PORT', default=3100)
STORAGE_DIR = os.environ.get('STORAGE_DIR', default="/mnt/storage")
PUBLIC_ID = secrets.token_hex(24)

with request.urlopen(CONFIG_URL) as response:
    config = yaml.load(response.read(), Loader=yaml.SafeLoader)

with request.urlopen('https://api.ipify.org') as response:
    PUBLIC_IP = response.read().decode('utf-8')

# Required
config['p2p']['listen_address'] = f"/ip4/0.0.0.0/tcp/{LISTEN_PORT}"
config['p2p']['public_address'] = f"/ip4/{PUBLIC_IP}/tcp/{LISTEN_PORT}"
config['p2p']['public_id'] = PUBLIC_ID
config['storage'] = STORAGE_DIR
config['rest']['listen'] = f"127.0.0.1:{REST_PORT}"

# Optional
config['p2p']['topics_of_interest']['blocks'] = "high"
config['p2p']['topics_of_interest']['messages'] = "high"

# From Jormungandr-for-Newbs tutorial
config['p2p']['max_connections'] = 1024
config['p2p']['gossip_interval'] = "10s"
config['mempool'] = {}
config['mempool']['fragment_ttl'] = '2h'
config['mempool']['log_ttl'] = '24h'
config['mempool']['garbage_collection_interval'] = '2h'

# Check peers
for idx, peer in enumerate(config['p2p']['trusted_peers']):
    _, _, host, _, port = peer['address'].split('/')
    t = tcpping(host, port)
    # Can set peers dynamically with t in future

with open(f"{ENV_PREFIX}/bin/config.yaml", 'w') as file:
    documents = yaml.dump(config, file)
