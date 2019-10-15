from http import HTTPStatus

from flask import Blueprint

from truedoc.db import db
from truedoc.db import schemas
from truedoc.response import success
from truedoc.website import utils

bp = Blueprint('document', __name__)


@bp.route('/', methods=['POST'])
def create_document():
    """Create document."""

    return success(
        http_code=HTTPStatus.ACCEPTED,
        result=schemas.DocumentProcessingSchema().dump(utils.uploaded_document()),
    )


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

    document_schema = schemas.DocumentSchema()
    document = document_schema.dump(db.Document.load(document_id))

    return success(result=document)


@bp.route('/<uuid:document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Delete given document."""

    document_id = str(document_id)

    document = db.Document.load(document_id)
    db.Document.delete(document)

    return success()
