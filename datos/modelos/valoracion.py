from peewee import ForeignKeyField, CharField, AutoField, IntegerField, DateTimeField, SQL
from datos.model_base import ModelBase
from datos.modelos.producto import Producto
from datos.modelos.usuario import Usuario
from auxiliares.datos_app import defecto


class Valoracion(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    comentario = CharField(max_length=500, null=True)
    fecha_valoracion = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )
    id_producto = ForeignKeyField(Producto, column_name='id_producto', lazy_load=False)
    id_usuario = ForeignKeyField(Usuario, column_name='id_usuario', lazy_load=False)
    id_valoracion = AutoField()
    puntuacion = IntegerField()

    class Meta:
        table_name = 'valoracion'
        indexes = (
            (("id_usuario", "id_producto"), True),
        )