from .serializers import SaborListSerializer, SaborCreateUpdateSerializer, CategoryCreateUpdateSerializer, CategoryListAllSerializer, BannerListAllSerializer, OrderListAllSerializer, OrderUpdateSerializer, TodasBebidaSerializer, OpenCreateUpdateSerializer, BordasListSerializer
from .models import Sabor, Category, Banner, Order, Open, Pizza, Bebida, Border
from django.contrib.auth.models import User
from datetime import datetime, timezone
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins


@api_view(['GET'])
def get_all_foods_and_categorys(request):
    sabores = Sabor.objects.all()
    categorys = Category.objects.all()
    banners = Banner.objects.all()
    bordas = Border.objects.all()
    bebidas = Bebida.objects.all()

    return Response({
        "banners": BannerListAllSerializer(banners, many=True).data,
        "categorys": CategoryListAllSerializer(categorys, many=True).data,
        "sabores": SaborListSerializer(sabores, many=True).data,
        "bordas": BordasListSerializer(bordas, many=True).data,
        "bebidas": TodasBebidaSerializer(bebidas, many=True).data,
    })


@api_view(['POST'])
def valor_pedido(request):
    print(f'request.data valor_pedido {request.data}')
    bebidas = None
    pizzas = None
    total = 0
    if request.data['pizzas']:
        pizzas = request.data['pizzas']
        for pizza in pizzas:
            print(f'pizza ---  {pizza}')
            tamanho = pizza['tamanho']
            print(f'tamanha ---  {tamanho}')
            dividido = len(pizza['sabores'])
            print(f'dividido ---  {dividido}')
            id_borda = pizza['borda']
            print(f'id_borda ---  {id_borda}')

            borda = Border.objects.get(id=id_borda)
            preco_borda = 0
            if borda:

                print(f'borda ---  {borda}')
                preco_borda = borda.preco
                print(f'preco_borda ---  {preco_borda}')
            valor_pizza = 0
            for sabor in pizza['sabores']:
                print(f'sabor = {sabor}')
                s = Sabor.objects.get(id=sabor)
                print(f's = {s}')
                if tamanho == 25:
                    valor_pizza += s.tipo_de_pizza.preco_broto
                if tamanho == 35:
                    valor_pizza += s.tipo_de_pizza.preco_media
                if tamanho == 40:
                    valor_pizza += s.tipo_de_pizza.preco_grande
            valor_pizza = valor_pizza/dividido
            print(f'valor_pizza ---  {valor_pizza}')
            total += valor_pizza

    print(f'valor_parcial {total}')

    if request.data['bebidas']:
        bebidas = request.data['bebidas']
        for bebida in bebidas:
            print(f'bebida {bebida}')
            quantidade = float(bebida['quantidade'])
            preco = float(bebida['preco'])
            print(f'quantidade {quantidade}')
            print(f'preco {preco}')
            print(f'type preco {type(preco)}')
            print(f'type quantidade {type(quantidade)}')
            preco_bebida = quantidade * preco
            total += preco_bebida

    return Response({

        "total": total
    })


@api_view(['POST'])
def confirmar_pedido(request):
    print(f'request.data {request.data}')

    #     {
    # 	"userid": 2,
    # 	"itemorder":[{"quantity": 1, "food": 1}, {"quantity": 20, "food": 3}],
    # 	"payment_type": "CREDITO",
    # 	"observation": "gostaria de borda de catupiNi"
    # }

    # itemorder = None
    # if request.data['itemorder']:
    #     order = Order.objects.create(
    #         user=user, payment_type=payment_type, observation=observation)
    #     itemorder = request.data['itemorder']
    #     for item in itemorder:
    #         quantity = item['quantity']
    #         f = Food.objects.get(id=item['food'])
    #         ItemOrder.objects.create(
    #             order=order, food=f, quantity=quantity)

    # if itemorder is None:
    #     raise ValidationError("Nenhum item no carrinho")

    return Response({
        "message": 'Pedido criado com sucesso!'
        # "order": OrderListAllSerializer(order).data
    })


class PizzaListAPIView(ListAPIView):
    serializer_class = Pizza

    def get_queryset(self, *args, **kwargs):

        queryset_list = Pizza.objects.all()  # filter(user=self.request.user)

        return queryset_list


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListAllSerializer

    def get_queryset(self, *args, **kwargs):

        # filter(user=self.request.user)
        queryset_list = Order.objects.all()

        return queryset_list


class SaboresListAPIView(ListAPIView):
    serializer_class = SaborListSerializer

    def get_queryset(self, *args, **kwargs):

        # filter(user=self.request.user)
        queryset_list = Sabor.objects.all()

        return queryset_list


class BebidasListAPIView(ListAPIView):
    serializer_class = TodasBebidaSerializer

    def get_queryset(self, *args, **kwargs):

        # filter(user=self.request.user)
        queryset_list = Bebida.objects.all()

        return queryset_list


class OpenOrderListAPIView(ListAPIView):
    serializer_class = OrderListAllSerializer

    def get_queryset(self, *args, **kwargs):

        queryset_list = Order.objects.exclude(
            status='Finalizado')  # filter(user=self.request.user)

        return queryset_list


class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListAPIView
    lookup_field = 'id'


class OrderUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save()


class OpenUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OpenCreateUpdateSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        open = Open.objects.first()
        return Response({
            "message": open.open
        })

    def perform_update(self, serializer):
        serializer.save()
        # email send_email
