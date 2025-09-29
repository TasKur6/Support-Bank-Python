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
    def __init__(self, date, fromAcc, toAcc, narrative, amount):
        self.date = date
        self.fromAcc = fromAcc
        self.toAcc = toAcc
        self.narrative = narrative
        self.amount = amount

def poundsToPence(pounds):
    return round(pounds*100, 0)

def penceToPounds(pence):
    return round(pence/100, 2)

def readfile(filePath, accountLedger, transactionLedger):
    with open(filePath, mode='r') as file:
        csvFile = csv.DictReader(file)
        for line in csvFile:
            amount = poundsToPence(float(line['Amount']))
            t = Transaction(line['Date'], line['From'], line['To'], line['Narrative'], amount)
            transactionLedger.append(t)
            if line['From'] not in accountLedger:
                accountLedger[line['From']] = Account(line['From'])
            if line['To'] not in accountLedger:
                accountLedger[line['To']] = Account(line['To'])
            accountLedger[line['From']].update_balance_for_from(amount)
            accountLedger[line['To']].update_balance_for_to(amount)
            accountLedger[line['From']].update_transactions(t)
            accountLedger[line['To']].update_transactions(t)

def listAll(accountLedger):
    for k, v in accountLedger.items():
        print(k, penceToPounds(v.balance))

def listAccount(accountLedger, account):
    accountTransactions = accountLedger[account].transactions
    for t in accountTransactions:
        print(t.date, t.fromAcc, t.toAcc, t.narrative, penceToPounds(t.amount))

def main():
    accountLedger = dict()
    transactionLedger = []
    readfile(r"C:\Users\taskur\Work\Training\PythonProjects\Support-Bank-Python\data\Transactions2014.csv", accountLedger, transactionLedger)
    command = input("Enter command: ")
    if command == 'List All':
        listAll(accountLedger)
    elif command[:4] == 'List':
        account = command[5:]
        listAccount(accountLedger, account)
    else:
        print("Wrong command!")


if __name__ == "__main__":
    main()