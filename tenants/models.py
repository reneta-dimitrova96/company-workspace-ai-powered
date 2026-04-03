from django.db import models

from api import settings


class Tenant(models.Model):
    SIZE_CHOICES = [
        ("micro", "Micro (1-10)"),
        ("small", "Small (11-50)"),
        ("medium", "Medium (51-250)"),
        ("large", "Large (250+)"),
    ]

    FIELD_CHOICES = [
        ("it", "IT"),
        ("finance", "Finance"),
        ("trade", "Trade"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("manufacturing", "Manufacturing"),
        ("marketing", "Marketing"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255)
    subdomain_prefix = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    field = models.CharField(max_length=20, choices=FIELD_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)


class TenantMembership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("employee", "Employee"),
    ]
    user = models.OneToOneField(
         settings.AUTH_USER_MODEL,
         on_delete=models.CASCADE,
         related_name="membership"
    )
    company = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)
