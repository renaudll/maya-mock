"""
Fixtures common to all tests
"""
# pylint: disable=redefined-outer-name
import os

import pytest

from maya_mock import (
    MockedSession,
    MockedCmdsSession,
    MockedPymelSession,
    MockedSessionSchema,
)

# We use an environment variable to determine if maya is available.
# If this variable is set, tests will be ran both in maya and our mock.
# Very useful to ensure we have the same behavior than maya.
_MAYA_IS_AVAILABLE = bool(os.environ.get("MAYA_MOCK_RUN_TEST_WITH_MAYA"))
_PARAMS = ["maya"] if _MAYA_IS_AVAILABLE else ["mock"]


@pytest.fixture
def schema():
    """
    Create a Maya session schema.
    This is made to be overridden by higher level tests.

    :return: A mocked session schema
    :rtype: MockedSessionSchema
    """
    return MockedSessionSchema()


@pytest.fixture
def session(schema):
    """
    Create a mocked Maya session

    :return: A mocked session instance.
    rtype: MockedSession
    """
    return MockedSession(schema=schema)


@pytest.fixture
def cmds_mock(session):
    """
    Create a maya.cmds mock

    :param MockedSession session: A mocked Maya session
    :return: A mock for maya.cmds
    :rtype: MockedCmdsSession
    """
    return MockedCmdsSession(session)


@pytest.fixture
def pymel_mock(session):
    """
    Create a pymel mock
    :param MockedSession session: A mocked Maya session
    :return: A mock for pymel
    :rtype: MockedPymelSession
    """
    return MockedPymelSession(session)


@pytest.fixture(scope="session", autouse=_MAYA_IS_AVAILABLE)
def init_maya():
    """
    Initialise a standalone Maya session
    """
    from maya import standalone  # pylint: disable=import-outside-toplevel

    standalone.initialize()

    yield

    standalone.uninitialize()


@pytest.fixture(autouse=_MAYA_IS_AVAILABLE)
def maya_session(maya_cmds):
    """
    Ensure that each test using a real Maya session start in an empty file.
    """
    maya_cmds.file(new=True, force=True)


@pytest.fixture(scope="session")
def maya_cmds():
    """
    Default maya.cmds module
    """
    from maya import cmds  # pylint: disable=import-error,import-outside-toplevel

    return cmds


@pytest.fixture(scope="session")
def maya_pymel():
    """
    Default pymel module
    """
    import pymel.core as pymel  # pylint: disable=import-error,import-outside-toplevel

    return pymel


@pytest.fixture(params=_PARAMS)
def cmds(request):
    """
    Parametrized fixture that run the test both in mocked cmds and maya.cmds.
    """
    if request.param == "maya":
        return request.getfixturevalue("maya_cmds")

    if request.param == "mock":
        return request.getfixturevalue("cmds_mock")

    raise ValueError("Unexpected request %r" % request.param)


@pytest.fixture(params=_PARAMS)
def pymel(request):
    """
    Parametrized fixture that run
    """
    if request.param == "maya":
        return request.getfixturevalue("maya_pymel")

    if request.param == "mock":
        return request.getfixturevalue("pymel_mock")

    raise ValueError("Unexpected request %r" % request.param)
