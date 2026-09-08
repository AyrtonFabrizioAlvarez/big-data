from pathlib import Path
from MRE import Job

# c. La página más visitada (en cuanto a cantidad de visitas, sin importar el tiempo de permanencia) por todos los usuarios. (<id_user, id_page, time>)

root_path = Path(__file__).parent
inputDir = str(root_path / "website")
tmpDir = str(root_path / "tmpEj5c")
outputDir = str(root_path / "outputEj5c")


# JOB 1

def fmap(key, value, context):
    pagina = value.split()[0]
    context.write(pagina, 1)

def fred(key, values, context):
    c = 0
    for v in values:
        c = c + int(v)
    context.write(key, c)

job = Job(inputDir, tmpDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()

# JOB 2

def fmap(key, value, context):
    context.write("total", (key, value))

def fred(key, values, context):
    max  = -1
    max_page = None
    for v in values:
        id_page, visitas = v
        if int(visitas) > max:
            max = int(visitas)
            max_page = id_page
    context.write(key, (max_page, max))

job = Job(tmpDir, outputDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()