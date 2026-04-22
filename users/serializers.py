from rest_framework import serializers

from users.models import User


class OwnerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    subdomain_prefix = serializers.CharField()
    size = serializers.CharField()
    field = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "position",
            "name",
            "subdomain_prefix",
            "size",
            "field",
        ]

    def create(self, validated_data):
        tenant_data = {
            "name": validated_data.pop("name"),
            "subdomain_prefix": validated_data.pop("subdomain_prefix"),
            "size": validated_data.pop("size"),
            "field": validated_data.pop("field"),
        }

        user = User.objects.create_user(**validated_data)
        return user, tenant_data


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "position",
        ]
