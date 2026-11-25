from playhouse.db_url import connect
from decouple import config

DB = connect(config('DATABASE'))