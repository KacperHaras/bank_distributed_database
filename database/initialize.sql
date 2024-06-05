CREATE LOGIN main WITH PASSWORD = 'Main!23';
CREATE LOGIN node1 WITH PASSWORD = 'Node1!23';
CREATE LOGIN node2 WITH PASSWORD = 'Node2!23';

CREATE DATABASE Branch1;
GO

USE Branch1;
GO

CREATE TABLE Client (
    ClientID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Address NVARCHAR(255),
    Email NVARCHAR(100)
);
GO

CREATE TABLE Account (
    AccountID INT PRIMARY KEY,
    ClientID INT FOREIGN KEY REFERENCES Client(ClientID),
    Balance DECIMAL(18, 2),
	SecretKey NVARCHAR(10),
    AccountType NVARCHAR(50)
);
GO

CREATE TABLE TransactionsLog (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    AccountID INT FOREIGN KEY REFERENCES Account(AccountID),
    TransactionType NVARCHAR(50),
    Amount DECIMAL(18, 2),
    Date DATETIME,
    TransactionState NVARCHAR(50)
);
GO

CREATE USER Node1 FOR LOGIN Node1;
EXEC sp_addrolemember 'db_owner', 'Node1';


CREATE DATABASE Branch2;
GO

USE Branch2;
GO

CREATE TABLE Client (
    ClientID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Address NVARCHAR(255),
    Email NVARCHAR(100)
);
GO

CREATE TABLE Account (
    AccountID INT PRIMARY KEY,
    ClientID INT FOREIGN KEY REFERENCES Client(ClientID),
    Balance DECIMAL(18, 2),
	SecretKey NVARCHAR(10),
    AccountType NVARCHAR(50)
);
GO

CREATE TABLE TransactionsLog (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    AccountID INT FOREIGN KEY REFERENCES Account(AccountID),
    TransactionType NVARCHAR(50),
    Amount DECIMAL(18, 2),
    Date DATETIME,
    TransactionState NVARCHAR(50)
);
GO

CREATE USER Node2 FOR LOGIN Node2;
EXEC sp_addrolemember 'db_owner', 'Node2';


CREATE DATABASE Main;
GO

USE Main;
GO


CREATE TABLE Client (
    ClientID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100),
    Address NVARCHAR(255),
    Email NVARCHAR(100)
);
GO

CREATE TABLE Account (
    AccountID INT IDENTITY(1,1) PRIMARY KEY,
    ClientID INT FOREIGN KEY REFERENCES Client(ClientID),
    Balance DECIMAL(18, 2),
	SecretKey NVARCHAR(10),
    AccountType NVARCHAR(50)
);
GO

CREATE TABLE Branches (
    BranchID INT PRIMARY KEY,
    BranchName NVARCHAR(100),
    BranchLocation NVARCHAR(255)
);
GO

CREATE TABLE Account_Branch (
    BranchID INT,
	AccountID INT,
    PRIMARY KEY (BranchID, AccountID),
    FOREIGN KEY (BranchID) REFERENCES Branches(BranchID),
	FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
);
GO

CREATE TABLE TransactionsLogMain (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    AccountID INT,
	AssociatedAccountID INT,
	BranchID INT,
    TransactionType NVARCHAR(50),
    Amount DECIMAL(18, 2),
    Date DATETIME,
    TransactionState NVARCHAR(50),
    FOREIGN KEY (BranchID) REFERENCES Branches(BranchID),
	FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
);
GO


CREATE USER Main FOR LOGIN Main;
EXEC sp_addrolemember 'db_owner', 'Main';