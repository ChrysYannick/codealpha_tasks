from django.contrib import admin
from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem
)
# enregistrement des classes dans l'admin pour les insertions et autres
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Category)
admin.site.register(Product)