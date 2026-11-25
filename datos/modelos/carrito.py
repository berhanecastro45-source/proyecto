from peewee import ForeignKeyField, AutoField, IntegerField, SQL
from datos.model_base import ModelBase
from datos.modelos.usuario import Usuario
from auxiliares.datos_app import defecto


class Carrito(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    id_carrito = AutoField()
    id_usuario = ForeignKeyField(Usuario, column_name='id_usuario', lazy_load=False, unique=True)

    class Meta:
        table_name = 'carrito'