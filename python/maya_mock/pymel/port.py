"""Mock for pymel.core.Attribute"""


class MockedPymelPort(object):
    """
    Port adaptor for a pymel.Attribute object.

    See `documentation <https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.Attribute.html#pymel.core.general.Attribute>`_ for details.
    """

    def __init__(self, session, port):
        """
        :param session:
        :param maya_mock.MockedPort, port: The port to translate.
        """
        self.__session = session
        self._port = port

    def __str__(self):
        return self.__melobject__()

    def __repr__(self):
        return 'Attribute(%r)' % self.__melobject__()

    def __melobject__(self):
        return u'{}.{}'.format(self._port.node.__melobject__(), self._port.name)

    def name(self):
        """
        :return: The name of the attribute (plug)
        :rtype: str
        """
        return self.__melobject__()

    def longName(self):
        return self._port.name

    def shortName(self):
        return self._port.short_name

    def get(self):
        return self._port.value

    def set(self, value):
        self._port.value = value
