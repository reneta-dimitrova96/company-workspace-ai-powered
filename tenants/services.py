from tenants.models import TenantMembership
from tenants.serializers import TenantSerializer


class TenantService:
    @staticmethod
    def create_tenant(owner_user, tenant_data: dict):
        if not owner_user or not tenant_data:
            raise Exception("Company initial data required")

        tenant_serializer = TenantSerializer(data=tenant_data)
        tenant_serializer.is_valid(raise_exception=True)

        tenant = tenant_serializer.save()

        TenantMembership.objects.create(
            user=owner_user,
            company=tenant,
            role="owner"
        )

        return tenant


tenant_service = TenantService()



