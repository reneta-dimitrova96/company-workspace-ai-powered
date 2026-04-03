from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tenants.models import TenantMembership
from users.serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.tenant:
            return Response({"detail": "Invalid tenant."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        TenantMembership.objects.create(
            user=user,
            company=request.tenant,
            role="employee"
        )

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "position": user.position,
                "tenant": request.tenant.name
            },
            status=status.HTTP_201_CREATED,
        )
