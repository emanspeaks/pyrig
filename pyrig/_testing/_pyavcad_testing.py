from os import environ

from pyapp._testing import _is_running_in_ci, _is_pyapp_unittest  # noqa: F401

# these constants are only relevant to testing, do not add to constants
ENV_PYRIG_UNITTEST_ACTIVE = 'PYRIG_UNITTEST_ACTIVE'


def _is_pyrig_unittest():
    return bool(environ.get(ENV_PYRIG_UNITTEST_ACTIVE))
