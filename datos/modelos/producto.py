from peewee import ForeignKeyField, CharField, AutoField, IntegerField, DecimalField, TextField, DateTimeField, SQL
from datos.model_base import ModelBase
from datos.modelos.categoria import Categoria
from datos.modelos.marca import Marca
from datos.modelos.proveedor import Proveedor
from auxiliares.datos_app import defecto


class Producto(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    descripcion = TextField()
    fecha_creacion = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )
    id_categoria = ForeignKeyField(Categoria, column_name='id_categoria', lazy_load=False)
    id_marca = ForeignKeyField(Marca, column_name='id_marca', lazy_load=False)
    id_producto = AutoField()
    id_proveedor = ForeignKeyField(Proveedor, column_name='id_proveedor', lazy_load=False)
    nombre = CharField(max_length=100)
    precio = DecimalField(max_digits=10, decimal_places=2)
    stock = IntegerField()
    stock_minimo = IntegerField(default=0, constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'producto'