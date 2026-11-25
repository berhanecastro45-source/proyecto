from peewee import CharField, AutoField, IntegerField, SQL
from datos.model_base import ModelBase
from auxiliares.datos_app import defecto


class Categoria(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    descripcion = CharField(max_length=255)
    id_categoria = AutoField()
    nombre = CharField(max_length=100, unique=True)

    class Meta:
        table_name = 'categoria'