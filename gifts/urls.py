from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"), 
    path("process_gift", views.process_gift, name="process_gift"),
    path("process_payment", views.process_payment, name="process_payment"),
    path("payment_notification", views.payment_notification, name="payment_notification"),
]