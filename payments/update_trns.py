from django.contrib.sessions.models import Session
from .models import Paytm_history
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User

@csrf_exempt
def update_data(request, **data_dict):
    update_user = request.user
    # update_user = auth.User
    user_updt = request.session.get('usersj')
    ver = Paytm_history.objects.create(user=update_user, **data_dict)
    return ver
