import re
import pytest


def test_uuid4_is_string(one_uuid4):
    """Check that truedoc.common.uuid4() returns 'string' object."""
    assert isinstance(one_uuid4, str)  # uuid is string


def test_uuid4_len36(one_uuid4):
    """Check that item length is 36."""
    assert len(one_uuid4) == 36


def test_uuid4_is_type4(one_uuid4):
    """Check UUID is type '4' (random uuid)."""
    assert one_uuid4[14] == '4'


def test_uuid4_match_regexp(one_uuid4):
    """Check that UUID regexp match."""
    assert re.compile('^[a-z0-9]{8}-[a-z0-9]{4}-4[a-z0-9]{3}-[a-z0-9]{4}-[a-z0-9]{12}$').match(one_uuid4)


def test_uuid4_all_unique_items(many_uuid4, many_uuid4_len):
    """Check all items are unique."""
    assert len(set(many_uuid4)) == many_uuid4_len
