from http import HTTPStatus

from celery.result import AsyncResult

from flask import Blueprint

import truedoc.common
import truedoc.constants

from truedoc.db import db
from truedoc.db import schemas
from truedoc.response import success
from truedoc.tasks import celery_app
from truedoc.website import utils

bp = Blueprint('document', __name__)


@bp.route('/', methods=['POST'])
def create_document():
    """Create document."""

    result = schemas.DocumentSchema().dump(utils.uploaded_document())
    result.update({
        'ref': f'/document/{result["document_id"]}/state',
    })

    return success(
        http_code=HTTPStatus.ACCEPTED,
        result=result,
    )


@bp.route('/<uuid:document_id>/state', methods=['GET'])
def document_state(document_id):
    """Document state."""

    document_id = str(document_id)

    # Remember that 'status' in Celery == 'state' in the project

    task = AsyncResult(document_id, app=celery_app)

    # TODO: see https://github.com/manlix/truedoc/issues/22

    return success(result={
        'state': truedoc.common.normalize_job_state(task.status),
    })


@bp.route('/', methods=['GET'])
def list_documents():
    """List documents."""

    documents_schema = schemas.DocumentSchema(many=True)
    documents = documents_schema.dump(db.Document.list_all())

    return success(result=documents)


@bp.route('/<uuid:document_id>', methods=['GET'])
def load_document(document_id):
    """Load document by document_id."""

    document_id = str(document_id)

    schema = schemas.DocumentSchema()
    document = schema.dump(db.Document.load(document_id))

    return success(result=document)


@bp.route('/<uuid:document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Delete given document."""

    document_id = str(document_id)

    document = db.Document.load(document_id)
    db.Document.delete(document)

    return success()