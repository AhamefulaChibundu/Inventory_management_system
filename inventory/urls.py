from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    # Redirect root URL to login page
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Item management URLs
    path('item_list/', views.item_list, name='item_list'),
    path('<int:item_id>/', views.item_detail, name='item_detail'),
    path('create/', views.item_create, name='item_create'),
    path('<int:item_id>/edit/', views.item_update, name='item_update'),
    path('<int:item_id>/delete/', views.item_delete, name='item_delete'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('total_inventory_value/', views.total_inventory_value, name='total_inventory_value'),
    path('inventory_by_category/', views.inventory_by_category, name='inventory_by_category'),
    path('low_stock_notifications/', views.low_stock_notifications, name='low_stock_notifications'),
    path('expiry_notifications/', views.expiry_notifications, name='expiry_notifications'),
    path('record_sale/', views.record_sale, name='record_sale'),
    path('sales_history/', views.sales_history, name='sales_history'),
]
