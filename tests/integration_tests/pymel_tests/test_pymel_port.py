# coding: utf-8
"""Unit-tests for our pymel.general.Attribute mock."""
import six

import pytest


@pytest.fixture
def port(pymel):
    """Fixture for a port on a node."""
    node = pymel.createNode("transform")
    pymel.addAttr(node, longName="fooLong", shortName="fooShort", niceName="fooNice")
    port = node.fooLong
    return port


def test_port_name(port):
    """Validate the `name` method behavior."""
    actual = port.name()
    assert actual == "transform1.fooLong"
    assert type(actual) is six.text_type


def test_port_longName(port):
    """Validate the `longName` method behavior."""
    actual = port.longName()
    assert actual == "fooLong"
    assert type(actual) is six.text_type


def test_port_shortName(port):
    """Validate the `shortName` method behavior."""
    actual = port.shortName()
    assert actual == "fooShort"
    assert type(actual) is six.text_type


def test_port_get(port):
    """Validate the `get` method behavior."""
    assert port.get() == 0.0


def test_port_set(port):
    """Validate the `set` method behavior."""
    port.set(10.0)
    assert port.get() == 10.0


def test_port__melobject__(port):
    """Validate the `__melobject__` magic method behavior."""
    actual = port.__melobject__()
    assert actual == "transform1.fooLong"
    assert type(actual) is six.text_type


def test_port__str__(port):
    """Validate the `__str__` magic method behavior."""
    actual = str(port)
    assert actual == "transform1.fooLong"
    assert type(actual) is str


def test_port__repr__(port):
    """Validate the `__repr__` magic method behavior."""
    actual = repr(port)
    assert actual == "Attribute(u'transform1.fooLong')"
    assert type(actual) is str
