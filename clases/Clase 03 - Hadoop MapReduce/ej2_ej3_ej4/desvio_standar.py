from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "input")
tmpDir1 = str(root_path / "tmpEj3-1")
tmpDir2 = str(root_path / "tmpEj3-2")
outputDir = str(root_path / "outputEj3")


# JOB 1: WordCount

def fmap(key, value, context):
    words = value.split()
    for w in words:
        context.write(w, 1)

def fred(key, values, context):
    c = 0
    for v in values:
        c = c + int(v)
    context.write(key, c)

job1 = Job(inputDir, tmpDir1, fmap, fred)
job1.setCombiner(fred)
success = job1.waitForCompletion()


# JOB 2: Estadísticas

def fmap(key, value, context):
    context.write(1, (key, value))

def fred(key, values, context):
    max = -1
    max_word = ""
    min = 999999999
    min_word = ""
    total = 0
    cant = 0
    for v in values:
        cant = cant + 1
        total = total + int(v[1])
        if int(v[1]) < min:
            min = int(v[1])
            min_word = v[0]
        if int(v[1]) > max:
            max = int(v[1])
            max_word = v[0]
    context.write("total_palabras", total)
    context.write("cantidad_palabras", cant)
    context.write("promedio", total/cant)
    context.write("maximo", (max, max_word))
    context.write("minimo", (min, min_word))

job2 = Job(tmpDir1, tmpDir2, fmap, fred)
success = job2.waitForCompletion()


# JOB 3: Desvío estándar

import math

promedio_global = 0
cantidad_palabras = 0
archivo_stats = Path(tmpDir2) / "output.txt"

with open(archivo_stats, "r", encoding="utf-8") as f:
    for linea in f:
        partes = linea.strip().split("\t")
        if len(partes) == 2:
            clave, valor = partes
            if clave == "promedio":
                promedio_global = float(valor)
            elif clave == "cantidad_palabras":
                cantidad_palabras = int(valor)

def fmap(key, value, context):
    frecuencia = int(value)
    dif_cuadrado = (frecuencia - promedio_global) ** 2
    context.write("desvio", dif_cuadrado)

def fcomb(key, values, context):
    suma_parcial = 0
    for v in values:
        suma_parcial = suma_parcial + float(v)
    context.write(key, suma_parcial)

def fred(key, values, context):
    suma_total = 0
    for v in values:
        suma_total = suma_total + float(v)
        
    varianza = suma_total / (cantidad_palabras - 1)
    desvio_estandar = math.sqrt(varianza)
    
    context.write("desvio_estandar", desvio_estandar)

job3 = Job(tmpDir1, outputDir, fmap, fred)
job3.setCombiner(fcomb)
success = job3.waitForCompletion()
