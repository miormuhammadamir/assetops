from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .maintenance_services import generate_due_work_orders
from .models import Asset, MaintenanceOccurrence, MaintenancePlan, WorkOrder, WorkOrderEvent


class MaintenancePlanTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.supervisor = User.objects.create_user(username='pm-supervisor', password='TestPassword!123')
        self.technician = User.objects.create_user(username='pm-tech', password='TestPassword!123')
        self.viewer = User.objects.create_user(username='pm-viewer', password='TestPassword!123')
        self.supervisor.groups.add(Group.objects.create(name='Supervisor'))
        self.technician.groups.add(Group.objects.create(name='Technician'))
        self.viewer.groups.add(Group.objects.create(name='Viewer'))
        self.asset = Asset.objects.create(code='PM-PUMP', name='Pump', location='Plant A')
        self.due = date(2026, 10, 1)
        self.plan = MaintenancePlan.objects.create(
            asset=self.asset, title='Monthly inspection', instructions='Inspect seals and bearings',
            interval_days=30, next_due=self.due, created_by=self.supervisor,
            assigned_to=self.technician,
        )

    def test_due_plan_generates_work_order_and_audit_event(self):
        self.assertEqual(generate_due_work_orders(as_of=self.due), 1)
        occurrence = MaintenanceOccurrence.objects.get(plan=self.plan)
        self.assertEqual(occurrence.scheduled_for, self.due)
        self.assertEqual(occurrence.work_order.asset, self.asset)
        self.assertEqual(occurrence.work_order.assigned_to, self.technician)
        self.assertEqual(occurrence.work_order.created_by, self.supervisor)
        self.assertEqual(WorkOrderEvent.objects.filter(order=occurrence.work_order).count(), 1)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.next_due, self.due + timedelta(days=30))

    def test_rerunning_for_same_date_does_not_duplicate(self):
        self.assertEqual(generate_due_work_orders(as_of=self.due), 1)
        self.assertEqual(generate_due_work_orders(as_of=self.due), 0)
        self.assertEqual(WorkOrder.objects.count(), 1)

    def test_catches_up_one_interval_per_run(self):
        self.assertEqual(generate_due_work_orders(as_of=date(2026, 12, 1)), 1)
        self.assertEqual(generate_due_work_orders(as_of=date(2026, 12, 1)), 1)
        self.assertEqual(generate_due_work_orders(as_of=date(2026, 12, 1)), 1)
        self.assertEqual(generate_due_work_orders(as_of=date(2026, 12, 1)), 0)
        self.assertEqual(WorkOrder.objects.count(), 3)

    def test_paused_plan_is_not_scheduled(self):
        self.plan.is_active = False
        self.plan.save(update_fields=['is_active'])
        self.assertEqual(generate_due_work_orders(as_of=self.due), 0)

    def test_unique_constraint_prevents_duplicate_occurrence(self):
        generate_due_work_orders(as_of=self.due)
        with self.assertRaises(IntegrityError):
            with self.connection_transaction():
                MaintenanceOccurrence.objects.create(
                    plan=self.plan, scheduled_for=self.due,
                    work_order=WorkOrder.objects.create(
                        asset=self.asset, title='Other', description='Other', created_by=self.supervisor,
                    ),
                )

    @staticmethod
    def connection_transaction():
        from django.db import transaction
        return transaction.atomic()

    def test_viewer_cannot_create_plan(self):
        self.client.force_login(self.viewer)
        response = self.client.post(reverse('maintenance_plan_create'), {
            'asset': self.asset.pk, 'title': 'New', 'instructions': 'Check',
            'interval_days': 7, 'next_due': self.due.isoformat(), 'priority': 'low',
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(MaintenancePlan.objects.count(), 1)

    def test_technician_cannot_pause_plan(self):
        self.client.force_login(self.technician)
        response = self.client.post(reverse('maintenance_plan_toggle', args=[self.plan.pk]))
        self.assertEqual(response.status_code, 403)

    def test_supervisor_can_pause_plan(self):
        self.client.force_login(self.supervisor)
        response = self.client.post(reverse('maintenance_plan_toggle', args=[self.plan.pk]))
        self.assertEqual(response.status_code, 302)
        self.plan.refresh_from_db()
        self.assertFalse(self.plan.is_active)

    def test_supervisor_can_create_plan(self):
        self.client.force_login(self.supervisor)
        response = self.client.post(reverse('maintenance_plan_create'), {
            'asset': self.asset.pk, 'title': 'Weekly check', 'instructions': 'Check oil',
            'interval_days': 7, 'next_due': self.due.isoformat(), 'priority': 'high',
            'assigned_to': self.technician.pk, 'is_active': 'on',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MaintenancePlan.objects.count(), 2)

    def test_invalid_interval_is_rejected_by_form(self):
        self.client.force_login(self.supervisor)
        response = self.client.post(reverse('maintenance_plan_create'), {
            'asset': self.asset.pk, 'title': 'Bad', 'instructions': 'Bad interval',
            'interval_days': 0, 'next_due': self.due.isoformat(), 'priority': 'high',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MaintenancePlan.objects.count(), 1)

    def test_command_accepts_date(self):
        call_command('generate_maintenance', date=self.due.isoformat())
        self.assertEqual(MaintenanceOccurrence.objects.count(), 1)
