from enum import Enum


class EnumAttrTypes(Enum):
    """
    # src: http://download.autodesk.com/us/maya/2010help/CommandsPython/addAttr.html
    """
    bool = 'bool'
    long = 'long'
    short = 'short'
    byte = 'byte'
    char = 'char'
    enum = 'enum'
    float = 'float'
    double = 'double'
    doubleAngle = 'doubleAngle'
    doubleLinear = 'doubleLinear'
    string = 'string'
    stringArray = 'stringArray'
    compound = 'compound'
    message = 'message'
    time = 'time'
    matrix = 'matrix'
    fltMatrix = 'fltMatrix'
    reflectanceRGB = 'reflectanceRGB'
    reflectance = 'reflectance'
    spectrumRGB = 'spectrumRGB'
    spectrum = 'spectrum'
    float2 = 'float2'
    float3 = 'float3'
    double2 = 'double2'
    double3 = 'double3'
    double4 = 'double4'
    long2 = 'long2'
    long3 = 'long3'
    short2 = 'short2'
    short3 = 'short3'
    doubleArray = 'doubleArray'
    Int32Array = 'Int32Array'
    vectorArray = 'vectorArray'
    nurbsCurve = 'nurbsCurve'
    nurbsSurface = 'nurbsSurface'
    mesh = 'mesh'
    lattice = 'lattice'
    pointArray = 'pointArray'

    # The types bellow are returned when generating a SessionSchema
    # We don't know why they exist and don't really want them.
    typed = 'typed'
    generic = 'generic'
