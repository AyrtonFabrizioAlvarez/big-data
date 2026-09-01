from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Libros")
outputDir = str(root_path / "titulos-libros")


def fmap(key, value, context):
    print(int(key))
    if int(key) == 0:
        context.write("titulo", value)


def fred(key, values, context):
    for v in values:
        context.write(key, v)


job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()