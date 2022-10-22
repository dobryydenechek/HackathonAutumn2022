from urllib.robotparser import RequestRate
from xmlrpc.client import ResponseError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from general.models import PCAPFile, Persone

@login_required
def main(request, *args, **kwargs):
    return render(request, 'start.html')

def sheet(request, *args, **kwargs):
    return render(request,'sheet.html')


def signin(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('sheet')
            else:
                messages.error(request, 'User not found')
        else:
            messages.error(request, 'Username or password is incorrect')
        return render(request,'signin.html')
    else:
        return render(request,'signin.html')
    
def signup(request, *args, **kwargs):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if not all([firstname, lastname, username, password1, password2, email]):
            messages.error(request, 'All fields are required')
            return render(request,'signup.html')
        if password1 or password1 == password2:
            user = User.objects.create_user(username, email, password1)
            user.save()
            login(request, user)
            return redirect('sheet')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request,'signup.html')
    return render(request,'signup.html')

@login_required
def signout(request, *args, **kwargs):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('signin')

@login_required
def create_persone(request, *args, **kwargs):
    print(request.POST.get('male'))
    if request.method == 'POST':
        persone = Persone.objects.create(
            firstname = request.POST.get('firstname', None),
            lastname = request.POST.get('lastname', None),
            telephone = request.POST.get('telephone', None),
            old = int(request.POST.get('old', None)) if request.POST.get('old', None) else None,
            male = int(request.POST.get('male', None)) if request.POST.get('male', None) else None,
            adres = request.POST.get('adres', None),
            email = request.POST.get('email', None)
        )
        if persone:
            return redirect('persone_list')
    return render(request,'create_persone.html')
    
@login_required
def persone_list(request, *args, **kwargs):
    persones = Persone.objects.all()
    return render(request,'persone_list.html', {'persones': persones})

@login_required
def persone_delete(request, pk, *args, **kwargs):
    Persone.objects.get(pk=pk).delete()
    messages.success(request, 'Persone deleted')
    return redirect('persone_list')
    

@login_required
def persone_view(request, pk, *args, **kwargs):
    persone = Persone.objects.get(pk=pk)
    pcap = PCAPFile.objects.filter()    
    return render(request, 'persone_view.html', {'persone': persone})
    
@login_required
def upload_pcap(request, *args):
    if request.method == 'POST':
        pcaps = request.FILES.getlist('files')
        pk = request.POST.get('pk')
        persone = Persone.objects.get(pk=pk)
        for pcap in pcaps:
            if pcap.name[-5:] != '.pcap':
                messages.warning(request, 'Format files must be a .pcap file')
                return redirect('persone_view', pk)
            else:
                pcap_model = PCAPFile(file=pcap, persone=persone)
                messages.success(request, f'File "{pcap.name}" was successfully uploaded')
        pcap_model.save()
        return redirect('persone_view', pk)
