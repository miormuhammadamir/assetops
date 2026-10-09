from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError,PermissionDenied
from django.test import TestCase
from django.urls import reverse
from .models import Asset,WorkOrder,WorkOrderEvent
from .services import change_status
class WorkflowTests(TestCase):
    def setUp(self):
        User=get_user_model()
        self.tech=User.objects.create_user('tech',password='LongTestPassword!12')
        self.supervisor=User.objects.create_user('boss',password='LongTestPassword!12')
        self.viewer=User.objects.create_user('viewer',password='LongTestPassword!12')
        self.tech.groups.add(Group.objects.create(name='Technician'))
        self.supervisor.groups.add(Group.objects.create(name='Supervisor'))
        self.viewer.groups.add(Group.objects.create(name='Viewer'))
        self.asset=Asset.objects.create(code='PMP-001',name='Pump',location='Plant A')
        self.order=WorkOrder.objects.create(asset=self.asset,title='Inspect pump',description='Noise',created_by=self.supervisor,assigned_to=self.tech)
    def test_login_required(self):
        self.assertEqual(self.client.get(reverse('assets')).status_code,302)
    def test_viewer_cannot_create_asset(self):
        self.client.force_login(self.viewer)
        self.assertEqual(self.client.post(reverse('asset_create'),{'code':'X'}).status_code,403)
    def test_assigned_technician_can_progress(self):
        change_status(order_id=self.order.pk,actor=self.tech,target='in_progress')
        self.order.refresh_from_db();self.assertEqual(self.order.status,'in_progress')
    def test_cannot_skip_to_complete(self):
        with self.assertRaises(ValidationError):change_status(order_id=self.order.pk,actor=self.supervisor,target='completed')
    def test_technician_cannot_approve(self):
        change_status(order_id=self.order.pk,actor=self.tech,target='in_progress')
        self.order.resolution_notes='Inspected';self.order.save(update_fields=['resolution_notes'])
        change_status(order_id=self.order.pk,actor=self.tech,target='review')
        with self.assertRaises(PermissionDenied):change_status(order_id=self.order.pk,actor=self.tech,target='completed')
        change_status(order_id=self.order.pk,actor=self.supervisor,target='completed')
        self.assertEqual(WorkOrderEvent.objects.filter(order=self.order).count(),3)
    def test_post_only_status(self):
        self.client.force_login(self.supervisor)
        self.assertEqual(self.client.get(reverse('order_status',args=[self.order.pk])).status_code,405)
    def test_technician_assignment_cannot_be_spoofed(self):
        self.client.force_login(self.tech)
        other=get_user_model().objects.create_user('other',password='LongTestPassword!12')
        self.client.post(reverse('order_create'),{'asset':self.asset.pk,'title':'New work','description':'Fix','priority':'low','assigned_to':other.pk})
        self.assertEqual(WorkOrder.objects.get(title='New work').assigned_to,self.tech)
