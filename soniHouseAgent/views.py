from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .models import*
from .forms import*
from django.shortcuts import redirect


def home(request):
    return render( request,'soniHouseAgent/homepage/home.html')


def my_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect ('dashboard')
    
    return render(request, 'soniHouseAgent/homepage/my-login.html', {'form': form})

def dashboard(request):
    return render (request, 'soniHouseAgent/adminpage/dashboard.html')

def tenant(request):
    form = TenantForm()
    tenants = Tenant.objects.select_related('house').all()  

    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenant')

    context = {
        'form': form,
        'tenants': tenants,
    }
    return render(request, 'soniHouseAgent/adminpage/tenant.html', context)

def tenant_info(request):
    return render (request, 'soniHouseAgent/adminpage/tenant-info.html')

def land_owner(request):
    owners = Landlord.objects.all()
    form = LandlordForm()
    if request.method == "POST":
        form =LandlordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landlord')
        else:
            return HttpResponse('something is not ok')

    context = {'owners':owners,
               'form':form
               }
    return render (request, 'soniHouseAgent/adminpage/landlord.html', context)

def property_listing(request):
    properties = House.objects.select_related('owner').all()
    form = HouseForm()
    if request.method =="POST":
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property')

    context ={'properties': properties,
              'form':form
              }
    return render(request, 'soniHouseAgent/adminpage/property.html', context)


def logout_view(request):
    auth_logout(request)  
    request.session.flush()
    return redirect('home')


