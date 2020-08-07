
from os import path
from pymongo import MongoClient
from configparser import ConfigParser
from model import Repository


class BaseClass:
    def __init__(self):
        self.mongo_connection = MongoClient(self.get_config('mongo')['uri'])
        self.mongo = Repository(self.mongo_connection)
        self.logger = None
        self.config = None

    def get_config(self, section):
        filename = path.abspath(path.join(__file__, '../config/config.cfg'))
        if path.exists(filename):
            self.config = ConfigParser()
            self.config.read(filename)
            return dict(self.config.items(section))

        return None

