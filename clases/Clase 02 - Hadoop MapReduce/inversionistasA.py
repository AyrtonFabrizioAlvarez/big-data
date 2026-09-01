from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Inversionistas")
outputDir = str(root_path / "inversionistasA")

def fmap(key, value, context):
    dni = key
    values = value.split()
    nombre = values[0]
    context.write("menor", (nombre,dni))

def fred(key, values, context):
    max = -1
    nombre_max = ""
    for nombre, dni in values:
        if int(dni) > max:
            max = int(dni)
            nombre_max = nombre
    context.write(nombre_max, max)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()