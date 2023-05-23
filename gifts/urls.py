from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"), 
    path("process_gift", views.process_gift, name="process_gift"),
    path("process_card", views.process_card, name="process_card"),
    path("process_mpesa", views.process_mpesa, name="process_mpesa"),
    path("error", views.error505, name="error505"),
    path("payment_notification", views.payment_notification, name="payment_notification"),
    path("mpesa_notification", views.mpesa_notification, name="mpesa_notification"),
    path("gift_processed", views.gift_processed, name="gift_processed"),
    path("gift_message", views.gift_message, name="gift_message")
]

