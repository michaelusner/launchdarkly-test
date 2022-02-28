import logging

import pytest

logging.basicConfig(level=logging.INFO)


@pytest.mark.feature_flag(key="TEST_FEATURE_FLAG", value=True)
def test_1(feature_flag, request):
    logging.info("Test: %s", request.node.name)


@pytest.mark.feature_flag(key="TEST_FEATURE_FLAG", value=False)
def test_2(feature_flag, request):
    logging.info("Test: %s", request.node.name)


@pytest.mark.feature_flag(key="TEST_FEATURE_FLAG", value=False)
def test_3(feature_flag, request):
    logging.info("Test: %s", request.node.name)


@pytest.mark.feature_flag(key="TEST_FEATURE_FLAG", value=False)
def test_4(feature_flag, request):
    logging.info("Test: %s", request.node.name)


@pytest.mark.feature_flag(key="TEST_FEATURE_FLAG", value=True)
def test_5(feature_flag, request):
    logging.info("Test: %s", request.node.name)


@pytest.mark.feature_flag(key="TEST_FEATURE_FLAG", value=True)
def test_6(feature_flag, request):
    logging.info("Test: %s", request.node.name)


@pytest.mark.feature_flag(key="TEST_FEATURE_FLAG", value=True)
def test_7(feature_flag, request):
    logging.info("Test: %s", request.node.name)
