from ...app import PyRigApp
from ...logging import log_func_call  # , get_logger


def get_ynab_budget():
    return PyRigApp.get('local.ynab_budget_id', None)


@log_func_call
def get_ynab_budgets():
    from .comm import ynab_base_get
    return ynab_base_get('budgets')
