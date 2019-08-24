from flask import Blueprint

from truedoc.db import db
from truedoc.db import schemas
from truedoc.response import success
from truedoc.website import utils

bp = Blueprint('document', __name__)


@bp.route('/', methods=['POST'])
def create_document():
    """Create document."""

    document_schema = schemas.DocumentSchema()
    data = document_schema.load(utils.uploaded_document())

    document = db.models.Document(
        # TODO: load profile_id to Schema and replace "dump_only=True" -> "load_only=True"
        profile_id='88fe325f-2572-4bbc-a60e-e7c0ae1c475d',
        **data,
    )
    db.Document.create(document)

    return success(result=document_schema.dump(document))


@bp.route('/', methods=['GET'])
def list_documents():
    """List documents."""

    documents_schema = schemas.DocumentSchema(many=True)
    documents = documents_schema.dump(db.Document.list_all())

    return success(result=documents)
