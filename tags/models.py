from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="tags"
    )


class TicketTag(models.Model):
    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="ticket_tags"
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="tag_tickets"
    )

    class Meta:
        unique_together = ("ticket", "tag")
