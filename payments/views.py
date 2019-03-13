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
    # request.session['usersj'] = user.id
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
    CUST_ID = user.email
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()

    if user.user_details.team_count == 1:
        bill_amount = 2000.00
    else:
        bill_amount = 5500.00


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
        # user_pays = request.session['usersj']
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'title': 'Paytm'})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")



@csrf_exempt
def recipt(request):
    if request.method == "POST":
        data_dict = {}
        data_dict = dict(request.POST.items())
        Paytm_history.objects.create(user=request.user, **data_dict)

    # user = request.user
    status = False
    # if Paytm_history.objects.filter(user=user, STATUS = 'TXN_SUCCESS'):
    #     status = True
    for key,value in data_dict.items():
        if key == 'STATUS' and value == 'TXN_SUCCESS':
            status = True
    return render(request, "payments/recipt.html", {"paytmr": data_dict, 'title': 'Recipt', "status": status})



@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}

        # data_dict = {
        #             'CHECKSUMHASH':request.POST.get('CHECKSUMHASH'),
        #             'ORDER_ID':request.POST.get('ORDER_ID'),
        #             'MID':request.POST.get('MID'),
        #             'TXN_AMOUNT': request.POST.get('TXN_AMOUNT'),
        #             'CUST_ID':request.POST.get('CUST_ID'),
        #             'INDUSTRY_TYPE_ID':request.POST.get('INDUSTRY_TYPE_ID'),
        #             'WEBSITE': request.POST.get('WEBSITE'),
        #             'CHANNEL_ID':request.POST.get('CHANNEL_ID'),
        #             'CALLBACK_URL':request.POST.get('CALLBACK_URL'),
        #             'user':request.POST.get('user')
        #         }
        data_dict = dict(request.POST.items())

        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        # for key in request.POST:
        #     data_dict[key] = request.POST[key]
        if verify:
            for key in request.POST:
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            # user = User.objects.get(id=request.user.id)
            # user.paytm_history( **data_dict)
            # user.paytm_history.save()
            # Paytm_history.objects.create(user=settings.USER, **data_dict)
            return render(request, "payments/response.html", {"paytm":data_dict, 'title': 'Confirm'})
            #     return HttpResponse("some html here")
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
