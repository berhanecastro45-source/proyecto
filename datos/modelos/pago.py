from peewee import ForeignKeyField, CharField, AutoField, IntegerField, DecimalField, DateTimeField, SQL
from datos.model_base import ModelBase
from datos.modelos.forma_pago import FormaPago
from datos.modelos.pedido import Pedido


class Pago(ModelBase):
    estado = CharField(max_length=30, default="PENDIENTE")
    fecha_pago = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )
    id_forma_pago = ForeignKeyField(FormaPago, column_name='id_forma_pago', lazy_load=False)
    id_pago = AutoField()
    id_pedido = ForeignKeyField(Pedido, column_name='id_pedido', lazy_load=False)
    monto = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = 'pago'