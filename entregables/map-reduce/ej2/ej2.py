from pathlib import Path
from MRE import Job


inputDirEstandar = str(Path(__file__).parent.parent / "input_estandar")
inputDirPlatinium = str(Path(__file__).parent.parent / "input_platinium")
outputDir = str(Path(__file__).parent / "output_ej2")

def mapEstandar(key, values, context):
    valores = values.split()
    id_visitante = valores[0]
    apuestas_local = int(valores[1])
    apuestas_visitante = int(valores[2])
    if apuestas_visitante > apuestas_local:
        context.write(id_visitante, "ESTANDAR")

def mapPlatinium(key, values, context):
    valores = values.split()
    id_visitante = valores[0]
    apuestas_local = int(valores[1])
    apuestas_visitante = int(valores[2])
    if apuestas_visitante > apuestas_local:
            context.write(id_visitante, "PLATINIUM")

def combiner(key, values, context):
    for etiqueta in set(values):
        context.write(key, etiqueta)

def reduce(key, values, context):
    estandar = False
    platinium = False
    for etiqueta in values:
        if etiqueta == "ESTANDAR":
            estandar = True
        if etiqueta == "PLATINIUM":
            platinium = True
        if estandar and platinium:
            context.write(key, "CUMPLE INTERSECCION")
            break

job = Job(inputDirEstandar, outputDir, mapEstandar, reduce)
job.addInputPath(inputDirPlatinium, mapPlatinium)
job.setCombiner(combiner)
success = job.waitForCompletion()
print(success)