from tenants.models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_prefix = request.headers.get("X-Tenant")

        if not tenant_prefix:
            host = request.get_host().split(":")[0]
            host_parts = host.split(".")

            if len(host_parts) > 1:
                tenant_prefix = host_parts[0]

        request.tenant = None

        if tenant_prefix:
            request.tenant = Tenant.objects.filter(subdomain_prefix=tenant_prefix).first()

        response = self.get_response(request)
        return response
