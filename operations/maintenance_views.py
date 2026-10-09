from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone

from .maintenance_forms import MaintenancePlanForm
from .models import MaintenancePlan
from .permissions import roles_required, has_role


@login_required
def plan_list(request):
    plans = MaintenancePlan.objects.select_related('asset', 'assigned_to').all()[:200]
    return render(request, 'operations/maintenance_plans.html', {
        'plans': plans,
        'today': timezone.localdate(),
        'can_manage': has_role(request.user, 'Admin', 'Supervisor'),
    })


@roles_required('Admin', 'Supervisor')
def plan_create(request):
    form = MaintenancePlanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        plan = form.save(commit=False)
        plan.created_by = request.user
        plan.save()
        messages.success(request, 'Maintenance plan created')
        return redirect('maintenance_plans')
    return render(request, 'operations/form.html', {'form': form, 'heading': 'New preventive maintenance plan'})


@require_POST
@roles_required('Admin', 'Supervisor')
def plan_toggle(request, pk):
    plan = get_object_or_404(MaintenancePlan, pk=pk)
    plan.is_active = not plan.is_active
    plan.save(update_fields=['is_active', 'updated_at'])
    messages.success(request, 'Maintenance plan status updated')
    return redirect('maintenance_plans')
