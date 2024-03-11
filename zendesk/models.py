from django.db import models
from django.utils import timezone
import datetime

# # Create your models here.
class AccessToken(models.Model):
    token = models.CharField(max_length=200)
    subdomain = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    last_fetch = models.DateTimeField(null=True)

    
    def __str__(self) -> str:
        return f"{self.subdomain} : token"

class Ticket(models.Model):
    # Fields that are not read-only or write-only can be directly mapped
    ticket_id = models.IntegerField()
    subdomain = models.CharField(max_length=50
    )
    assignee_id = models.IntegerField(null=True, blank=True)  # Nullable since it's not mandatory
    assignee_email = models.EmailField(max_length=255, blank=True)  # Write-only in API, might not need to store
    attribute_value_ids = models.JSONField(default=list, blank=True)  # Array, write-only
    brand_id = models.IntegerField(null=True, blank=True)  # Nullable for non-Enterprise
    collaborator_ids = models.JSONField(default=list, blank=True)  # Array
    collaborators = models.JSONField(default=list, blank=True)  # Array, POST requests only
    comment = models.JSONField(default=dict, blank=True)  # Object, write-only
    created_at = models.DateTimeField(default=timezone.now)  # Auto set on creation
    custom_fields = models.JSONField(default=list, blank=True)  # Array
    custom_status_id = models.IntegerField(null=True, blank=True)  # Nullable
    description = models.TextField(blank=True)  # Read-only, use comment for creation
    due_at = models.DateTimeField(null=True, blank=True)  # Nullable
    email_cc_ids = models.JSONField(default=list, blank=True)  # Array
    email_ccs = models.JSONField(default=list, blank=True)  # Array, write-only
    external_id = models.CharField(max_length=255, null=True, blank=True)  # Nullable
    follower_ids = models.JSONField(default=list, blank=True)  # Array
    followers = models.JSONField(default=list, blank=True)  # Array, write-only
    group_id = models.IntegerField(null=True, blank=True)  # Nullable
    organization_id = models.IntegerField(null=True, blank=True)  # Nullable
    priority = models.CharField(max_length=50, null=True, blank=True)  # Nullable
    problem_id = models.IntegerField(null=True, blank=True)  # Nullable
    raw_subject = models.CharField(max_length=255, blank=True)  # Nullable
    recipient = models.EmailField(max_length=255, null=True, blank=True)  # Nullable
    requester_id = models.IntegerField()  # Mandatory
    safe_update = models.BooleanField(default=False)  # Write-only, optional
    satisfaction_rating = models.JSONField(default=dict, null=True,blank=True)  # Object, read-only
    status = models.CharField(max_length=50)  # Not nullable as it's a mandatory field with default value
    subject = models.CharField(max_length=255)  # Mandatory
    submitter_id = models.IntegerField(null=True, blank=True)  # Nullable
    tags = models.JSONField(default=list, blank=True)  # Array
    ticket_form_id = models.IntegerField(null=True, blank=True)  # Nullable for non-Enterprise
    type = models.CharField(max_length=50, null=True, blank=True)  # Nullable
    updated_at = models.DateTimeField(auto_now=True)  # Auto updated on save
    updated_stamp = models.DateTimeField(null=True, blank=True)  # Write-only, for safe updates
    url = models.URLField(max_length=200, blank=True)  # Read-only
    via = models.JSONField(default=dict, blank=True)  # Object
    via_followup_source_id = models.IntegerField(null=True, blank=True)  # POST requests only, nullable
    via_id = models.IntegerField(null=True, blank=True)  # Write-only
    voice_comment = models.JSONField(default=dict, blank=True)  # Object, write-only

    class Meta:
        unique_together = (('ticket_id', 'subdomain'),)
    

class DailyTicketCount(models.Model):
    subdomain = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    ticket_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.subdomain} - {self.date}: {self.ticket_count} tickets"

    class Meta:
        unique_together = (('subdomain', 'date'),)
        ordering = ['-date']
