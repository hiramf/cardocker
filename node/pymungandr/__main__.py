from .rest import Api
from . import settings


jrest = Api(settings.CONFIG)
print(jrest.stats())