from django.urls import path
from . import views

urlpatterns = [

    #  Authentication
    path('', views.home, name="home"),
    path('my-login', views.my_login, name="my-login"),
    path('logout/', views.logout_view, name='logout'),

    #  Dashboard
    path('dashboard', views.dashboard, name="dashboard"),

    #  Tenant Management
    path('tenant', views.tenant, name="tenant"),
    path('tenant-info/<int:pk>', views.tenant_info, name="tenant-info"),
    path('renew-rent/<int:pk>', views.renew_rent, name="renew-rent"),

    #  Landlord Management
    path('landlord', views.land_owner, name="landlord"),

    #  Property Listings
    path('property', views.property_listing, name="property"),
    path('property-info/<int:pk>', views.property_info, name="property-info"),

    #  Global Search
    path('search-result', views.global_search, name="search-result"),

    #  Payment Calendar
    path('payment-calendar/', views.payment_calendar, name='payment-calendar'),
    path('api/payment-events/', views.payment_events, name='payment-events'),

]
