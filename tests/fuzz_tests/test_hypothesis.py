import os
import pytest

import hypothesis.strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, Bundle, consumes
from maya import cmds, standalone

from maya_mock import MockedSession, MockedCmdsSession, MockedSessionSchema

from maya_mock.base import constants

standalone.initialize()

schema_file = os.path.join(constants.TEST_RESOURCE_DIR, "schema2017.json")
schema = MockedSessionSchema.from_json_file(schema_file)

# schema = MockedSessionSchema.generate()
known_types = schema.get_known_node_types()
strategy_node_type = st.sampled_from(known_types)

# strategy_node_name = st.from_regex('^[\w]+\Z')
strategy_node_name = st.text()


def _dump(cmds):
    result = {}
    node_names = cmds.ls()
    for node_name in node_names:
        attrs = set(cmds.listAttr(node_name))
        attrs = {
            attr.split(".")[-1] for attr in attrs
        }  # HACK: We currently don't support child attributes...
        result[node_name] = attrs
    return result


class MayaComparison(RuleBasedStateMachine):
    NODES = Bundle("NODES")

    def __init__(self):
        super(MayaComparison, self).__init__()

        cmds.file(new=True, force=True)

        self.session = MockedSession(schema=schema)
        self.mockCmds = MockedCmdsSession(self.session)

    def _cmd(self, cmd, *args, **kwargs):
        fn_mock = getattr(self.mockCmds, cmd)
        fn_maya = getattr(cmds, cmd)
        v_mock = None
        v_maya = None
        e_mock = None
        e_maya = None

        try:
            v_mock = fn_mock(*args, **kwargs)  # Create in mock
        except Exception as e_mock:
            pass
        try:
            v_maya = fn_maya(*args, **kwargs)  # Create in maya
        except Exception as e_maya:
            pass

        # If exception have been raised, assert they are the same.
        assert repr(e_mock) == repr(e_maya)

        # If values have been returned, assert they are the same.
        assert v_mock == v_maya

        return v_mock

    @rule(target=NODES, name=strategy_node_name, type_=strategy_node_type)
    def create_node(self, name, type_):
        before = {node.dagpath for node in self.session.nodes}
        self._cmd("createNode", type_, name=name)
        after = {node.dagpath for node in self.session.nodes}
        return after - before

    # @precondition(lambda self: self._cmd['ls'])  # Only if nodes are remaining
    # @rule(name=consumes(NODES))
    # def delete_node(self, name):
    #     before = {node.dagpath for node in self.session.nodes}
    #     self._cmd('delete', name)
    #     after = {node.dagpath for node in self.session.nodes}
    #     return before - after

    @invariant()
    def values_agree(self):
        # Ensure the name exist
        actual = _dump(self.mockCmds)
        expected = _dump(cmds)

        assert set(actual.keys()) == set(expected.keys())
        assert actual == expected


# TODO: Uncomment to run
TestDBComparison = MayaComparison.TestCase
