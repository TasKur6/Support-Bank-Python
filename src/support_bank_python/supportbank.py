import csv

class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = []
    
    def update_balance_for_from(self, amount):
        self.balance -= amount

    def update_balance_for_to(self, amount):
        self.balance += amount

    def update_transactions(self, transaction):
        self.transactions.append(transaction)


class Transaction:
    def __init__(self, date, from_acc, to_acc, narrative, amount):
        self.date = date
        self.from_acc = from_acc
        self.to_acc = to_acc
        self.narrative = narrative
        self.amount = amount

def pounds_to_pence(pounds):
    return round(pounds*100, 0)

def pence_to_pounds(pence):
    return round(pence/100, 2)

def read_file(file_path, account_ledger, transaction_ledger):
    with open(file_path, mode='r') as file:
        csv_file = csv.DictReader(file)
        for line in csv_file:
            amount = pounds_to_pence(float(line['Amount']))
            t = Transaction(line['Date'], line['From'], line['To'], line['Narrative'], amount)
            transaction_ledger.append(t)
            if line['From'] not in account_ledger:
                account_ledger[line['From']] = Account(line['From'])
            if line['To'] not in account_ledger:
                account_ledger[line['To']] = Account(line['To'])
            account_ledger[line['From']].update_balance_for_from(amount)
            account_ledger[line['To']].update_balance_for_to(amount)
            account_ledger[line['From']].update_transactions(t)
            account_ledger[line['To']].update_transactions(t)

def list_all(account_ledger):
    for k, v in account_ledger.items():
        print(k, pence_to_pounds(v.balance))

def list_account(account_ledger, account):
    account_transactions = account_ledger[account].transactions
    for t in account_transactions:
        print(t.date, t.from_acc, t.to_acc, t.narrative, pence_to_pounds(t.amount))

def main():
    account_ledger = dict()
    transaction_ledger = []
    read_file(r"C:\Users\taskur\Work\Training\PythonProjects\Support-Bank-Python\data\Transactions2014.csv", account_ledger, transaction_ledger)
    command = input("Enter command: ")
    if command == 'List All':
        list_all(account_ledger)
    elif command[:4] == 'List':
        account = command[5:]
        list_account(account_ledger, account)
    else:
        print("Wrong command!")


if __name__ == "__main__":
    main()