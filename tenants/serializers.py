from rest_framework import serializers

from tenants.models import Tenant, TenantMembership


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class TenantMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantMembership
        fields = '__all__'
