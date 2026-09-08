from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "input")
outputDir = str(root_path / "outputEj2")


def fmap(key, value, context):
    words = value.split()
    for w in words:
        context.write(w, 1)


def fred(key, values, context):
    c = 0
    for v in values:
        c = c + int(v)
    context.write(key, c)


job = Job(inputDir, outputDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()