"""
Configure pytest so that all integration tests are run against their mock and their Maya equivalent.
"""
import pytest


@pytest.fixture(scope='session', autouse=True)
def init_maya():
    """
    Initialise a standalone Maya session
    """
    from maya import cmds, standalone

    standalone.initialize()

    yield

    # Starting Maya 2016, we have to call uninitialize
    if float(cmds.about(v=True)) >= 2016.0:
        standalone.uninitialize()


@pytest.fixture(autouse=True)
def maya_session(maya_cmds):
    """
    Ensure that each test using a real Maya session start in an empty file.
    """
    maya_cmds.file(new=True, force=True)


@pytest.fixture(scope='session')
def maya_cmds():
    """
    Default maya.cmds module

    :return: The maya.cmds module
    :rtype: object
    """
    from maya import cmds
    return cmds


@pytest.fixture(scope='session')
def maya_pymel():
    """
    Default pymel module

    :return: The pymel module
    :rtype object
    """
    import pymel.core as pymel
    return pymel


@pytest.fixture(params=['maya', 'mock'])
def cmds(request):
    """
    Parametrized fixture that run the test both in mocked cmds and maya.cmds.
    """
    if request.param == 'maya':
        return request.getfixturevalue('maya_cmds')
    elif request.param == 'mock':
        return request.getfixturevalue('cmds_mock')


@pytest.fixture(params=['maya', 'mock'])
def pymel(request):
    """
    Parametrized fixture that run
    """
    if request.param == 'maya':
        return request.getfixturevalue('maya_pymel')
    elif request.param == 'mock':
        return request.getfixturevalue('pymel_mock')
