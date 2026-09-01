from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Inversionistas")
outputDir = str(root_path / "inversionistasB")

def fmap(key, value, context):
    values = value.split()
    invertido = values[4]
    context.write("invertido", invertido)

def fred(key, values, context):
    total = 0
    for v in values:
        total = total + int(v)
    context.write(key, total)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()