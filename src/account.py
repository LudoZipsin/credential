from playhouse.sqlcipher_ext import *
import yaml


# Globals:
# config.yml contains the location of the db, the passphrase
CONFIG_PATH = "/etc/credential/config.yml"
DB_PATH_ACCESSOR = "db_path"
DB_PASSPHRASE_ACCESSOR = "db_passphrase"


# must be root...
def _get_db_passphrase():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.load(f)
    return config[DB_PASSPHRASE_ACCESSOR]


# must be root...
def _get_db_path():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.load(f)
    return config[DB_PATH_ACCESSOR]


# must be root...
def init_db():
    db_passphrase = _get_db_passphrase()
    db_path = _get_db_path()
    return SqlCipherDatabase(db_path, passphrase=db_passphrase)

db = init_db()


class Account(Model):
    service = TextField()
    account = TextField()
    passphrase = TextField()

    class Meta:
        database = db
