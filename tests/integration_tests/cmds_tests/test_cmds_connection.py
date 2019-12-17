import os
import itertools

import pytest

from maya_mock.base.constants import EnumAttrTypes, CONVERSION_FACTOR_BY_TYPE
from maya_mock.base.schema import MockedSessionSchema

# src: http://download.autodesk.com/us/maya/2010help/CommandsPython/addAttr.html
_g_addAttr_kwargs_map = {
    EnumAttrTypes.bool: {"at": "double"},
    EnumAttrTypes.long: {"at": "long"},
    EnumAttrTypes.short: {"at": "short"},
    EnumAttrTypes.byte: {"at": "byte"},
    # EnumAttrTypes.char: {'at': 'char'},  # char -> char don't work
    EnumAttrTypes.float: {"at": "float"},
    EnumAttrTypes.double: {"at": "double"},
    EnumAttrTypes.doubleAngle: {"at": "doubleAngle"},
    EnumAttrTypes.doubleLinear: {"at": "doubleLinear"},
    EnumAttrTypes.string: {"dt": "string"},
    # 'enum': {'at': 'enum'},
    # 'stringArray': {'dt': 'stringArray'},
    # 'compound': {'at': 'compound'},
    # 'message': {'at': 'message'},
    # 'time': {'at': 'time'},
    # 'matrix': {'dt': 'matrix'},
    # 'fltMatrix': {'at': 'fltMatrix'},
    # 'reflectanceRGB': {'dt': 'reflectanceRGB'},
    # 'reflectance': {'at': 'reflectance'},
    # 'spectrumRGB': {'dt': 'spectrumRGB'},
    # 'spectrum': {'at': 'spectrum'},
    # 'float2': {'dt': 'float2'},
    # 'float3': {'dt': 'float3'},
    # 'double2': {'dt': 'double2'},
    # 'double3': {'dt': 'double3'},
    # 'long2': {'dt': 'long2'},
    # 'long3': {'dt': 'long3'},
    # 'short2': {'dt': 'short2'},
    # 'short3': {'dt': 'short3'},
    # 'doubleArray': {'dt': 'doubleArray'},
    # 'Int32Array': {'dt': 'Int32Array'},
    # 'vectorArray': {'dt': 'vectorArray'},
    # 'nurbsCurve': {'dt': 'nurbsCurve'},
    # 'nurbsSurface': {'dt': 'nurbsSurface'},
    # 'mesh': {'dt': 'mesh'},
    # 'lattice': {'dt': 'lattice'},
    # 'pointArray': {'dt': 'pointArray'}
}
_g_addAttr_kwargs_map = [
    (key, val) for key, val in _g_addAttr_kwargs_map.items()
]  # convert to tuple


@pytest.fixture
def schema_file():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "resources", "schema2017.json"
        )
    )


@pytest.fixture
def schema(schema_file):
    return MockedSessionSchema.from_json_file(schema_file)


@pytest.fixture
def connection(cmds):
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="src")
    cmds.addAttr(node, longName="dst")
    cmds.connectAttr("transform1.src", "transform1.dst")


def test_connectAttr(cmds):
    """Ensure we can create a connection."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="src")
    cmds.addAttr(node, longName="dst")
    cmds.connectAttr("transform1.src", "transform1.dst")

    assert cmds.connectionInfo("transform1.src", destinationFromSource=True) == [
        "transform1.dst"
    ]
    assert cmds.connectionInfo("transform1.src", sourceFromDestination=True) == ""
    assert (
        cmds.connectionInfo("transform1.dst", sourceFromDestination=True)
        == "transform1.src"
    )
    assert cmds.connectionInfo("transform1.dst", destinationFromSource=True) == []


def test_connectAttr_missing_src(cmds):
    """Ensure proper behavior when trying to create a connection for a non-existent source."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="dst")

    with pytest.raises(RuntimeError) as exception:
        cmds.connectAttr("transform1.src", "transform1.dst")
    assert exception.match("The source attribute 'transform1.src' cannot be found.")


def test_connectAttr_missing_dst(cmds):
    """Ensure proper behavior when trying to create a connection from a non-existent destination."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="src")
    with pytest.raises(RuntimeError) as exception:
        cmds.connectAttr("transform1.src", "transform1.dst")
    assert exception.match(
        "The destination attribute 'transform1.dst' cannot be found."
    )


def test_connectAttr_existing_connection(cmds):
    """Ensure that trying to create a connection using already connection nodes raise a RuntimeError."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="src")
    cmds.addAttr(node, longName="dst")
    cmds.connectAttr("transform1.src", "transform1.dst")
    with pytest.raises(RuntimeError) as exception:
        cmds.connectAttr("transform1.src", "transform1.dst")
    assert exception.match("Maya command error")


def test_connectAttr_incompatible_ports(cmds):
    """Ensure that trying to connect two incompatible ports result in a RuntimeError."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="src", at="char")
    cmds.addAttr(node, longName="dst", dt="string")
    with pytest.raises(RuntimeError) as exception:
        cmds.connectAttr("transform1.src", "transform1.dst")
    assert exception.match(
        "The attribute '|transform1.src' cannot be connected to '|transform1.dst'."
    )


@pytest.mark.usefixtures("connection")
def test_disconnectAttr(cmds):
    """Ensure that trying to create a connection using already connection nodes raise a RuntimeError."""
    cmds.disconnectAttr("transform1.src", "transform1.dst")
    assert cmds.connectionInfo("transform1.src", destinationFromSource=True) == []
    assert cmds.connectionInfo("transform1.src", sourceFromDestination=True) == ""
    assert cmds.connectionInfo("transform1.dst", sourceFromDestination=True) == ""
    assert cmds.connectionInfo("transform1.dst", destinationFromSource=True) == []


@pytest.mark.usefixtures("connection")
def test_connectionInfo_no_flag(cmds):
    """Ensure connectionInfo error out correctly if no flags are provided."""
    with pytest.raises(RuntimeError) as exception:
        cmds.connectionInfo("transform1.src")
    assert exception.match("You must specify exactly one flag.")


@pytest.mark.usefixtures("connection")
def test_connectionInfo_both_flag_at_once(cmds):
    """Ensure connectionInfo error out correctly if both flags are provided at once."""
    with pytest.raises(RuntimeError) as exception:
        cmds.connectionInfo(
            "transform1.src", sourceFromDestination=True, destinationFromSource=True
        )
    assert exception.match("You cannot specify more than one flag.")


@pytest.mark.usefixtures("connection")
def test_disconnectAttr_no_connection(cmds):
    with pytest.raises(RuntimeError) as exception:
        cmds.disconnectAttr(
            "transform1.dst", "transform1.src"
        )  # note: args are inverted
    assert exception.match(
        "There is no connection from 'transform1.dst' to 'transform1.src' to disconnect"
    )


@pytest.fixture(
    params=itertools.permutations(
        (
            EnumAttrTypes.byte,
            EnumAttrTypes.doubleAngle,
            EnumAttrTypes.double,
            EnumAttrTypes.long,
            EnumAttrTypes.short,
        )
    )
)
def test_connect_different_types(request, cmds, maya_session, src_data, dst_data):
    """Assert that when connecting a double port to a doubleAngle port a unitConversion is created."""
    # Hack: Need to determine why the object sometimes exist...
    for obj in cmds.ls(type="transform") + cmds.ls(type="unitConversion"):
        cmds.delete(obj)
    cmds.delete("transform*")
    cmds.delete("unitConversion*")

    type_src, type_dst = request.param
    src_kwargs = _g_addAttr_kwargs_map[type_src]
    dst_kwargs = _g_addAttr_kwargs_map[type_dst]

    port_src_name = "testSrc" + type_src.value
    port_dst_name = "testDst" + type_dst.value
    port_src_dagpath = u"transform1." + port_src_name
    port_dst_dagpath = u"transform1." + port_dst_name
    cmds.createNode("transform")
    cmds.addAttr("transform1", longName=port_src_name, **src_kwargs)
    cmds.addAttr("transform1", longName=port_dst_name, **dst_kwargs)
    cmds.connectAttr(port_src_dagpath, port_dst_dagpath)

    factor = CONVERSION_FACTOR_BY_TYPE.get((type_src, type_dst))

    if factor:
        assert cmds.connectionInfo(port_src_dagpath, destinationFromSource=True) == [
            u"unitConversion1.input"
        ]
        assert (
            cmds.connectionInfo(port_dst_dagpath, sourceFromDestination=True)
            == u"unitConversion1.output"
        )
        assert cmds.getAttr("unitConversion1.conversionFactor") == factor
    else:
        assert cmds.connectionInfo(port_src_dagpath, destinationFromSource=True) == [
            port_dst_dagpath
        ]
        assert (
            cmds.connectionInfo(port_dst_dagpath, sourceFromDestination=True)
            == port_src_dagpath
        )
