from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria, Producto, Carrito, ItemCarrito
from .serializers import ProductoSerializer, CategoriaSerializer, CarritoSerializer, ItemCarritoSerializer


class CategoriaView(APIView):
    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

class ProductoView(APIView):
    def get(self, request):
        categoria_id = request.query_params.get('categoria')
        productos = Producto.objects.all()
        if categoria_id:
            productos = Producto.objects.filter(categoria=categoria_id)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class ProductoDetailView(APIView):
    def get(self, request, id_producto):
        producto = Producto.objects.get(pk=id_producto)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    
    def patch(self, request, id_producto):
        producto = Producto.objects.get(pk=id_producto)
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class CarritoView(APIView):
    def get(self, request):
        carritos = Carrito.objects.all()
        serializer = CarritoSerializer(carritos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarritoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
class ItemCarritoView(APIView):
    def get(self, request, id_carrito):
        try:
            carrito = Carrito.objects.get(pk=id_carrito)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito not found'}, status=status.HTTP_404_NOT_FOUND)

        items = ItemCarrito.objects.filter(carrito=id_carrito).select_related('producto')
        item_serializer = ItemCarritoSerializer(items, many=True)
        
        for item in item_serializer.data:
            producto_id = item['producto']
            try:
                producto = Producto.objects.get(pk=producto_id)
            except Producto.DoesNotExist:
                return Response({'error': f'Producto with id {producto_id} not found'}, status=status.HTTP_404_NOT_FOUND)
            
            producto_serializer = ProductoSerializer(producto)
            item['producto'] = producto_serializer.data

        response_data = {
            'precio_total': carrito.precio_total,
            'items': item_serializer.data,
        }

        return Response(response_data)

    def post(self, request, id_carrito):
        if not isinstance(request.data, list):
            return Response({'error': 'Invalid data format. Expected a list of items.'}, status=status.HTTP_400_BAD_REQUEST)

        response_data = []
        for item_data in request.data:
            item_data['carrito'] = id_carrito
            serializer = ItemCarritoSerializer(data=item_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data.append(serializer.data)

        try:
            carrito = Carrito.objects.get(pk=id_carrito)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'precio_total': carrito.precio_total,
            'items': response_data,
        }, status=status.HTTP_201_CREATED)  
    
    
class ItemCarritoDetailView(APIView):
    def get(self, request, id_carrito, id_item):
        item = ItemCarrito.objects.get(pk=id_item, carrito=id_carrito)
        serializer = ItemCarritoSerializer(item)

        return Response(serializer.data)

    def delete(self, request, id_carrito, id_item):
        item = ItemCarrito.objects.get(pk=id_item, carrito=id_carrito)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, id_carrito, id_item):
        item = ItemCarrito.objects.get(pk=id_item, carrito=id_carrito)
        serializer = ItemCarritoSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
