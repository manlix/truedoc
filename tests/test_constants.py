import truedoc.constants


def test_class_status():
    """Test class truedoc.constants.STATUS."""
    assert truedoc.constants.STATUS.ERROR == 'error'
    assert truedoc.constants.STATUS.SUCCESS == 'success'


def test_class_size():
    """Test class truedoc.constants.SIZE."""

    assert truedoc.constants.SIZE.BYTE == 1
    assert truedoc.constants.SIZE.KILOBYTE == 1024  # 1024 * 1
    assert truedoc.constants.SIZE.MEGABYTE == 1048576  # 1024 * 1024


def test_class_time():
    """Test class truedoc.constants.TIME."""

    assert truedoc.constants.TIME.SECOND == 1
    assert truedoc.constants.TIME.MINUTE == 60
    assert truedoc.constants.TIME.HOUR == 3600  # 60 * 60
