# -*- coding: utf-8 -*-

"""
Autores: 
Alberto Marquez
Álvaro Asenjo
Juan Jose Montiel 
Declaramos que esta solución
es fruto exclusivamente de nuestro trabajo personal. No hemos sido
ayudados por ninguna otra persona ni hemos obtenido la solución de
fuentes externas, y tampoco hemos compartido nuestra solución con
nadie. Declaramos además que no hemos realizado de manera desho-
nesta ninguna otra actividad que pueda mejorar nuestros resultados
ni perjudicar los resultados de los demás.

"""

from mongoengine import connect

#Conectamos a nuestra base de datos
connect('giw_mongoengine')

#Comenzamos a crear las clases que heredarán de Document ya que son esquemas fijos
class dni(EmmbeddedDocument):
    numero: intField(required=True, max_length=8, min_length=8) 
    letra: StringField(required=True, min_length=1, max_length=1)

    def clean(self):
        listLetter ['T','R','W','A','G','M','Y','F','P','D','X','B','N','J','Z','S','Q','V','H','L','C','K','E']
        if(self.letra != listLetter[self.numero%23]):
            raise ValidationError("DNI no valido")


class Usuario(Document):
# DNI (obligatorio, ´unico)
# Nombre (obligatorio)
# Primer apellidos (obligatorio)
# Segundo apellido (opcional)
# Fecha de nacimiento (obligatorio, formato ’AAAA-MM-DD’)
# Fecha de los ´ultimos 10 accesos al sistema (opcional, las fechas tienen el
# formato ’AAAA,MM,DD,HH,MM,SS,NNNNNN’)
# Lista de tarjetas de cr´edito (opcional)
# Lista de referencias a pedidos (opcional)

    dni = EmmbeddedDocumentField(dni, required=True, unique=True)
    nombre = StringField(required = True)
    apellido_1 = StringField(required = True)
    apellido_2 = StringField()
    fecha_nac = DateTimeField(required = True)
    fecha_accesos = ComplexDateTimeField(max_length = 10)
    tarjetas = ListField(ReferenceField(Tarjeta, reverse_delete_rule = CASCADE))
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=CASCADE))

class Tarjeta(Document):
    nombre_propietario = StringField(required=True)
    numero = intField(primary_key=True, required = True, min_length=16, max_length=16)
    caducidad_mes = intField(required = True, min_length=1, max_length=2, min_value=1, max_value=12)
    caducidad_año = intField(required=True, min_length=4 ,max_length=4, min_value=1800)
    cvv = intField(required=True, min_length=3, max_length=3)

class Pedido(Document):
    total = FloatField(required=True, min_value=0.0)
    fecha = DateTimeField(required=True)
    linea_pedido = ListField(Linea_Pedido, required=True)

    def clean(self):
        total = 0
        for l in self.linea_pedido:
            total += l.total
        if (self.total != total):
            raise ValidationError("El total del pedido no coincide")

class Linea_Pedido(Document):
    cantidad_productos = intField(required=True, min_value = 1)
    precio_producto = FloatField(required=True, min_value=0.0)
    nombre_producto = StringField(required=True)
    total = FloatField(required=True, min_value=0)
    referencia_producto = ReferenceField(Producto, required=True)

    def clean(self):
        if ((self.cantidad_productos * self.precio_producto) != self.total):
            raise ValidationError("El total de la linea no coincide")
        if(self.nombre_producto != self.referencia_producto.nombre):
            raise ValidationError("Nombre de producto no valido")

class Producto(Document):
    codigo = 
    nombre = 
    categoria = 
    categorias = 

