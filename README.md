# mock_maya

A mock for Autodesk Maya cmds and pymel API.

Originally developed to ease testing of omtk2.

## Installation

Using the mock require the `mock` and `enum` python package.

Running the test require `pytest`.

## Running the tests

To run the tests, run `test.sh`

## Usage

To create a `maya.cmds` mock:

```python
from maya_mock import MockedCmdsSession

cmds = MockedCmdsSession()
```

To create a `pymel` mock:

```python
from maya_mock import MockedPymelSession

pymel = MockedPymelSession()
```

You can also create temporary mock using `maya_mock.decorators`.

Temporary mock will patch `sys.modules` so that any import on  `maya.cmds` or `pymel` will import the mock.

```python
from maya_mock.decorators import mock_cmds

with mock_cmds() as cmds:
    pass  # Some code
``` 

```python
from maya_mock.decorators import mock_pymel

with mock_pymel() as pymel:
    pass  # Some code
```

## Contributing

Contributions are welcome
