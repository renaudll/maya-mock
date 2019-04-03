"""
Simplistic mock for Maya cmds and pymel API.
"""
import logging

from maya_mock.base.connection import MockedConnection
from maya_mock.base.node import MockedNode
from maya_mock.base.port import MockedPort
from maya_mock.base.schema import MockedSessionSchema
from maya_mock.base.session import MockedSession
from maya_mock.cmds import MockedCmdsSession
from maya_mock.pymel import MockedPymelSession, MockedPymelNode, MockedPymelPort

# Configure root logger
log = logging.getLogger('maya_mock')

__all__ = (
    'MockedNode',
    'MockedPort',
    'MockedConnection',
    'MockedSession',
    'MockedSessionSchema',
    'MockedCmdsSession',
    'MockedPymelSession',
    'MockedPymelNode',
    'MockedPymelPort',
    'LOG'
)
