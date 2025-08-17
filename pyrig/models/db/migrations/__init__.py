from sqlite3 import Connection
from importlib import import_module

from packaging.version import Version

from pyapp.utils.sqlite import execute_select

from ....logging import log_func_call, get_logger
from ....version import __version__ as PYRIG_VERSION
from .schema_map import PKG_VERSION_TO_SCHEMA


@log_func_call
def get_package_schema_version():
    "Get the expected database schema version for the current package version."
    current_ver = Version(PYRIG_VERSION)
    for i in reversed(range(len(PKG_VERSION_TO_SCHEMA))):
        if current_ver >= Version(PKG_VERSION_TO_SCHEMA[i]):
            return i + 1
    return len(PKG_VERSION_TO_SCHEMA)


@log_func_call
def get_current_schema_version(cxn: Connection) -> int:
    "Get the current schema version from the settings table."
    result = execute_select(cxn, 'settings', 'value',
                            "name = 'schema_version'").fetchone()
    if result:
        return int(result[0])
    return 0


@log_func_call
def set_schema_version(cxn: Connection, version: int):
    "Set the schema version in the settings table."
    with cxn:
        cxn.execute("INSERT OR REPLACE INTO settings (name, value) "
                    "VALUES (?, ?)", ("schema_version", str(version)))


@log_func_call
def apply_migrations(cxn: Connection, from_version: int, to_version: int):
    "Apply migrations from one schema version to another."
    log = get_logger()
    if from_version >= to_version:
        log.debug(f"No migrations needed (current: {from_version}, "
                  f"target: {to_version})")
        return

    for version in range(from_version + 1, to_version + 1):
        # log.info(f"Applying migration to schema version {version}")
        migration_module = import_module(f".v{version}", package=__name__)
        migrate = getattr(migration_module, 'migrate', None)
        if callable(migrate):
            migrate(cxn)
            set_schema_version(cxn, version)
            log.info(f"Successfully migrated to schema version {version}")


def check_schema_version(cxn: Connection):
    "Check the database schema version and apply migrations if needed."
    log = get_logger()

    current_schema = get_current_schema_version(cxn)
    log.debug(f"Current schema version: {current_schema}")

    target_schema = get_package_schema_version()
    log.debug(f"Target schema version: {target_schema}")

    if current_schema < target_schema:
        log.info("Database schema upgrade needed: "
                 f"{current_schema} > {target_schema}")
        apply_migrations(cxn, current_schema, target_schema)

    elif current_schema > target_schema:
        log.warning("Database schema is newer than package expects: "
                    f"{current_schema} > {target_schema}. "
                    "This may cause compatibility issues.")


@log_func_call
def init_pyrig_db(cxn: Connection):
    "Initialize the PyRig database with initial schema."
    log = get_logger()
    log.info("Initializing PyRig database")
    with cxn:
        # Create settings table
        cxn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            name TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """)
        set_schema_version(cxn, 0)
