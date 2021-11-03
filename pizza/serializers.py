

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ImageField,
    ReadOnlyField,
    CharField
)


from accounts.serializers import UserSerializer

from .models import Category, Sabor, Banner, Order, Pizza, Open, Ingrediente, Bebida, PedidoBebidas, Border


class CategoryCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class BannerCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"


class OrderCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class SaborCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Sabor
        fields = "__all__"


class SaborNomeSerializer(ModelSerializer):

    class Meta:
        model = Sabor
        fields = ['nome']


class OpenCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Open
        fields = "__all__"


class BebidaSerializer(ModelSerializer):
    item = CharField(source='item.nome')

    class Meta:
        model = PedidoBebidas
        fields = ['item', 'quantidade']


class TodasBebidaSerializer(ModelSerializer):

    class Meta:
        model = Bebida
        fields = ('__all__')


class IngredientesSerializers(ModelSerializer):

    class Meta:
        model = Ingrediente
        fields = ["nome"]


class SaborListSerializer(ModelSerializer):
    # ingredientes = IngredientesSerializers(
    #     "ingredientes", many=True)
    lista_ingredientes = SerializerMethodField()
    tipo = CharField(source='tipo_de_pizza.tipo_pizza')

    def get_lista_ingredientes(self, obj):
        lista = []
        for o in obj.ingredientes.all():
            lista.append(o.nome)
        return lista

    class Meta:
        model = Sabor
        fields = ['id', 'nome',
                  'lista_ingredientes', 'tipo', 'image']


class PizzaSerializer(ModelSerializer):
    borda = CharField(source='borda.nome')
    sabores = SerializerMethodField()

    def get_sabores(self, obj):
        lista = []
        for s in obj.sabores.all():
            lista.append(s.nome)
        return lista
        # return SaborNomeSerializer(obj.sabores.all(), many=True).data

    class Meta:
        model = Pizza
        fields = ['id', 'tamanho', 'borda', "sabores"]


class PedidoBebidaSerializer(ModelSerializer):
    item = CharField(source='item.nome')

    class Meta:
        model = Pizza
        fields = ['id', 'item', 'quantidade']

# class ItemOrderListSerializer(ModelSerializer):
#     total = SerializerMethodField()
#     food_name = CharField(source="food.name")

#     def get_total(self, obj):

#         t = obj.quantity * obj.food.price
#         return t

#     class Meta:
#         model = ItemOrder
#         fields = ['quantity', 'order', 'food_name', 'total']


class CategoryListAllSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'image']


class OrderListAllSerializer(ModelSerializer):
    cliente = ReadOnlyField(source='user.first_name')
    endereco = ReadOnlyField(source='user.profile.endereco')
    telefone = ReadOnlyField(source='user.profile.fone')
    lista_pizza = SerializerMethodField()
    lista_bebida = SerializerMethodField()

    def get_lista_pizza(self, obj):
        return PizzaSerializer(obj.pizzas.all(), many=True).data

        # for piz in obj.pizzas.all():

        #     for sab in piz.sabores.all():
        #         lista.append(sab.nome)
        # return lista

    def get_lista_bebida(self, obj):
        return BebidaSerializer(obj.bebidas.all(), many=True).data

    class Meta:
        model = Order
        fields = ['id', 'cliente', 'endereco', 'telefone', 'lista_pizza', 'observacao',
                  'lista_bebida', 'payment_type', 'status', 'total']


class BannerListAllSerializer(ModelSerializer):

    class Meta:
        model = Banner
        fields = ['id', 'image']


class BordasListSerializer(ModelSerializer):

    class Meta:
        model = Border
        fields = ['id', 'nome']


class OrderUpdateSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ['status']
