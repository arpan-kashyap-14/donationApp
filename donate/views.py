from django.shortcuts import render

import razorpay

from .models import Donation

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from django.core.mail import send_mail

from django.template.loader import render_to_string

# Create your views here.

def home(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        amount=int(request.POST.get("amount")) * 100
        client=razorpay.Client(auth=("rzp_test_Ad7QoMbMk0aVEN","rCWRqFlin6ovb9pQRJHHdhn0"))
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        print(payment)
        donation=Donation(name=name,amount=amount,email=email,payment_id=payment['id'])
        donation.save()
        return render(request,'donate/index.html',{'payment':payment})

    return render(request,'donate/index.html')    


@csrf_exempt
def success(request):
    if request.method=="POST":
        a=request.POST
        order_id=""
        for key, val in a.items():
            if key=="razorpay_order_id":
                order_id=val
                break
        user=Donation.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()

        send_mail("your donation has been recieved",'Thanks for donation',settings.EMAIL_HOST_USER,
                 [user.email]
                 )


    return render(request,'donate/success.html')    

