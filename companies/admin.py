from django.contrib import admin

from .models import (
    Address,
    Category,
    Company,
    PaymentOption,
    PendingChanges,
    WrongCompanyInfoReprot,
)

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Address)
admin.site.register(PaymentOption)
admin.site.register(WrongCompanyInfoReprot)
admin.site.register(PendingChanges)
