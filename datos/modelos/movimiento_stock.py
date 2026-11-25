from peewee import ForeignKeyField, CharField, AutoField, IntegerField, DateTimeField, SQL
from datos.model_base import ModelBase
from datos.modelos.producto import Producto


class MovimientoStock(ModelBase):
    cantidad = IntegerField()
    fecha_movimiento = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )
    id_movimiento = AutoField()
    id_producto = ForeignKeyField(Producto, column_name='id_producto', lazy_load=False)
    tipo = CharField(max_length=20)

    class Meta:
        table_name = 'movimiento_stock'