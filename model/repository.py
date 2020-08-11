import datetime
from bson.codec_options import CodecOptions
from model.collections import Drugs
from model.collections.indication_restriction import IndicationRestriction
from model.collections.atc_group import AtcGroup
from model.collections.shortcut import Shortcut
from model.collections.state import State


class Repository(object):
    def __init__(self, mongo_connection):
        self._mongo = mongo_connection
        self._codec_options = CodecOptions(tz_aware=True, tzinfo=datetime.timezone.utc)
        self._collections = {}

    @property
    def drugs(self):
        return self._get_repo(Drugs)

    @property
    def indication_restriction(self):
        return self._get_repo(IndicationRestriction)

    @property
    def atc_group(self):
        return self._get_repo(AtcGroup)

    @property
    def shortcut(self):
        return self._get_repo(Shortcut)

    @property
    def state(self):
        return self._get_repo(State)

    def _get_repo(self, coll):
        if coll not in self._collections:
            self._collections[coll] = self._mongo[coll.DATABASE][coll.COLLECTION].with_options(self._codec_options)

        return self._collections[coll]
