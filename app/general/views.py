import os
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files import File
from app.settings import MEDIA_ROOT

from general.models import CSVFile, PCAPFile, Package, Persone, Trafic

from ml.predict import save_csv


@login_required
def main(request, *args, **kwargs):
    # return render(request, 'start.html')
    return redirect('persone_list')

@login_required
def analysis(request, pk, *args, **kwargs):
    trafics = Trafic.objects.filter(package__pk=pk)
    if trafics:
        types = {}
        for c, s in Trafic.CHOICES:
            count = trafics.filter(type=c).count()
            if count: types[s] = count
        maxx = max(types.values())
        response = {}
        for k, v in types.items():
            response[k] = int(v / (maxx / 100))
        return render(request,'analysis.html', {'trafics': trafics, "types":response, "maxx": maxx})
    else:
        messages.warning(request, 'Error of Trafoc or Trafic not found.')
        return redirect('persone_view', pk)

def signin(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('persone_list')
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
            return redirect('persone_list')
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
    if request.method == 'POST':
        persone = Persone.objects.create(
            firstname = request.POST.get('firstname', None),
            lastname = request.POST.get('lastname', None),
            telephone = request.POST.get('telephone', None),
            old = int(request.POST.get('old', None)) if request.POST.get('old', None) else None,
            male = int(request.POST.get('male', None)) if request.POST.get('male', None) else None,
            adres = request.POST.get('adres', None),
            email = request.POST.get('email', None),
            imei = request.POST.get('imei', None)
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
    packages = Package.objects.filter(persone=persone.pk)
    return render(request, 'persone_view.html', {'packages': packages,
                                                 'persone': persone
                                                 })


@login_required
def upload_pcap(request, *args):
    if request.method == 'POST':
        pcaps = request.FILES.getlist('files')
        pk = request.POST.get('pk')
        persone = Persone.objects.get(pk=pk)
        package = Package.objects.create(persone=persone)
        for pcap in pcaps:
            if pcap.name[-5:] != '.pcap':
                messages.warning(request, 'Format files must be a .pcap file')
                return redirect('persone_view', pk)
            else:
                pcap_model = PCAPFile.objects.create(file=pcap, persone=persone, filename=pcap.name)
                print(pcap_model.pk)
                package.pcaps.add(pcap_model)

        cwd = os.getcwd()
        path_to_dir = pcap_model.get_path_dir()
        bsdir = os.path.join(MEDIA_ROOT, path_to_dir)

        t = datetime.now()
        csv_path = f'persone_pk_{persone.pk}/{t.year}/{t.month}/{t.day}/{t.time().minute}/result.csv'
        bsdircsv = os.path.join(MEDIA_ROOT, 'upload/', csv_path)

        save_csv(bsdircsv, bsdir)
        csv = CSVFile.objects.create(file=csv_path, filename='filename.csv', persone=persone)
        package.csv = csv
        package.save()

        check = True
        with open(bsdircsv, 'r', encoding='utf-8') as file:
            for row in file:
                if check:
                    check = False
                    continue
                row = row.split(',')
                te=row[10][-2:]

                t = Trafic.objects.create()
                t.package=package
                t.sport=row[1]
                t.dport=row[2]
                t.seq=row[3]
                t.ask=row[4]
                t.dataofs=row[5]
                t.window=row[6]
                t.chksum=row[7]
                t.timestamp=row[8]+'.'+row[9]
                t.type=te
                t.save()

        messages.success(request, f'Files was successfully uploaded')
        return redirect('persone_view', pk)

@login_required
def package_delete(request, *args, **kwargs):
    if request.method == 'POST':
        Package.objects.get(pk=request.POST.get('package')).delete()
    person_pk = request.POST.get('persone')
    return redirect('persone_view', int(person_pk))

