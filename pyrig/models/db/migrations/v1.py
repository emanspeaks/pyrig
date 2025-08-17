from sqlite3 import Connection

from ....logging import log_func_call
from ...acctng.db import create_accounting_tables, insert_default_accounts


@log_func_call
def migrate(cxn: Connection):
    with cxn:
        # Create double-entry bookkeeping tables
        create_accounting_tables(cxn)
        insert_default_accounts(cxn)
