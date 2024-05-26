import datetime
import hashlib
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse_lazy

from dependencies.encryption_with_keys import decrypt_data, encrypt_data, generate_key_pair
from sharing.models import ShareData
from .models import  FileDrive, file_collection ,acoount_collection,credential_collection,CredentialsDrive,Profile,PasswordOTP
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.models import User
from .forms import UserUpdateForm,ProfileUpdateForm
# In your Django views or models
# from filebaseApi import FilebaseClient

# def upload_data(request):
#     if request.method == 'POST' and request.FILES['data_file']:
#         data_file = request.FILES['data_file']
#         client = FilebaseClient(api_key=settings.FILEBASE_CONFIG['API_KEY'],
#                                 secret_key=settings.FILEBASE_CONFIG['SECRET_KEY'],
#                                 region=settings.FILEBASE_CONFIG['REGION'])
#         bucket_name = settings.FILEBASE_CONFIG['BUCKET_NAME']
#         client.upload_file(bucket_name, data_file.name, data_file.read())
#         return HttpResponse('Data file uploaded successfully!')
#     return render(request, 'upload_data.html')


@login_required
def identityDrive(request):
    
    return render(request, "identity.html", {})



def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  email=request.POST.get('email')
  if form.is_valid():
   form.save()
   return redirect("space:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})

# creating file 
@login_required
def create_file(request):
    # if request.method == 'POST':
    #     name = request.POST['name']
    #     data = request.POST['data']
    #     file_collection.insert_one({
    #         'name': name,
    #         'data': data
    #     })
    # else:
    #     files = file_collection.find()
    if request.method == 'POST':
        tag = request.POST.get('filename')
        description = request.POST.get('description')
        file =  request.FILES.get('file')
        user = request.user
        tdn = datetime.datetime.today()
        file_id = int(len(FileDrive.objects.all()))+1
        FileDrive(file_id,description=description,user=user,file=file,file_tag=tag,created=tdn).save()
    
        # file_collection.insert_one({
        #     'File Name': tag,
        #     'Description': description,
        #     'File': file,
        # })
        
        
    return render(request, 'create_file.html')

@login_required
def account(request):
    
    return render(request, 'account.html')


from dependencies.issuer import generate_username,process_identity_text_advanced
@login_required
def credentials(request):
    if request.method == 'POST':
        current_user = request.user
        crd_tag = request.POST.get("crd-tag")
        username = request.POST.get("username")
        userAddress = request.POST.get("userAddress")
        description = request.POST.get("crd-desc")
        body = request.POST.get("body")
        
        # registering 
        uname = generate_username(username)
        # registered = register_user(uname)
        identity_text = process_identity_text_advanced(body)
        print(uname)        
        # credential_collection.insert_one({
        #     'Credential Tag ':crd_tag,
        #     'Username': username,
        #     'userAddress': userAddress,
        #     'Description': description,
        #     'Credential': body,
        # })
        credential_id = int(len(CredentialsDrive.objects.all()))+1
        CredentialsDrive(credential_id,user=current_user,id_name = crd_tag,given_name=username,userAddress=userAddress,description=description,body=body).save()
        
    return render(request, 'credential.html')

        
# landing 
@login_required
def landing(request):
    return render(request, 'landing.html')


# Importing library
import qrcode
@login_required
def main(request):    
    
    return render(request, 'main.html')

@login_required
def credential_repo(request):
    if request.method == 'POST':
        search_item = request.POST.get('search')
        Credentials = CredentialsDrive.objects.filter(id_name=search_item,user=request.user) 
    elif request.method == 'GET':
        Credentials = CredentialsDrive.objects.filter(user=request.user) 
    return render(request, 'credential_repo.html',{"Credentials":Credentials})


# dashboard 
@login_required
def myDashboard(request):
    return render(request, 'dashboard.html')

import json

# profile

@login_required
def myProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Profile saved")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile.html',{'u_form':u_form, 'p_form':p_form})


# vault

@login_required
def myVault(request):
    if request.method == 'POST':
        search_item = request.POST.get('search')
        files = FileDrive.objects.filter(file_tag=search_item,user=request.user) 
    elif request.method == 'GET':
        files = FileDrive.objects.filter(user=request.user) 
    return render(request, 'vault.html',{'files':files})

# authorizeAccess 
# @login_required
# def authorizeAccess(request):
#     details = "0xbc0000000000"
#     signature = json.dumps(details)
    
#     return render(request, 'authorizeAccess.html',{"signature":signature})


# add contents 
@login_required
def addContents(request):
    
    return render(request, 'addContent.html')

from dependencies.emailer import generate_otp, send_email, send_reset_password_email, send_user_credential_via_email
def emailPager(request):
    
    if request.method == 'GET' and request.user:
        verify_otp = request.GET.get("otp")
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
    if request.method == 'POST':
        user = "User"
        address = request.POST.get("address")
        # user_email = User.objects.filter(username=user).first().email
        otp = generate_otp()
        send_reset_password_email(username=user, receiver=address, otp=otp)
        otp_id = int(len(PasswordOTP.objects.all()))+1  
        PasswordOTP(otp_id,user=request.user,otp=otp).save()
        

        
    return render(request,"emailer.html")


from django.utils import timezone
from datetime import datetime, timedelta
from identityManagement.identity_management import IdentityManagement
@login_required
def shared_credential_list(request):
    shared_texts = ShareData.objects.filter(recipient=request.user)
    return render(request, 'shared_text_list.html', {'shared_texts': shared_texts})

from django.http import JsonResponse, HttpResponseForbidden
from blockchain_app.utils import encrypt_data as  cipher_code,decrypt_data as decipher_code,key as k
@login_required
def add_shared_credential(request):
    expiration_time = timezone.now() + timedelta(hours=1)
    users = User.objects.all()
    expire_data = ShareData.objects.filter(time_limit= timezone.now())
    expire_data.delete()
    if request.method == 'POST':
        text = request.POST.get('text')
        recv = request.POST.get("recipient")
        user = User.objects.get(username=recv)
        time_limit = request.POST.get('time_limit')

        try:
            str_time = str(time_limit)
            time_limit = datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
                           
        global iv,ciphertext
        iv, ciphertext = cipher_code(text, k)
        print(f"IV {iv}")
        print(f"CT {ciphertext}")
        print(f"KEY {k}")

        try:
            ShareData.objects.create(text=ciphertext, owner=request.user,recipient=user,time_limit=time_limit)
            body = f"A content is delivered to you on foundationX. To access these content here are your requirements,\n[encrypted key] : {iv}\n[decrypted key] : {k}"
            # send_user_credential_via_email(user_name=request.user.username,user_email=request.user.email,credential_info=body)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Recipient does not exist'}, status=404)


        return redirect('shared credential')
    return render(request, 'add_shared_text.html',{'users':users})



from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from blockchain_app.utils import key

@login_required
def edit_shared_credential(request, shared_text_id):
    users = User.objects.all()
    decrypted = ""
    encrypted = ""
    shared_text = get_object_or_404(ShareData, pk=shared_text_id)
    pt = "information"
    if request.method =='GET':
        pass
        # iv = request.GET.get("iv")
        
        # print(f"deciphered code {decipher_code(iv=iv,ct=shared_text,key=key)}")
    if request.method == 'POST':
        shared_text.text = request.POST.get('text')
        # shared_text.save()  
        iv = request.POST.get("iv")
        ct = request.POST.get('ct')
        key = request.POST.get('key') 
        agree = request.POST.get('agree')
        try:
            pt = decipher_code(iv, ct, k)
            
        except Exception:
            return HttpResponse("Could not decrypt")
        print(pt)
        if agree:
            shared_text.save() 
    # Convert iv to bytes if it's not already
        
        return redirect('shared credential')
    return render(request, 'edit_shared_text.html', {'shared_text': shared_text,'users': users,"decrypted":decrypted,"encrypted":encrypted,"pt":pt})



def calculate_hash(block):
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def is_valid_block(block, previous_block):
    if previous_block.index + 1 != block.index:
        return False
    if previous_block.hash != block.previous_hash:
        return False
    if calculate_hash(block) != block.hash:
        return False
    return True


# encryption_app/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.backends import default_backend
from sharing.models import EncryptedData

def decrypt_data(request, encrypted_data_id):
    # Retrieve the encrypted data from the database
    encrypted_data = get_object_or_404(EncryptedData, pk=encrypted_data_id)
    
    # Retrieve the associated private key
    private_key_text = encrypted_data.private_key.private_key_text
    
    # Load the private key
    private_key = serialization.load_pem_private_key(
        private_key_text.encode(),
        password=None,
        backend=default_backend()
    )
    
    # Decrypt the encrypted text
    decrypted_text = private_key.decrypt(
        encrypted_data.encrypted_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return HttpResponse(decrypted_text.decode())  # Assuming the decrypted text is a string



# # views.py

# from django.shortcuts import render
# from django.http import JsonResponse
# from .utils import upload_to_ipfs

# import requests

# # Set your Infura project ID and API key
# PROJECT_ID = 'b8211144561c422bbeeb55546e0d27d2'
# API_KEY = 'ii0qQKoigvFl4OB6gJjufr02s9uSkRZ/Dwn83RG4/AOtazDRNbN4hw'

# # Base URL for the Infura IPFS API
# BASE_URL = f'https://ipfs.infura.io:5001/api/v0'
# def upload_file(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         uploaded_file = request.FILES['file']
#         file_content = uploaded_file.read()  # Read the content of the uploaded file
#         headers = {'Authorization': f'Bearer {API_KEY}'}
#         files = {'file': (uploaded_file.name, file_content)}  # Use the file's content directly
#         response = requests.post(f'{BASE_URL}/add', headers=headers, files=files)
#         if response.status_code == 200:
#             return JsonResponse({'ipfs_hash': response.json()['Hash']})
#         else:
#             return JsonResponse({'error': f'Error uploading file: {response.text}'}, status=500)
#     return render(request, "upload_to_ipfs.html")
