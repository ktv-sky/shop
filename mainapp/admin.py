from django.contrib import admin

from .models import (Cart, CartProduct, Category, Customer, Product,
                     Specification)


admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Specification)
