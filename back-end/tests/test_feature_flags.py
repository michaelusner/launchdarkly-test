import feature_flags
import pytest
from fastapi import Depends, HTTPException

anonymous_user = {"cid": "pytest", "email": "anonymous"}


@pytest.mark.mock_feature_flag(key="test_flag_should_equal_value", value="123")
def test_flag_should_equal_value(mock_feature_flag):
    assert (
        feature_flags.flag(
            key="test_flag_should_equal_value",
            user=feature_flags.get_launchdarkly_user(**anonymous_user),
        )
        == mock_feature_flag
    )


@pytest.mark.asyncio
@pytest.mark.mock_feature_flag(
    key="test_flag_context_manager_should_return_flag", value="456"
)
async def test_flag_context_manager_should_return_flag(mock_feature_flag):
    with feature_flags.FeatureFlag(
        "test_flag_context_manager_should_return_flag",
        user=feature_flags.get_launchdarkly_user(**anonymous_user),
        default=None,
    ) as flag:
        assert flag == "456"


# @pytest.mark.asyncio
# @pytest.mark.mock_feature_flag(
#     key="test_flag_route_decorator_disabled_should_raise", value="789"
# )
# async def test_flag_route_decorator_disabled_should_raise(mock_feature_flag):
#     @feature_flags.route_feature_flag(
#         key="test_flag_route_decorator_disabled_should_raise",
#         value="asd",
#         raise_on_disabled=HTTPException,
#         status_code=404,
#     )
#     async def flag_function():
#         return

#     with pytest.raises(HTTPException):
#         await flag_function()


# @pytest.mark.asyncio
# @pytest.mark.mock_feature_flag(
#     key="test_flag_route_decorator_enabled_should_not_raise", value=True
# )
# async def test_flag_route_decorator_enabled_should_not_raise(mock_feature_flag):
#     @feature_flags.route_feature_flag(
#         key="test_flag_route_decorator_enabled_should_not_raise",
#         value=True,
#         raise_on_disabled=True,
#     )
#     async def flag_function(ld_user=Depends(feature_flags.get_launchdarkly_user)):
#         return

#     await flag_function()
