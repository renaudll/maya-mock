#!/usr/bin/python2
"""
A schema is a snapshot of a Maya session registered node.
"""
import argparse
import copy
import glob
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile

from maya_mock.base.constants import MAYA_INSTALL_DIR_PER_PLATFORM
from maya_mock.base.schema import MockedSessionSchema

LOG = logging.getLogger(__name__)
_DEFAULT_PATH = os.path.abspath('schema.json')

_parser = argparse.ArgumentParser(description='Generate a schema.json file from a maya session.')
_parser.add_argument('path', nargs='?', default=_DEFAULT_PATH)
_parser.add_argument('-d', '--debug', action='store_true', help='Increate LOG level to DEBUG')


def _get_platform():
    platform = sys.platform

    if platform == 'linux2':
        return 'linux'

    return platform


def find_mayapy():
    """
    Resolve the path to a desired mayapy executable.
    :return:
    """
    platform = _get_platform()
    try:
        patterns = MAYA_INSTALL_DIR_PER_PLATFORM[platform]
    except KeyError:
        raise NotImplementedError("%s platform not implemented" % platform)

    files = {
        os.path.realpath(path)
        for pattern in patterns
        for path in glob.glob(pattern)
    }

    if not files:
        LOG.warning("Found no maya installed on system.")
        return

    if len(files) > 1:
        LOG.warning("Found more than one maya installation, choosing first: %s") % files

    interpreter_path = sorted(files, reverse=True)[0]

    return interpreter_path


def bootstrap():
    global args
    args = sys.argv
    LOG.debug("Scanning filesystem for mayapy...")
    mayapy = find_mayapy()
    LOG.debug("Found %r" % mayapy)

    args = [mayapy] + args
    env = copy.copy(os.environ)
    env['MAYA_MOCK_BOOTSTRAPED'] = '1'
    LOG.info("Bootstraping to %r" % mayapy)
    process = subprocess.Popen(args, env=env)
    process.communicate()


def _progress(iteration, total, prefix=''):
    percent = float(iteration) / total * 100
    msg = '[{:04.1f}%] Scanning {}\n'.format(percent, prefix)
    sys.stdout.write(msg)
    sys.stdout.flush()


def main():
    args = _parser.parse_args()
    if args.debug:
        LOG.setLevel(logging.DEBUG)
        LOG.debug('Detected debug flag, LOG level changed to DEBUG')

    LOG.debug('Checking if we are in Maya...')
    try:
        from maya import cmds, standalone
    except ImportError:
        # Before bootstraping, ensure we are not in a loop
        if 'MAYA_MOCK_BOOTSTRAPED' in os.environ:
            raise Exception('Bootstrap loop detected, abording.')

        LOG.warning('We are not in Maya, trying to boostrap...')
        bootstrap()
        return

    _, path_tmp = tempfile.mkstemp(suffix='json')
    path = os.path.abspath(args.path)
    LOG.info('Will save schema to %r', path)

    LOG.info("Initializing Maya...")
    standalone.initialize()
    cmds.loadPlugin('matrixNodes')

    LOG.info('Generating schema...')
    schema = MockedSessionSchema.generate(fn_progress=_progress)
    data = schema.to_dict()

    LOG.debug('Saving schema...')
    with open(path_tmp, 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True)

    LOG.debug('Applying changes...')
    shutil.copy2(path_tmp, path)
    os.remove(path_tmp)

    LOG.info('Done. Closing Maya...')


if __name__ == '__main__':
    main()
