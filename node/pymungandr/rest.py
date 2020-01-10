import logging
import os
import socket
import sys
import urllib.request
from timeit import default_timer as timer

import yaml

logging.basicConfig(level=logging.DEBUG,
                    # Use Jormungandr logging format
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%b %d %H:%M:%S',
                    )
logger = logging.getLogger(__file__)


class Api:
    def __init__(self, config):
        self.config = config
    
    @staticmethod
    def yaml(x:str):
        return yaml.load(
            x,
            Loader=yaml.SafeLoader
        )

    @staticmethod
    def check_peer(host, port=3000, timeout=4):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s_start = timer()
            s.connect((host, int(port)))
            s.shutdown(socket.SHUT_RD)
        # Connection Timed Out
        except socket.timeout as e:
            logger.error(f"FAIL: Peer timed out: {host}[{port}]")
            raise ConnectionError from e
        except ConnectionRefusedError as e:
            logger.error(f"FAIL: Peer refused connection: {host}[{port}]")
            raise
        except OSError as e:
            logging.error(f"FAIL: Could not connect to {host}[{port}]")
            raise
        else:
            # Stop Timer
            s_stop = timer()
            s_runtime = "%.2f" % (1000 * (s_stop - s_start))
            logger.info(f"SUCESS: Connected to trusted peer {host}:{port} in {s_runtime} ms")
            return s_runtime
    
    def request(self, x:str):
        return self.yaml(
            urllib.request.urlopen(
                    f"http://{self.config['rest']['listen']}/api/v0/{x}"
                ).read()
        )

    @property
    def stats(self):
        return self.request("node/stats")
    
    @property
    def tip(self):
        return self.request("tip")
    
    @property
    def settings(self):
        return self.request("settings")
    
    @property
    def diagnostic(self):
        return self.request("diagnostic")

    @property
    def stake(self):
        return self.request("stake")
    
    @property
    def stake_pools(self):
        return self.request("stake_pools")
    
    def stake_pool(self, stake_pool_hash):
        return self.request(f"stake_pool/{stake_pool_hash}")
