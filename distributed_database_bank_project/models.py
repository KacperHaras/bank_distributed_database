from .database import db

class Client(db.Model):
    __tablename__ = 'Client'

    ClientID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    Email = db.Column(db.String(100))

    Caccount = db.relationship("Account", back_populates="Aclient")

    def __init__(self, name, address, email):
        self.Name = name
        self.Address = address
        self.Email = email

    def __repr__(self):
        return f"<Client {self.Name}, ID: {self.ClientID}>"
    
    @classmethod
    def get_by_id(cls, session, id):        
        db_client = session.query(cls).filter(Client.ClientID == id).first()
        return db_client


class Account(db.Model):
    __tablename__ = 'Account'
    
    AccountID = db.Column(db.Integer, primary_key=True)
    ClientID = db.Column(db.Integer, db.ForeignKey('Client.ClientID'))
    Balance = db.Column(db.Numeric(18, 2))
    SecretKey = db.Column(db.String(10))
    AccountType = db.Column(db.String(50))

    Aclient = db.relationship("Client", back_populates="Caccount")
    Atransactions = db.relationship("TransactionsLogMain", back_populates="Taccount")
    Abranches2 = db.relationship("Account_Branch", back_populates="ABaccount")

    def __init__(self, client_id, balance, secret_key, account_type):
        self.ClientID = client_id
        self.Balance = balance
        self.SecretKey = secret_key
        self.AccountType = account_type

    def __repr__(self):
        return f"<Account {self.AccountID}, Client ID: {self.ClientID}, Balance: {self.Balance}, Account Type: {self.AccountType}>"
    
    @classmethod
    def account_authentication(cls, session, id, password):
        return session.query(cls).filter(cls.AccountID == id, cls.SecretKey == password).first()

        
    @classmethod  
    def get_account(cls, session, id):        
        db_account = session.query(cls).filter(Account.AccountID==id).first()
        return db_account
    


class Branches(db.Model):
    __tablename__ = 'Branches'
    
    BranchID = db.Column(db.Integer, primary_key=True)
    BranchName = db.Column(db.String(50))
    BranchLocation = db.Column(db.String(50))

    Baccounts2 = db.relationship("Account_Branch", back_populates="ABbranches")
    Btransactions = db.relationship("TransactionsLogMain", back_populates="Tbranch")

    def __init__(self, id, name, location):
        self.BranchID = id
        self.BranchName = name
        self.BranchLocation = location

    
class Account_Branch(db.Model):
    __tablename__ = 'Account_Branch'
    
    AccountID = db.Column(db.Integer, db.ForeignKey('Account.AccountID'), primary_key=True)
    BranchID = db.Column(db.Integer, db.ForeignKey('Branches.BranchID'), primary_key=True)
    
    ABaccount = db.relationship("Account", back_populates="Abranches2")
    ABbranches = db.relationship("Branches", back_populates="Baccounts2")

    def __init__(self, account_id, branch_id):
        self.AccountID = account_id
        self.BranchID = branch_id


class TransactionsLogMain(db.Model):
    __tablename__ = 'TransactionsLogMain'
    TransactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AccountID = db.Column(db.Integer, db.ForeignKey('Account.AccountID'))
    AssociatedAccountID = db.Column(db.Integer)
    BranchID = db.Column(db.Integer, db.ForeignKey('Branches.BranchID'))
    TransactionType = db.Column(db.String(50))
    Amount = db.Column(db.Numeric(18, 2))
    Date = db.Column(db.DateTime)
    TransactionState = db.Column(db.String(50))

    Taccount = db.relationship("Account", back_populates="Atransactions")
    Tbranch = db.relationship("Branches", back_populates="Btransactions")

    def __init__(self, account_id, associated_account_id, branch_id, transaction_type, amount, date, transaction_state):
        self.AccountID = account_id
        self.AssociatedAccountID = associated_account_id
        self.BranchID = branch_id
        self.TransactionType = transaction_type
        self.Amount = amount
        self.Date = date
        self.TransactionState = transaction_state

    @classmethod
    def get_transactions(cls, session, id):        
        transactions = session.query(cls).filter(TransactionsLogMain.AccountID==id or TransactionsLogMain.AssociatedAccountID ==id).all()
        return transactions