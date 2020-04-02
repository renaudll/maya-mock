"""
Test cases for MockedPymelPort
"""
# pylint: disable=redefined-outer-name
import six

import pytest


@pytest.fixture
def port(pymel):
    """Fixture for a port on a node."""
    node = pymel.createNode("transform")
    pymel.addAttr(node, longName="fooLong", shortName="fooShort", niceName="fooNice")
    port = node.fooLong
    return port


def test_name(port):
    """Validate the `name` method behavior."""
    actual = port.name()
    assert actual == "transform1.fooLong"
    assert isinstance(actual, six.text_type)


def testlongName(port):  # pylint: disable=invalid-name
    """Validate the `longName` method behavior."""
    actual = port.longName()
    assert actual == "fooLong"
    assert isinstance(actual, six.text_type)


def testshortName(port):  # pylint: disable=invalid-name
    """Validate the `shortName` method behavior."""
    actual = port.shortName()
    assert actual == "fooShort"
    assert isinstance(actual, six.text_type)


def test_get(port):
    """Validate the `get` method behavior."""
    assert port.get() == 0.0


def test_set(port):
    """Validate the `set` method behavior."""
    port.set(10.0)
    assert port.get() == 10.0


def test_melobject__(port):
    """Validate the `__melobject__` magic method behavior."""
    actual = port.__melobject__()
    assert actual == "transform1.fooLong"
    assert isinstance(actual, six.text_type)


def test_str__(port):
    """Validate the `__str__` magic method behavior."""
    actual = str(port)
    assert actual == "transform1.fooLong"
    assert isinstance(actual, str)


def test_repr__(port):
    """Validate the `__repr__` magic method behavior."""
    actual = repr(port)
    assert actual == "Attribute(u'transform1.fooLong')"
    assert isinstance(actual, str)
