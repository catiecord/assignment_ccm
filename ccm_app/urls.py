from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views. payment_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('user_management/', views.user_management, name='user_management'),
    path("user_active_status/<int:user_id>/", views.user_active_status,
         name="user_active_status", ),
    path("user_logs/", views.user_logs, name="user_logs"),
]
