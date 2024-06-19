from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='categoria_media', null=True,  blank=True)
    
    @property
    def productos(self):
        return self.producto_set.count()
    
    def __str__(self) :
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    imagen = models.ImageField(upload_to='producto_media', null=True, blank=True)
    
    def __str__(self) :
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    @property
    def precio_total(self):
        total = sum(detalle.precio_subtotal for detalle in self.itemcarrito_set.all())
        return total

    def __str__(self):
        return f"Carrito {self.id} - Usuario: {self.usuario}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    @property
    def precio_subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.producto.nombre} - Cantidad: {self.cantidad}"
