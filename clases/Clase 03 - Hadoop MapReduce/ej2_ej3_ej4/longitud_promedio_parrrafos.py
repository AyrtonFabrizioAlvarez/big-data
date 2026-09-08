from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "input")
tmpDir = str(root_path / "tmpEj4")
outputDir = str(root_path / "outputEj4")


# JOB 1

def fmap(key, value, context):
    context.write("caracteres", len(value))

def fred(key, values, context):
    total_caracteres = 0
    total_parrafos = 0
    for v in values:
        total_parrafos += 1
        total_caracteres += int(v)
    context.write("promedio", total_caracteres / total_parrafos)

job1 = Job(inputDir, tmpDir, fmap, fred)
success = job1.waitForCompletion()

import math

promedio = 0
archivo_stats = Path(tmpDir) / "output.txt"

with open(archivo_stats, "r", encoding="utf-8") as f:
    for linea in f:
        clave, valor = linea.strip().split("\t")
        if clave == "promedio":
            promedio = float(valor)

# JOB 2

def fmap(key, value, context):
    if len(value) > promedio:
        context.write("parrafo", value)

def fred(key, values, context):
    for parrafo in values:
        context.write(len(parrafo), parrafo)

job2 = Job(inputDir, outputDir, fmap, fred)
success = job2.waitForCompletion()