from django.urls import path 
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('superadmin_dashboard',views.superadmin_dashboard, name='superadmin_dashboard'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('logout', views.logout, name='logout'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('approval/', views.approval, name='approval'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('delete_notapproved_user/<int:user_id>/', views.delete_notapproved_user, name='delete_notapproved_user'),
    path('add_admin', views.add_admin, name='add_admin'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),

    
]