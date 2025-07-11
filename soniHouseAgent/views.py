from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .models import*
from .forms import*
from django.shortcuts import redirect
from django.db.models import Q


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
    tenants = Tenant.objects.all()
    total_houses = House.objects.count()
    occupied = tenants.count()
    context = {
        'tenant_count': occupied,
        'property_count': total_houses,
        'landlord_count': Landlord.objects.count(),
        
    }
    return render(request, 'soniHouseAgent/adminpage/dashboard.html', context)


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

def tenant_info(request, pk):
    tenant = Tenant.objects.get(id=pk)
    context = {'tenant':tenant}
    return render (request, 'soniHouseAgent/adminpage/tenant-info.html', context)

def renew_rent(request, pk):
    tenant = Tenant.objects.get(id=pk)
    context = {'tenant':tenant}
    return render (request, 'soniHouseAgent/adminpage/renew-rent.html', context)

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
    
    properties = House.objects.select_related('owner').all().order_by('-is_available', 'owner__last_name')

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

def property_info(request, pk):
    property = House.objects.get(id=pk)
    context = {'property': property}
    return render(request, 'soniHouseAgent/adminpage/property-info.html', context)



def logout_view(request):
    auth_logout(request)  
    request.session.flush()
    return redirect('home')

def global_search(request):
    query = request.GET.get('q')
    
    tenant = owner = property = []

    if query:
        tenant = Tenant.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(id_card__icontains=query) |
            Q(phone_number__icontains=query)
        )

        owner = Landlord.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(id_card__icontains=query) |
            Q(phone_number__icontains=query)
        )

        property = House.objects.filter(  # Make sure this is the actual model
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(num_bedrooms__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        return redirect(request.META.get('HTTP_REFERER', '/')) 
        #this keeps u on the same page if search is empty

    context = {
        'query': query,
        'tenant': tenant,
        'owner': owner,
        'property': property
    }

    return render(request, 'soniHouseAgent/adminpage/search-result.html', context)
