from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "wordcount")
outputDir = str(root_path / "top-20")


def fmap(key, value, context):
    words = value.split()
    for w in words:
        context.write("top-20", (int(value), w))


def fred(key, values, context):
    top_20 = sorted(values, reverse=True)[:20]
    for cantidad, palabra in top_20:
        context.write(palabra, cantidad)


job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()