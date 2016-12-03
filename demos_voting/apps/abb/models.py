# File: models.py

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from demos_voting.common import storage
from demos_voting.common.models import (Election, Ballot, Part, Question, Option, POption, PQuestion, Task,
    PrivateApiUser, PrivateApiNonce)

logger = logging.getLogger(__name__)


cert_fs = storage.FileSystemStorage(
    location=os.path.join(settings.MEDIA_ROOT, 'abb/certs'),
    file_permissions_mode=0o600, directory_permissions_mode=0o700
)

def cert_directory_path(election, filename):
    return "%s%s" % (election.id, os.path.splitext(filename)[-1])


class Election(Election):

    cert = models.FileField(_("certificate"), storage=cert_fs, upload_to=cert_directory_path)

    tallying_started_at = models.DateTimeField(_("tallying started at"), null=True, default=None)
    tallying_ended_at = models.DateTimeField(_("tallying ended at"), null=True, default=None)

    coins = models.CharField(_("coins"), max_length=128, null=True, default=None)


class Ballot(Ballot):

    cast_at = models.DateTimeField(_("cast at"), null=True, default=None)


class Part(Part):

    credential = models.CharField(_("credential"), max_length=32, null=True, default=None)
    credential_hash = models.CharField(_("credential hash"), max_length=255)


class Question(Question):
    pass


class Option(Option):

    votes = models.PositiveIntegerField(_("number of votes"), null=True, default=None)


class POption(POption):

    voted = models.NullBooleanField(_("marked as voted"), default=None)

    votecode = models.CharField(_("vote-code"), max_length=32, null=True, default=None)
    votecode_hash = models.CharField(_("vote-code hash"), max_length=255, null=True, default=None)

    receipt = models.CharField(_("receipt"), max_length=1024)


class PQuestion(PQuestion):
    pass


class Task(Task):
    pass


class PrivateApiUser(PrivateApiUser):
    pass


class PrivateApiNonce(PrivateApiNonce):
    pass

