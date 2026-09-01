from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Inversionistas")
outputDir = str(root_path / "inversionistas_completo")

def fmap(key, value, context):
    dni = key
    values = value.split()
    nombre = values[0]
    año = values[3]
    invertido = values[4]
    context.write("completo", (nombre, dni, 2026-int(año), invertido))

def fred(key, values, context):
    suma_edades = 0
    total_personas = 0
    max = -1
    nombre_max = ""
    total_invertido = 0
    for nombre, dni, edad, invertido in values:
        if int(dni) > max:
            max = int(dni)
            nombre_max = nombre
        suma_edades = suma_edades + int(edad)
        total_personas = total_personas + 1
        total_invertido = total_invertido + int(invertido)
    context.write("mayor_dni", (nombre_max, max))
    context.write(key, suma_edades/total_personas)
    context.write("total_invertido", total_invertido)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()