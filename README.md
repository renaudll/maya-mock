# maya_mock

[![Actions](https://github.com/renaudll/maya-mock/workflows/tests/badge.svg)](https://github.com/renaudll/maya-mock/actions)
[![codecov](https://codecov.io/gh/renaudll/maya-mock/branch/master/graph/badge.svg)](https://codecov.io/gh/renaudll/maya-mock)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A mock for Autodesk Maya and it's `cmds` and `pymel` API. 

Originally developed to ease testing of omtk2. 

## Installation

You can install the project with all it's dependencies with pip.
Navigate to the root directory and run:

```bash
pip install .
```

## Testing

To run the tests you'll need to install tox.

```bash
pip install tox
```

Then assuming you have python-2, python-3 and maya-2017 on your system, you can run all checks with:

```bash
tox
```

### Tox tips

You can run individual checks with the `-e` flag.
See the `tox.ini` file for the available targets.

```bash
tox -e unit-py2.7
```

You can also pass arguments to your tests with the `--` flag.
For example, here's how to run a single test named `test_node_shape_transform_melobject` in python-2.7:

```bash
tox -e unit-py2.7 -- -k test_node_shape_transform_melobject
```

## Usage

You can create a session and interact with it directly.

```python
import maya_mock
session = maya_mock.MockedSession()
session.create_node('transform', name='test')
```

You can also interact with a session via a binding like `cmds` or `pymel`.

```python
import maya_mock
session = maya_mock.MockedSession()
cmds = maya_mock.MockedCmdsSession(session)
cmds.createNode('transform', name='test')
```

```python
import maya_mock
session = maya_mock.MockedSession()
pymel = maya_mock.MockedPymelSession(session)
pymel.createNode('transform', name='test')
```

## Schemas

A schema is a snapshot of a Maya version.

You can generate a search from a maya session with this command:

```python
from maya_mock import MockedSessionSchema
schema = MockedSessionSchema.generate()
```

You can also use generate a schema from anywhere with this simple script:

```bash
./generate ./schemas/test_schema.json
```

By default, a mocked session instance is schema-less.
This mean that a scene will be truly empty and no node type are registered.
Off course, a Maya installation is not as minimal, some objects are pre-registered and an empty scene is not empty.

When initializing a session, you can provide the schema to use:

```python
from maya_mock import MockedSession, MockedSessionSchema
schema = MockedSessionSchema.from_json_file('/path/to.json')
session = MockedSession(schema=schema)
```

## Decorators

You also have access to decorators that will temporary expose a binding.
This is usefull if you have want to use the mock with already existing code.

These decorators will temporary patch `sys.modules` so that any import on  `maya.cmds` or `pymel` will import the mock.

```python
import maya_mock
from maya_mock.decorators import mock_cmds, mock_pymel

session = maya_mock.MockedSession()

with mock_cmds(session) as cmds:
    pass  # Some code


with mock_pymel(session) as pymel:
    pass  # Some code
```

## Contributing

Any contributions are welcome in the form of a PR! 
