from pathlib import Path
from MRE import Job

# b. El usuario que más páginas distintas visitó (<id_user, id_page, time>)

root_path = Path(__file__).parent

inputDir = str(root_path / "website")
tmpDir = str(root_path / "tmpEj5b")
outputDir = str(root_path / "outputEjb")


# JOB 1

def fmap(key, value, context):
    id_user = key
    id_page, time = value.split()
    context.write(id_user, id_page)


def fcomb(key, values, context):
    paginas_visitadas = set()
    for v in values:
        paginas_visitadas.add(v)
    for p in paginas_visitadas:
        context.write(key, p)

def fred(key, values, context):
    paginas_visitadas = set()
    for v in values:
        paginas_visitadas.add(v)
    context.write(key, len(paginas_visitadas))
    

job = Job(inputDir, tmpDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()

# JOB 2

def fmap(key, value, context):
    id_user = key
    paginas_visitadas = value
    context.write("total", (id_user, paginas_visitadas))

def fred(key, values, context):
    max_paginas = -1
    max_user = None
    for v in values:
        id_user, paginas_visitadas = v
        if int(paginas_visitadas) > max_paginas:
            max_paginas = int(paginas_visitadas)
            max_user = id_user
    context.write(key, (max_user, max_paginas))

job = Job(tmpDir, outputDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()