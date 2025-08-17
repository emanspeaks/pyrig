from pathlib import Path
from sqlite3 import connect

from pyapp.utils.sqlite import get_tables

from ...app import PyRigApp
from ...logging import log_func_call, get_logger
from .migrations import init_pyrig_db, check_schema_version


@log_func_call
def get_pyrig_db_path() -> Path:
    """
    Get the path to the database directory.
    """
    return PyRigApp["local.default_db_file"]


@log_func_call
def check_pyrig_db(create_if_missing: bool = False):
    "Check PyRig database, creating or migrating as needed."
    dbpath = get_pyrig_db_path()
    log = get_logger()

    # Database exists, check/migrate
    with connect(dbpath) as cxn:
        tables = get_tables(cxn)

        if 'settings' not in tables:
            if not create_if_missing:
                log.warning("Settings table not found "
                            "and create_if_missing is False")
                return

            log.info("Settings table not found, initializing database")
            init_pyrig_db(cxn)

        check_schema_version(cxn)
