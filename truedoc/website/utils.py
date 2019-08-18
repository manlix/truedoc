import hashlib

from flask import request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from truedoc.exceptions import DocumentNoFileInRequest


def uploaded_document():
    """Helper to make dict for scheme to validate data."""

    # See 'Uploading files': https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

    if 'document' not in request.files or not isinstance(request.files['document'], FileStorage):
        raise DocumentNoFileInRequest('No file in request.')

    # TODO: should saves file to object storage.
    document_in_memory = request.files['document'].read()

    document = {
        'title': request.form.get('title', None),
        'document': document_in_memory,
        'filename': secure_filename(request.files['document'].filename),
        'digest': hashlib.md5(document_in_memory).hexdigest(),
        'filesize': len(document_in_memory),
    }

    return document
