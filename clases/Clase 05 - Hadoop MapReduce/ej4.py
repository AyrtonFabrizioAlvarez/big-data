from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent
inputDir = str(root_path / "website")
outputDirCount = str(root_path / "outputEj5" / "job1")
outputDirMedian = str(root_path / "outputEj5" / "job2")


def fmap(key, value, context):
    # cada línea cuenta como 1
    context.write(1, 1)

def fred(key, values, context):
    c = 0
    for v in values:
        c += 1
    context.write("N", c)

job = Job(inputDir, outputDirCount, fmap, fred)
job.waitForCompletion()


def fmap(key, value, context):
    columnas = value.split("\t")
    tiempo = columnas[1]   # columna con "tiempo de permanencia"
    context.write(tiempo, tiempo)

def fshuffle(aKey, anotherKey):
    # todos los valores van al mismo reducer
    return 0

def fsort(aKey, anotherKey):
    num1 = float(aKey)
    num2 = float(anotherKey)
    if num1 == num2:
        return 0
    elif num1 < num2:
        return -1
    else:
        return 1

def fred(key, values, context):
    N = context["N"]
    mediana = None
    i = 1
    if N % 2 == 0:
        valor_izq = None
        valor_der = None
        for v in values:
            if i == N//2:
                valor_izq = float(v)
            elif i == N//2 + 1:
                valor_der = float(v)
                break
            i += 1
        mediana = (valor_izq + valor_der) / 2
    else:
        for v in values:
            if i == (N+1)//2:
                mediana = float(v)
                break
            i += 1

    context.write("mediana", mediana)


N = None
with open(outputDirCount + "/output.txt", "r") as arch:
    linea = arch.readline()
    N = int(linea.split("\t")[1])

job = Job(inputDir, outputDirMedian, fmap, fred)
job.setShuffleCmp(fshuffle)
job.setSortCmp(fsort)
job.setParams({"N": N})
job.waitForCompletion()
