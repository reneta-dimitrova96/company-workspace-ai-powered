from django.db import models

from api import settings


class Idea(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    company = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="ideas"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_ideas"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)


class IdeaVote(models.Model):
    VOTE_CHOICES = [
        (1, "Upvote"),
        (-1, "Downvote"),
    ]

    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="idea_votes"
    )
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("idea", "user")

