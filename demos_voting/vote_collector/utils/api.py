# File: api.py

from __future__ import absolute_import, division, print_function, unicode_literals

from demos_voting.base.utils.api import APIAuth, APISession, APIUser
from demos_voting.vote_collector.models import APIAuthNonce


class APIAuth(APIAuth):
    auth_nonce_cls = APIAuthNonce


class APISession(APISession):
    auth_cls = APIAuth


class APIUser(APIUser):
    user_permissions = {
        'election_authority': {
            'vote_collector.add_election',
            'vote_collector.change_election',
            'vote_collector.add_ballot'
        },
    }

