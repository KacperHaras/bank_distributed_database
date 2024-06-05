use Main;

select * from Account;

select * from TransactionsLogMain;

use Branch1;
select Client.ClientID, AccountID, Balance, AccountType, Name, Address, Email from Account
join Client on Account.ClientID=Client.ClientID;

use Branch2;
select Client.ClientID, AccountID, Balance, AccountType, Name, Address, Email from Account
join Client on Account.ClientID=Client.ClientID;