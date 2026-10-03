from pathlib import Path
from MRE import Job



inputDirPlatinium = str(Path(__file__).parent.parent / "input_platinium")
inputDirPremium = str(Path(__file__).parent.parent / "input_premium")
outputDir = str(Path(__file__).parent / "output_ej3")

def mapPremium(key, values, context):
    id_local = key
    valores = values.split()
    apuestas_local = int(valores[1])
    apuestas_visitante = int(valores[2])
    if apuestas_local > context["PARAMETRO"] * apuestas_visitante:
        context.write(id_local, "PREMIUM")

def mapPlatinium(key, values, context):
    id_local = key
    valores = values.split()
    apuestas_local = int(valores[1])
    apuestas_visitante = int(valores[2])
    if apuestas_local > context["PARAMETRO"] * apuestas_visitante:
            context.write(id_local, "PLATINIUM")

def combiner(key, values, context):
    for etiqueta in set(values):
        context.write(key, etiqueta)

def reduce(key, values, context):
    cumple = True
    for etiqueta in values:
        if etiqueta == "PREMIUM":
            cumple = False
            break
    if cumple:
        context.write(key, "CUMPLE DIFERENCIA")

job = Job(inputDirPremium, outputDir, mapPremium, reduce)
job.addInputPath(inputDirPlatinium, mapPlatinium)
job.setCombiner(combiner)
job.setParams({"PARAMETRO": 2})
success = job.waitForCompletion()
print(success)