"""Common module."""

import hashlib
import uuid

import truedoc.constants


def uuid4():
    """This uuid4 used for 'Primary key' in database."""
    return str(uuid.uuid4())


def normalize_job_state(state):
    """Normalize job state to expected value and lowercase."""

    state = state.lower()

    if state not in truedoc.constants.JOB_STATE.ALL_STATES:
        state = truedoc.constants.JOB_STATE.UNKNOWN

    return state


def document_hash(document):
    """Common hash function for documents."""

    return hashlib.blake2b(document).hexdigest()
