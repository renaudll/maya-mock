"""
Fuzz test using hypothesis.
"""
import hypothesis.strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, Bundle
from maya_mock import MockedSession, MockedCmdsSession, MockedSessionSchema
from maya import cmds, standalone

from .. import constants

standalone.initialize()

_SCHEMA = MockedSessionSchema.from_json_file(constants.PATH_SCHEMA_2017)

# schema = MockedSessionSchema.generate()
_KNOWN_TYPES = _SCHEMA.get_known_node_types()
_STRATEGY_NODE_TYPE = st.sampled_from(_KNOWN_TYPES)

# _STRATEGY_NODE_NAME = st.from_regex('^[\w]+\Z')
_STRATEGY_NODE_NAME = st.text()


def _dump(cmds_):
    result = {}
    node_names = cmds_.ls()
    for node_name in node_names:
        attrs = set(cmds_.listAttr(node_name))
        attrs = {
            attr.split(".")[-1] for attr in attrs
        }  # HACK: We currently don't support child attributes...
        result[node_name] = attrs
    return result


class MayaComparison(RuleBasedStateMachine):
    """
    Hypothesis fuzz test that does various operations in maya and our mock at the same time.
    """

    NODES = Bundle("NODES")

    def __init__(self):
        super(MayaComparison, self).__init__()

        cmds.file(new=True, force=True)

        self.session = MockedSession(schema=_SCHEMA)
        self.mocked_cmds = MockedCmdsSession(self.session)

    def _cmd(self, cmd, *args, **kwargs):
        fn_mock = getattr(self.mocked_cmds, cmd)
        fn_maya = getattr(cmds, cmd)
        result_mock = None
        result_maya = None
        error_mock = None
        error_maya = None

        try:
            result_mock = fn_mock(*args, **kwargs)  # Create in mock
        except Exception as error_mock:  # pylint: disable=broad-except
            pass
        try:
            result_maya = fn_maya(*args, **kwargs)  # Create in maya
        except Exception as error_maya:  # pylint: disable=broad-except
            pass

        # If exception have been raised, assert they are the same.
        assert repr(error_mock) == repr(error_maya)

        # If values have been returned, assert they are the same.
        assert result_mock == result_maya

        return result_mock

    @rule(target=NODES, name=_STRATEGY_NODE_NAME, type_=_STRATEGY_NODE_TYPE)
    def create_node(self, name, type_):
        """
        Create a node both in our mock and in maya.

        :param str name: A node name
        :param str type_: A node type
        :return: The created node
        :rtype: set[str]
        """
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
        """
        Validate that maya and our mock share the same state.

        :raises AssertionError: If maya and our mock differ in any way.
        """
        # Ensure the name exist
        actual = _dump(self.mocked_cmds)
        expected = _dump(cmds)

        assert set(actual.keys()) == set(expected.keys())
        assert actual == expected


# Necessary for the tests to run via pytest
TestDBComparison = MayaComparison.TestCase  # pylint: disable=invalid-name
