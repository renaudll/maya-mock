#!/usr/bin/python2
"""
A schema is a snapshot of a Maya session registered node.
"""
import argparse
import json
import logging
import os
import shutil
import sys
import tempfile

from maya_mock.base.schema import MockedSessionSchema

LOG = logging.getLogger(__name__)
_DEFAULT_PATH = os.path.abspath("schema.json")

_parser = argparse.ArgumentParser(
    description="Generate a schema.json file from a maya session."
)
_parser.add_argument("path", nargs="?", default=_DEFAULT_PATH)
_parser.add_argument(
    "-d", "--debug", action="store_true", help="Increate LOG level to DEBUG"
)


def _progress(iteration, total, prefix=""):
    percent = float(iteration) / total * 100
    msg = "[{:04.1f}%] Scanning {}\n".format(percent, prefix)
    sys.stdout.write(msg)
    sys.stdout.flush()


def main():
    args = _parser.parse_args()
    if args.debug:
        LOG.setLevel(logging.DEBUG)
        LOG.debug("Detected debug flag, LOG level changed to DEBUG")

    from maya import cmds, standalone

    _, path_tmp = tempfile.mkstemp(suffix="json")
    path = os.path.abspath(args.path)
    LOG.info("Will save schema to %r", path)

    LOG.info("Initializing Maya...")
    standalone.initialize()
    cmds.loadPlugin("matrixNodes")

    LOG.info("Generating schema...")
    schema = MockedSessionSchema.generate(fn_progress=_progress)
    data = schema.to_dict()

    LOG.debug("Saving schema...")
    with open(path_tmp, "w") as fp:
        json.dump(data, fp, indent=4, sort_keys=True)

    LOG.debug("Applying changes...")
    shutil.copy2(path_tmp, path)
    os.remove(path_tmp)

    LOG.info("Saved to %r" % path)
    LOG.info("Done. Closing Maya...")

    standalone.uninitialize()
