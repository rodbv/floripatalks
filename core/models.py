# Create your models here.

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.choices import VoteChoices


class AppUser(AbstractUser):
    date_of_birth = models.DateField(_("Date of birth"), null=True, blank=True)
    linkedin_url = models.URLField(
        _("LinkedIn URL"), max_length=255, blank=True, null=True
    )
    avatar = models.URLField(_("Avatar URL"), max_length=500, blank=True, null=True)

    def __str__(self):
        return self.email or self.username


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Talk(BaseModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_by = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="talks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TalkVote(BaseModel):
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="votes")
    vote = models.IntegerField(_("Vote"), choices=VoteChoices.choices)

    def __str__(self):
        return f"{self.talk.title} - {self.user.username} - {'Up' if self.vote == VoteChoices.UP else 'Down'}"
