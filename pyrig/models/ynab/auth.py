from pathlib import Path
from sqlite3 import connect, Connection

from pyapp.utils.sqlite import execute_select

from ...app import PyRigApp
from ...logging import log_func_call, get_logger
from ..db import get_pyrig_db_path


def get_ynab_token():
    return PyRigApp.get('local.ynab_token', None)


@log_func_call
def get_ynab_token_from_file():
    token_file_path: Path = PyRigApp.get('local.ynab_token_file', None)
    if token_file_path and token_file_path.exists():
        token = token_file_path.read_text().strip()
        get_logger().debug(f"Read YNAB token from file: {token_file_path}")
        return token


def get_ynab_token_from_db(cxn: Connection):
    result = execute_select(cxn, 'settings', 'value',
                            "name = 'ynab_token'").fetchone()
    if result:
        return result[0]


def set_ynab_db_token(cxn: Connection, token: str):
    cxn.execute("INSERT OR REPLACE INTO settings (name, value) "
                "VALUES (?, ?)", ("ynab_token", token))
    get_logger().info("Stored YNAB token in database settings")


@log_func_call
def load_ynab_token():
    """
    Load YNAB token from database settings, local config, or token file.

    Priority order:
    1. Database setting 'ynab_token' (with warning if differs from config)
    2. PyRigApp['local.ynab_token']
    3. File at PyRigApp['local.ynab_token_file']

    The final token is stored back into PyRigApp['local.ynab_token'].
    """
    log = get_logger()

    local_token = get_ynab_token()
    if local_token is None:
        local_token = get_ynab_token_from_file()

    with connect(get_pyrig_db_path()) as cxn:
        db_token = get_ynab_token_from_db(cxn)
        if local_token:
            if db_token:
                if db_token != local_token:
                    log.warning("YNAB token in database differs from local "
                                "config. Using database value.")

            else:
                # Only local token exists - store it in database
                db_token = local_token
                set_ynab_db_token(cxn, db_token)

        elif not db_token:
            # No token found anywhere
            log.warning("No YNAB token found in database, config, or "
                        "token file")
            return

        # Set the final token in PyRigApp
        PyRigApp.set('local.ynab_token', db_token)
        log.debug("YNAB token loaded successfully")
