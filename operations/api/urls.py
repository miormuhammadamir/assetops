from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, MaintenancePlanViewSet, WorkOrderViewSet

router = DefaultRouter()
router.register('assets', AssetViewSet, basename='api-assets')
router.register('work-orders', WorkOrderViewSet, basename='api-work-orders')
router.register('maintenance-plans', MaintenancePlanViewSet, basename='api-maintenance-plans')
urlpatterns = [path('', include(router.urls))]
