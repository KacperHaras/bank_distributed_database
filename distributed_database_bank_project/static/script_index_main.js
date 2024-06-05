document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submitLogin').addEventListener('click', function() {
        const account_id = document.getElementById('account_id').value;
        const secret_key = document.getElementById('secret_key').value;
        const loginData = { account_id: account_id, secret_key: secret_key };
        
        fetch('/account-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showToast('Login failed: '+ data.error);
                setTimeout(function() {
                    window.location.href = '/';
                }, 3000);
            } else {
                sessionStorage.setItem('accountData', JSON.stringify(data));
                window.location.href = '/display-account-info';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
