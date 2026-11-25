from peewee import ForeignKeyField, AutoField, IntegerField, DecimalField
from datos.model_base import ModelBase
from datos.modelos.pedido import Pedido
from datos.modelos.producto import Producto


class DetallePedido(ModelBase):
    cantidad = IntegerField()
    id_detalle = AutoField()
    id_pedido = ForeignKeyField(Pedido, column_name='id_pedido', lazy_load=False)
    id_producto = ForeignKeyField(Producto, column_name='id_producto', lazy_load=False)
    precio_unitario = DecimalField(max_digits=10, decimal_places=2)
    subtotal = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = 'detalle_pedido'
        indexes = (
            (("id_pedido", "id_producto"), True),
        )