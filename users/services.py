from django.db import transaction

from tenants.models import Tenant, TenantMembership
from tenants.services import tenant_service
from users.serializers import OwnerRegisterSerializer, EmployeeRegisterSerializer


class UserService:
    @staticmethod
    def register_owner(form_data: dict):
        """Register an owner and return the created user and tenant."""
        if not form_data:
            raise ValueError("Invalid or missing form data.")

        subdomain_prefix = form_data.get("subdomain_prefix")
        if not subdomain_prefix:
            raise ValueError("Tenant subdomain_prefix is required for registration.")

        if Tenant.objects.filter(subdomain_prefix=subdomain_prefix).exists():
            raise ValueError(
                f"Tenant with subdomain_prefix '{subdomain_prefix}' already exists."
            )

        serializer = OwnerRegisterSerializer(data=form_data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user, tenant_data = serializer.save()

            tenant = tenant_service.create_tenant(
                owner_user=user,
                tenant_data=tenant_data
            )

        return user, tenant

    @staticmethod
    def register_employee(form_data: dict):
        if not form_data:
            raise ValueError("Invalid or missing form data.")

        subdomain_prefix = form_data.get("subdomain_prefix")

        if not subdomain_prefix:
            raise ValueError("Tenant subdomain_prefix is required for registration.")

        tenant = Tenant.objects.get(subdomain_prefix=subdomain_prefix)
        if not tenant:
            raise ValueError(
                f"Tenant with subdomain_prefix '{subdomain_prefix}' does not exists."
            )

        serializer = EmployeeRegisterSerializer(data=form_data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()

            TenantMembership.objects.create(
                user=user,
                company=tenant,
                role="employee"
            )

        return user


user_service = UserService()
