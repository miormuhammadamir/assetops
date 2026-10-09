from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
class Command(BaseCommand):
    help='Create application roles'
    def handle(self,*args,**kwargs):
        for name in ['Admin','Supervisor','Technician','Viewer']:
            Group.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Roles created'))
