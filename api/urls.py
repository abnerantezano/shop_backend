from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('categorias', views.CategoriaView.as_view(), name='categorias'),
    path('productos', views.ProductoView.as_view(), name='productos'),
    path('productos/<int:id_producto>', views.ProductoDetailView.as_view(), name='detalle_producto'),
    path('carritos', views.CarritoView.as_view(), name='carritos'),
    path('carritos/<int:id_carrito>', views.ItemCarritoView.as_view(), name='items_carrito'),
    path('carritos/<int:id_carrito>/<int:id_item>', views.ItemCarritoDetailView.as_view(), name='detalle_item')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
