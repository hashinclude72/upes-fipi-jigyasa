from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import Paytm_history

from . import Checksum


@login_required
def payments_home(request):
    user = request.user
    status = False
    trns = 0
    bill_amount = 00
    if Paytm_history.objects.filter(user=user, STATUS = 'TXN_SUCCESS'):
        trns = Paytm_history.objects.filter(user=user, STATUS = 'TXN_SUCCESS')[0]
        status = True

    if user.user_details.team_count == 1:
        bill_amount = 2000.00
    else:
        bill_amount = 5500.00

    return render(request, 'payments/payments_home.html', {'title': 'Payments', 'status': status, 'trns': trns, 'bill_amount': bill_amount})

@login_required
@ensure_csrf_cookie
def paytm(request):
    user = request.user
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
    P_URL = settings.PAYTM_URL
    CUST_ID = user.email
    order_id = Checksum.__id_generator__()

    if user.user_details.team_count == 1:
        bill_amount = 2053.00
    else:
        bill_amount = 5615.00


    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': bill_amount,
                    'CUST_ID': CUST_ID,
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':CALLBACK_URL,
                }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'paytmurl' :P_URL, 'title': 'Paytm'})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")



@csrf_exempt
def recipt(request):
    if request.method == "POST":
        user=request.user
        data_dict = {}
        data_dict = dict(request.POST.items())
        Paytm_history.objects.create(user=request.user, **data_dict)

    status = False
    for key,value in data_dict.items():
        if key == 'STATUS':
            user.user_details.status = value
            user.user_details.save()
            # if value == 'TXN_SUCCESS':
            status = value
    return render(request, "payments/recipt.html", {"paytmr": data_dict, 'title': 'Recipt', "status": status})



@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        data_dict = dict(request.POST.items())

        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            for key in request.POST:
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            # Paytm_history.objects.create(user=settings.USER, **data_dict)
            return render(request, "payments/response.html", {"paytm":data_dict, 'title': 'Confirm'})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
