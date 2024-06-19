from rest_framework import serializers
from .models import Categoria, Producto, Carrito, ItemCarrito

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'productos']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"


class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = ["id", "usuario", "fecha_creacion", "precio_total"]


class ItemCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrito
        fields = ["id", "carrito", "producto", "cantidad", "precio_subtotal"]
