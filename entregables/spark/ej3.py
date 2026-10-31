from pathlib import Path

from pyspark import SparkContext


sc = SparkContext("local[*]", "Ejercicio 3")

franja_horaria = 3000
N = 30

base_dir = Path(__file__).parent
zootopia_dir = base_dir / "dataset.txt"

def parser(x):
    x = x.split("\t")
    return ((int(x[3]) // franja_horaria, x[0]), 1)

def parser2(x):
    return (x[0][0], 1)
    

datos = sc.textFile(str(zootopia_dir))
datos = datos.map(parser).reduceByKey(lambda a, b: a + b)

datos = datos.filter(lambda x: x[1] >= N)
datos = datos.map(parser2).reduceByKey(lambda a, b: a + b)


print(datos.take(20))