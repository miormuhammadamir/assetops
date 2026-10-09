"""Idempotent work order generation for calendar-based preventive maintenance."""
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import MaintenanceOccurrence, MaintenancePlan, WorkOrder, WorkOrderEvent


def generate_due_work_orders(*, as_of=None):
    """Create at most one occurrence per due plan per run.

    Each run advances the plan by one interval. Repeated runs catch up overdue
    schedules without skipping dates; the unique DB constraint is a final guard.
    Schedule this command from ONE worker in SQLite environments. PostgreSQL
    row locking supports concurrent workers; SQLite does not implement SELECT FOR UPDATE.
    """
    as_of = as_of or timezone.localdate()
    created_count = 0
    ids = list(MaintenancePlan.objects.filter(is_active=True, next_due__lte=as_of).values_list('pk', flat=True))
    for plan_id in ids:
        with transaction.atomic():
            plan = MaintenancePlan.objects.select_for_update().get(pk=plan_id)
            if not plan.is_active or plan.next_due > as_of:
                continue
            if not 1 <= plan.interval_days <= 3650:
                raise ValidationError(f'Invalid interval for maintenance plan {plan.pk}')
            due = plan.next_due
            if not MaintenanceOccurrence.objects.filter(plan=plan, scheduled_for=due).exists():
                order = WorkOrder.objects.create(
                    asset=plan.asset,
                    title=f'PM: {plan.title}',
                    description=plan.instructions,
                    priority=plan.priority,
                    created_by=plan.created_by,
                    assigned_to=plan.assigned_to,
                )
                MaintenanceOccurrence.objects.create(plan=plan, scheduled_for=due, work_order=order)
                WorkOrderEvent.objects.create(order=order, actor=plan.created_by, to_status=order.status, note=f'Scheduled maintenance due {due.isoformat()}')
                created_count += 1
            plan.next_due = due + timedelta(days=plan.interval_days)
            plan.save(update_fields=['next_due', 'updated_at'])
    return created_count
