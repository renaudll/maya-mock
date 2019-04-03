import os
import pytest

from maya_mock import MockedSession, MockedCmdsSession, MockedPymelSession, MockedSessionSchema


@pytest.fixture
def schema_maya_2017():
    """
    Path to a schema export with maya 2017
    Unused by default.

    :return: An absolute file path
    :rtype: str
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'schema2017.json'))


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
