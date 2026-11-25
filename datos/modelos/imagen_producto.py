from peewee import ForeignKeyField, CharField, AutoField, IntegerField, SQL
from datos.model_base import ModelBase
from datos.modelos.producto import Producto
from auxiliares.datos_app import defecto


class ImagenProducto(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    id_imagen = AutoField()
    id_producto = ForeignKeyField(Producto, column_name='id_producto', lazy_load=False)
    url_imagen = CharField(max_length=255)

    class Meta:
        table_name = 'imagen_producto'