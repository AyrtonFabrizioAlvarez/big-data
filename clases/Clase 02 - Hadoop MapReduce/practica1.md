# Conceptos y aplicaciones en Big Data

## Práctica 1–Paradigma Map Reduce

### 1) Dado el siguiente dataset:

| Split 1   | Split 2   | Split 3   | Split 4   |
| --------- | --------- | --------- | --------- |
| Key Value | Key Value | Key Value | Key Value |
| 34 21     | 23 45     | 3 21      | 30 91     |
| 21 34     | 12 12     | 15 10     | 31 32     |
| 10 18     | 36 18     | 14 18     | 32 53     |
| 32 45     | 4 97      | 3 15      | 19 35     |

#### Responda para cada job:

- ¿Cuántas veces (invocaciones) se ejecuta la función map?
- ¿Cuántas veces (invocaciones) se ejecuta la función reduce?
- ¿Cuántos mappers se ejecutan?
- ¿Cuántos reducersse ejecutan?
- ¿Qué datos recibe cada función reduce?
- ¿Cuál es la salida de cada job?

```
# JOB A
def map(k1, v1, context):
	context.write(1, v1)
def reduce(k2, v2, context):
	n = 0
	for v in v2:
		n = n + 1
	context.write(k2, n)

- invocaciones funcion map:
    - 16 (1 por cada fila de data) 4splitX4filas
- invocaciones funcion reduce:
    - 1 (siempre se usa la misma clave "1")
- mappers ejecutados:
    - 4 (1 en paralelo por cada split de data)
- reducers ejecutados:
    - 1 (existe una sola clave)
- datos que recibe funcion reduce:
    - <1, [21, 34, 18, 45, 45, 12, 18, 97, 21, 10, 18, 15, 91, 32, 53, 35]>
- salida:
    - <1,16>
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

- invocaciones funcion map:
    - 16 (1 por cada fila de data)
- invocaciones funcion reduce:
    - 1 (siempre se usa la misma clave "1")
- mappers ejecutados:
    - 4 (1 en paralelo por cada split de data)
- reducers ejecutados:
    - 1 (existe una sola clave)
- datos que recibe funcion reduce:
    - <1, [21, 34, 18, 45, 45, 12, 18, 97, 21, 10, 18, 15, 91, 32, 53, 35]>
- salida:
    - <1, 565>
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

- invocaciones funcion map:
    - 16 (1 por cada fila de data)
- invocaciones funcion reduce:
    - 2 (tenemos 2 etiqueras "1" y "2")
- mappers ejecutados:
    - 4 (1 por cada split de data)
- reducers ejecutados:
    - 2 (tenemos 2 etiquetas "1" y "2")
- datos que recibe funcion reduce:
    - <1, [34,10,12,36,3,15,14,3]>
    - <2, [21,32,23,4,30,31,32,19]>
- salida:
    - <1, 36>
    - <2, 32>
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

- invocaciones funcion map:
    - 16 (1 por cada fila de data)
- invocaciones funcion reduce:
    - 14 (1 por cada "key" unicas)
- mappers ejecutados:
    - 4 (1 por cada split de data)
- reducers ejecutados:
    - 14 (1 por cada "key" unicas)
- datos que recibe funcion reduce:
    - <34, [21,21,21...21]> - 21 veces
    - <21, [34,34,34...34]> - 34 veces
    - <10, [18,18,18...18]> - 18 veces
    - <32, [45,45,45...45,53,53,53...53]> - 45 veces 45 + 53 veces 53
    - <23, [45,45,45...45]> - 45 veces
    - <12, [12,12,12...12]> - 12 veces
    - <36, [18,18,18...18]> - 18 veces
    - <4, [97,97,97...97]> -  97 veces
    - <3, [21,21,21...21,15,15,15...15]> - 21 veces 21 + 15 veces 15
    - <15, [10,10,10...10]> - 10 veces
    - <14, [18,18,18...18]> - 18 veces
    - <30, [91,91,91...91]> - 91 veces
    - <31, [32,32,32...32]> - 32 veces
    - <19, [35,35,35...35]> - 35 veces
- salida:
    - <34, 21>
    - <21, 34>
    - <10, 18>
    - <32, 98>
    - <23, 45>
    - <12, 12>
    - <36, 18>
    - <4, 97>
    - <3, 36>
    - <15, 10>
    - <14, 18>
    - <30, 91>
    - <31, 32>
    - <19, 35>
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

- invocaciones funcion map:
    - 16 (1 por cada fila de data)
- invocaciones funcion reduce:
    - 12 (1 por cada "value" unico)
- mappers ejecutados:
    - 4 (1 por cada split de data)
- reducers ejecutados:
    - 12 (1 por cada "value" unico)
- datos que recibe funcion reduce:
    - <21,[34,3]>
    - <34,[21]>
    - <18,[10,36,14]>
    - <45,[32,23]>
    - <12,[12]>
    - <97,[4]>
    - <10,[15]>
    - <15,[3]>
    - <91,[30]>
    - <32,[31]>
    - <53,[32]>
    - <35,[19]>
- salida:
    - <34,1>
    - <3,2>  
    - <21,1>
	- <10,1>
    - <36,2>
    - <14,3>
    - <32,1>
    - <23,2>
    - <12,1>
    - <4,1>
    - <3,1>
    - <30,1>
    - <31,1>
    - <32,1>
    - <19,1>
```

### 2) El dataset Libros provisto por la cátedra almacena libros cada uno en un archivo separado. Dentro de cada archivo, la primera línea tiene el título del libro y luego en las líneas siguientes un párrafo por línea. Ejecute el proyecto WordCount dado por la cátedra para saber cuántas veces es utilizadacada palabra.

### 3) En el ejercicio anterior¿Cómo haría para obtener el top 20 de las palabras más usadas?

### 4) Modifique el proyecto WordCount para contar cuántas vocales, consonantes, dígitos, espacios y otros caracteres posee el data setLibros.

### 5) Indique siutilizando el datasetLibros es posible resolver los siguientes problemas:

- **a. Obtener los títulos de todos los libros**
  - No es posible ya que como el emulador provisto por la catedra maneja siempre el mismo offset acumulativo no se puede detectar el byte 0 de cada split donde <k1,v1> = <0, "titulo> ya que el titulo es la primera línea y segun internet MapReduce en el Map recibe el numero de byte como key
- **b. Obtener la cantidad de palabras promedio por párrafo**
  - si, cada funcion map para cada linea **(linea==parrafo)** calcula y devuelve <k,cant_palabras> (de cada párrafo obtendríamos la cantidad total de palabras bajo una key única)
  - la funcion reduce (1 sola) va a ir llevando 2 contadores (total de palabras y cantidad de parrafos), al final dividir el total de palabras por la cantidad de parrafos
- **c. Obtener la cantidad de párrafos promedio por libro**
  - No es posible ya que las funciones map se ejecutan de manera aislada y no mantienen un estado, pro esto un funcion map que lee un parrafo random del quijote no podría al menos en el emulador saber a que libro le pertenece
- **d. Obtener la cantidad de caracteres del párrafo más extenso**
  - Si es posible, en la funcion map se calculará el largo de cada párrafo
  - en la funcion reduce se calculara el máximo y  tendra como output la cantidad de caracteres que previamente dijo el mapper
- **e. Cantidad total de párrafos con diálogos(se entiendepor párrafo con diálogo aquel que empieza con un guión)**
  - Si es posible, en la funcion map se verifica si el primer caracter es un "-" (.startswith()), en ese caso se escribe <"dialogo", 1>
  - la funcion reduce hace un conteo de la cantidad de "dialogo"
- **f. El diálogo más largo (se entiende por diálogo a una secuencia de párrafos con diálogo que aparecen de manera consecutiva)**
  - No se puede, por el aislamiento y la falta de estado no podríamos detectar la consecutividad de los parrafos
- **g. El top 20 de las palabras más usadas por cada libro**
  - No se puede, por el aislamiento y la falta de estado no podríamos llevar un conteo por libro, al parecer fuera del emulador en un ambiente real si se podría

### 6) Una empresa proveedora de internet realizó una encuesta para conocer el grado de satisfacción de sus clientes, en un formulario web los clientes debían completar un campo con los textos "Muy satisfecho", "Algo satisfecho", "Poco satisfecho", “Disconforme”o"Muy disconforme". Utilice el dataset Encuesta para saber cuántos clientes están en cada una de las cinco categorías.

### 7) El dataset Inversionistas posee los nombres, dni, fecha de nacimiento(día, mes y año como campos separados) e importe invertido por diferentes personas en laapertura de un nuevo negocio en la ciudad. Se desea saber:

- **a. El nombre del inversionista más joven**
- **b. El total delimporteinvertido por todos los inversionistas**
- **c. El promedio de edad Implemente una solución en MapReduce.**
- **¿Se puede resolver los tres problemasen un único job?**

### 8) Si contáramos con un cluster donde podemos configurar 100 nodos para la tarea de reduce ¿De qué manera se podrían usar esos 100 nodos en el ejemplo de los eventos POSITIVO, NEGATIVO y NEUTRO visto en la teoría?

Este ejercicio apunta a que nuestros mappers no trabajen con 3 key unicas como podrian ser POSITIVO, NEGATIVO y NEUTRO, porque de esa manera solo trabajarian 3 nodos en reduce, la estrategia para esto seria poder agregar un salt random a cada una de las claves intermedias generadas (POSITIVO_1, NEGATIVO_15, NEUTRO_23), de esta manera manejando ese salt de manera random para cada una de las etiquetas base tendriamos hasta 33 de cada una, de esa manera trabajariamos con hasta 99 nodos reduce
