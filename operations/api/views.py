from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from operations.models import Asset, MaintenancePlan, WorkOrder, WorkOrderEvent
from operations.permissions import has_role
from operations.services import change_status
from .permissions import ManagerWritePermission, WorkOrderPermission
from .serializers import (
    AssetSerializer, MaintenancePlanSerializer, ResolutionSerializer,
    StatusTransitionSerializer, WorkOrderSerializer,
)

def filtered_choice(queryset, key, value, choices):
    if value is None:
        return queryset
    if value not in choices:
        raise ValidationError({key: 'Invalid filter value.'})
    return queryset.filter(**{key: value})

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [ManagerWritePermission]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('search', '').strip()[:100]
        if q:
            qs = qs.filter(Q(code__icontains=q) | Q(name__icontains=q) | Q(location__icontains=q))
        return filtered_choice(qs, 'status', self.request.query_params.get('status'), Asset.Status.values)

class MaintenancePlanViewSet(viewsets.ModelViewSet):
    queryset = MaintenancePlan.objects.select_related('asset', 'assigned_to')
    serializer_class = MaintenancePlanSerializer
    permission_classes = [ManagerWritePermission]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        active = self.request.query_params.get('active')
        if active is not None:
            if active not in ('true', 'false'):
                raise ValidationError({'active': 'Use true or false.'})
            qs = qs.filter(is_active=(active == 'true'))
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.select_related('asset', 'assigned_to', 'created_by')
    serializer_class = WorkOrderSerializer
    permission_classes = [WorkOrderPermission]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = filtered_choice(qs, 'status', self.request.query_params.get('status'), WorkOrder.Status.values)
        return filtered_choice(qs, 'priority', self.request.query_params.get('priority'), WorkOrder.Priority.values)

    @transaction.atomic
    def perform_create(self, serializer):
        order = serializer.save(created_by=self.request.user)
        WorkOrderEvent.objects.create(order=order, actor=self.request.user,
                                      to_status=order.status, note='Created via API')

    @action(detail=True, methods=['post'], url_path='transition')
    def transition(self, request, pk=None):
        serializer = StatusTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.get_object()
        try:
            order = change_status(order_id=pk, actor=request.user,
                                  target=serializer.validated_data['status'],
                                  note=serializer.validated_data.get('note', ''))
        except DjangoPermissionDenied as exc:
            raise PermissionDenied(str(exc)) from exc
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(self.get_serializer(order).data)

    @action(detail=True, methods=['post'], url_path='resolution')
    def resolution(self, request, pk=None):
        serializer = ResolutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            order = WorkOrder.objects.select_for_update().get(pk=self.get_object().pk)
            manager = has_role(request.user, 'Admin', 'Supervisor')
            assigned = has_role(request.user, 'Technician') and order.assigned_to_id == request.user.pk
            if not (manager or assigned):
                raise PermissionDenied('Only a manager or assigned technician may edit resolution notes.')
            if order.status in (WorkOrder.Status.COMPLETED, WorkOrder.Status.CANCELLED):
                raise ValidationError('Closed work orders cannot be edited.')
            order.resolution_notes = serializer.validated_data['resolution_notes']
            order.save(update_fields=['resolution_notes', 'updated_at'])
        return Response(self.get_serializer(order).data)
