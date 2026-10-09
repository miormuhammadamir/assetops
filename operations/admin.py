from django.contrib import admin
from .models import Asset,WorkOrder,WorkOrderEvent
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
