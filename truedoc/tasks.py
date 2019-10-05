"""Tasks for Celery. """

import datetime
import hashlib
import shutil

from celery import Celery
from pathlib import Path

import truedoc.config

from truedoc.db import schemas

celery_app = Celery(
    'truedoctasks',
    broker=truedoc.config.Rabbitmq.PATH,
)

celery_app.conf.update(truedoc.config.Celery.CONFIG)


@celery_app.task
def process_document(document):
    schema_DocumentWorkerProcessing = schemas.DocumentWorkerProcessingSchema()
    data_DocumentWorkerProcessing = schema_DocumentWorkerProcessing.dump(document)

    document_path = Path(truedoc.config.DocumentProcessing.save_to(data_DocumentWorkerProcessing['document_id']))

    filesize = document_path.stat().st_size
    digest = hashlib.md5(document_path.read_bytes()).hexdigest()
    created_at = datetime.datetime.utcnow()

    # Move uploaded document
    shutil.move(str(document_path), str(document_path) + '.DONE')

    schema_DocumentDetailedSchema = schemas.DocumentDetailedSchema()
    data_DocumentDetailedSchema = schema_DocumentDetailedSchema.load(
        {
            **data_DocumentWorkerProcessing,
            'digest': digest,
            'filesize': filesize,
            'created_at': str(created_at),
        }
    )

    return data_DocumentDetailedSchema
