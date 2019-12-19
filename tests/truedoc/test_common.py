import re
import pytest

import truedoc.common
import truedoc.constants


@pytest.mark.usefixtures("one_uuid4", "many_uuid4")
class TestUuid4:
    """Test uuid4 object."""

    def test_uuid4_is_string(self, one_uuid4):
        """Check that truedoc.common.uuid4() returns 'string' object."""
        assert isinstance(one_uuid4, str)  # uuid is string

    def test_uuid4_len36(self, one_uuid4):
        """Check that item length is 36."""
        assert len(one_uuid4) == 36

    def test_uuid4_is_type4(self, one_uuid4):
        """Check UUID is type '4' (random uuid)."""
        assert one_uuid4[14] == '4'

    def test_uuid4_match_regexp(self, one_uuid4):
        """Check that UUID regexp match."""
        assert re.compile('^[a-z0-9]{8}-[a-z0-9]{4}-4[a-z0-9]{3}-[a-z0-9]{4}-[a-z0-9]{12}$').match(one_uuid4)

    def test_uuid4_all_unique_items(self, many_uuid4, many_uuid4_len):
        """Check all items are unique."""
        assert len(set(many_uuid4)) == many_uuid4_len


class TestJobState:
    def test_unknown_job_sate(self):
        """Check that 'unknown' state normalizing to 'truedoc.constants.JOB_STATE.UNKNOWN'."""
        unknown_state = 'zZz'
        assert truedoc.common.normalize_job_state(unknown_state) == truedoc.constants.JOB_STATE.UNKNOWN

    def test_all_job_states(self):
        """Check that all possible job states are declared."""
        job_states = frozenset(
            {
                'failure',
                'pending',
                'processing',
                'success',
                'unknown',
            }
        )

        assert job_states == truedoc.constants.JOB_STATE.ALL_STATES

    def test_normalized_state_always_in_lowercase(self):
        """Check that valid state in non-lowercase in valid"""

        state = 'SucCeSs'
        assert truedoc.common.normalize_job_state(state) == state.lower()
