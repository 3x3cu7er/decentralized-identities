const addrs = document.querySelector('#addrs');
const Wallet = document.querySelector('#getWallet');
let meta_wallet;
async function getWallet() {
    try {
      if (window.ethereum) {
        let wallet = await window.ethereum.request({
          method: "eth_requestAccounts",
        });
        meta_wallet = wallet[0]
        addrs.innerHTML = meta_wallet
      } else {
        console.log("wallet is not available");
      }
    } catch (e) {}
  }

Wallet.addEventListener("submit", getWallet());


let issueIdentity = document.querySelector(".issueIdentity")
issueIdentity.onclick =  () =>{
  const userAddress = document.querySelector('#userAddressInput').value;  // Get user address from form input
  const identityData = document.querySelector('#identityDataInput').value;  // Get identity data from form input
  
  const response =  fetch('http://localhost:8000/credentials', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_address: userAddress, identity_data: identityData }),
  });

  const responseData =  response.json();
  console.log(responseData);
}





// In your frontend JavaScript

// Function to verify identity
async function verifyIdentity() {
  const userAddress = "";  // Get user address from form input

  const response = await fetch('/verify_identity/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_address: userAddress }),
  });

  const responseData = await response.json();
  console.log(responseData);
}

// Function to send identity
async function sendIdentity() {
  const senderAddress = "";  // Get sender address from form input
  const receiverAddress = "";  // Get receiver address from form input

  const response = await fetch('/send_identity/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ sender_address: senderAddress, receiver_address: receiverAddress }),
  });

  const responseData = await response.json();
  console.log(responseData);
}
