from .rest import Api
from . import settings

import time

j = Api(settings.CONFIG)


stats = j.stats
del stats['version']

for k,v in stats.items():
    print(f'{k}: {v}')
