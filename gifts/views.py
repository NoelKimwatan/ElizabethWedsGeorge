from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests, json, random
from django.views.decorators.csrf import csrf_exempt
from .models import *
from elizabethandgeorge.settings import PESAPAL_REDIRECT_URL, PESAPAL_RESPONSE_URL

# Create your views here.
def index(request):
    return render(request, "gifts/index.html")

def process_gift(request):
    if request.method == "POST":
        amount = request.POST["giftAmount"]
        phoneNo = request.POST["phoneNo"]
        phoneNo = phoneNo[-9:]
        giftMethod = request.POST["giftMethod"]

        print("Selected amount is {} and the phone number is {}. Finally the giftmethod is {}".format(amount,phoneNo,giftMethod))
        if giftMethod == "Card":
            return process_card(request,amount,phoneNo)
        elif giftMethod == "Mpesa":
            pass
        else:
            pass
    else:
        pass

def process_card(request,amount,phoneNo):
    gift_object = Gift(
        phone_no = phoneNo,
        amount =  amount,
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
            "url": PESAPAL_RESPONSE_URL,
            "ipn_notification_type": "POST"
        }

        ipn_registration =requests.post(settings.PESAPAL_IPN_REGISTRATION_URL,headers = ipn_registration_header, data=json.dumps(ipn_registration_body)).json()
        print("IPN regsitration response: ",ipn_registration)

        ipn_id = ipn_registration["ipn_id"]
        gift_object.ipn_id = ipn_id
        gift_object.save()

        # print("IPN registration id: ",ipn_id)

        order_request_customer_address = {
            "phone_number": phoneNo
        }


        print("Gift object id ",gift_object.id)


        unique_id = gift_object.id + 1000
        print("Unique order id: ",unique_id)

        order_request_payload = {
            "id": unique_id ,
            "currency": "KES",
            "amount": amount,
            "description": "Elizabeth weds George",
            "callback_url": PESAPAL_REDIRECT_URL,
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
        return render(request, "gifts/process_card.html",context)

def gift_processed(request):
    order_tracking_id = request.GET["OrderTrackingId"]
    gift_object = Gift.objects.get(order_tracking_id=order_tracking_id)

    message = str()

    #Transaction complete
    if gift_object.status == 4:
        message = "Thank you. Your gift has been received"
    elif gift_object.status == 2:
        message = "Transaction rejected. Please try again"
    elif gift_object.status == 1:
        message = "Your transaction is being processed"

    context = {
        "status": gift_object.status,
        "message": message,
        "order_tracking_id": order_tracking_id
    }
    return render(request,'gifts/gift_processed.html', context)

def gift_message(request):
    order_tracking_id = request.POST["order_tracking_id_number"]
    message = request.POST["giftMessage"]

    gift_object = Gift.objects.get(order_tracking_id=order_tracking_id)
    gift_object.message = message
    gift_object.save()

    return redirect('index')

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
            phone_no = customer_phone,
            amount =  constribution_amount,
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
                "url": PESAPAL_RESPONSE_URL,
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

            try:
                print("Gift object id ",gift_object.id);
            except:
                pass

            unique_id = random.randint(1,999999999999999999999999999999999) + 498656259
            print("Unique order id: ",unique_id)

            order_request_payload = {
                "id": unique_id ,
                "currency": "KES",
                "amount": constribution_amount,
                "description": "Elizabeth weds George",
                "callback_url": PESAPAL_REDIRECT_URL,
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
