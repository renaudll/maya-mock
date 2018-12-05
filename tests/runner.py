"""
The runner launched pytest with either pytest from mayapy or from the system python site-packages
https://github.com/arubertoson/mayatest
"""
import os
import sys
import pytest


class PytestMayaPlugin(object):

    def pytest_sessionstart(self):
        import maya.standalone
        maya.standalone.initialize()

        # If testing a maya module make sure PYTHONPATH and sys.path are
        # identical
        realsyspath = [os.path.realpath(path) for path in sys.path]
        pythonpath = os.environ.get('PYTHONPATH', '')
        for p in pythonpath.split(os.pathsep):
            p = os.path.realpath(p)
            if p not in realsyspath:
                sys.path.insert(0, p)

    def pytest_sessionfinish(self):
        import maya.standalone
        from maya import cmds
        # Starting Maya 2016, we have to call uninitialize
        if float(cmds.about(v=True)) >= 2016.0:
            maya.standalone.uninitialize()


def main():
    pytest_args = sys.argv[1]
    pytest.main([pytest_args], plugins=[PytestMayaPlugin()])


if __name__ == '__main__':
    main()