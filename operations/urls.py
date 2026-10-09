from django.urls import path
from . import views
urlpatterns=[path('',views.dashboard,name='dashboard'),path('assets/',views.assets,name='assets'),path('assets/new/',views.asset_create,name='asset_create'),path('work-orders/',views.orders,name='orders'),path('work-orders/new/',views.order_create,name='order_create'),path('work-orders/<int:pk>/',views.order_detail,name='order_detail'),path('work-orders/<int:pk>/resolution/',views.order_resolution,name='order_resolution'),path('work-orders/<int:pk>/status/',views.order_status,name='order_status')]
