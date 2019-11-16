from http import HTTPStatus

from celery.result import AsyncResult

from flask import Blueprint

import truedoc.common
import truedoc.constants
import truedoc.website.context

from truedoc.db import db
from truedoc.db import schemas
from truedoc.decorators import require_valid_token
from truedoc.response import success
from truedoc.tasks import celery_app
from truedoc.website import utils

bp = Blueprint('document', __name__)


@bp.route('/', methods=['POST'])
@require_valid_token
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
@require_valid_token
def document_state(document_id):
    """Document state."""

    document_id = str(document_id)

    # Remember that 'status' in Celery == 'state' in the project

    task = AsyncResult(document_id, app=celery_app)

    # TODO: see https://github.com/manlix/truedoc/issues/22

    return success(result={
        'state': truedoc.common.normalize_job_state(task.status),
    })


@bp.route('/list', methods=['POST'])
@require_valid_token
def list_documents():
    """List documents."""

    documents_schema = schemas.DocumentSchema(many=True)
    documents = documents_schema.dump(db.Document.documents(truedoc.website.context.get("token")["profile_id"]))

    return success(result=documents)


@bp.route('/<uuid:document_id>', methods=['GET'])
@require_valid_token
def load_document(document_id):
    """Load document by document_id."""

    document_id = str(document_id)

    schema = schemas.DocumentSchema()
    document = schema.dump(db.Document.load(document_id))

    return success(result=document)


# TODO: drop or move to admin scope
@bp.route('/<uuid:document_id>', methods=['DELETE'])
@require_valid_token
def delete_document(document_id):
    """Delete given document."""

    document_id = str(document_id)

    document = db.Document.load(document_id)
    db.Document.delete(document)

    return success()
