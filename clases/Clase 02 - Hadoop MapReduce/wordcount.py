from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Libros")
outputDir = str(root_path / "wordcount")

print(root_path)
print(inputDir)
print(outputDir)

print("------------------------------")

def fmap(key, value, context):
    words = value.split()
    for w in words:
        context.write(w, 1)


def fred(key, values, context):
    c = 0
    for v in values:
        c = c + 1
    context.write(key, c)


job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()