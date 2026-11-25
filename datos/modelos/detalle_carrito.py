from peewee import ForeignKeyField, AutoField, IntegerField, DecimalField
from datos.model_base import ModelBase
from datos.modelos.carrito import Carrito
from datos.modelos.producto import Producto


class DetalleCarrito(ModelBase):
    cantidad = IntegerField()
    id_carrito = ForeignKeyField(Carrito, column_name='id_carrito', lazy_load=False)
    id_detalle_carrito = AutoField()
    id_producto = ForeignKeyField(Producto, column_name='id_producto', lazy_load=False)
    precio_unitario = DecimalField(max_digits=10, decimal_places=2)
    subtotal = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = 'detalle_carrito'
        indexes = (
            (("id_carrito", "id_producto"), True),
        )