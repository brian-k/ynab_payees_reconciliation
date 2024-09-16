import requests
import os
import csv
import json
import io
import pandas as pd
import numpy as np

YNAB_API_KEY = os.environ['YNAB_API_KEY']
BUDGET_ID = os.environ['BUDGET_ID']
BASE_URL = f'https://api.youneedabudget.com/v1/budgets/{BUDGET_ID}'

headers = {
    'Authorization': f'Bearer {YNAB_API_KEY}'
}

def get_payees():
    url = f'{BASE_URL}/payees'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        payees = pd.DataFrame.from_dict(response.json().get('data', {}).get('payees', []))
        return payees
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return []

def update_payee(payee_id, new_name):
    url = f'{BASE_URL}/payees/{payee_id}'
    data = {
        'payee': {
            'name': new_name,
        }
    }

    response = requests.patch(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f'Payee {payee_id} updated successfully to {new_name}.')
    else:
        print(f'Error: {response.status_code} - {response.text}')

# Retrieve and print payees
payees = get_payees()
payees_orig = payees.copy(deep=True)

# remove all rows with account_transfer_id
payees = payees[payees['transfer_account_id'].isnull()]

# Drop the account_transfer_id and deleted columns
payees = payees.drop(columns=['transfer_account_id', 'deleted'])

# write the DataFrame to CSV
payees.to_csv('ynab_payees.csv', index=False)

# Example: Update the first payee in the list
#if payees:
#    first_payee_id = payees[0]['id']
#    update_payee(payee_id=first_payee_id, new_name='Updated Payee Name')
