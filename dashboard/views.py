from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import Order

# Create your views here.
@login_required
def dashboard(request):
    orders = Order.objects.all().order_by('-ordered_at')
    context = {
        'orders': orders,
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
        'preparing_orders': orders.filter(status='preparing').count(),
    }
    return render(request, 'dashboard/index.html', context)