import urllib.request
import yaml
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    # Use Jormungandr logging format
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%b %d %H:%M:%S',
                    )
logger = logging.getLogger(__file__)


class Api:
    def __init__(self, config):
        self.config = config
    
    def request(self, x:str):
        return yaml.load(
            urllib.request.urlopen(
                    f"{self.listen}/api/v0/{x}"
                ).read(), 
            Loader=yaml.SafeLoader
        )

    @property
    def listen(self):
        return f"http://{self.config['rest']['listen']}"

    def stats(self):
        return self.request("node/stats")
    
    def account_settings(self, account_address):
        return self.request(f"settings?account-id={account_address}")
    
