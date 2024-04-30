from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='landing'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('login_authenticate', views.login_authenticate, name='login_authenticate'),
    path('register_user', views.user_register, name='user_register'),
    path('authenticate_user', views.authenticate_user, name='authenticate_user'),
    path('register_company', views.company_register, name='company_register'),
    path('authenticate_company', views.authenticate_company, name='authenticate_company'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('company_dashboard', views.company_dashboard, name='company_dashboard'),
    path('book', views.user_book, name='user_book'),
    path('new_location', views.new_location, name='new_location'),
    path('company_search', views.company_search, name='company_search'),
    path('all_orders', views.all_orders, name='all_orders'),
    path('pending_orders', views.pending_orders, name='pending_orders'),
    path('processing_orders', views.processing_orders, name='processing_orders'),
    path('successful_orders', views.processed_orders, name='processed_orders'),
    path('booked/<str:company_id>', views.successfully_booked, name='booked'),
    path('delete_destination/<str:dest_id>', views.delete_destination, name='delete_destination'),
    path('process_pending/<str:order_id>', views.process_pending, name='process_pending'),
    path('process_processing/<str:order_id>', views.process_processing, name='process_processing'),
]
