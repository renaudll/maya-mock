#!/bin/bash
# Common recipe for bootstraping maya and it's dependencies.

function _APPEND() {
  # $1: The name of the variable to append to
  # $2: The value to append
  echo "[setup] Append to $1: $2"
  eval "$1=\$$1:$2"
}
function _PREPEND() {
  # $1: The name of the variable to prepend to
  # $2: The value to append
  echo "[setup] Prepend to $1: $2"
  eval "$1=$2:\$$1"
}

# Export mayapy
_SRC_DIR=$(pwd)/src
_APPEND "PYTHONPATH" "${_SRC_DIR}"

# Expose maya
_MAYA_BIN=$(readlink -f `command -v maya`)
_MAYA_DIR=$(dirname "${_MAYA_BIN}")
_MAYA_ROOT=$(dirname "${_MAYA_DIR}")
_PREPEND "PATH" "${_MAYA_DIR}"
_APPEND "LD_LIBRARY_PATH" "${_MAYA_ROOT}/lib"
_APPEND "PYTHONPATH" "${_MAYA_ROOT}/lib/python2.7/site-packages"

# Expose pytest
_PYTEST_BIN=$(python -c "import pytest; print pytest.__file__")
_PYTEST_DIR=$(dirname "${_PYTEST_BIN}")
_APPEND "PYTHONPATH" "${_PYTEST_DIR}"

$@
