from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from . import Checksum


from payments.models import PaytmHistory
# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html', {'title': 'home'})


def payment(request):
    user = request.user
    # request.session.flush()
    request.session.set_test_cookie()
    request.session['userid'] = user.id
    # settings.USER = user
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()

    bill_amount = '100'
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
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        #params = urllib.urlencode(param)
        return render(request,"payment.html",{'paytmdict':param_dict,
                                              # 'CHECKSUMHASH':param_dict['CHECKSUMHASH'],
                                              # 'ORDER_ID':param_dict['ORDER_ID'],
                                              # 'MID':param_dict['MID'],
                                              # 'TXN_AMOUNT':param_dict['TXN_AMOUNT'],
                                              # 'CUST_ID':param_dict['CUST_ID'],
                                              # 'INDUSTRY_TYPE_ID':param_dict['INDUSTRY_TYPE_ID'],
                                              # 'WEBSITE':param_dict['WEBSITE'],
                                              # 'CHANNEL_ID':param_dict['CHANNEL_ID'],
                                              # 'CALLBACK_URL':param_dict['CALLBACK_URL'],
                                              'user': user,
                                              })
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def response(request):
    if request.method == "POST":
        rqst_usr = request.user
        bnmcv = request.session.test_cookie_worked()
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
        user_idd = request.session['userid']
        user = User.objects.get(id=user_idd)
        # user = SimpleLazyObject.user

        # for key in request.POST:
        #     data_dict[key] = request.POST[key]
        if verify:
            # user = User.objects.get(id=request.user.id)
            user.paytmHistory( **data_dict)
            user.user_details.save()
            # PaytmHistory.objects.create(user=user, **data_dict)
            return render(request, "response.html", {"paytm":data_dict})
        else:
            #return render(request,"response.html",{"paytm":data_dict})
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
