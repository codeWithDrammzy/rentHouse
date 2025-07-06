from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('tenant', views.tenant, name="tenant"),
    path('tenant-info', views.tenant_info, name="tenant-info"),
    path('landlord', views.land_owner, name="landlord"),
    path('property', views.property_listing, name="property"),



    path('logout/', views.logout_view, name='logout'),
    
]
