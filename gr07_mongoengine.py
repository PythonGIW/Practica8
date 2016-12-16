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

from mongoengine import *
import datetime
#import barcode


#Conectamos a nuestra base de datos
connect('giw_mongoengine')

#Comenzamos a crear las clases que heredarán de Document ya que son esquemas fijos
class Dni(EmbeddedDocument):
    numero= IntField(required=True, max_length=8, min_length=8) 
    letra= StringField(required=True, min_length=1, max_length=1)

    def clean(self):
        listLetter = ['T','R','W','A','G','M','Y','F','P','D','X','B','N','J','Z','S','Q','V','H','L','C','K','E']
        if(self.letra != listLetter[self.numero%23]):
            raise ValidationError("DNI no valido")

class Tarjeta(Document):
    nombre_propietario = StringField(required=True)
    numero = IntField(primary_key=True, required = True, min_length=16, max_length=16)
    caducidad_mes = IntField(required = True, min_length=1, max_length=2, min_value=1, max_value=12)
    caducidad_ano = IntField(required=True, min_length=4 ,max_length=4, min_value=1800)
    cvv = IntField(required=True, min_length=3, max_length=3)

class Producto(Document):
    codigo = IntField(min_value=0, unique=True)
    nombre =  StringField(required = True)
    categoria = IntField(min_value=0,required = True)
    categorias = ListField(IntField(min_value=0, max_value=1000))

    def crear_ean13(valor, archivo):
        ean = barcode.get('ean13', valor, writer=barcode.writer.ImageWriter())
        # mostramos el codigo de barras en consola
        print ean.to_ascii()
    
    def clean(self):
    if ((self.codigo%10 != digito_control(self.codigo//10)):#Le pasamos el numero, sin el de control
        raise ValidationError("El digito de control no coincide")
        
        #Por ejemplo, para 123456789041 el dígito de control será:
        #Numeramos de derecha a izquierda: 140987654321
        #Suma de los números en los lugares impares: 1+0+8+6+4+2 = 21
        #Multiplicado (por 3): 21 × 3 = 63
        #Suma de los números en los lugares pares: 4+9+7+5+3+1 = 29
        #Suma total: 63 + 29 = 92
        #Decena inmediatamente superior = 100
        #Dígito de control: 100 - 92 = 8
        #El código quedará así: 1234567890418.
    def digito_control(numero):
        numero = invertir(numero)
        pares = suma_pares(numero)*3
        impares = suma_impares(numero)
        dSuperior = round(pares+ impares/10.)*10
        return dSuperior - (pares + impares)
        
    #probar con esto en caso de no funcionar int(str(123456789)[::-1]) 
    def invertir(a):
        y=(a%10==0)  #Aquí le damos el valor a la variable "y", True, o False, si el N° termina en 0.
        z=len(str(a))
        for i in range(z):
            b=a%10
            a=a//10
            x=x*10+b
        if y:
            x=str(x)
            x='0'+x
        return x
        
    def suma_pares(numero):
        i = 0
        aux=str(numero)
        while i <= len(numero):
            suma+=aux[i]
            print(i)
            i += 2
            
    def suma_pares(numero):
        i = 1
        aux=str(numero)
        while i <= len(numero):
            suma+=aux[i]
            print(i)
            i += 2
    

class Linea_Pedido(Document):
    cantidad_productos = IntField(required=True, min_value = 1)
    precio_producto = FloatField(required=True, min_value=0.0)
    nombre_producto = StringField(required=True)
    total = FloatField(required=True, min_value=0)
    referencia_producto = ReferenceField(Producto, required=True)

    def clean(self):
        if ((self.cantidad_productos * self.precio_producto) != self.total):
            raise ValidationError("El total de la linea no coincide")
        if(self.nombre_producto != self.referencia_producto.nombre):
            raise ValidationError("Nombre de producto no valido")
            
class Pedido(Document):
    total = FloatField(required=True, min_value=0.0)
    fecha = ComplexDateTimeField(required=True)
    linea_pedido = ListField(ReferenceField(Linea_Pedido), required=True)

    def clean(self):
        total = 0
        for l in self.linea_pedido:
            total += l.total
        if (self.total != total):
            raise ValidationError("El total del pedido no coincide")

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

    dni = EmbeddedDocumentField(Dni, required=True, unique=True)
    nombre = StringField(required = True)
    apellido_1 = StringField(required = True)
    apellido_2 = StringField()
    fecha_nac = DateTimeField(required = True)
    fecha_accesos = ComplexDateTimeField(max_length = 10)
    tarjetas = ListField(ReferenceField(Tarjeta, reverse_delete_rule = CASCADE))
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=CASCADE))

producto = Producto(codigo = 1234567890418, nombre="producto1", categoria=1)
producto2 = Producto(codigo = 1234567890429, nombre="producto2", categoria=1)
producto.drop_collection()
producto.save()
producto2.save()
linea = Linea_Pedido(cantidad_productos=2, precio_producto=2, nombre_producto="producto1", total=4, referencia_producto=producto)
linea.drop_collection()
linea.save()
linea2 = Linea_Pedido(cantidad_productos=1, precio_producto=1, nombre_producto="producto2", total=1, referencia_producto=producto2)
linea2.save()
pedido = Pedido(total=5, fecha=datetime.datetime.now(),linea_pedido=[linea,linea2])
pedido.drop_collection()
pedido.save()


