from pathlib import Path
from MRE import Job

inputDirEstandar = str(Path(__file__).parent.parent / "input_estandar")
inputDirPlatinium = str(Path(__file__).parent.parent / "input_platinium")
inputDirPremium = str(Path(__file__).parent.parent / "input_premium")
outputDir1 = str(Path(__file__).parent / "output_parte1")
outputDir2 = str(Path(__file__).parent / "output_parte2")
outputDir3 = str(Path(__file__).parent / "output_parte3")
outputDir4 = str(Path(__file__).parent / "output_parte4")

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

def reduce1(key, values, context):
    cumple = True
    for etiqueta in values:
        if etiqueta == "PREMIUM" or etiqueta == "ESTANDAR":
            cumple = False
            break
    if cumple:
        context.write(key, "CUMPLE 'PLATINIUM - (PREMIUM U ESTANDAR)'")

job1 = Job(inputDirEstandar, outputDir1, mapEstandar, reduce1)
job1.addInputPath(inputDirPremium, mapPremium)
job1.addInputPath(inputDirPlatinium, mapPlatinium)
job1.setCombiner(combiner)
success = job1.waitForCompletion()

def reduce2(key, values, context):
    cumple = True
    for etiqueta in values:
        if etiqueta == "ESTANDAR" or etiqueta == "PLATINIUM":
            cumple = False
            break
    if cumple:
        context.write(key, "CUMPLE 'PREMIUM - (PLATINIUM U ESTANDAR)'")


job2 = Job(inputDirEstandar, outputDir2, mapEstandar, reduce2)
job2.addInputPath(inputDirPremium, mapPremium)
job2.addInputPath(inputDirPlatinium, mapPlatinium)
job2.setCombiner(combiner)
success = job2.waitForCompletion()

def reduce3(key, values, context):
    cumple = True
    for etiqueta in values:
        if etiqueta == "PREMIUM" or etiqueta == "PLATINIUM":
            cumple = False
            break
    if cumple:
        context.write(key, "CUMPLE 'ESTANDAR - (PLATINIUM U PREMIUM)'")


job3 = Job(inputDirEstandar, outputDir3, mapEstandar, reduce3)
job3.addInputPath(inputDirPremium, mapPremium)
job3.addInputPath(inputDirPlatinium, mapPlatinium)
job3.setCombiner(combiner)
success = job3.waitForCompletion()

def map(key, values, context):
    id_equipo = key
    context.write(id_equipo, 1)

def reduce4(key, values, context):
    context.write(key, "CUMPLE CONDICION")

job4 = Job(outputDir1, outputDir4, map, reduce4)
job4.addInputPath(outputDir2, map)
job4.addInputPath(outputDir3, map)
success = job4.waitForCompletion()
