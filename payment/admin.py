from django.contrib import admin
from .models import ShippingAddress , Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#create an orderItem inline
class OrderItemInline(admin.TabularInline ):
     model = OrderItem

 #extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['user', 'full_name', 'email', 'shipping_address', 'date_ordered', 'amount_paid', 'is_shipped', 'date_shipped']
    inlines = [OrderItemInline]

#unregister order model
admin.site.unregister(Order)
#reregister Our order AND orderitems
admin.site.register(Order, OrderAdmin)


