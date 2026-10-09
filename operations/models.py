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
