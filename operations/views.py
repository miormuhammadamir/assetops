from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import AssetForm,WorkOrderForm,ResolutionForm
from .models import Asset,WorkOrder,WorkOrderEvent,MaintenancePlan
from .permissions import roles_required,has_role
from .services import change_status,ALLOWED

@login_required
def dashboard(request):
    return render(request,'operations/dashboard.html',{
        'asset_count':Asset.objects.count(),
        'plan_count':MaintenancePlan.objects.filter(is_active=True).count(),
        'overdue_plan_count':MaintenancePlan.objects.filter(is_active=True,next_due__lt=timezone.localdate()).count(),
        'open_count':WorkOrder.objects.exclude(status__in=['completed','cancelled']).count(),
        'high_count':WorkOrder.objects.filter(priority__in=['high','urgent']).exclude(status__in=['completed','cancelled']).count(),
        'recent':WorkOrder.objects.select_related('asset','assigned_to')[:8],
    })
@login_required
def assets(request):
    q=request.GET.get('q','').strip()[:100]
    records=Asset.objects.all()
    if q:records=records.filter(Q(code__icontains=q)|Q(name__icontains=q)|Q(location__icontains=q))
    return render(request,'operations/assets.html',{'records':records[:100],'q':q})
@roles_required('Admin','Supervisor')
def asset_create(request):
    form=AssetForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save();messages.success(request,'Asset added');return redirect('assets')
    return render(request,'operations/form.html',{'form':form,'heading':'Register asset'})
@login_required
def orders(request):
    records=WorkOrder.objects.select_related('asset','assigned_to','created_by')
    status=request.GET.get('status','')
    if status in WorkOrder.Status.values: records=records.filter(status=status)
    return render(request,'operations/orders.html',{'records':records[:100],'status':status,'statuses':WorkOrder.Status.choices})
@roles_required('Admin','Supervisor','Technician')
def order_create(request):
    form = WorkOrderForm(request.POST or None)
    is_technician = has_role(request.user, 'Technician') and not has_role(request.user, 'Admin', 'Supervisor')
    if is_technician:
        form.fields.pop('assigned_to', None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        if is_technician:
            obj.assigned_to = request.user
        obj.save()
        WorkOrderEvent.objects.create(order=obj, actor=request.user, to_status=obj.status, note='Created')
        messages.success(request, 'Work order created')
        return redirect('order_detail', pk=obj.pk)
    return render(request, 'operations/form.html', {'form': form, 'heading': 'Create work order'})
@login_required
def order_detail(request,pk):
    order=get_object_or_404(WorkOrder.objects.select_related('asset','assigned_to','created_by'),pk=pk)
    can_manage=has_role(request.user,'Admin','Supervisor')
    can_work=can_manage or (has_role(request.user,'Technician') and order.assigned_to_id==request.user.pk)
    choices=[(status,label) for status,label in WorkOrder.Status.choices if status in ALLOWED[order.status] and ((can_manage) or status not in ('completed','cancelled') and can_work)]
    return render(request,'operations/detail.html',{'order':order,'events':order.events.select_related('actor'),'choices':choices,'can_work':can_work,'resolution_form':ResolutionForm(instance=order)})
@require_POST
@roles_required('Admin','Supervisor','Technician')
def order_resolution(request,pk):
    order=get_object_or_404(WorkOrder,pk=pk)
    if not (has_role(request.user,'Admin','Supervisor') or order.assigned_to_id==request.user.pk and has_role(request.user,'Technician')):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()
    if order.status in ('completed','cancelled'):
        messages.error(request,'Closed work orders cannot be edited')
    else:
        form=ResolutionForm(request.POST,instance=order)
        if form.is_valid():form.save();messages.success(request,'Resolution notes saved')
    return redirect('order_detail',pk=pk)
@require_POST
@roles_required('Admin','Supervisor','Technician')
def order_status(request,pk):
    try:
        change_status(order_id=pk,actor=request.user,target=request.POST.get('status',''),note=request.POST.get('note',''))
        messages.success(request,'Work order updated')
    except ValidationError as exc:messages.error(request,'; '.join(exc.messages))
    return redirect('order_detail',pk=pk)
