from flask import Blueprint
from flask import request

from marshmallow.exceptions import ValidationError

from truedoc.db import db
from truedoc.db import schemas
from truedoc.response import failure, success
from truedoc.website import utils

bp = Blueprint('document', __name__)

@bp.route('/', methods=['POST'])
def create_document():
    """Create document.

    Test request: http -v -f POST truedoc-app.localhost/document/  title="document_title" document@~/checm.docx
    """

    try:

        document = schemas.DocumentSchema().load(utils.uploaded_document())
    except ValidationError as err:
        return failure(error_fields=err.messages)
    else:
        document = db.models.Document(
            profile_id='88fe325f-2572-4bbc-a60e-e7c0ae1c475d',  # TODO: load profile_id to Schema and replace "dump_only=True" -> "load_only=True"
            **document,
        )
        db.Document.create(document)
        return success(result=schemas.DocumentSchema().dump(document))


@bp.route('/', methods=['GET'])
def list_documents():
    """List documents."""

    documents_schema = schemas.DocumentSchema(many=True)
    documents = documents_schema.dump(db.Document.list_all())

    return success(result=documents)
