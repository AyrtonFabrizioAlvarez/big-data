from pathlib import Path

from pyspark import SparkContext


sc = SparkContext("local[*]", "Ejercicio 4")

base_dir = Path(__file__).parent
zootopia_dir = base_dir / "dataset.txt"

def parser(x):
    x = x.split("\t")
    return (x[0], (int(x[3]), x[4]))

def parser2(x):
    return (x[0], x[1][0])

datos = sc.textFile(str(zootopia_dir))
datos = datos.map(parser) # (idVehiculo, (timestamp, destino))

datos_con_destino = datos.filter(lambda x: x[1][1] != "")
datos_con_destino = datos_con_destino.map(parser2) # (idVehiculo, timestampDestino)

datos_join = datos.map(lambda x: (x[0], x[1][0])).join(datos_con_destino) # (idVehiculo, (timestamp, timestampDestino))
datos_join = datos_join.filter(lambda x: x[1][0] < x[1][1])
datos_join = datos_join.map(lambda x: ( (x[0], x[1][0]), x[1][1] )) # ((idVehiculo, timestamp), timestampDestino)
datos_join = datos_join.reduceByKey(lambda x, y: x if x < y else y)
datos_join = datos_join.map(lambda x: ( (x[0][0], x[1]), x[0][1])) # ((idVehiculo, timestampDestino), timestamp)

datos_velocidades = datos_join.aggregateByKey(
    (99999, 0),
    (lambda res, ori: (res[0] if res[0] < ori else ori, res[1] + 1)),
    (lambda res1, res2: (res1[0] if res1[0] < res2[0] else res2[0], res1[1] + res2[1]))
) # ((idVehiculo, timestampDestino), (timestampMinimo, cantidadDeRegistros))

datos_velocidades = datos_velocidades.map(lambda x: (x[0][0], (x[0][1] - x[1][0]) / x[1][1]))

datos_final = datos_velocidades.aggregateByKey(
    (0,0),
    (lambda res, ori: (res[0] + ori, res[1] + 1)),
    (lambda res1, res2: (res1[0] + res2[0], res1[1] + res2[1]))
)
datos_final = datos_final.map(lambda x: (x[0], x[1][0] / x[1][1]))

print(datos_final.take(100))