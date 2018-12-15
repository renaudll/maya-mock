
class MockedPymelPort(object):
    """
    Port adaptor for a pymel.Attribute object.
    """
    def __init__(self, session, port):
        """
        :param session:
        :param maya_mock.MockedPort, port: The port to translate.
        """
        self.__session = session
        self._port = port

    def __repr__(self):
        return '<Mocked pymel.Attribute "{0}">'.format(self._port.name)

    def __melobject__(self):
        return self._port.dagpath

    def name(self):
        return '{}.{}'.format(self._port.node.__melobject__(), self._port.name)

    def longName(self):
        return self._port.name

    def shortName(self):
        return self._port.short_name

    def niceName(self):
        return self._port.nice_name
