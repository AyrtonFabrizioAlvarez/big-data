from pathlib import Path

from pyspark import SparkContext



sc = SparkContext("local[*]", "Ejercicio 2")

base_dir = Path(__file__).parent
zootopia_dir = base_dir / "dataset.txt"

def parser(x):
    x = x.split("\t")
    return (x[4], x[0]) 

datos = sc.textFile(str(zootopia_dir))
datos = datos.map(parser)
datos = datos.filter(lambda x: x[0] != "" and x[0] != "Otro")
datos = datos.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b)


print(datos.top(3, key=lambda x: x[1]))