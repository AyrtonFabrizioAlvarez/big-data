from pathlib import Path

from pyspark import SparkContext



def es_capricornio(fecha):
    _, mes, dia = map(int, fecha.split("-"))

    return (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19)


sc = SparkContext("local[*]", "Ejercicio 3")

base_dir = Path(__file__).parent
banco_dir = base_dir / "datasets" / "banco"
ruta_clientes = banco_dir / "Clientes.txt"
ruta_cajas = banco_dir / "CajasDeAhorro.txt"
ruta_prestamos = banco_dir / "Prestamos.txt"
ruta_movimientos = banco_dir / "Movimientos.txt"


clientes = sc.textFile(str(ruta_clientes))
clientes = clientes.map(lambda x: x.split("\t"))

prestamos = sc.textFile(str(ruta_prestamos))
prestamos = prestamos.map(lambda x: x.split("\t"))

cajas = sc.textFile(str(ruta_cajas))
cajas = cajas.map(lambda x: x.split("\t"))

movimientos = sc.textFile(str(ruta_movimientos))
movimientos = movimientos.map(lambda x: x.split("\t"))

#Ejercicio a
capricornios = clientes.filter(lambda x: es_capricornio(x[4]))
a = capricornios.map(lambda x: (x[1], x[2]))

#Ejercicio b
argentinos = clientes.filter(lambda x: x[5] == "ARG")
b = argentinos.map(lambda x: (x[1], x[2]))

#Ejercicio c
c = capricornios.count()

#Ejercicio d
joven, viejo = (
    argentinos
    .map(lambda x: (x, x))
    .reduce(
        lambda x, y: (
            x[0] if x[0][4] > y[0][4] else y[0],
            x[1] if x[1][4] < y[1][4] else y[1],
        )
    )
)

#ejercicio e
mayor_prestamo = prestamos.reduce(lambda x, y: x if (x[1] > y[1]) or (x[1] == y[1] and x[1] > y[1]) else y)

#Ejercicio f
cajas_positivas = cajas.filter(lambda x: float(x[2]) > 300)
f = cajas_positivas.map(lambda x: x[1]).distinct()

#Ejercicio g
mayor_movimiento, ultimo_movimiento = (
    movimientos
    .map(lambda x: (x, x))
    .reduce(
        lambda x, y: (
            x[0] if float(x[0][1]) > float(y[0][1]) else y[0],
            x[1] if x[1][2] > y[1][2] else y[1],
        )
    )
)
