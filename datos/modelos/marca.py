from peewee import CharField, AutoField, IntegerField, SQL
from datos.model_base import ModelBase
from auxiliares.datos_app import defecto


class Marca(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    id_marca = AutoField()
    nombre = CharField(max_length=100, unique=True)

    class Meta:
        table_name = 'marca'