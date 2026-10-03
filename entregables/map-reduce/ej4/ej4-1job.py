from pathlib import Path
from MRE import Job

inputDirEstandar = str(Path(__file__).parent.parent / "input_estandar")
inputDirPlatinium = str(Path(__file__).parent.parent / "input_platinium")
inputDirPremium = str(Path(__file__).parent.parent / "input_premium")
outputDir = str(Path(__file__).parent / "output_ej4")


def mapEstandar(key, values, context):
    id_local = key
    valores = values.split()
    id_visitante = valores[0]
    context.write(id_local, "ESTANDAR")
    context.write(id_visitante, "ESTANDAR")

def mapPremium(key, values, context):
    valores = values.split()
    id_visitante = valores[0]
    context.write(id_visitante, "PREMIUM")

def mapPlatinium(key, values, context):
    id_local = key
    context.write(id_local, "PLATINIUM")

def combiner(key, values, context):
    for etiqueta in set(values):
        context.write(key, etiqueta)

def reduce(key, values, context):
    premium = False
    estandar = False
    platinium = False
    for etiqueta in values:
        if etiqueta == "PREMIUM":
            premium = True
        if etiqueta == "ESTANDAR":
            estandar = True
        if etiqueta == "PLATINIUM":
            platinium = True
    if platinium and not premium and not estandar:
        context.write(key, "CUMPLE CONDICION")
    elif premium and not platinium and not estandar:
        context.write(key, "CUMPLE CONDICION")
    elif estandar and not platinium and not premium:
        context.write(key, "CUMPLE CONDICION")

job = Job(inputDirEstandar, outputDir, mapEstandar, reduce)
job.addInputPath(inputDirPremium, mapPremium)
job.addInputPath(inputDirPlatinium, mapPlatinium)
job.setCombiner(combiner)
success = job.waitForCompletion()
