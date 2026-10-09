from django.core.exceptions import ValidationError,PermissionDenied
from django.db import transaction
from django.utils import timezone
from .models import WorkOrder,WorkOrderEvent
from .permissions import has_role

ALLOWED={
    WorkOrder.Status.OPEN:{WorkOrder.Status.IN_PROGRESS,WorkOrder.Status.CANCELLED},
    WorkOrder.Status.IN_PROGRESS:{WorkOrder.Status.REVIEW,WorkOrder.Status.CANCELLED},
    WorkOrder.Status.REVIEW:{WorkOrder.Status.COMPLETED,WorkOrder.Status.IN_PROGRESS},
    WorkOrder.Status.COMPLETED:set(), WorkOrder.Status.CANCELLED:set(),
}
@transaction.atomic
def change_status(*,order_id,actor,target,note=''):
    order=WorkOrder.objects.select_for_update().get(pk=order_id)
    if target not in ALLOWED.get(order.status,set()):raise ValidationError('Invalid status transition')
    manager=has_role(actor,'Admin','Supervisor')
    assigned=order.assigned_to_id==actor.pk and has_role(actor,'Technician')
    if target in (WorkOrder.Status.COMPLETED,WorkOrder.Status.CANCELLED) and not manager:
        raise PermissionDenied('Only a manager may complete/cancel orders')
    if target in (WorkOrder.Status.IN_PROGRESS,WorkOrder.Status.REVIEW) and not (manager or assigned):
        raise PermissionDenied('Only assigned technician or manager may update work')
    if target==WorkOrder.Status.REVIEW and not order.resolution_notes.strip():
        raise ValidationError('Add resolution notes before requesting review')
    before=order.status;order.status=target
    order.completed_at=timezone.now() if target==WorkOrder.Status.COMPLETED else None
    order.save(update_fields=['status','completed_at','updated_at'])
    WorkOrderEvent.objects.create(order=order,actor=actor,from_status=before,to_status=target,note=note[:1000])
    return order
