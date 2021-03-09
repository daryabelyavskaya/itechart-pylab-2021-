from enum import Enum

import dacite
from dataclasses import dataclass
from decouple import config


class Backend(Enum):
    mongodb = 1
    postgresql = 2


converters = {
    int: lambda x: int(x),
    Backend: lambda x: Backend[x],
}


@dataclass
class Configuration:
    port: int
    host: str
    database: Backend
    database_name: str
    user: str
    password: str


class DBConfig():
    port = config("PORT")
    host = config("HOST")
    database = config('DATABASE')
    database_name = config('DATABASE_NAME')
    user = config('CLIENT')
    password = config('PASSWORD')

    def configs(self):
        config_dict = {
            'port': self.port,
            'host': self.host,
            'database': self.database,
            'database_name': self.database_name,
            'user': self.user,
            'password': self.password
        }

        configs = dacite.from_dict(
            data_class=Configuration, data=config_dict,
            config=dacite.Config(type_hooks=converters),
        )
        return configs
