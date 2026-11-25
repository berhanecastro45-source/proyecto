from peewee import ForeignKeyField, CharField, AutoField, IntegerField, SQL
from datos.model_base import ModelBase
from datos.modelos.usuario import Usuario
from auxiliares.datos_app import defecto


class Direccion(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    calle = CharField(max_length=150)
    ciudad = CharField(max_length=100)
    codigo_postal = CharField(max_length=20, null=True)
    comuna = CharField(max_length=100)
    id_direccion = AutoField()
    id_usuario = ForeignKeyField(Usuario, column_name='id_usuario', lazy_load=False)
    region = CharField(max_length=100)

    class Meta:
        table_name = 'direccion'