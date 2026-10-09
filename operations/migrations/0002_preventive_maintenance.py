from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('operations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='MaintenancePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('instructions', models.TextField()),
                ('interval_days', models.PositiveIntegerField()),
                ('next_due', models.DateField(db_index=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='maintenance_plans', to='operations.asset')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='maintenance_plans', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_maintenance_plans', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['next_due', 'id']},
        ),
        migrations.CreateModel(
            name='MaintenanceOccurrence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_for', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='occurrences', to='operations.maintenanceplan')),
                ('work_order', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='maintenance_occurrence', to='operations.workorder')),
            ],
            options={'ordering': ['-scheduled_for']},
        ),
        migrations.AddConstraint(
            model_name='maintenanceoccurrence',
            constraint=models.UniqueConstraint(fields=('plan', 'scheduled_for'), name='unique_maintenance_plan_due_date'),
        ),
    ]
