from peewee import ForeignKeyField, CharField, AutoField, IntegerField, DecimalField, DateTimeField, SQL
from datos.model_base import ModelBase
from datos.modelos.cupon import Cupon
from datos.modelos.usuario import Usuario


class Pedido(ModelBase):
    direccion_envio = CharField(max_length=300)
    estado = CharField(max_length=30, default="PENDIENTE")
    fecha_pedido = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )
    id_cupon = ForeignKeyField(Cupon, column_name='id_cupon', lazy_load=False, null=True)
    id_pedido = AutoField()
    id_usuario = ForeignKeyField(Usuario, column_name='id_usuario', lazy_load=False)
    total = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = 'pedido'