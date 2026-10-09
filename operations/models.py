from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Asset(models.Model):
    class Status(models.TextChoices):
        OPERATIONAL='operational','Operational'
        MAINTENANCE='maintenance','Under maintenance'
        OUT_OF_SERVICE='out_of_service','Out of service'
    class Criticality(models.TextChoices):
        LOW='low','Low'
        MEDIUM='medium','Medium'
        HIGH='high','High'
    code=models.CharField(max_length=40,unique=True)
    name=models.CharField(max_length=160)
    location=models.CharField(max_length=160)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=24,choices=Status.choices,default=Status.OPERATIONAL,db_index=True)
    criticality=models.CharField(max_length=12,choices=Criticality.choices,default=Criticality.MEDIUM)
    next_maintenance=models.DateField(null=True,blank=True,db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['code']
    def __str__(self):return f'{self.code} — {self.name}'

class WorkOrder(models.Model):
    class Priority(models.TextChoices):
        LOW='low','Low'
        MEDIUM='medium','Medium'
        HIGH='high','High'
        URGENT='urgent','Urgent'
    class Status(models.TextChoices):
        OPEN='open','Open'
        IN_PROGRESS='in_progress','In progress'
        REVIEW='review','Awaiting review'
        COMPLETED='completed','Completed'
        CANCELLED='cancelled','Cancelled'
    asset=models.ForeignKey(Asset,on_delete=models.PROTECT,related_name='work_orders')
    title=models.CharField(max_length=180)
    description=models.TextField()
    priority=models.CharField(max_length=12,choices=Priority.choices,default=Priority.MEDIUM)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN,db_index=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='created_work_orders')
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='assigned_work_orders',null=True,blank=True)
    resolution_notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    class Meta:
        ordering=['-created_at']
        indexes=[models.Index(fields=['status','priority'])]
    def __str__(self):return f'WO-{self.pk}: {self.title}'

class WorkOrderEvent(models.Model):
    order=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,related_name='events')
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    from_status=models.CharField(max_length=20,blank=True)
    to_status=models.CharField(max_length=20)
    note=models.TextField(blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-timestamp']


class MaintenancePlan(models.Model):
    """Recurring calendar-based maintenance; each plan represents one activity."""

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='maintenance_plans')
    title = models.CharField(max_length=180)
    instructions = models.TextField()
    interval_days = models.PositiveIntegerField()
    next_due = models.DateField(db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    priority = models.CharField(max_length=12, choices=WorkOrder.Priority.choices, default=WorkOrder.Priority.MEDIUM)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
        related_name='maintenance_plans',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_maintenance_plans',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_due', 'id']

    def clean(self):
        super().clean()
        if self.interval_days is not None and not 1 <= self.interval_days <= 3650:
            raise ValidationError({'interval_days': 'Interval must be between 1 and 3650 days.'})

    def __str__(self):
        return f'{self.asset.code}: {self.title}'


class MaintenanceOccurrence(models.Model):
    """One scheduled work order per plan and due date."""

    plan = models.ForeignKey(MaintenancePlan, on_delete=models.PROTECT, related_name='occurrences')
    scheduled_for = models.DateField()
    work_order = models.OneToOneField(
        WorkOrder, on_delete=models.PROTECT, related_name='maintenance_occurrence',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_for']
        constraints = [
            models.UniqueConstraint(fields=['plan', 'scheduled_for'], name='unique_maintenance_plan_due_date'),
        ]

    def __str__(self):
        return f'{self.plan_id} due {self.scheduled_for}'
