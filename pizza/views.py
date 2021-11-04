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
    if request.data['pizzas']:
        pizzas = request.data['pizzas']
    if request.data['bebidas']:
        bebidas = request.data['bebidas']
    total = 0
    for bebida in bebidas:
        print(f'bebida {bebida}')
    for pizza in pizzas:
        print(f'pizza {pizza}')

    return Response({
        "bebidas": BebidasListAPIView(bebidas, many=True).data,
        "pizzas": PizzaListAPIView(pizzas, many=True).data,
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
