from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Banco")
outputDir = str(root_path / "outputEj1")

def map(key, values, context):
    words = values.split()
    for w in words:
        context.write(w[0], 1)

def reduce(key, values, context):
    c = 0
    for v in values:
        c += 1
    context.write(key.lower(), c)

def shuffle(k1, k2):
    if k1.lower() == k2.lower():
        return 0
    elif k1.lower() < k2.lower():
        return -1
    else:
        return 1

def sort(k1, k2):
    if k1.lower() == k2.lower():
        return 0
    elif k1.lower() < k2.lower():
        return -1
    else:
        return 1

job = Job(inputDir, outputDir, map, reduce)
job.setShuffleCmp(shuffle)
job.setSortCmp(sort)

success = job.waitForCompletion()
print(success)
