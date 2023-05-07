from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests, json, random
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "gifts/index.html")
    elif request.method == "POST":
        pass
    

def process_payment(request):
    if request.method == "POST":
        customer_fname = request.POST["fname"]
        customer_lname = request.POST["lname"]
        customer_phone = request.POST["phone"]
        customer_email = request.POST["email"]
        message = request.POST["message"]
        print("Message to the couple: ",message)
        constribution_amount = request.POST["amount"]

        gift_object = Gift(
            first_name = customer_fname,
            last_name = customer_lname,
            phone_no = customer_phone,
            email = customer_email,
            amount =  constribution_amount,
            message = message
        )
        gift_object.save()

        request_response = generate_authentication_token()

        if request_response['status'] == '200':
            authentication_token = request_response['token']
            # print("Authentication token: ",authentication_token)

            authorization_token = "Bearer {}".format(authentication_token)

            ipn_registration_header = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Content-Type": "application/json",
                "Authorization": authorization_token
            }

            ipn_registration_body = {
                "url": "https://3d54-41-90-64-81.ngrok-free.app/payment_notification",
                "ipn_notification_type": "POST"
            }

            ipn_registration =requests.post(settings.PESAPAL_IPN_REGISTRATION_URL,headers = ipn_registration_header, data=json.dumps(ipn_registration_body)).json()
            print("IPN regsitration response: ",ipn_registration)

            ipn_id = ipn_registration["ipn_id"]
            gift_object.ipn_id = ipn_id
            gift_object.save()

            # print("IPN registration id: ",ipn_id)

            order_request_customer_address = {
                "first_name": customer_fname,
                "last_name": customer_lname,
                "email_address": customer_email,
                "phone_number": customer_phone
            }

            unique_id = gift_object.id + 498656259
            print("Unique order id: ",unique_id)

            order_request_payload = {
                "id": unique_id ,
                "currency": "KES",
                "amount": constribution_amount,
                "description": "Elizabeth weds George",
                "callback_url": "https://3d54-41-90-64-81.ngrok-free.app",
                "notification_id": ipn_id,
                "billing_address": order_request_customer_address
            }

            order_request_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": authorization_token
            }

            order_request = requests.post(settings.PESAPAL_ORDER_REQUEST_URL,headers = order_request_headers, data=json.dumps(order_request_payload)).json()
            

            print("--------------------------------------------------------------------------------------------------------------------------------------")
            print("Order request response: ",order_request)
            print("--------------------------------------------------------------------------------------------------------------------------------------")
            redirect_url = order_request['redirect_url']
            order_tracking_id = order_request['order_tracking_id']

            gift_object.order_tracking_id = order_tracking_id
            gift_object.save()

            context = {"redirect_url": redirect_url }
            return render(request, "gifts/processing_payments.html",context)
    else:
        pass

@csrf_exempt
def payment_notification(request):
    payment_response = json.loads(request.body)
    payment_order_tracking_id = payment_response['OrderTrackingId']
    print("Payment notification: ",payment_response)

    #----Check payment------
    request_response = generate_authentication_token()
    authentication_token = request_response['token']

    pesapal_get_transaction_status_url = settings.PESAPAL_GET_TRANSACTION_STATUS_URL

    transaction_status_header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": authentication_token
    }

    get_transaction_status_params = {
        "orderTrackingId": payment_order_tracking_id
    }

    transaction_response =  requests.get(
        pesapal_get_transaction_status_url,
        params = get_transaction_status_params, 
        headers= transaction_status_header
    ).json()

    print("Check Transaction status response: ",transaction_response)

    gift_object = Gift.objects.get(order_tracking_id=payment_order_tracking_id)

    gift_object.payment_method = transaction_response["payment_method"]
    gift_object.amount = transaction_response["amount"]
    gift_object.currency = transaction_response["currency"]

    payment_status_description = transaction_response["payment_status_description"]

    if payment_status_description == "Completed":
        gift_object.status = 4
    elif payment_status_description == "Failed":
        gift_object.status = 2

    gift_object.save()

    print("Transaction status response: ",transaction_response)

    return redirect('index')


def generate_authentication_token():
    pesapal_authentication_url = settings.PESAPAL_AUTHENTICATION_URL
    pesapal_consumer_key = settings.PESAPAL_CONSUMER_KEY
    pesapal_consumer_secret = settings.PESAPAL_CONSUMER_SECRET


    request_payload = {
        "consumer_key": pesapal_consumer_key,
        "consumer_secret": pesapal_consumer_secret
    }

    request_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    request_response = requests.post(pesapal_authentication_url, headers=request_headers, data=json.dumps(request_payload)).json()
    return request_response


