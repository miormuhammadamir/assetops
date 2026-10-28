from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Asset, MaintenancePlan, WorkOrder, WorkOrderEvent

class APIWorkflowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.supervisor = User.objects.create_user('boss_api', password='TestingSecret!345')
        self.tech = User.objects.create_user('tech_api', password='TestingSecret!345')
        self.viewer = User.objects.create_user('viewer_api', password='TestingSecret!345')
        for user, role in ((self.supervisor, 'Supervisor'), (self.tech, 'Technician'), (self.viewer, 'Viewer')):
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
        self.asset = Asset.objects.create(code='API-001', name='Pump', location='Plant A')
        self.order = WorkOrder.objects.create(asset=self.asset, title='Inspect', description='Noise',
                                              created_by=self.supervisor, assigned_to=self.tech)
        self.client = APIClient()

    def test_authentication_required(self):
        response = self.client.get('/api/v1/assets/')
        self.assertIn(response.status_code, (401, 403))

    def test_viewer_can_read_but_cannot_create_asset(self):
        self.client.force_authenticate(self.viewer)
        self.assertEqual(self.client.get('/api/v1/assets/').status_code, 200)
        response = self.client.post('/api/v1/assets/', {'code': 'NEW', 'name': 'x', 'location': 'A'})
        self.assertEqual(response.status_code, 403)

    def test_manager_creates_asset(self):
        self.client.force_authenticate(self.supervisor)
        response = self.client.post('/api/v1/assets/', {'code': 'NEW', 'name': 'Compressor', 'location': 'Plant B'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Asset.objects.filter(code='NEW').count(), 1)

    def test_technician_cannot_spoof_assignment(self):
        self.client.force_authenticate(self.tech)
        response = self.client.post('/api/v1/work-orders/', {
            'asset': self.asset.pk, 'title': 'New work', 'description': 'Inspection',
            'priority': 'low', 'assigned_to': self.supervisor.pk,
        })
        self.assertEqual(response.status_code, 201, response.data)
        created = WorkOrder.objects.get(title='New work')
        self.assertEqual(created.assigned_to, self.tech)
        self.assertEqual(WorkOrderEvent.objects.filter(order=created).count(), 1)

    def test_invalid_manager_assignee_rejected(self):
        self.client.force_authenticate(self.supervisor)
        response = self.client.post('/api/v1/work-orders/', {
            'asset': self.asset.pk, 'title': 'New work', 'description': 'Inspection',
            'assigned_to': self.viewer.pk,
        })
        self.assertEqual(response.status_code, 400)

    def test_status_transition_reuses_existing_security(self):
        self.client.force_authenticate(self.tech)
        url = f'/api/v1/work-orders/{self.order.pk}/transition/'
        self.assertEqual(self.client.post(url, {'status': 'completed'}).status_code, 400)
        self.assertEqual(self.client.post(url, {'status': 'in_progress'}).status_code, 200)
        self.assertEqual(self.client.post(f'/api/v1/work-orders/{self.order.pk}/resolution/',
                                          {'resolution_notes': 'Inspected'}).status_code, 200)
        self.assertEqual(self.client.post(url, {'status': 'review'}).status_code, 200)
        self.assertEqual(self.client.post(url, {'status': 'completed'}).status_code, 403)
        self.client.force_authenticate(self.supervisor)
        self.assertEqual(self.client.post(url, {'status': 'completed'}).status_code, 200)

    def test_viewer_cannot_change_resolution(self):
        self.client.force_authenticate(self.viewer)
        response = self.client.post(f'/api/v1/work-orders/{self.order.pk}/resolution/', {'resolution_notes': 'faked'})
        self.assertEqual(response.status_code, 403)

    def test_technician_cannot_edit_maintenance_plan(self):
        plan = MaintenancePlan.objects.create(asset=self.asset, title='Monthly', instructions='Clean',
            interval_days=30, next_due='2026-11-01', created_by=self.supervisor)
        self.client.force_authenticate(self.tech)
        self.assertEqual(self.client.patch(f'/api/v1/maintenance-plans/{plan.pk}/', {'is_active': False}, format='json').status_code, 403)

    def test_invalid_plan_interval(self):
        self.client.force_authenticate(self.supervisor)
        response = self.client.post('/api/v1/maintenance-plans/', {
            'asset': self.asset.pk, 'title': 'Invalid', 'instructions': 'Clean',
            'interval_days': 0, 'next_due': '2026-11-01',
        })
        self.assertEqual(response.status_code, 400)

    def test_session_authentication_enforces_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.supervisor)
        response = client.post('/api/v1/assets/', {'code': 'X', 'name': 'Test', 'location': 'Lab'})
        self.assertEqual(response.status_code, 403)

    def test_pagination(self):
        self.client.force_authenticate(self.viewer)
        response = self.client.get('/api/v1/assets/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
