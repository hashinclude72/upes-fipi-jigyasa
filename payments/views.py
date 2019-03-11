from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import Paytm_history

from . import Checksum , update_trns


@login_required
def home(request):
    return render(request, 'payments/home.html', {'title': 'home'})

# @login_required
def payment(request):
    user = request.user
    # settings.USER = user
    # request.session['userid'] = user.id
    request.session['usersj'] = user.id
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()

    bill_amount = 100.0
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': bill_amount,
                    'CUST_ID':'shubhamjaswal772@gmail.com',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':CALLBACK_URL,
                }
        param_dict = data_dict
        user_pays = request.session['usersj']
        # user_pays = request.session['userwe']
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request,"payments/payment.html",{'paytmdict':param_dict, 'user': user})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


# @login_required
# @csrf_exempt
# def update_data(request, **data_dict):
#     update_user = request.user
#     user_res = request.session.get('usersj')
#     ver = Paytm_history.objects.create(user=update_user, **data_dict)
#     return ver
#


# @csrf_exempt
# def recipt(request, data_dict):
#     # if request.method == "POST":
#     # data_dict = {}
#     # data_dict = dict(request.POST.items())
#     Paytm_history.objects.create(user=request.user, **data_dict)
#
#     return render(request, "recipt.html", {"paytmr":data_dict})



# @login_required
@csrf_exempt
def response(request):
    if request.method == "POST":
        # rqst_usr_res = request.user.id
        # user_res = request.session.get('usersj')
        # bnmcv = request.session.test_cookie_worked()
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        # sdcv = request.POST
        #data_dict = request.POST.get('paytmdict')

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
        # user = request.POST.get('user')

        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        # user_idd = request.session['userid']
        # user = User.objects.get(id=user_idd)
        # user = SimpleLazyObject.user

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
            ver = update_trns.update_data(request, **data_dict)
            # user = User.objects.get(id=request.user.id)
            # user.paytm_history( **data_dict)
            # user.paytm_history.save()
            # Paytm_history.objects.create(user=settings.USER, **data_dict)
            return render(request, "payments/response.html", {"paytm":data_dict})
            # if ver:
            #     return HttpResponse("some html here")
            # return redirect('recipt', data_dict)
        else:
            #return render(request,"response.html",{"paytm":data_dict})
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
