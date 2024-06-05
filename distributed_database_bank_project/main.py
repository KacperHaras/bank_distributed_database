from flask import Blueprint, request, jsonify, render_template
from .database import db, SessionMain, Session1, Session2, session_table
from .models import Account, Client, Account_Branch, TransactionsLogMain
from datetime import datetime
from decimal import Decimal
import requests

main = Blueprint('main', __name__)

@main.route('/')
def main_index():
    return render_template("index_main.html")


@main.route('/account-info', methods=['POST'])
def get_account_info():
    sessionMain = session_table[0]()
    try:
        data = request.get_json()
        account_id = data['account_id']
        secret_key = data['secret_key']

        account = Account.account_authentication(sessionMain, account_id, secret_key)
        if account:
            client = Client.get_by_id(sessionMain, account.ClientID)
            account_data = {
                'AccountID': account.AccountID,
                'ClientID': client.ClientID,
                'ClientName': client.Name,
                'ClientAddress': client.Address,
                'ClientEmail': client.Email,
                'AccountBalance': account.Balance,
                'AccountType': account.AccountType
            }

            return jsonify(account_data)
        else:
            return jsonify({'error': 'Invalid account ID or secret key'}), 401     #{'error': 'Invalid account ID or secret key'}
        
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if sessionMain:
            sessionMain.close()


@main.route('/display-account-info')
def display_account_info():
    return render_template('account_info.html')


@main.route('/account-transactions', methods=['POST'])
def get_transactions():
    data = request.get_json()
    account_id = data.get('account_id')

    transactions = TransactionsLogMain.query.filter_by(AccountID=account_id).all()
    transactions_data = []
    for trans in transactions:
        tmp =   {   'transaction_id': trans.TransactionID,
                    'associated_account' : trans.AssociatedAccountID,
                    'date': trans.Date.strftime('%Y-%m-%d %H:%M:%S'),
                    'amount': trans.Amount,
                    'type': trans.TransactionType,
                    'state': trans.TransactionState
                }
        transactions_data.append(tmp)

    return jsonify(transactions_data)


def get_branches(session, account_id, receiver_id):
    branch1 = session.query(Account_Branch.BranchID).filter(Account_Branch.AccountID == account_id).distinct().first()
    branch2 = session.query(Account_Branch.BranchID).filter(Account_Branch.AccountID == receiver_id).distinct().first()
    return [branch1, branch2]


def get_transaction_data(data):
    account_id = data['transactionData']['account_id']
    secret_key = data['transactionData']['secret_key']
    receiver_id = data['transactionData']['receiver_id']
    if data['transactionData']['money_amount'] != '':
        money_amount = float(data['transactionData']['money_amount'])
    else:
        money_amount = 0.0

    return account_id, secret_key, receiver_id, Decimal(str(money_amount))


def validate_transaction_data(account_id, secret_key, money_amount, receiver_id):
    if not account_id or not secret_key or not money_amount or not receiver_id:
        raise Exception('Missing required data')

    if money_amount <= 0:
        raise Exception('Invalid money amount')

    if int(account_id) == int(receiver_id):
        raise Exception('Cannot send money to yourself')
    

@main.route('/send-money', methods=['POST'])  
def send_money():
    data = request.get_json()
    account_id, secret_key, receiver_id, money_amount = get_transaction_data(data)
    
    sessionMain = session_table[0]()
    branches = get_branches(sessionMain, account_id, receiver_id)
    
    try:
        if branches[0] is None or branches[1] is None:
            raise Exception('Branch for this reciever not found')
        session1 = session_table[branches[0][0]]()
        session2 = session_table[branches[1][0]]()
    except Exception as e:
        print('Error: ', e)
        return jsonify(data, {'error': str(e)}) 
    finally:
        if sessionMain:
            sessionMain.close()
    

    try:
        validate_transaction_data(account_id, secret_key, money_amount, receiver_id)
        
        sender_account = Account.account_authentication(sessionMain, account_id, secret_key)
        if not sender_account:
            raise Exception('Invalid Secret Key')

        if sender_account.Balance < money_amount:
            raise Exception('Insufficient funds')
            
        sender_account.Balance -= money_amount
        data['accountData']['AccountBalance'] = str(sender_account.Balance)

        receiver_account = Account.account_authentication(sessionMain, receiver_id, secret_key)
        if not receiver_account:
            raise Exception('Receiver account not found')

        receiver_account.Balance += money_amount

        sender_account = Account.account_authentication(session1, account_id, secret_key)
        if not sender_account:
            raise Exception('Maching account not found in branch 1')            
        else:
            if sender_account.Balance < money_amount:
                raise Exception('Insufficient funds')
            sender_account.Balance -= money_amount

        receiver_account = Account.account_authentication(session2, receiver_id, secret_key)
        if not receiver_account:      
            raise Exception('Matching account not found in branch 2') 
        else:
            receiver_account.Balance += money_amount

        time = datetime.now()
        transaction_out = TransactionsLogMain(account_id, receiver_id, branches[0][0], 'Outgoing transfer', money_amount, time, 'Success')
        transaction_in = TransactionsLogMain(receiver_id, account_id, branches[1][0], 'Incoming transfer', money_amount, time, 'Success')

        sessionMain.add(transaction_out)
        sessionMain.add(transaction_in)

        sessionMain.commit()
        session1.commit()
        session2.commit()

        return jsonify(data, {'status': 'Money sent successfully'})
    

    except Exception as e:
        print('Error: ', e)

        sessionMain.rollback()
        session1.rollback()
        session2.rollback()

        time = datetime.now()
        transaction_out = TransactionsLogMain(account_id, receiver_id, branches[0][0], 'Outgoing transfer', money_amount, time, 'Failed due to ' + str(e))
        transaction_in = TransactionsLogMain(receiver_id, account_id, branches[1][0], 'Incoming transfer', money_amount, time, 'Failed due to ' + str(e))

        sessionMain.add(transaction_out)
        sessionMain.add(transaction_in)
        sessionMain.commit()
        return jsonify(data, {'error': str(e)})
    
    finally:
        if sessionMain:
            sessionMain.close()
        if session1:
            session1.close()
        if session2:
            session2.close()


if __name__ == '__main__':
    main.run(port=5000, debug=True)
