from django.shortcuts import render, redirect, get_object_or_404
from .models import IdentityManager
from .forms import IdentityForm
from .identity_management import IdentityManagement
from ssi_app.models import Identity as ssid
contract = IdentityManagement()

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

def share_data(request):
    if request.method == 'POST':
        owner_address = request.POST['owner_address']
        receiver_address = request.POST['receiver_address']
        data = request.POST['data']
        contract.share_data(owner_address, receiver_address, data)
        return redirect('identity_list')
    identities = ssid.objects.all()
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
