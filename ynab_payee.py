import requests
import os
import csv

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
        payees = response.json().get('data', {}).get('payees', [])
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
with open('ynab_payees.csv', 'w', newline='') as csvfile:
    payee_writer = csv.DictWriter(csvfile, dialect='excel', fieldnames = ['id', 'name', 'transfer_account_id', 'deleted'])
    payee_writer.writeheader()

    for payee in payees:
        payee_writer.writerow(payee)
        #print(f'ID: {payee["id"]}, Name: {payee["name"]}')

# Example: Update the first payee in the list
if payees:
    first_payee_id = payees[0]['id']
    update_payee(payee_id=first_payee_id, new_name='Updated Payee Name')
