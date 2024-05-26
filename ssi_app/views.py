from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import Identity
from web3 import Web3
import requests
from django.contrib.auth.decorators import login_required
from identityManagement.models import IdentityManager
from identityManagement.forms import IdentityForm
from identityManagement.identity_management import IdentityManagement
from .models import Identity as ssid
from django.contrib.auth.models import User
from dependencies.emailer import generate_otp, send_reset_password_email, send_user_credential_via_email
from space.models import PasswordOTP
contract = IdentityManagement()
# Initialize Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b8211144561c422bbeeb55546e0d27d2'))

IPFS_API_URL = 'http://127.0.0.1:5001/api/v0/'

def register(request):
    if request.method == 'POST':
        
        user_address = request.POST['user_address']
        user_name = request.POST['user_name']
        user_data = request.POST['user_data']
        email = request.POST['user_email']
        # Store user data on IPFS
        response = requests.post(IPFS_API_URL + 'add', files={'file': user_data})
        ipfs_hash = response.json()['Hash']
        
        # Save identity information to the database
        identity = ssid(user_address=user_address, user_name=user_name, ipfs_hash=ipfs_hash)
        identity.save()
        contract.register_identity(user_address, user_name, email)
        uid = int(len(IdentityManager.objects.all()))+1
        IdentityManager(uid,user=request.user,ethereum_address=user_address,name=user_name,email=email,shared_data = user_data).save()
        otp = generate_otp()
        otp_id = int(len(PasswordOTP.objects.all()))+1  
        PasswordOTP(otp_id,user=request.user,otp=otp).save()
        send_user_credential_via_email(user_name=request.user,user_email=email,credential_info=f"[foundationX Identity Issuing OTP] : {otp}") 
        
        return JsonResponse({'status': 'success', 'message': 'Identity registered'})
    return render(request, 'register.html')

def register_identity(request):
    if request.method == 'POST':
        form = IdentityForm(request.POST)
        if form.is_valid():
            ethereum_address = form.cleaned_data['ethereum_address']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contract.register_identity(ethereum_address, name, email)
            form.save()
            return redirect('identity_list')
    else:
        form = IdentityForm()
    return render(request, 'identities/register_identity.html', {'form': form})

def identity_list(request):
    identities = IdentityManager.objects.all()
    return render(request, 'identities/identity_list.html', {'identities': identities})


def authenticate(request):
    if request.method == 'POST':
        user_address = request.POST['user_address']
        verify_otp = request.POST['otp']
        pt =int(len( PasswordOTP.objects.all()))
        diff = pt-1
        if diff < 0:
            diff = 0
            code = 0
        else:
            val =PasswordOTP.objects.all()[diff:] 
            code = val[0].otp
        
        
        try:
            if code  == verify_otp:
                PasswordOTP.objects.all().delete()
                identity = ssid.objects.get(user_address=user_address)
                response = requests.post(IPFS_API_URL + 'cat', params={'arg': identity.ipfs_hash})
                user_data = response.text
                verify_account = IdentityManager.objects.get(ethereum_address=user_address)
                verify_account.verified = True
                verify_account.save()
                return JsonResponse({'status': 'success', 'identity': identity.user_name, 'user_data': user_data})
        except Identity.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Identity not found'})
    return render(request, 'authenticate.html')




@login_required
def dashboard(request):
    credentials = ""
    user = request.user
    did = ""
    # did = did_registry.get_did(user.username)
    user_id = Identifier.objects.all()
    for uid in user_id:
        if uid.user == request.user:
            did = uid.did
            credentials = VerifiableCredential.objects.filter(did=did)
    return render(request, 'identity_management/dashboard.html', {'did': did, 'credentials': credentials})

@login_required
def create_did(request):
    if request.method == 'POST':
        print("POST request received for creating DID")
        form = CreateDIDForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            did = form.cleaned_data['did']
            did_registry.register_did(request.user.username, did)
            Identifier.objects.create(user=request.user, did=did)
            return redirect('dashboard')
        else:
            print("Form is not valid", form.errors)
    else:
        form = CreateDIDForm()
    return render(request, 'identity_management/create_did.html', {'form': form})


from identities.models import Identity
@login_required
def issue_credential(request):
    if request.method == 'POST':
        print("POST request received for issuing credential")
        verify_otp = request.POST.get("otp")
        pt =int(len( PasswordOTP.objects.all()))
        diff = pt-1
        if diff < 0:
            diff = 0
            code = 0
        else:
            val =PasswordOTP.objects.all()[diff:] 
            code = val[0].otp
        
        
        if code  == verify_otp:
            PasswordOTP.objects.all().delete()
            return redirect("myProfile")
        form = IssueCredentialForm(request.POST)
        if form.is_valid():
            user_id = Identifier.objects.all()
            for uid in user_id:
                if uid.user == request.user and code  == verify_otp:
                    did = uid.did
                    credential_data = form.cleaned_data['credential_data']
                    credential_id = credential_registry.issue_credential(did, credential_data)
                    VerifiableCredential.objects.create(did=did, credential_data=credential_id)
            return redirect('dashboard')
        else:
            print("Form is not valid", form.errors)
    else:
        form = IssueCredentialForm()
    return render(request, 'identity_management/issue_credential.html', {'form': form})

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_proof(data):
    key = RSA.generate(2048)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return key.publickey().export_key(), signature

def verify_proof(data, public_key, signature):
    key = RSA.import_key(public_key)
    h = SHA256.new(data.encode())
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False


@login_required
def list_credentials(request):
    credentials = ""
    user_did = Identifier.objects.filter(user=request.user)
    for uid in user_did:
        credentials = VerifiableCredential.objects.filter(did=uid.did)
    return render(request, 'identity_management/list_credentials.html', {'credentials': credentials})

@login_required
def update_credential(request, credential_id):
    credential = VerifiableCredential.objects.get(id=credential_id)
    if request.method == 'POST':
        form = UpdateCredentialForm(request.POST, instance=credential)
        if form.is_valid():
            form.save()
            return redirect('list_credentials')
    else:
        form = UpdateCredentialForm(instance=credential)
    return render(request, 'identity_management/update_credential.html', {'form': form})

@login_required
def revoke_credential(request, credential_id):
    credential = VerifiableCredential.objects.get(id=credential_id)
    credential.delete()
    return redirect('list_credentials')



def share_data(request):
    if request.method == 'POST':
        owner_address = request.POST['owner_address']
        receiver_address = request.POST['receiver_address']
        data = request.POST['data']
        contract.share_data(owner_address, receiver_address, data)
        return redirect('identity_list')
    identities = User.objects.all()
    return render(request, 'identities/share_data.html', {'identities': identities})

def access_shared_data(request, address):
    shared_data = contract.access_shared_data(address)
    return render(request, 'identities/access_shared_data.html', {'shared_data': shared_data})

def revoke_data(request):
    if request.method == 'POST':
        owner_address = request.POST['owner_address']
        receiver_address = request.POST['receiver_address']
        contract.revoke_shared_data(owner_address, receiver_address)
        return redirect('identity_list')
    identities = IdentityManager.objects.all()
    return render(request, 'identities/revoke_data.html', {'identities': identities})
