from .serializers import SaborListSerializer, SaborCreateUpdateSerializer, CategoryCreateUpdateSerializer, CategoryListAllSerializer, BannerListAllSerializer, OrderListAllSerializer, OrderUpdateSerializer, TodasBebidaSerializer, OpenCreateUpdateSerializer, BordasListSerializer, OrderSerializer
from .models import Sabor, Category, Banner, Order, Open, Pizza, Bebida, Border, PedidoBebidas
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


@api_view(["GET"])
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
            total += preco_borda

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
            print(f'preco_bebida {preco_bebida}')
            print(f'total {total}')
            print(f'type total {type(total)}')
            total = float(total) + preco_bebida
            print(f'total bebida final {total}')

    return Response({

        "total": total
    })


@api_view(['POST'])
def confirmar_pedido(request):
    print(f'request.data {request.data}')
    number = 1
    lista_pizza_id = []
    lista_bebidas_id = []

    if request.data['pizzas']:
        pizzas = request.data['pizzas']
        print(f'pizzas = {pizzas}')

        for pizza in pizzas:
            tamanho = int(pizza['tamanho'])
            borda = int(pizza['borda'])
            sabores = pizza['sabores']
            print(f'tamanho {tamanho}')
            print(f' type tamanho {type(tamanho)}')
            print(f'type borda {type(borda)}')
            print(f' type sabores {type(sabores)}')
            print(f'sabores {sabores}')
            descricao = f'Pelo tamanho {tamanho}'
            borda_pizza = Border.objects.get(id=borda)
            p = Pizza.objects.create(
                tamanho=tamanho, borda=borda_pizza, descricao=descricao)
            p.sabores.set(sabores)
            print(f'p depois = {p}')
            print(f'p.id = {p.id}')
            lista_pizza_id.append(p.id)

    if request.data['bebidas']:
        bebidas = request.data['bebidas']
        print(f'bebidas = {bebidas}')
        for bebida in bebidas:
            item = bebida['bebida']
            bebida_item = Bebida.objects.get(id=item)
            print(f'item em bebida = {item}')
            quantidade = bebida['quantidade']
            b = PedidoBebidas.objects.create(
                item=bebida_item, quantidade=quantidade)
            lista_bebidas_id.append(b.id)

    print(f'lista_bebidas_id = {lista_bebidas_id}')
    print(f'lista_pizza_id = {lista_pizza_id}')

    if request.data['payment_type']:
        payment_type = request.data['payment_type']

    print(f'payment_type = {payment_type}')
    if request.data['end']:
        end = request.data['end']
    print(f'end = {end}')
    if request.data['nome']:
        nome = request.data['nome']
    print(f'nome = {nome}')
    if request.data['fone']:
        fone = request.data['fone']
    print(f'fone = {fone}')
    if request.data['observacao']:
        observacao = request.data['observacao']

    print(f'observacao = {observacao}')
    if request.data['user']:
        id = request.data['user']
        user = User.objects.get(id=id)
    else:
        user = User.objects.first()

    print(f'user {user}')
    order = Order.objects.create(
        user=user, nome=nome, payment_type="DINHEIRO", endereco=end, fone=fone, observacao=observacao)

    print(f'order = {order}')
    order.pizzas.set(lista_pizza_id)
    order.bebidas.set(lista_bebidas_id)

    print(f'order = {order}')
    return Response({
        "message": 'Pedido criado com sucesso!',
        "number": OrderSerializer(order)
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
