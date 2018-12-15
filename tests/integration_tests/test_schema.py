import pytest

from maya_mock import MockedSession
from maya_mock.base.schema import SessionSchema


@pytest.fixture(scope='session')
def schema():
    """
    Generate a schema from the current session.
    """
    return SessionSchema.generate()


@pytest.fixture
def session(schema):
    """
    Create a mocked Maya session
    """
    return MockedSession(preset=schema)


def test_create_node_from_schema(session, schema):
    """Ensure that creating a node will correctly create ports from the schema."""
    # TODO: Test more than port names
    node = session.create_node("transform")
    node_def = schema.get(node.type)
    actual = {port.name for port in session.ports}
    expected = set(node_def.data.keys())
    assert actual == expected
