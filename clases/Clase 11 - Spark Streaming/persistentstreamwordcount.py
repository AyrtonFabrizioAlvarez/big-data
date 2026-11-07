root_path = '/content/input/'

# Creamos el contexto de Spark
from pyspark import SparkContext
sc = SparkContext("local", "Prueba")

from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, 10)

ssc.checkpoint("buffer")

streamOriginal = ssc.textFileStream(root_path)
stream = streamOriginal.flatMap(lambda t: t.split(" "))
stream = stream.map(lambda t: (t, 1))
stream = stream.reduceByKey(lambda t1, t2: t1+t2)
stream.pprint()

def fUpdate(newValues, history):
	if(history == None):
		history = 0
	if(newValues == None):
		newValues = 0
	else:
		newValues = sum(newValues)
	return newValues + history

history = stream.updateStateByKey(fUpdate)
history.pprint()

ssc.start()
ssc.awaitTermination()