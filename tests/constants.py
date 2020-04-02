"""
Constants for tests
"""

import os

PATH_RESOURCE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "resources",)
)

PATH_SCHEMA_2017 = os.path.join(PATH_RESOURCE_DIR.TEST_RESOURCE_DIR, "schema2017.json")
