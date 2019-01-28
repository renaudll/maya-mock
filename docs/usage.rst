Usage
=====

You can create a session and interact with it directly.

.. code-block:: python

    import maya_mock
    session = maya_mock.MockedSession()
    session.create_node('transform', name='test')


You can also interact with a session via a binding like `cmds` or `pymel`.

.. code-block:: python

    import maya_mock
    session = maya_mock.MockedSession()
    cmds = maya_mock.MockedCmdsSession(session)
    cmds.createNode('transform', name='test')


.. code-block:: python

    import maya_mock
    session = maya_mock.MockedSession()
    pymel = maya_mock.MockedPymelSession(session)
    pymel.createNode('transform', name='test')


Schemas
-------

A schema is a snapshot of a Maya version.

You can generate a search from a maya session with this command:

.. code-block:: python

    from maya_mock import MockedSessionSchema
    schema = MockedSessionSchema.generate()


You can also use generate a schema from anywhere with this simple script:

.. code-block:: bash

    ./generate.sh ./schemas/test_schema.json


By default, a mocked session instance is schema-less.
This mean that a scene will be truly empty and no node type are registered.
Off course, a Maya installation is not as minimal, some objects are pre-registered and an empty scene is not empty.

When initializing a session, you can provide the schema to use:

.. code-block:: python

    from maya_mock import MockedSession, MockedSessionSchema
    schema = MockedSessionSchema.from_json_file('/path/to.json')
    session = MockedSession(schema=schema)


Decorators
----------

You also have access to decorators that will temporary expose a binding.
This is usefull if you have want to use the mock with already existing code.

These decorators will temporary patch `sys.modules` so that any import on  `maya.cmds` or `pymel` will import the mock.

.. code-block:: python

    import maya_mock
    from maya_mock.decorators import mock_cmds, mock_pymel

    session = maya_mock.MockedSession()

    with mock_cmds(session) as cmds:
        pass  # Some code


    with mock_pymel(session) as pymel:
        pass  # Some code
