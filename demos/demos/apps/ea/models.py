# File: models.py

from __future__ import absolute_import, division, unicode_literals

import logging

from django.db import models

from demos.common.models import base
from demos.common.utils import crypto, fields

logger = logging.getLogger(__name__)

class Election(base.Election):
    pass


class Question(base.Question):
    pass


class OptionC(base.OptionC):
    pass


class Ballot(base.Ballot):
    pass


class Part(base.Part):
    pass


class OptionV(base.OptionV):
    
    decom = fields.ProtoField(cls=crypto.Decom)
    zk_state = fields.ProtoField(cls=crypto.ZKState)


class Trustee(base.Trustee):
    pass


class Task(base.Task):
    pass


# Common models ----------------------------------------------------------------

from demos.common.utils.api import RemoteUserBase
from demos.common.utils.config import ConfigBase

class Config(ConfigBase):
    pass

class RemoteUser(RemoteUserBase):
    pass

