from peewee import Model
from datos.conexion import DB


class ModelBase(Model):
    """Clase base compartida por todos los modelos ORM."""

    class Meta:
        database = DB
