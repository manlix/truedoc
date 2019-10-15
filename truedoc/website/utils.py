import os

from flask import request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from truedoc.db import schemas
from truedoc.exceptions import DocumentNoFileInRequest

import truedoc.constants
import truedoc.common
import truedoc.tasks


def uploaded_document():
    """Helper to make dict for scheme to validate Document processing."""

    # See 'Uploading files': https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

    if 'document' not in request.files or not isinstance(request.files['document'], FileStorage):
        raise DocumentNoFileInRequest

    # TODO: should saves file to object storage.
    # document_in_memory = request.files['document'].read()

    profile_id = request.form.get('profile_id', None)  # TODO: read profile_id from JWT
    document_id = truedoc.common.uuid4()
    title = request.form.get('title', None)  # TODO: edit schema to replace empty string ('') to None

    filename = secure_filename(request.files['document'].filename)  # TODO: handle None of the filename

    request.files['document'].save(os.path.join('/upload', document_id))

    just_uploaded = schemas.DocumentProcessingSchema().load(
        {
            'document_id': document_id,
            'profile_id': profile_id,
            'title': title,
            'filename': filename,
            'state': truedoc.constants.JOB_STATE.PENDING,  # Default state for new task
        }
    )

    # Send task to workers
    task = truedoc.tasks.process_document.apply_async(
        args=(just_uploaded,),
        task_id=document_id,
    )

    return just_uploaded
