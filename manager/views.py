from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from space.models import PasswordOTP

from .forms import CreateDIDForm, IssueCredentialForm
from .models import Identifier, VerifiableCredential
from .smart_contract import did_registry, credential_registry
from  .forms import UpdateCredentialForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'identity_management/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'identity_management/login.html', {'error': 'Invalid username or password'})
    return render(request, 'identity_management/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

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
