from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from tenants.models import Tenant, TenantMembership
from tenants.serializers import TenantSerializer


class TenantsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def partial_update(self, request, *args, **kwargs):
        """Partially update the current tenant if the user belongs to it."""
        form_data: dict = request.data
        if not form_data:
            return Response(data={'message': "Invalid or missing form data."}, status=status.HTTP_400_BAD_REQUEST)

        tenant_user_exist = TenantMembership.objects.filter(user=request.user, company=request.tenant,
                                                            role__in=['owner', 'admin']).exists()
        if not tenant_user_exist:
            return Response(
                {"message": "User does not have permission to update this tenant."},
                status=status.HTTP_403_FORBIDDEN
            )

        tenant = get_object_or_404(Tenant, pk=request.tenant.id)
        serializer = self.serializer_class(tenant, data=form_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """Get the current tenant info if the user belongs to it."""
        tenant_user_exist = TenantMembership.objects.filter(user=request.user, company=request.tenant).exist()
        if not tenant_user_exist:
            return Response(
                {"message": "User does not belong to this tenant."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(request.tenant)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
