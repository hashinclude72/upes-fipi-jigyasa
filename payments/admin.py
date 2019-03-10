from django.contrib import admin
# from .models import Paytm_history
from payments.models import Paytm_history
# # Register your models here.
# class Paytm_historyAdmin(admin.ModelAdmin):
#     list_display = ("PAYTM_HISTORY", 'MID', 'TXNAMOUNT', 'STATUS')


admin.site.register(Paytm_history)
# , Paytm_historyAdmin)
