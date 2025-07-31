from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from store.models import Product, Category, Customer, Order, Profile


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('email',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_sale')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_sale')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'address', 'phone', 'date', 'status')
    search_fields = ('customer__first_name', 'product__name', 'address', 'phone')
    list_filter = ('status', 'date')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address1', 'city', 'zipcode', 'country')
    search_fields = ('user__username', 'name', 'phone', 'city', 'state', 'zipcode', 'country')
    list_filter = ('country', 'city')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)

#  Profile Inline in UserAdmin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Extended user functionality
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

# Unregister and register new UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
