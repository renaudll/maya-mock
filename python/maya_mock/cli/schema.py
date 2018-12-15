"""
A schema is a snapshot of a Maya session registered node.
"""
import argparse
import json
import logging
import os

from maya import cmds
from maya import standalone
from maya_mock.base.schema import SessionSchema

log = logging.getLogger(__name__)

_DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    'schema.json'
)
_DEFAULT_PATH = os.path.abspath(_DEFAULT_PATH)

_PARSER = argparse.ArgumentParser(description='Generate a schema.json file from a maya session.')
_PARSER.add_argument('-p', '--path', default=_DEFAULT_PATH)

if __name__ == '__main__':
    standalone.initialize()

    args = _PARSER.parse_args()

    path = args.path

    cmds.loadPlugin('matrixNodes')

    schema = SessionSchema.generate()
    data = schema.data

    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True)
