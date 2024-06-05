document.addEventListener('DOMContentLoaded', function() {
    const accountData = sessionStorage.getItem('accountData');
    if (accountData) {
        const account = JSON.parse(accountData);
        console.log(account);
        document.getElementById('account_id').textContent += account.AccountID || 'N/A';
        document.getElementById('client_name').textContent += account.ClientName || 'N/A';
        document.getElementById('client_email').textContent += account.ClientEmail || 'N/A';
        document.getElementById('account_balance').textContent += account.AccountBalance || 'N/A';
        document.getElementById('client_address').textContent += account.ClientAddress || 'N/A';
        document.getElementById('account_type').textContent += account.AccountType || 'N/A';
    } else {
        console.error('No account data found in sessionStorage.');
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const showTransactionsBtn = document.getElementById('showTransactionHistory');
    const transactionsPanel = document.getElementById('showTransactionHtistoryPanel');

    showTransactionsBtn.addEventListener('click', function() {
        const accountData = JSON.parse(sessionStorage.getItem('accountData'));
        if (accountData && accountData.AccountID) {
            fetch('/account-transactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ account_id: accountData.AccountID })
            })
            .then(response => response.json())
            .then(data => {
                if(transactionsPanel.style.display === 'none'){
                    if (data.length > 0) {
                        displayTransactions(data, transactionsPanel);
                    } else {
                        transactionsPanel.innerHTML = 'No transaction data available.';
                        transactionsPanel.style.display = 'block';
                    }
                }else{
                    transactionsPanel.style.display = 'none';
                }   
            })
            .catch(error => {
                console.error('Fetch error:', error);
                transactionsPanel.innerHTML = 'Failed to load transactions.';
                transactionsPanel.style.display = 'block';
            });
        }
    });
});

function displayTransactions(transactions, panel) {
    let tableHTML = '<div class="scrollable-table"><table><thead><tr><th>Transaction ID</th><th>Date</th><th>Type</th><th>Associated account</th><th>Amount</th><th>State</th></tr></thead><tbody>';
    transactions.forEach(trans => {
        tableHTML += `<tr><td>${trans.transaction_id}</td><td>${trans.date}</td><td>${trans.type}</td><td>${trans.associated_account}</td><td>${trans.amount}</td><td>${trans.state}</td></tr>`;
    });
    tableHTML += '</tbody></table></div>';
    panel.innerHTML = tableHTML;
    panel.style.display = 'block';
}



document.getElementById('sendMoneyBtn').addEventListener('click', function() {
    var panel = document.getElementById('sendMoneyPanel');
    if (panel.style.display === 'none') {
        panel.style.display = 'block';
    } else {
        panel.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const accountData = sessionStorage.getItem('accountData');
    const account = JSON.parse(accountData);
    const sendMoneyPanel = document.querySelector('#sendMoneyPanel');

    sendMoneyPanel.addEventListener('click', function(event) {
        if (event.target.id === 'submitMoney') {
            const account_id = account.AccountID;
            const receiver_id = document.getElementById('receiver_id').value;
            const money_amount = document.getElementById('money_amount').value;
            const password = document.getElementById('password').value;
            
            const data = {account_id: account_id, secret_key: password, receiver_id: receiver_id, money_amount: money_amount};
            const loginData = {accountData: account ,transactionData: data};
            fetch('/send-money', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData)
            })
            .then(response => response.json())
            .then(data => {
                if (data[1].error) {
                    showToast(data[1].error)

                } else {
                    console.log(data[0].accountData);
                    sessionStorage.setItem('accountData', JSON.stringify(data[0].accountData));
                    showToast('Transaction completed successfully');
                    setTimeout(function() {
                        window.location.href = '/display-account-info';
                    }, 3000);
                }
            })
            .catch(error => console.error('Error:', error)
        );
        }
    });
});


function showToast(message) {
    var toast = document.getElementById("toastMessage");
    toast.textContent = message;
    toast.className = "toast show";
    setTimeout(function() {
        toast.className = toast.className.replace("toast show", "toast hidden");
    }, 5000);
}
