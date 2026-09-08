# Practica 2

## 1. ¿En el dataset del ejercicio 1 de la práctica 1 indique para cada Job, si se vería beneficiado por una función combiner? En caso afirmativo, ¿cuál es la implementación de dicha función? ¿Qué datos recibe cada reduce, al utilizar la función combiner?

```
# JOB A
def map(k1, v1, context):
	context.write(1, v1)
def reduce(k2, v2, context):
	n = 0
	for v in v2:
		n = n + 1
	context.write(k2, n)

En este JOB no se beneficia de tener una funcion combiner porque existe la posibilidad de que MapReduce no lo ejecute nunca, en este escenario 
si usaramos un combiner deberiamos hacer que el bucle for haga "n = n + v" tanto en combiner como en reduce, pero si el mapper no se ejecuta 
el reduce estaria sumando los valores erroneos ya que su entrada seria <1, [W, X, Y, Z]>
```

```

# JOB B
def map(k1, v1, context):
	context.write(1, v1)
def reduce(k2, v2, context):
	n = 0
	for v in v2:
		n = n + v
	context.write(k2, n)

Este JOB si se beneficiaria de un cobiner ya que la funcionalidad del reduce en este caso es sumar todos los valores que lee el map y no un contador 
de cantidades, entonces aca podríamos sumar un combiner que haga exactamente lo mismo que el reduce y va a ser como una suma "intermedia" de los 
valores que tiene cada split.

def combiner(k2, v2, context):
	n = 0
	for v in v2:
		n = n + v
	context.write(k2, n)
```

```
#JOB C
def map(k1, v1, context):
	if (v1 < 30):
		context.write(1, k1)
	else:
		context.write(2, k1)
def reduce(k2, v2, context):
	max =-1
	for v in v2:
		if(v > max):
			max = v
	context.write(k2,max)

Este JOB se beneficiaria de un combiner ya que esta calculando máximos, en ese caso, cada combiner calcularia el maximo "intermedio" o de cada split 
por separado y luego el reduce haria el máximo entre cada una de las salidas de los combiner.

def combiner(k2, v2, context):
	max =-1
	for v in v2:
		if(v > max):
			max = v
	context.write(k2,max)
```

```
# JOB D
def map(k1, v1, context):
	for v in range(v1):
		context.write(k1, v1)
def reduce(k2, v2, context):
	n = 0
	for v in v2:
		n = n + 1
	context.write(k2, n)

Este JOB no se beneficiaria, por como esta el map las salidas serian por ejemplo <34, 21> (21 veces) y el reduce recibiria <34, [21...21]>, 
si de manera intermedia tuvieramos el combiner el reduce recibiria <34, 21> y terminaria dando un output de <34, 1> lo cual sería incorrecto
```

```
# JOB E
def map(k1, v1, context):
	context.write(v1, k1)
def reduce(k2, v2, context):
	n = 0
	for v in v2:
		n = n + 1
		context.write(v, n)

Este JOB no se beneficiaria de un combiner, ya que por ejemplo en la fase map obtendriamos <18, 10>, <18, 36>, <18, 14>, el reduce para esto recibe 
<18, [10,36,14]> y su salida seria <10, 1>, <36, 2>, <14, 3>, si nosotros sumaramos un combiner lo que pasaria es que al recibir la salida de la fase 
map el combiner tendria como salida <10, 1>, <36, 1>, <14, 1>, y si eso lo toma el reduce su salida seria <1, 1>, <1, 1>, <1, 1>
```

## 2. Implemente una función combiner para el problema del WordCount.

## 3. Implemente un job MapReduce para calcular el máximo, mínimo, promedio y desvío stándard de las ocurrencias de todas las palabras del dataset Libros.

## 4. Utilice el dataset Libros para implementar una aplicación MapReduce que devuelva como salida todos los párrafos que tienen una longitud mayor al promedio.

## 5. El dataset website tiene información sobre el tiempo de permanencia de sus usuariosen cada una de las páginas del sitio. El formato de los datos del dataset es: <id_user, id_page, time>

#### Implemente una aplicación MapReduce, utilizando combiners en los casos que considere necesario, que calcule

* **a. La página más visitada (la página en la que más tiempo permaneció) para cada usuario**
* **b. El usuario que más páginas distintas visitó**
* **c. La página más visitada (en cuanto a cantidad de visitas, sin importar el tiempo de permanencia) por todos los usuarios.**

#### Indique como queda el DAG del proceso completo (las tres consultas)

## 6. Cómo plantearía una solución MapReduce a los siguientes algoritmos secuenciales:

```
a.
	i. entrada
		textos: array [1..N] of string (dataset libros)
	ii. algoritmo
		a={}; b={}; N = len(textos)
		for l in textos:
			words = l.split()
			for w in words:
				a[w] = a[w]+1
		for w in a.keys():
			for l in lines:
				words = l.split()
				if w in words:
					b[w]=b[w]+1
        for k in a.keys():
			print(k + " = " + str(a[w] * (N / b[w])))
```

```
b.
	i. entrada
		datos: array [1..N] of <int1, int2, ..., intM>
			(todos los valores están dentro de un rango de valores conocido, para poder usarlos como índices del tensor)
	ii. algoritmo
    	for t in datos:
        	v = t.split("\t")
            c = v[-1]
            for a in range(len(v)-1):
            	x= v[a]
				m[a][x][c] = m[a][x][c] + 1
            
          max=[[0,0,0], [0,0,0]]
          for x in range(len(m)):
          	  for y in range(len(m[0])):
              	  for z in range(2):
                	  if(m[x][y][z] > max[z][0]):
                    	  max[z][0] = m[x][y][z]
                          max[z][1]=x
                          max[z][2]=y
          for z in range(2):
			  print(z +";" + max[z][1] +";" + max[z][2])
```
