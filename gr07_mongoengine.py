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
import barcode


#Conectamos a nuestra base de datos
connect('giw_mongoengine')

#Comenzamos a crear las clases que heredarán de Document ya que son esquemas fijos
class Dni(EmbeddedDocument):
    numero= IntField(required=True, max_length=8, min_length=8) 
    letra= StringField(required=True, min_length=1, max_length=1)

    def clean(self):
        
        listLetter = ['T','R','W','A','G','M','Y','F','P','D','X','B','N','J','Z','S','Q','V','H','L','C','K','E']
    
        if(self.letra != listLetter[int(self.numero)%23]):
            raise ValidationError("DNI no valido")

class Tarjeta(Document):
    nombre_propietario = StringField(required=True)
    numero = IntField(primary_key=True, required = True, min_length=16, max_length=16)
    caducidad_mes = IntField(required = True, min_length=1, max_length=2, min_value=1, max_value=12)
    caducidad_ano = IntField(required=True, min_length=4 ,max_length=4, min_value=1800)
    cvv = IntField(required=True, min_length=3, max_length=3)

class Producto(Document):
    codigo = IntField(min_value=0, unique=True, barcode="EAN13")
    nombre =  StringField(required = True)
    categoria = IntField(min_value=0,required = True)
    categorias = ListField(IntField(min_value=0, max_value=1000))

    def clean(self):
        if self.categorias:
            if(self.categoria != self.categorias[0]):
                raise ValidationError("La categoria principal no coincide con la primera")
        cod = self.codigo//10
        if(self.codigo%10 != self.digito_control(cod) ):   #Le pasamos el numero sin el de control
            raise ValidationError("El digito de control no coincide")

    def crear_ean13(valor, archivo):
        ean = barcode.get('ean13', valor, writer=barcode.writer.ImageWriter())
        # mostramos el codigo de barras en consola
        return ean.to_ascii()

    def digito_control(self, digito):
        numero = self.invertir(digito)

        pares = self.suma_pares(digito)
        impares = self.suma_impares(digito)*3
        suma = pares+ impares
        dSuperior = suma
        while dSuperior % 10 != 0:
            dSuperior+=1

        dc = dSuperior - suma
        return dc
    
        
        #Por ejemplo, para 123456789041 el dígito de control será:
        #Numeramos de derecha a izquierda: 140987654321
        #Suma de los números en los lugares impares: 1+0+8+6+4+2 = 21
        #Multiplicado (por 3): 21 × 3 = 63
        #Suma de los números en los lugares pares: 4+9+7+5+3+1 = 29
        #Suma total: 63 + 29 = 92
        #Decena inmediatamente superior = 100
        #Dígito de control: 100 - 92 = 8
        #El código quedará así: 1234567890418.
    
    def invertir(self, a):
        return int(str(a)[::-1])
        
    def suma_pares(self, numero):
        i = 0
        suma = 0
        aux=str(numero)
        while i <= len(str(numero)) - 1:
            suma+=int(aux[i])
            i += 2
        return suma
            
    def suma_impares(self, numero):
        i = 1
        suma = 0
        aux=str(numero)
        while i <= len(str(numero)) - 1:
            suma+=int(aux[i])
            i += 2
        return suma
    

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
    dni = EmbeddedDocumentField(Dni, required=True, unique=True)
    nombre = StringField(required = True)
    apellido_1 = StringField(required = True)
    apellido_2 = StringField()
    fecha_nac = DateTimeField(required = True)
    fecha_accesos = ComplexDateTimeField(max_length = 10)
    tarjetas = ListField(ReferenceField(Tarjeta, reverse_delete_rule = CASCADE))
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=CASCADE))


def insertar():


    producto = Producto(codigo = 1234567890418, nombre="producto1", categoria=1, categorias = [1,2,3])
    producto.drop_collection()
    producto.save()
    producto2 = Producto(codigo = 7702004003508, nombre="producto2", categoria=1).save()
   

    linea = Linea_Pedido(cantidad_productos=2, precio_producto=2, nombre_producto="producto1", total=4, referencia_producto=producto)
    linea.drop_collection()
    linea.save()
    linea2 = Linea_Pedido(cantidad_productos=1, precio_producto=1, nombre_producto="producto2", total=1, referencia_producto=producto2).save()
    linea3 = Linea_Pedido(cantidad_productos=1, precio_producto=2, nombre_producto="producto1", total=2, referencia_producto=producto).save()
    linea4 = Linea_Pedido(cantidad_productos=3, precio_producto=1, nombre_producto="producto2", total=3, referencia_producto=producto2).save()

    
    pedido = Pedido(total=5, fecha=datetime.datetime.now(),linea_pedido=[linea,linea2])
    pedido.drop_collection()
    pedido.save()
    pedido2 = Pedido(total=5, fecha=datetime.datetime.now(),linea_pedido=[linea3,linea4]).save()
    pedido3 = Pedido(total=7, fecha=datetime.datetime.now(),linea_pedido=[linea4,linea]).save()
    pedido4 = Pedido(total=3, fecha=datetime.datetime.now(),linea_pedido=[linea3,linea2]).save()
   
    
    tarjeta = Tarjeta(nombre_propietario = 'Luis', numero = 0000000000000000, caducidad_mes = 12, caducidad_ano = 2016, cvv = 100)
    tarjeta.drop_collection()
    tarjeta.save()
    tarjeta2 = Tarjeta(nombre_propietario = 'Zinedine', numero = 0000000000000001, caducidad_mes = 11, caducidad_ano = 2016, cvv = 100).save()
    tarjeta3 = Tarjeta(nombre_propietario = 'Zinedine', numero = 0000000000000003, caducidad_mes = 10, caducidad_ano = 2016, cvv = 100).save()
    

    dni_ = Dni(numero = 97295845, letra = 'A')
    dni_2 = Dni(numero = 79870277, letra = 'V')
    
    
    usuario = Usuario(dni = dni_, nombre='Luis', apellido_1='Figo', apellido_2='Figuinio', fecha_nac = datetime.datetime(1960, 1, 5, 0, 0 ,0), fecha_accesos = datetime.datetime.now(), tarjetas = [tarjeta], pedidos = [pedido, pedido2])
    usuario.drop_collection()
    usuario.save()
    
    usuario2 = Usuario(dni = dni_2, nombre='Zinedine', apellido_1='Zidane', apellido_2='Zizou', fecha_nac = datetime.datetime(1981, 1, 5, 0, 0 ,0), fecha_accesos = datetime.datetime.now(), tarjetas = [tarjeta2, tarjeta3], pedidos = [pedido3, pedido4]).save()
    
    dni_.save()
    dni_2.save()

    # producto.drop_collection()
    # producto2.drop_collection()
    
    # tarjeta.drop_collection()

    # linea.drop_collection()
    # linea2.drop_collection()
    # linea3.drop_collection()
    # linea4.drop_collection()

    # pedido.drop_collection()
    
    # usuario.drop_collection()
   

if __name__ == "__main__":
    insertar()

