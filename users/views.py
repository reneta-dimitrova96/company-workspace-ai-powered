from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services import user_service


class OwnerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Register an owner and return the created user and tenant."""
        try:
            user, tenant = user_service.register_owner(request.data)
        except ValueError as exc:
            return Response(
                {"message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "position": user.position,
                "tenant": tenant.company_name,
                "subdomain_prefix": tenant.subdomain_prefix,
            },
            status=status.HTTP_201_CREATED,
        )


class EmployeeRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = user_service.register_employee(request.data)
        except ValueError as exc:
            return Response(
                {"message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "position": user.position,
            },
            status=status.HTTP_201_CREATED,
        )
