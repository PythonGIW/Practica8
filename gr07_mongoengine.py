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
    nombre = StringField(required = true)
    apellido_1 = StringField(required = True)
    apellido_2 = StringField(required = False)
    fecha_nac = DateField(required = True)
    fecha_accesos = ComplexDateTimeField(max_length = 10, required = False)
    tarjetas = ReferenceField(Tarjeta, required = False, reverse_delete_rule = CASCADE)
    pedidos = ReferenceField(Pedido, required = False, reverse_delete_rule=CASCADE)

class Tarjeta(Document):
    nombre_propietario = 
    numero =
    caducidad_mes = 
    caducidad_año = 
    cvv = 

class Pedido(Document):
    total = 
    fecha = 
    linea_pedido = 

class Linea_Pedido(Document):
    cantidad_productos = 
    precio_producto = 
    nombre_producto =
    total = 
    referencia_producto = 

class Producto(Document):
    codigo = 
    nombre = 
    categoria = 
    categorias = 

