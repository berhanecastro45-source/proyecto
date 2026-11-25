from peewee import CharField, AutoField, IntegerField, DecimalField, DateField, SQL
from datos.model_base import ModelBase
from auxiliares.datos_app import defecto


class Cupon(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    codigo = CharField(max_length=50, unique=True)
    descuento = DecimalField(max_digits=5, decimal_places=2)
    fecha_fin = DateField()
    fecha_inicio = DateField()
    id_cupon = AutoField()

    class Meta:
        table_name = 'cupon'