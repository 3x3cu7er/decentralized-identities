# identities/views.py

import subprocess
from django.http import HttpResponse
from django.shortcuts import render, redirect

from dependencies.emailer import generate_otp, send_reset_password_email, send_user_credential_via_email
from space.models import PasswordOTP
from .models import Identity, IPFSData
from cryptography.fernet import Fernet
import os

# Function to load or generate the encryption key
def load_or_generate_key():
    key_path = "secret.key"
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    else:
        with open(key_path, "rb") as key_file:
            key = key_file.read()
    return key

key = load_or_generate_key()
cipher_suite = Fernet(key)
from blockchain_app.models import Wallet
import didkit
def create_identity(request):
    did = didkit.key_to_did("key", didkit.generate_ed25519_key())
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        ethereum = request.POST.get('ethereum')
        ipfs_data = f"Name: {name}\nEmail: {email}\nEthereum: {ethereum}"
        encrypted_data = cipher_suite.encrypt(ipfs_data.encode())

        try:
            result = subprocess.run(['ipfs', 'add', '-Q'], input=encrypted_data, capture_output=True, check=True)
            ipfs_hash = result.stdout.decode().strip()
            identity, created = Identity.objects.get_or_create(ipfs_hash=ipfs_hash, defaults={'name': name, 'email': email})
            if not created:
                identity.name = name
                identity.email = email
                identity.ipfs_hash = ipfs_hash
                identity.save()
            body = f"You have successfully created a new identity wallet.\n************   Here are your details ******\nWallte Address, {ipfs_hash}\nDecentralized Identifier(DID), {did}"
            Wallet(user=request.user,address=ipfs_hash, private_key=did,ethereum_address=ethereum).save()
            send_user_credential_via_email(user_name=request.user,user_email=email,credential_info=body) 

            user = "User"
            address = request.user.email
            # user_email = User.objects.filter(username=user).first().email
            otp = generate_otp()
            send_user_credential_via_email(user_name=request.user,user_email=address,credential_info=f"[foundationX Identity Issuing OTP] : {otp}") 
            otp_id = int(len(PasswordOTP.objects.all()))+1  
            PasswordOTP(otp_id,user=request.user,otp=otp).save()
            
            return redirect('identity_detail', pk=identity.pk)
        except Exception:
            pass
            # return HttpResponse("invalid credentials\n Please cross-check your credentials")
    return render(request, 'identities/create_identity.html')
def view_identity(request, pk):
    identity = Identity.objects.get(pk=pk)
    try:
        result = subprocess.run(['ipfs', 'cat', identity.ipfs_hash], capture_output=True, check=True)
        decrypted_data = cipher_suite.decrypt(result.stdout).decode()
        return render(request, 'identities/view_identity.html', {'identity': identity, 'ipfs_data': decrypted_data})
    except subprocess.CalledProcessError as e:
        return render(request, 'identities/view_identity.html', {'identity': identity, 'error': 'IPFS error occurred'})

def upload_data(request):
    if request.method == 'POST':
        ipfs_hash = request.POST.get('ipfs_hash')  # Assuming ipfs_hash is used for user identification
        data_description = request.POST.get('data_description')
        data_content = request.POST.get('data_content')
        encrypted_data = cipher_suite.encrypt(data_content.encode())

        try:
            result = subprocess.run(['ipfs', 'add', '-Q'], input=encrypted_data, capture_output=True, check=True)
            new_ipfs_hash = result.stdout.decode().strip()
            IPFSData.objects.create(user_ipfs_hash=ipfs_hash, ipfs_hash=new_ipfs_hash, data_description=data_description)
            return redirect('list_data', ipfs_hash=ipfs_hash)
        except subprocess.CalledProcessError as e:
            return render(request, 'identities/upload_data.html', {'error': 'IPFS error occurred'})
    return render(request, 'identities/upload_data.html')

def list_data(request, ipfs_hash):
    data_list = IPFSData.objects.filter(user_ipfs_hash=ipfs_hash)
    return render(request, 'identities/list_data.html', {'data_list': data_list, 'ipfs_hash': ipfs_hash})

def view_data(request,ipfs_hash):
    if request.method == 'POST':
        ipfs_hash = request.POST.get('ipfs_hash')
    try:
        result = subprocess.run(['ipfs', 'cat', ipfs_hash], capture_output=True, check=True)
        decrypted_data = cipher_suite.decrypt(result.stdout).decode()
        return render(request, 'identities/view_data.html', {'ipfs_hash': ipfs_hash, 'data_content': decrypted_data})
    except subprocess.CalledProcessError as e:
        return render(request, 'identities/view_data.html', {'ipfs_hash': ipfs_hash, 'error': 'IPFS error occurred'})


