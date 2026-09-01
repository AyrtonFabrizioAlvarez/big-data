from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Libros")
outputDir = str(root_path / "wordcount2")

print(root_path)
print(inputDir)
print(outputDir)

print("------------------------------")

def fmap(key, value, context):
    for char in value:
        if char.isalpha():
            if char.lower() in "aeiouáéíóúü":
                context.write("vocales", 1)
            else:
                context.write("consonantes", 1)
        elif char.isdigit():
            context.write("dígitos", 1)
        elif char.isspace():
            context.write("espacios", 1)
        else:
            context.write("otros", 1)


def fred(key, values, context):
    c = 0
    for v in values:
        c = c + 1
    context.write(key, c)


job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()