from pathlib import Path
from sqlite3 import connect

from pyapp.utils.sqlite import get_tables, execute_select
from pyapp.utils.tqdm import FileSetTqdm
from pyapp.utils.filemeta import FileSet

from ...logging import log_func_call, DEBUG, get_logger, INFO
from ...app import PyRigApp

from .constants import CFG_AVCAD_DB_KEY  # , CXNS_REGEX

OMIT_TABLES = (
    'sqlite_sequence',
    'Options',
    'Options_Hard',
    'Full_Table',
)
MODEL_FIELD_NAME = "Model"


@log_func_call
def get_avcad_tables(dbpath: Path) -> set[str]:
    with connect(dbpath) as db:
        return sorted(set(t for t in get_tables(db) if t not in OMIT_TABLES))


@log_func_call
def get_db_fileset() -> FileSet:
    p = get_avcad_db_dir()
    return set(f.relative_to(p) for f in p.glob('*.xml'))


@log_func_call
def get_avcad_db_dir() -> Path:
    """
    Get the path to the database directory.
    """
    return PyRigApp[CFG_AVCAD_DB_KEY]


@log_func_call
def log_avcad_db_dir(level: int | str = INFO):
    dbdir = get_avcad_db_dir()
    get_logger().log(level, f"AVCAD Database directory: {dbdir.as_posix()}")


@log_func_call
def set_avcad_db_dir(db_dir: Path):
    """
    Set the path to the database directory.
    """
    PyRigApp.set(CFG_AVCAD_DB_KEY, Path(db_dir))
    log_avcad_db_dir(DEBUG)


@log_func_call
def get_db_file(manuf: str) -> Path:
    """
    Get the path to the database file for the specified manufacturer.
    """
    db_dir = get_avcad_db_dir()
    return db_dir / f"{manuf}.xml"


@log_func_call
def print_all_models():
    db_dir = get_avcad_db_dir()
    with FileSetTqdm(get_db_fileset(), leave=False) as tq:
        for f in tq:
            dbp = db_dir/f
            manuf = f.stem
            tq.write(f"* {manuf}")
            for tbl in get_avcad_tables(dbp):
                tq.write(f"  * {tbl}")
                with connect(dbp) as db:
                    for row in sorted(execute_select(db, tbl,
                                                     MODEL_FIELD_NAME),
                                      key=lambda x: str(x)):
                        tq.write(f"    * {row[0]}")
