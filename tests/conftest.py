import pytest

from maya_mock import MockedSession, MockedCmdsSession, MockedPymelSession


@pytest.fixture
def session():
    """
    Create a mocked Maya session

    :return: A mocked session instance.
    rtype: MockedSession
    """
    return MockedSession()


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

