"""
A schema is a snapshot of a Maya session registered node.
This can be used
"""
import argparse
import json
import logging
import os

from maya import cmds
from maya import standalone

log = logging.getLogger(__name__)

_DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    'schema.json'
)
_DEFAULT_PATH = os.path.abspath(_DEFAULT_PATH)

_PARSER = argparse.ArgumentParser()
_PARSER.add_argument('-p', '--path', default=_DEFAULT_PATH)


def _get_node_schema(node_type):
    data = {}

    attributes = cmds.attributeInfo(allAttributes=True, type=node_type)
    for attribute in attributes:
        attr_type = cmds.attributeQuery(attribute, type=node_type, attributeType=True)

        # Some attributes will return 'typed' as the type.
        # I don't know of any way of knowing in advance the type.
        # However for what we need, guessing might be enough.
        if attr_type == 'typed':
            if 'matrix' in attribute.lower():  # HACK
                attr_type = 'matrix'

        attr_name_short = cmds.attributeQuery(attribute, type=node_type, shortName=True)
        attr_name_nice = cmds.attributeQuery(attribute, type=node_type, niceName=True)

        attr_data = {
            'port_type': attr_type,
            'short_name': attr_name_short,
            'nice_name': attr_name_nice,
        }

        data[attribute] = attr_data

    return data


def _generate():
    data = {}
    node_types = cmds.allNodeTypes(includeAbstract=False)
    for node_type in node_types:
        sub_data = _get_node_schema(node_type)
        if sub_data:
            data[node_type] = sub_data
    return data


if __name__ == '__main__':
    standalone.initialize()

    args = _PARSER.parse_args()

    path = args.path

    cmds.loadPlugin('matrixNodes')

    data = _generate()

    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True)
