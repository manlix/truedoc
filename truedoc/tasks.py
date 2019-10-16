"""Tasks for Celery workers. """

import datetime
import hashlib
import shutil

from celery import Celery
from pathlib import Path

import truedoc.config

from truedoc.db import db
from truedoc.db import schemas

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init("https://f6de8903ce254aa89bfc41f021320f5d@sentry.io/1513696", integrations=[CeleryIntegration()])

celery_app = Celery(
    'truedoctasks',
    backend='amqp',
    broker=truedoc.config.Rabbitmq.PATH,
)

celery_app.conf.update(truedoc.config.Celery.CONFIG)


class Document:

    def __init__(self, document):
        self.document = document

        self.valid_document = None
        self.processing_data = None
        self.path_to_save = None

        self.validate()
        self.generate_path_to_save()
        self.processing()
        self.save_to_storage()

    def validate(self):
        if self.valid_document is None:
            schema = schemas.DocumentSchema()
            self.valid_document = schema.load(self.document)

    def generate_path_to_save(self):

        if self.path_to_save is None:
            self.path_to_save = Path(truedoc.config.DocumentProcessing.save_to(self.valid_document['document_id']))

    def processing(self):

        if self.processing_data is None:
            self.processing_data = {
                'digest': hashlib.md5(self.path_to_save.read_bytes()).hexdigest(),
            }

    def save_to_storage(self):
        shutil.move(str(self.path_to_save), str(self.path_to_save) + '.DONE')


@celery_app.task
def process_document(document):
    """Processing document."""

    res = Document(document)

    schema = schemas.DocumentSchema(exclude=['state'])  # Drop 'state' — does not exist in document db model.
    detailed_document = schema.dump(
        {
            **res.valid_document,
            **res.processing_data,
        }
    )

    db.Document.create(db.models.Document(**detailed_document))

    return detailed_document
