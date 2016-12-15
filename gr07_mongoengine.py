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

    dni = 
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

class Linea_Pedido(Document):
    cantidad_productos = intField(required=True, min_value = 1)
    precio_producto = FloatField(required=True, min_value=0.0)
    nombre_producto = StringField(required=True)
    total = FloatField(required=True, min_value=0)
    referencia_producto = ReferenceField(Producto, required=True)

class Producto(Document):
    codigo = 
    nombre = 
    categoria = 
    categorias = 

