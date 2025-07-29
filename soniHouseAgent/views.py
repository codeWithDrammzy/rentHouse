from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.dateformat import format as dj_format
from .models import *
from .forms import *
from datetime import date

# ======= AUTHENTICATION =======
def home(request):
    return render(request, 'soniHouseAgent/homepage/home.html')

def my_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    return render(request, 'soniHouseAgent/homepage/my-login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    request.session.flush()
    return redirect('home')


# ======= DASHBOARD =======
def dashboard(request):
    tenants = Tenant.objects.all()
    total_houses = House.objects.count()
    occupied = tenants.count()

    tenant_status = Tenant.objects.select_related('house').all().order_by('-last_payment_date')

    context = {
        'tenant_count': occupied,
        'property_count': total_houses,
        'landlord_count': Landlord.objects.count(),
        'tenant_status': tenant_status
    }
    return render(request, 'soniHouseAgent/adminpage/dashboard.html', context)


# ======= TENANT =======
def tenant(request):
    form = TenantForm()
    tenants = Tenant.objects.select_related('house').all()

    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenant')

    return render(request, 'soniHouseAgent/adminpage/tenant.html', {
        'form': form,
        'tenants': tenants
    })

def tenant_info(request, pk):
    tenant = Tenant.objects.get(id=pk)
    return render(request, 'soniHouseAgent/adminpage/tenant-info.html', {'tenant': tenant})

def renew_rent(request, pk):
    tenant = Tenant.objects.get(id=pk)
    return render(request, 'soniHouseAgent/adminpage/renew-rent.html', {'tenant': tenant})


# ======= LANDLORD =======
def land_owner(request):
    owners = Landlord.objects.all()
    form = LandlordForm()

    if request.method == "POST":
        form = LandlordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landlord')
        else:
            return HttpResponse('Something is not ok')

    return render(request, 'soniHouseAgent/adminpage/landlord.html', {
        'owners': owners,
        'form': form
    })

# ======= PROPERTY =======
def property_listing(request):
    properties = House.objects.select_related('owner').all().order_by('-is_available', 'owner__last_name')
    form = HouseForm()

    if request.method == "POST":
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property')

    return render(request, 'soniHouseAgent/adminpage/property.html', {
        'properties': properties,
        'form': form
    })

def property_info(request, pk):
    property = House.objects.get(id=pk)
    return render(request, 'soniHouseAgent/adminpage/property-info.html', {'property': property})


# ======= SEARCH =======
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

        property = House.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(num_bedrooms__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'query': query,
        'tenant': tenant,
        'owner': owner,
        'property': property
    }

    return render(request, 'soniHouseAgent/adminpage/search-result.html', context)


# ======= PAYMENT CALENDAR & EVENTS =======
def payment_calendar(request):
    tenants = Tenant.objects.select_related('house').all()

    calendar_data = []

    for tenant in tenants:
        due_date = tenant.get_next_due_date()
        calendar_data.append({
            'name': f"{tenant.first_name} {tenant.last_name}",
            'house': tenant.house.title,
            'due_date': due_date,
            'status': tenant.get_payment_status()
        })

    calendar_data.sort(key=lambda x: x['due_date'])  # Sort by upcoming due dates

    return render(request, 'soniHouseAgent/adminpage/payment_calendar.html', {'calendar_data': calendar_data})


def payment_events(request):
    tenants = Tenant.objects.select_related('house').all()
    events = []

    for t in tenants:
        status = t.get_payment_status()
        color = {
            'paid': '#10b981',        # green
            'due_soon': '#facc15',    # yellow
            'overdue': '#ef4444'      # red
        }.get(status, '#9ca3af')      # fallback gray

        events.append({
            'title': f"{(t.first_name + ' ' + t.last_name).upper()}",

            'start': dj_format(t.get_next_due_date(), 'Y-m-d'),
            'color': color
        })

    return JsonResponse(events, safe=False)
