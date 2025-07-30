from django.urls import path
from . import views

urlpatterns = [

    #  Authentication
    path('', views.home, name="home"),
    path('my-login', views.my_login, name="my-login"),
    path('logout/', views.logout_view, name='logout'),
    path('house/info/<int:pk>', views.house_info, name="house-info"),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search/', views.search_view, name='search'),


    #  Dashboard
    path('dashboard', views.dashboard, name="dashboard"),

    #  Tenant Management
    path('tenant', views.tenant, name="tenant"),
    path('tenant-info/<int:pk>', views.tenant_info, name="tenant-info"),
    path('renew-rent/<int:pk>', views.renew_rent, name="renew-rent"),
    path('tenant/delete/<int:pk>/', views.delete_tenant, name='delete-tenant'),


    #  Landlord Management
    path('landlord', views.land_owner, name="landlord"),

    #  Property Listings
    path('property', views.property_listing, name="property"),
    path('property-info/<int:pk>', views.property_info, name="property-info"),

    #  Global Search
    path('search-result', views.global_search, name="search-result"),
    path('tenants/overdue/', views.overdue_tenants, name='overdue-tenants'),
    path('export-all-tenants-csv/', views.export_all_tenants_csv, name='export-all-tenants-csv'),




    #  Payment Calendar
    path('payment-calendar/', views.payment_calendar, name='payment-calendar'),
    path('api/payment-events/', views.payment_events, name='payment-events'),


    #  bin and restore
    path('bin/', views.bin_view, name='bin-view'),
    path('tenant/restore/<int:pk>/', views.restore_tenant, name='restore-tenant'),
    path('house/restore/<int:pk>/', views.restore_house, name='restore-house'),
    path('landlord/restore/<int:pk>/', views.restore_landlord, name='restore-landlord'),

    #pamanent delete
    path('permanent-delete/<str:model_name>/<int:pk>/', views.permanently_delete_record, name='permanent-delete-record'),



]
