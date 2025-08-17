from requests import get as reqget

from .auth import get_ynab_token
from .budget import get_ynab_budget

YNAB_API_BASE = "https://api.ynab.com/v1"


def get_ynab_req_headers():
    return {
        'Authorization': f'Bearer {get_ynab_token()}',
        # 'Accept': 'application/json'
    }


def ynab_base_get(api_url: str):
    return reqget(f'{YNAB_API_BASE}/{api_url}',
                  headers={'Authorization': f'Bearer {get_ynab_token()}'}).json()['data']  # noqa: E501


def ynab_get(api_url: str, budget_id: str = None):
    budget_id = budget_id or get_ynab_budget()
    return ynab_base_get(f'budgets/{budget_id}/{api_url}')
