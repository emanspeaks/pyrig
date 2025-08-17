from sqlite3 import Connection

from ...logging import log_func_call


@log_func_call
def create_accounting_tables(cxn: Connection):
    """Create double-entry bookkeeping database tables."""

    # Chart of Accounts - defines all account types and categories
    cxn.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        account_type TEXT NOT NULL CHECK (account_type IN (
            'ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE'
        )),
        parent_account_id INTEGER,
        is_active BOOLEAN NOT NULL DEFAULT 1,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_account_id) REFERENCES accounts(id)
    )
    """)

    # Journal Entries - header for each accounting transaction
    cxn.execute("""
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY,
        entry_number TEXT UNIQUE,
        entry_date DATE NOT NULL,
        description TEXT NOT NULL,
        reference TEXT,
        source_document TEXT,
        posted BOOLEAN NOT NULL DEFAULT 0,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Journal Entry Lines - individual debits and credits for each transaction
    cxn.execute("""
    CREATE TABLE IF NOT EXISTS journal_entry_lines (
        id INTEGER PRIMARY KEY,
        journal_entry_id INTEGER NOT NULL,
        account_id INTEGER NOT NULL,
        debit_amount DECIMAL(15,2) DEFAULT 0.00,
        credit_amount DECIMAL(15,2) DEFAULT 0.00,
        description TEXT,
        line_number INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id)
            ON DELETE CASCADE,
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        CHECK (
            (debit_amount > 0 AND credit_amount = 0) OR
            (credit_amount > 0 AND debit_amount = 0)
        )
    )
    """)

    # Fiscal Periods - for period-based reporting
    cxn.execute("""
    CREATE TABLE IF NOT EXISTS fiscal_periods (
        id INTEGER PRIMARY KEY,
        period_name TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        is_closed BOOLEAN NOT NULL DEFAULT 0,
        fiscal_year INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(period_name, fiscal_year)
    )
    """)

    # Account Balances - periodic snapshots for performance
    cxn.execute("""
    CREATE TABLE IF NOT EXISTS account_balances (
        id INTEGER PRIMARY KEY,
        account_id INTEGER NOT NULL,
        fiscal_period_id INTEGER NOT NULL,
        opening_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        closing_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        debit_total DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        credit_total DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        FOREIGN KEY (fiscal_period_id) REFERENCES fiscal_periods(id),
        UNIQUE(account_id, fiscal_period_id)
    )
    """)

    # Create indexes for performance
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_accounts_type "
        "ON accounts(account_type)"
    )
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_accounts_code ON accounts(code)"
    )
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_journal_entries_date "
        "ON journal_entries(entry_date)"
    )
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_journal_entries_posted "
        "ON journal_entries(posted)"
    )
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_journal_entry_lines_account "
        "ON journal_entry_lines(account_id)"
    )
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_journal_entry_lines_entry "
        "ON journal_entry_lines(journal_entry_id)"
    )
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_fiscal_periods_dates "
        "ON fiscal_periods(start_date, end_date)"
    )
    cxn.execute(
        "CREATE INDEX IF NOT EXISTS idx_account_balances_account "
        "ON account_balances(account_id)"
    )

    # Create triggers to maintain data integrity
    # Update journal entry timestamp when lines are modified
    cxn.execute("""
    CREATE TRIGGER IF NOT EXISTS update_journal_entry_timestamp
    AFTER INSERT ON journal_entry_lines
    BEGIN
        UPDATE journal_entries
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.journal_entry_id;
    END
    """)

    # Update account updated_at timestamp
    cxn.execute("""
    CREATE TRIGGER IF NOT EXISTS update_account_timestamp
    AFTER UPDATE ON accounts
    BEGIN
        UPDATE accounts
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.id;
    END
    """)


@log_func_call
def insert_default_accounts(cxn: Connection):
    """Insert standard chart of accounts."""

    # Standard account structure
    default_accounts = [
        # ASSETS
        ('1000', 'ASSETS', 'ASSET', None, 'Total Assets'),
        ('1100', 'CURRENT ASSETS', 'ASSET', 1, 'Current Assets'),
        ('1101', 'Cash and Cash Equivalents', 'ASSET', 2,
         'Cash, checking, savings'),
        ('1102', 'Accounts Receivable', 'ASSET', 2, 'Money owed to us'),
        ('1103', 'Inventory', 'ASSET', 2, 'Products for sale'),
        ('1104', 'Prepaid Expenses', 'ASSET', 2,
         'Prepaid insurance, rent, etc.'),

        ('1200', 'NON-CURRENT ASSETS', 'ASSET', 1, 'Long-term Assets'),
        ('1201', 'Property, Plant & Equipment', 'ASSET', 7, 'Fixed assets'),
        ('1202', 'Accumulated Depreciation', 'ASSET', 7,
         'Contra-asset account'),

        # LIABILITIES
        ('2000', 'LIABILITIES', 'LIABILITY', None, 'Total Liabilities'),
        ('2100', 'CURRENT LIABILITIES', 'LIABILITY', 10,
         'Short-term obligations'),
        ('2101', 'Accounts Payable', 'LIABILITY', 11, 'Money we owe'),
        ('2102', 'Accrued Expenses', 'LIABILITY', 11,
         'Expenses incurred but not paid'),
        ('2103', 'Short-term Debt', 'LIABILITY', 11,
         'Loans due within 1 year'),

        ('2200', 'NON-CURRENT LIABILITIES', 'LIABILITY', 10,
         'Long-term obligations'),
        ('2201', 'Long-term Debt', 'LIABILITY', 14,
         'Loans due after 1 year'),

        # EQUITY
        ('3000', 'EQUITY', 'EQUITY', None, 'Owner Equity'),
        ('3101', 'Retained Earnings', 'EQUITY', 16, 'Accumulated profits'),
        ('3102', 'Owner Capital', 'EQUITY', 16, 'Owner investments'),

        # REVENUE
        ('4000', 'REVENUE', 'REVENUE', None, 'Total Revenue'),
        ('4101', 'Sales Revenue', 'REVENUE', 19, 'Product/service sales'),
        ('4102', 'Interest Income', 'REVENUE', 19, 'Interest earned'),
        ('4103', 'Other Income', 'REVENUE', 19, 'Miscellaneous income'),

        # EXPENSES
        ('5000', 'EXPENSES', 'EXPENSE', None, 'Total Expenses'),
        ('5100', 'OPERATING EXPENSES', 'EXPENSE', 23, 'Day-to-day expenses'),
        ('5101', 'Cost of Goods Sold', 'EXPENSE', 24,
         'Direct costs of products'),
        ('5102', 'Salaries and Wages', 'EXPENSE', 24,
         'Employee compensation'),
        ('5103', 'Rent Expense', 'EXPENSE', 24, 'Facility rental costs'),
        ('5104', 'Utilities Expense', 'EXPENSE', 24,
         'Electric, water, gas, etc.'),
        ('5105', 'Office Supplies', 'EXPENSE', 24, 'General office supplies'),
        ('5106', 'Depreciation Expense', 'EXPENSE', 24, 'Asset depreciation'),
        ('5107', 'Interest Expense', 'EXPENSE', 24, 'Interest on loans'),
    ]

    for i, (code, name, acc_type, parent_ref, desc) in enumerate(
        default_accounts, 1
    ):
        parent_id = parent_ref if parent_ref is None else parent_ref
        cxn.execute("""
        INSERT OR IGNORE INTO accounts
        (id, code, name, account_type, parent_account_id, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (i, code, name, acc_type, parent_id, desc))
