# Initial schema generated for the AssetOps MVP.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Asset', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('code',models.CharField(max_length=40,unique=True)),
            ('name',models.CharField(max_length=160)),
            ('location',models.CharField(max_length=160)),
            ('description',models.TextField(blank=True)),
            ('status',models.CharField(choices=[('operational','Operational'),('maintenance','Under maintenance'),('out_of_service','Out of service')],db_index=True,default='operational',max_length=24)),
            ('criticality',models.CharField(choices=[('low','Low'),('medium','Medium'),('high','High')],default='medium',max_length=12)),
            ('next_maintenance',models.DateField(blank=True,db_index=True,null=True)),
            ('created_at',models.DateTimeField(auto_now_add=True)),
            ('updated_at',models.DateTimeField(auto_now=True)),
        ],options={'ordering':['code']}),
        migrations.CreateModel(name='WorkOrder',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('title',models.CharField(max_length=180)),
            ('description',models.TextField()),
            ('priority',models.CharField(choices=[('low','Low'),('medium','Medium'),('high','High'),('urgent','Urgent')],default='medium',max_length=12)),
            ('status',models.CharField(choices=[('open','Open'),('in_progress','In progress'),('review','Awaiting review'),('completed','Completed'),('cancelled','Cancelled')],db_index=True,default='open',max_length=20)),
            ('resolution_notes',models.TextField(blank=True)),
            ('created_at',models.DateTimeField(auto_now_add=True)),
            ('updated_at',models.DateTimeField(auto_now=True)),
            ('completed_at',models.DateTimeField(blank=True,null=True)),
            ('asset',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='work_orders',to='operations.asset')),
            ('assigned_to',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,related_name='assigned_work_orders',to=settings.AUTH_USER_MODEL)),
            ('created_by',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='created_work_orders',to=settings.AUTH_USER_MODEL)),
        ],options={'ordering':['-created_at']}),
        migrations.CreateModel(name='WorkOrderEvent',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('from_status',models.CharField(blank=True,max_length=20)),
            ('to_status',models.CharField(max_length=20)),
            ('note',models.TextField(blank=True)),
            ('timestamp',models.DateTimeField(auto_now_add=True)),
            ('actor',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to=settings.AUTH_USER_MODEL)),
            ('order',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='events',to='operations.workorder')),
        ],options={'ordering':['-timestamp']}),
        migrations.AddIndex(model_name='workorder',index=models.Index(fields=['status','priority'],name='operations__status_33d17f_idx')),
    ]
