from django.contrib import admin

# Register your models here.
from .models import Pizza, Order, Sabor, Tipo, Ingrediente, Border, Bebida, PedidoBebidas, Banner, Category
# Register your models here.


admin.site.register(Pizza)
admin.site.register(Bebida)
admin.site.register(PedidoBebidas)
admin.site.register(Ingrediente)
admin.site.register(Border)
admin.site.register(Order)
admin.site.register(Tipo)
admin.site.register(Sabor)
admin.site.register(Banner)
admin.site.register(Category)
