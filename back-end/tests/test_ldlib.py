import pytest
from ldlib import FeatureFlag

anonymous_user = {"key": "abc", "anonymous": True}


@pytest.mark.parametrize("flag_state", [(True), (False)])
def test_flag_status(flag_state, synopsis_flag_on):
    with FeatureFlag(
        key="musner_movie_synopsis_1_20220214", user=anonymous_user
    ) as flag:
        assert flag == flag_state
