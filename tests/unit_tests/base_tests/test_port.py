"""
Test cases for MockedPost
"""
# pylint: disable=redefined-outer-name
import six
import pytest

from maya_mock import MockedSession, MockedPort


@pytest.fixture
def session():
    """
    :rtype: maya_mock.MockedSession
    """
    return MockedSession()


@pytest.fixture
def node(session):
    """
    :rtype: maya_mock.MockedNode
    """
    return session.create_node("transform")


@pytest.mark.parametrize(
    "actual,expected",
    ((None, u"foo"), ("fooShort", u"fooShort"), (u"fooShort", u"fooShort")),
)  # pylint: disable=invalid-name
def test_port_init_shortName(node, actual, expected):
    """Validate we can define a port 'short_name'."""
    port = MockedPort(node, "foo", short_name=actual)
    assert port.short_name == expected
    assert isinstance(port.short_name, six.text_type)


@pytest.mark.parametrize(
    "actual,expected",
    ((None, u"foo"), ("fooNice", u"fooNice"), (u"fooNice", u"fooNice")),
)  # pylint: disable=invalid-name
def test_port_init_niceName(node, actual, expected):
    """Validate we can define a port 'nice_name'."""
    port = MockedPort(node, "foo", nice_name=actual)
    assert port.nice_name == expected
    assert isinstance(port.nice_name, six.text_type)


@pytest.mark.parametrize(
    "name,match,expected",
    (
        ("foo", None, True),
        ("foo", "foo", True),
        ("foo1", "foo", False),
        ("foo1", "foo*", True),
    ),
)
def test_port_match(node, name, match, expected):
    """Validate the port match function."""
    port = MockedPort(node, name)
    assert port.match(match) == expected
