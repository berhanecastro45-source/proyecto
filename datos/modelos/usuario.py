from peewee import CharField, AutoField, IntegerField, DateField, SQL
from datos.model_base import ModelBase
from auxiliares.datos_app import defecto


class Usuario(ModelBase):
    activo = IntegerField(default=1, constraints=[SQL(defecto)])
    apellido_materno = CharField(max_length=100, null=True)
    apellido_paterno = CharField(max_length=100)
    email = CharField(max_length=150, unique=True)
    fecha_nacimiento = DateField(null=True)
    id_usuario = AutoField()
    nombre = CharField(max_length=100)
    password_hash = CharField(max_length=255)
    telefono = CharField(max_length=20, null=True)
    rol = CharField(max_length=30, default="CLIENTE")
    rut = CharField(max_length=12, unique=True)

    class Meta:
        table_name = 'usuario'