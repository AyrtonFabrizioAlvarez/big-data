from pathlib import Path
from MRE import Job

# a. La página más visitada (la página en la que más tiempo permaneció) para cada usuario (<id_user, id_page, time>)

root_path = Path(__file__).parent

inputDir = str(root_path / "website")
tmpDir = str(root_path / "tmpEj5a")
outputDir = str(root_path / "outputEj5a")

# JOB 1: Calcular el tiempo total de permanencia de cada usuario en cada página

def fmap(key, value, context):
    id_user = key
    id_page, time = value.split()
    context.write((id_user, id_page), time)


def fred(key, values, context):
    total_time = 0
    for v in values:
        total_time += int(v)
    context.write(key, total_time)
    

job = Job(inputDir, tmpDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()

# JOB 2: Calcular la página más visitada por cada usuario

def fmap(key, value, context):
    id_user = key
    id_page, time = value.split()
    context.write(id_user, (id_page, time))

def fred(key, values, context):
    max  = -1
    max_page = None
    for v in values:
        id_page, time = v
        if int(time) > max:
            max = int(time)
            max_page = id_page
    context.write(key, (max_page, max))

job = Job(tmpDir, outputDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()