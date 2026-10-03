from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "input_ej1")
outputDir = str(root_path / "output_ej1")

def map(key, values, context):
    id_local = key
    valores = values.split()
    id_visitante = valores[0]
    apuestas_local = int(valores[1])
    apuestas_visitante = int(valores[2])
    if apuestas_local > context["PARAMETRO"]:
        context.write(id_local, apuestas_local)
    if apuestas_visitante > context["PARAMETRO"]:
        context.write(id_visitante, apuestas_visitante)

def reduce(key, values, context):
    context.write(key, 1)

job = Job(inputDir, outputDir, map, reduce)
job.setParams({"PARAMETRO": 4799})
job.setCombiner(reduce)
success = job.waitForCompletion()
print(success)