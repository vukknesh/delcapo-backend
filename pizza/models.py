from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime


class Category(models.Model):
    name = models.CharField(
        max_length=50, default='', null=True, blank=True)
    color = models.CharField(
        max_length=50, default='', null=True, blank=True)
    image = models.ImageField(
        upload_to='uploads/category/',  null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.color}'


class Banner(models.Model):

    image = models.ImageField(
        upload_to='uploads/banner/',  null=True, blank=True)

    def __str__(self):
        return f'{self.image}'


class Border(models.Model):

    nome = models.CharField(max_length=60)
    preco = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.nome} - {self.preco}'


class Bebida(models.Model):

    image = models.ImageField(
        upload_to='uploads/bebidas/', null=True, blank=True)
    nome = models.CharField(max_length=60)
    preco = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.nome} - {self.preco}'


class PedidoBebidas(models.Model):

    item = models.ForeignKey(Bebida,
                             on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.item} - {self.quantidade}'


class Tipo(models.Model):
    TIPO_PIZZA = (
        ('TRADICIONAL', 'TRADICIONAL'),
        ('ESPECIAL', 'ESPECIAL'),
        ('DOCE', 'DOCE'),
    )
    preco_broto = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.0)
    preco_media = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.0)
    preco_grande = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.0)
    tipo_pizza = models.CharField(
        max_length=20, choices=TIPO_PIZZA, default=1, blank=False)

    def __str__(self):
        return f'{self.tipo_pizza}'


class Ingrediente(models.Model):

    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome


class Sabor(models.Model):

    nome = models.CharField(max_length=60)
    ingredientes = models.ManyToManyField(
        Ingrediente, blank=True, related_name='ingrediente')
    tipo_de_pizza = models.ForeignKey(Tipo,
                                      on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to='uploads/sabores/', null=True, blank=True)

    def __str__(self):
        return self.nome


class Pizza(models.Model):
    TAMANHO_PIZZA = (
        (25, '25cm'),
        (35, '35cm'),
        (40, '40cm'),
    )
    tamanho = models.IntegerField(
        choices=TAMANHO_PIZZA, default=25, blank=False)
    sabores = models.ManyToManyField(
        Sabor, blank=True, related_name='sabor')
    borda = models.ForeignKey(Border,
                              on_delete=models.CASCADE, default=4)
    descricao = models.TextField(null=True)

    def __str__(self):
        return f'{self.id} - {self.descricao}'


class Order(models.Model):
    STATUS_A = 'Aberto'
    STATUS_B = 'Recebido'
    STATUS_C = 'Pizza no forno'
    STATUS_D = 'Saiu pra entrega'
    STATUS_E = 'Finalizado'
    STATUS_CHOICES = (
        (STATUS_A, 'Aberto'),
        (STATUS_B, 'Recebido'),
        (STATUS_C, 'Pizza no forno'),
        (STATUS_D, 'Saiu pra entrega'),
        (STATUS_E, 'Finalizado'),
    )
    PAYMENT_TYPES_CHOICES = (
        ('DINHEIRO', 'Dinheiro'),
        ('DEBITO', 'Debito'),
        ('CREDITO', 'Credito'),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    pizzas = models.ManyToManyField(
        Pizza, blank=True, related_name='pizza')
    bebidas = models.ManyToManyField(
        PedidoBebidas, blank=True, related_name='pedidobebida')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, blank=True, default="Aberto")
    payment_type = models.CharField(
        max_length=50, choices=PAYMENT_TYPES_CHOICES, default='DINHEIRO')
    observacao = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-timestamp']

    @property
    def total(self):
        """ Returns the price of the order. """

        preco = 0
        if self.bebidas:
            for bebida in self.bebidas.all():
                valor_bebidas = 0
                valor_bebidas = bebida.quantidade * bebida.item.preco
                preco += valor_bebidas

            pass
        if self.pizzas:
            for pizza in self.pizzas.all():

                quantidade_sabores = pizza.sabores.count()
                tamanho = pizza.tamanho
                valor = 0
                if tamanho == 25:
                    for sabor in pizza.sabores.all():
                        if sabor.tipo_de_pizza.tipo_pizza == 'TRADICIONAL':
                            valor += sabor.tipo_de_pizza.preco_broto
                        if sabor.tipo_de_pizza.tipo_pizza == 'ESPECIAL':
                            valor += sabor.tipo_de_pizza.preco_broto
                        if sabor.tipo_de_pizza.tipo_pizza == 'DOCE':
                            valor += sabor.tipo_de_pizza.preco_broto

                if tamanho == 35:
                    for sabor in pizza.sabores.all():
                        if sabor.tipo_de_pizza.tipo_pizza == 'TRADICIONAL':
                            valor += sabor.tipo_de_pizza.preco_media
                        if sabor.tipo_de_pizza.tipo_pizza == 'ESPECIAL':
                            valor += sabor.tipo_de_pizza.preco_media
                        if sabor.tipo_de_pizza.tipo_pizza == 'DOCE':
                            valor += sabor.tipo_de_pizza.preco_media

                if tamanho == 40:
                    for sabor in pizza.sabores.all():
                        if sabor.tipo_de_pizza.tipo_pizza == 'TRADICIONAL':
                            valor += sabor.tipo_de_pizza.preco_grande
                        if sabor.tipo_de_pizza.tipo_pizza == 'ESPECIAL':
                            valor += sabor.tipo_de_pizza.preco_grande
                        if sabor.tipo_de_pizza.tipo_pizza == 'DOCE':
                            valor += sabor.tipo_de_pizza.preco_grande
                valor = valor/quantidade_sabores
                valor += pizza.borda.preco

                print(
                    f'tamanho {tamanho} - quantidade sabores {pizza.sabores.count()} - preco borda = {pizza.borda.preco}  R$ {valor}')
                preco += valor
                # print(f'{pizza.descricao}')
                # print(f'pizza= {pizza.descricao}')
                # print(f'{sabor}')
            # print(f'preco  =  {self.pizzas}')
            # for pizza in pizzas:
            #   print(f'pizza = {pizza.sabor[0]}')

        # If there are more than 2 tamanhos, this should be cleaned. But for this simple App it's fine.
        # if self.tamanho == 25:
        #     return self.pizza.preco_broto
        # if self.tamanho == 35:
        #     return self.pizza.preco_media
        # if self.tamanho == 40:
        #     return self.pizza.preco_grande
        return preco

    def __str__(self):
        if self.user:

            return f'{self.user.first_name} - {self.status} - {self.total}'
        else:
            return f'{self.id} - {self.status}  - {self.total}'


class Open(models.Model):
    open = models.BooleanField(default=False)

    class Meta:
        ordering = ['open']

    def __str__(self):
        return f'{self.open}'


# class Cart(models.Model):
#     PAYMENT_TYPES_CHOICES = (
#         ('DINHEIRO', 'Dinheiro'),
#         ('DEBITO', 'Debito'),
#         ('CREDITO', 'Credito'),
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, blank=True, null=True)
#     pizzas = models.ManyToManyField(
#         Pizza, blank=True, related_name='pizza')
#     bebidas = models.ManyToManyField(
#         PedidoBebidas, blank=True, related_name='pedidobebida')
#     payment_type = models.CharField(
#         max_length=50, choices=PAYMENT_TYPES_CHOICES, default='DINHEIRO')
#     total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
#     timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False)

#     class Meta:
#         ordering = ['timestamp']

#     def __str__(self):
#         if user:
#             return f'{self.user.first_name}'
#         else:
#             return f'{self.timestamp} - {self.total}'
