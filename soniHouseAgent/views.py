from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.dateformat import format as dj_format
from .models import *
from .forms import *
from django.apps import apps
from datetime import date
import csv

# ======= AUTHENTICATION =======
def home(request):
    available_rent =  House.objects.filter(is_available ='True')[:4]
    context ={'available_rent':available_rent}
    return render(request, 'soniHouseAgent/homepage/home.html', context)

def house_info(request, pk):
    house = House.objects.get(id=pk)
    context ={'house':house}
    return render(request, 'soniHouseAgent/homepage/house-info.html',context)

def contact(request):
    return render(request, 'soniHouseAgent/homepage/contact.html')
def about(request):
    return render(request, 'soniHouseAgent/homepage/about.html')

def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = House.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(price__icontains=query) |
            Q(num_bedrooms__icontains=query) |
            Q(description__icontains=query),
            is_available=True 
        )

    context = {
        'results': results,
        'query': query
    }
    return render(request, 'soniHouseAgent/homepage/search_results.html', context)


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
    tenants = Tenant.objects.filter(is_deleted=False)
    total_houses = House.objects.filter(is_deleted=False).count()
    occupied = tenants.count()

    tenant_status = Tenant.objects.select_related('house').filter(is_deleted=False).order_by('-last_payment_date')

    context = {
        'tenant_count': occupied,
        'property_count': total_houses,
        'landlord_count': Landlord.objects.filter(is_deleted=False).count(),
        'tenant_status': tenant_status
    }
    return render(request, 'soniHouseAgent/adminpage/dashboard.html', context)


# ======= TENANT =======
def tenant(request):
    form = TenantForm()
    tenants = Tenant.objects.select_related('house').filter(is_deleted=False)

    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenant')
    context = {
        'form': form,
        'tenants': tenants
        }
    return render(request, 'soniHouseAgent/adminpage/tenant.html', context)

def tenant_info(request, pk):
    tenant = Tenant.objects.get(id=pk, is_deleted=False)
    context ={'tenant': tenant}
    return render(request, 'soniHouseAgent/adminpage/tenant-info.html', context)


def renew_rent(request, pk):
    tenant = Tenant.objects.get(id=pk, is_deleted=False)
    return render(request, 'soniHouseAgent/adminpage/renew-rent.html', {'tenant': tenant})

def delete_tenant(request, pk):
    tenant = Tenant.objects.get(id=pk)
    tenant.is_deleted = True
    tenant.save()
    return redirect('tenant')

def restore_tenant(request, pk):
    tenant = Tenant.objects.get(id=pk)
    tenant.is_deleted = False
    tenant.save()
    return redirect('bin-view')

def delete_tenant(request, pk):
    tenant = get_object_or_404(Tenant, id=pk)
    tenant.delete()
    return redirect('tenant') 

# ======= LANDLORD =======
def land_owner(request):
    owners = Landlord.objects.filter(is_deleted=False)
    form = LandlordForm()

    if request.method == "POST":
        form = LandlordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landlord')
        else:
            return HttpResponse('Something is not ok')
    context ={
        'owners': owners,
        'form': form}
    return render(request, 'soniHouseAgent/adminpage/landlord.html', context)

def delete_landlord(request, pk):
    landlord = Landlord.objects.get(id=pk)
    landlord.is_deleted = True
    landlord.save()
    return redirect('landlord')

def restore_landlord(request, pk):
    landlord = Landlord.objects.get(id=pk)
    landlord.is_deleted = False
    landlord.save()
    return redirect('bin-view')


# ======= PROPERTY =======
def property_listing(request):
    properties = House.objects.select_related('owner').filter(is_deleted=False).order_by('-is_available', 'owner__last_name')
    form = HouseForm()

    if request.method == "POST":
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property')
    context={
        'properties': properties,
        'form': form
        }
    return render(request, 'soniHouseAgent/adminpage/property.html', context)

def property_info(request, pk):
    property = House.objects.get(id=pk, is_deleted=False)
    context ={'property': property}
    return render(request, 'soniHouseAgent/adminpage/property-info.html', context)

def delete_house(request, pk):
    house = House.objects.get(id=pk)
    house.is_deleted = True
    house.save()
    return redirect('property')

def restore_house(request, pk):
    house = House.objects.get(id=pk)
    house.is_deleted = False
    house.save()
    return redirect('bin-view')

# ======= SEARCH =======
def global_search(request):
    query = request.GET.get('q')

    tenant = owner = property = []

    if query:
        tenant = Tenant.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(id_card__icontains=query) |
            Q(phone_number__icontains=query),
            is_deleted=False
        )

        owner = Landlord.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(id_card__icontains=query) |
            Q(phone_number__icontains=query),
            is_deleted=False
        )

        property = House.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(num_bedrooms__icontains=query) |
            Q(price__icontains=query),
            is_deleted=False
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

def overdue_tenants(request):
    tenants = Tenant.objects.select_related('house').filter(is_deleted=False)
    overdue_list = [t for t in tenants if t.get_payment_status() == 'overdue']

    context = {
        'tenants': overdue_list,
    }
    return render(request, 'soniHouseAgent/adminpage/overdue-tenants.html', context)


def export_all_tenants_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Tenants_Data.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'First Name', 'Last Name', 'Phone Number', 'House',
        'Move-In Date', 'Last Payment Date', 'Next Due Date',
        'Payment Option', 'Payment Amount', 'Status'
    ])

    tenants = Tenant.objects.select_related('house').filter(is_deleted=False)

    for tenant in tenants:
        writer.writerow([
            tenant.first_name.title(),
            tenant.last_name.title(),
            tenant.phone_number,
            tenant.house.title,
            tenant.move_in_date,
            tenant.last_payment_date,
            tenant.get_next_due_date(),
            tenant.get_payment_option_display(),
            tenant.payment_amount,
            tenant.get_payment_status().replace('_', ' ').title()
        ])

    return response


# ======= PAYMENT CALENDAR & EVENTS =======
def payment_calendar(request):
    tenants = Tenant.objects.select_related('house').filter(is_deleted=False)

    calendar_data = []

    for tenant in tenants:
        due_date = tenant.get_next_due_date()
        calendar_data.append({
            'name': f"{tenant.first_name} {tenant.last_name}",
            'house': tenant.house.title,
            'due_date': due_date,
            'status': tenant.get_payment_status()
        })

    calendar_data.sort(key=lambda x: x['due_date'])

    return render(request, 'soniHouseAgent/adminpage/payment_calendar.html', {'calendar_data': calendar_data})


def payment_events(request):
    tenants = Tenant.objects.select_related('house').filter(is_deleted=False)
    events = []

    for t in tenants:
        status = t.get_payment_status()
        color = {
            'paid': '#10b981',
            'due_soon': '#facc15',
            'overdue': '#ef4444'
        }.get(status, '#9ca3af')

        events.append({
            'title': f"{(t.first_name + ' ' + t.last_name).upper()}",
            'start': dj_format(t.get_next_due_date(), 'Y-m-d'),
            'color': color
        })

    return JsonResponse(events, safe=False)


# ======= BIN/RESTORE VIEW =======
def bin_view(request):
    deleted_tenants = Tenant.objects.filter(is_deleted=True)
    deleted_houses = House.objects.filter(is_deleted=True)
    deleted_landlords = Landlord.objects.filter(is_deleted=True)
    context ={
        'tenants': deleted_tenants,
        'houses': deleted_houses,
        'landlords': deleted_landlords
    }

    return render(request, 'soniHouseAgent/adminpage/bin.html', context)


# ======= PAMANENTLY DELETE VIEW =======
def permanently_delete_record(request, model_name, pk):
    try:
        model = apps.get_model('soniHouseAgent', model_name)

        # Check if object exists and is marked deleted
        obj_qs = model.objects.filter(pk=pk, is_deleted=True)
        if not obj_qs.exists():
            return HttpResponseBadRequest("Object not found or not marked as deleted.")

        # Permanently delete from DB, bypassing model's delete()
        obj_qs.delete()

        return redirect('bin-view')  # Make sure this URL name exists
    except LookupError:
        return HttpResponseBadRequest("Invalid model name.")