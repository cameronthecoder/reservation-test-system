from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-session', views.create_session, name='create_session'),
    path('success', views.payment_success, name='payment_success'),
    path('webhook', views.my_webhook_view, name='webhook'),
    path('check-availability', views.check_availability, name="check_availability")
]