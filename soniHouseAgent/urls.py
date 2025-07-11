from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('tenant', views.tenant, name="tenant"),
    path('tenant-info/<int:pk>', views.tenant_info, name="tenant-info"),
    path('renew-rent/<int:pk>', views.renew_rent, name="renew-rent"),
    path('landlord', views.land_owner, name="landlord"),
    path('property', views.property_listing, name="property"),
    path('property-info/<int:pk>', views.property_info, name="property-info"),
    path('search-result', views.global_search, name="search-result"),



    path('logout/', views.logout_view, name='logout'),
    
]
