from django.contrib import admin
from ecom.models import *

# Register your models here.
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Coupon)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)