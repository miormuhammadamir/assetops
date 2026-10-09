from django.contrib import admin
from .models import Asset,WorkOrder,WorkOrderEvent,MaintenancePlan,MaintenanceOccurrence
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=['code','name','location','status','criticality','next_maintenance']
    search_fields=['code','name','location']
    list_filter=['status','criticality']
@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display=['id','title','asset','priority','status','assigned_to','created_at']
    list_filter=['status','priority']
    search_fields=['title','asset__code']
    readonly_fields=['created_at','updated_at','completed_at']
@admin.register(WorkOrderEvent)
class WorkOrderEventAdmin(admin.ModelAdmin):
    list_display=['order','actor','from_status','to_status','timestamp']
    def has_add_permission(self,request):return False
    def has_change_permission(self,request,obj=None):return False
    def has_delete_permission(self,request,obj=None):return False


@admin.register(MaintenancePlan)
class MaintenancePlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'asset', 'interval_days', 'next_due', 'is_active', 'assigned_to']
    list_filter = ['is_active', 'next_due']
    search_fields = ['title', 'asset__code']


@admin.register(MaintenanceOccurrence)
class MaintenanceOccurrenceAdmin(admin.ModelAdmin):
    list_display = ['plan', 'scheduled_for', 'work_order', 'created_at']
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
