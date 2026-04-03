from django.db import models

from api import settings


class AILog(models.Model):
    CONTEXT_CHOICES = [
        ("ticket", "Ticket"),
        ("idea", "Idea"),
        ("general", "General"),
    ]

    company = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="ai_logs"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_logs"
    )
    context_type = models.CharField(max_length=20, choices=CONTEXT_CHOICES)
    context_id = models.IntegerField(null=True, blank=True)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

