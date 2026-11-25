from peewee import CharField, AutoField, IntegerField, SQL
from datos.model_base import ModelBase
from auxiliares.datos_app import defecto


class Proveedor(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    email = CharField(max_length=150, unique=True)
    id_proveedor = AutoField()
    nombre = CharField(max_length=100)
    rut = CharField(max_length=12, unique=True)
    telefono = CharField(max_length=20, null=True)

    class Meta:
        table_name = 'proveedor'