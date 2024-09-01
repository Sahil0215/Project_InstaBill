from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Bank)
admin.site.register(FinancialYear)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(BilledItem)
admin.site.register(Invoice)
