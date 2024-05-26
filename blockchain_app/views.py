import time
from django.shortcuts import render
from django.http import JsonResponse
import hashlib

def mine_block(request):
    # Implement block mining logic here
    return JsonResponse({"message": "Block mined successfully"})

def send_transaction(request):
    # Implement transaction sending logic here
    return JsonResponse({"message": "Transaction sent successfully"})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserIdentity
from .forms import UserIdentityForm

def manage_identity(request):
    # Ensure that the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated
    
    try:
        # Attempt to retrieve the user's identity
        user_identity = UserIdentity.objects.get(user=request.user)
    except UserIdentity.DoesNotExist:
        user_identity = None
    
    if request.method == 'POST':
        form = UserIdentityForm(request.POST, instance=user_identity)
        if form.is_valid():
            user_identity = form.save(commit=False)
            user_identity.user = request.user
            user_identity.save()
            return redirect('manage_identity')
    else:
        form = UserIdentityForm(instance=user_identity)

    return render(request, 'blockchain_app/manage_identity.html', {'form': form})

    if request.method == 'POST':
        sender_identity = UserIdentity.objects.get(user=request.user)
        recipient_identity_id = request.POST.get('recipient_identity_id')
        recipient_identity = get_object_or_404(UserIdentity, id=recipient_identity_id)
        amount = request.POST.get('amount')
        # Implement transaction logic
        return JsonResponse({'message': 'Transaction sent successfully'})
    return JsonResponse({'error': 'Invalid request method'})
def receive_transaction(request):
    # Ensure that the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated
    
    # Retrieve received transactions for the authenticated user
    transactions = Transaction.objects.filter(recipient_identity=request.user)
    
    # Render the template with the received transactions
    return render(request, 'blockchain_app/received_transaction.html', {'transactions': transactions})


from .forms import UserLoginForm
from django.contrib.auth import authenticate, login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('view_blockchain')  # Redirect to home page after login
    else:
        form = UserLoginForm()
    return render(request, 'blockchain_app/login.html', {'form': form})



from django.http import JsonResponse
import hashlib
import uuid
from .models import Wallet

# import didkit
# def create_wallet(request):
#     wallet_address = "0ccdds"
#     private_key = ""
#     if request.method == 'POST':
#         # Generate a unique wallet address and private key
#         wallet_address = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
#         private_key = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
#         previous_hash =100
        
#     did = didkit.key_to_did("key", didkit.generate_ed25519_key())
#     for indices in Block.objects.all():
#         current = indices.index
#         next_index = current - 1
#         current = next_index
#         previous_hash = Block.objects.get(index =current +1)
#         if previous_hash != indices.previous_hash and int(len(Block.objects.all()))<= 10:
#             Block(index=int(len(Block.objects.all()))+1,timestamp=time.time(),hash =wallet_address,previous_hash = previous_hash.hash,did = did,contains_did = True).save()
#         elif  int(len(Block.objects.all())) > 10:
#             warning = f"You have reach your limit"   
#         break
#     # Save the wallet in the database
#     wallet = Wallet(address=wallet_address, private_key=private_key)
#     Block(index=int(len(Block.objects.all()))+1,timestamp=time.time(),hash =wallet_address,previous_hash = private_key).save()
       

#     return render(request, 'wallet/create_wallet.html')



from .models import SharedData
from .utils import encrypt_data  # Assuming you have encryption utility functions

def share_data(request):
    if request.method == 'POST':
        data_to_share = request.POST.get('data')
        recipient_address = request.POST.get('recipient')
        encrypt_data = request.POST.get('encrypt')

        # Encrypt data if requested
        if encrypt_data:
            data_to_share = encrypt_data(data_to_share)

        # Save shared data to database
        shared_data = SharedData.objects.create(
            sender=request.user,  # Assuming you have user authentication
            recipient=recipient_address,
            data=data_to_share
        )
        
        return JsonResponse({'message': 'Data shared successfully'})
    else:
        return render(request, 'wallet/share_data.html')  # Render the share_data.html template for GET requests
    

# views.py

from django.shortcuts import render, redirect
from .models import SharedData
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Encryption key (ensure this is securely stored)
KEY = b'sixteen byte key'


def receive_data(request):
    decrypted_message = None
    if request.method == 'POST':
        shared_data = SharedData.objects.latest('id')
        encrypted_message = shared_data.encrypted_message
        decrypted_message = decrypt_aes(encrypted_message)
    return render(request, 'receive_data.html', {'decrypted_message': decrypted_message})

def encrypt_and_share_data(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        message = request.POST.get('message')
        encrypted_message = encrypt_aes(message.encode())
        SharedData.objects.create(sender=request.user.username, recipient=recipient, encrypted_message=encrypted_message)
        return redirect('receive_data')
    else:
        return render(request, 'share_data.html', {'error': 'Invalid request method'})

def encrypt_aes(message):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ':' + ct

def decrypt_aes(encrypted_message):
    iv, ct = encrypted_message.split(':')
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')


def encrypted_data(request):
    # Retrieve the encrypted data associated with the current user
    encrypted_data = SharedData.objects.filter(recipient=request.user).last()
    return render(request, 'wallet/encrypted_data.html', {'encrypted_data': encrypted_data})