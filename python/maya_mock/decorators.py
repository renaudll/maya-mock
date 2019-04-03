import sys
from contextlib import contextmanager

from maya_mock.cmds import MockedCmdsSession
from maya_mock.pymel import MockedPymelSession, MockedPymelNode, MockedPymelPort


@contextmanager
def _patched_sys_modules(data):
    """
    Temporary override sys.modules with provided data.
    This will take control of the import process.

    :param dict data: The data to overrides.
    """
    # Hold sys.modules
    old_data = {key: sys.modules.get(key) for key in data}

    # Patch sys.modules
    for key, val in data.iteritems():
        sys.modules[key] = val

    yield

    # Restore sys.modules
    for key, val in old_data.iteritems():
        if val is None:
            sys.modules.pop(key)
        else:
            sys.modules[key] = val


def _create_cmds_module_mock(cmds):
    """
    Create a MagicMock for the cmds module.
    """
    import mock

    kwargs = {'cmds': cmds}
    module_maya = mock.MagicMock(**kwargs)
    return module_maya


@contextmanager
def mock_cmds(session):
    """
    Context that temporary intercept maya.session with our mock.
    Use this to run complex maya operations in a mocked env.

    Usage:

    >>> with mock_cmds(session) as session:
    >>>     cmds.createNode('transform1')

    :param MockedSession session: The session to mock.
    :return: A context
    :rtype: contextmanager.GeneratorContextManager
    """
    cmds = session if isinstance(session, MockedCmdsSession) else MockedCmdsSession(session)

    # Prepare sys.modules patch
    module_maya = _create_cmds_module_mock(cmds)
    new_sys = {'maya': module_maya, 'maya.cmds': cmds}

    with _patched_sys_modules(new_sys):
        yield cmds


def _create_pymel_module_mock(pymel):
    # kwargs = {'core': pymel}
    import mock

    kwargs = {
        'core.PyNode': MockedPymelNode,
        'core.Attribute': MockedPymelPort,
    }
    for attr in dir(pymel):
        if not attr.startswith("_"):
            kwargs['core.{}'.format(attr)] = getattr(pymel, attr)

    module_pymel = mock.MagicMock(**kwargs)

    return module_pymel

@contextmanager
def mock_pymel(session):
    """
    Context that temporary intercept maya.cmds with our mock.
    Use this to run complex maya operations in a mocked env.

    Usage:

    >>> with mock_pymel(session) as pymel:
    >>>    pymel.createNode('transform')

    :param MockedPymelSession session: The session to mock.
    :return: A context
    :rtype: contextmanager.GeneratorContextManager
    """
    # Context manager that ensure that when trying to import pymel it import a mock.
    # Useful when using external methods that don't expect the mock.
    pymel = session if isinstance(session, MockedPymelSession) else MockedPymelSession(session)

    # Prepare sys.modules patch
    module_pymel = _create_pymel_module_mock(pymel)
    sys_data = {
        'pymel': module_pymel,
        'pymel.core': module_pymel.core,
        'pymel.core.PyNode': module_pymel.core.PyNode,
        'pymel.core.Attribute': module_pymel.core.Attribute,
    }

    with _patched_sys_modules(sys_data):
        yield pymel
