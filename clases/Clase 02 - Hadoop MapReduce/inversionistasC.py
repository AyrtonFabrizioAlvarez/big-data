from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Inversionistas")
outputDir = str(root_path / "inversionistasC")

def fmap(key, value, context):
    values = value.split()
    año = values[3]
    context.write("edad", 2026-int(año))

def fred(key, values, context):
    suma = 0
    total = 0
    for v in values:
        suma = suma + int(v)
        total = total + 1
    context.write(key, suma/total)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()