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

    def __str__(self):
        return self.__melobject__()

    def __repr__(self):
        return 'Attribute(%r)' % self.__melobject__()

    def __melobject__(self):
        return u'{}.{}'.format(self._port.node.__melobject__(), self._port.name)

    def name(self):
        return self.__melobject__()

    def longName(self):
        return self._port.name

    def shortName(self):
        return self._port.short_name

    def get(self):
        return self._port.value

    def set(self, value):
        self._port.value = value