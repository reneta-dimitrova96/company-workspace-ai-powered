from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from tenants.models import Tenant, TenantMembership
from tenants.serializers import TenantSerializer
from tenants.services import tenant_service


class TenantsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def create(self, request, *args, **kwargs):
        tenant = tenant_service.create_tenant(
            owner_user=request.user,
            tenant_data=request.data
        )

        serializer = self.serializer_class(tenant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        form_data: dict = request.data
        if not form_data:
            return Response(data={'message': "Invalid or missing form data."}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        company = request.tenant
        tenant_user = TenantMembership.objects.filter(user=request.user, company=request.tenant).first()
        if tenant_user:
            tenant = get_object_or_404(Tenant, pk=request.tenant.id)
            input_serializer = self.serializer_class(tenant, data=form_data, partial=True)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()

            return Response(data=input_serializer.data, status=status.HTTP_200_OK)
