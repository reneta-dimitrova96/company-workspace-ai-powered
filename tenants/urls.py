from django.urls import path
from tenants.views import TenantsViewSet

urlpatterns = [
    path('tenants/', TenantsViewSet.as_view({
        'post': 'create',
        'patch': 'partial_update',
    }))
]
