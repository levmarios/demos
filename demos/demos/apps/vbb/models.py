# File: models.py

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import re

from django.db import models

from demos.common.models import base
from demos.common.utils import base32

logger = logging.getLogger(__name__)



class Election(base.Election):
    
    voting_started_at = models.DateTimeField(null=True, default=None)
    voting_ended_at = models.DateTimeField(null=True, default=None)


class Ballot(base.Ballot):
    
    credential_hash = models.CharField(max_length=128)
    cast_at = models.DateTimeField(null=True, default=None)
    
    @property
    def is_cast(self):
        return self.cast_at is not None
    
    def verify_credential(self, credential):
        
        hasher = self.election.hasher
        regex = r'^%s{%d}$' % (base32.regex, (self.conf.credential_bits + 4) // 5)
        
        return (re.match(regex, credential) and
                hasher.verify(base32.normalize(credential), self.credential_hash))


class Part(base.Part):
    
    security_code_hash = models.CharField(max_length=128)
    
    def verify_security_code(self, security_code):
        
        hasher = self.election.hasher
        regex = r'^%s{%d}$' % (base32.regex, self.conf.security_code_len)
        
        return (re.match(regex, security_code) and
                hasher.verify(base32.normalize(security_code), self.security_code_hash))


class Question(base.Question):
    pass


class Option_P(base.Option_P):
    pass


class Option_C(base.Option_C):
    
    votecode = models.CharField(max_length=32, null=True, default=None)
    votecode_hash_value = models.CharField(max_length=128, null=True, default=None)
    
    receipt = models.CharField(max_length=32)


class PartQuestion(base.PartQuestion):
    
    votecode_hash_salt = models.CharField(max_length=32, null=True, default=None)
    votecode_hash_params = models.CharField(max_length=16, null=True, default=None)


class Task(base.Task):
    pass


# Common models ----------------------------------------------------------------

from demos.common.utils.api import RemoteUserBase

class RemoteUser(RemoteUserBase):
    pass


