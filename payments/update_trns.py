from django.contrib.sessions.models import Session
from .models import Paytm_history
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_data(request, **data_dict):
    update_user = request.user
    user_res = request.session.get('usersj')
    ver = Paytm_history.objects.create(user=update_user, **data_dict)
    return ver
