
from functools import singledispatch

from planetmint.config import Config
from planetmint import backend
from planetmint.backend.tarantool.connection import TarantoolDB
from planetmint.backend.utils import module_dispatch_registrar

register_schema = module_dispatch_registrar(backend.schema)

#@register_schema(TarantoolDB)
#def __read_commands(connection, file_path):
#    with open(file_path, "r") as cmd_file:
#        commands = [line.strip() for line in cmd_file.readlines() if len(str(line)) > 1]
#        cmd_file.close()
#    return commands

@register_schema(TarantoolDB)
def drop_database(connection, dbname=None):
    connection.drop_database()

@register_schema(TarantoolDB)
def init_database(connection, dbname = None):
    connection.init_database()