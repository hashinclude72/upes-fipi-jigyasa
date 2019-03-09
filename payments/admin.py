from django.contrib import admin
from .models import Paytm_history
# from payments.models import PaytmHistory
# # Register your models here.
# class PaytmHistoryAdmin(admin.ModelAdmin):
#     list_display = ('user', 'MID', 'TXNAMOUNT', 'STATUS')
#
#
admin.site.register(Paytm_history)

# PaytmHistoryAdmin)
