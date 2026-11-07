from pathlib import Path
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

base_dir = Path(__file__).parent
input = str(base_dir / "input")

sc = SparkContext("local[2]", "Entrega Spark Streaming")
ssc = StreamingContext(sc, 5)
ssc.checkpoint("buffer")
stream = ssc.textFileStream(input)

def parser(x):
    x = x.split("\t")
    return (x[4], x[0]) 

stream = stream.map(parser)
stream = stream.filter(lambda x: x[0] != "" and x[0] != "Otro")
stream = stream.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b)

def fUpdate(newValues, history):
    return sum(newValues) + (history or 0)

history = stream.updateStateByKey(fUpdate)

history.foreachRDD(lambda rdd: print(rdd.top(3, key=lambda x: x[1]))) 


ssc.start()
ssc.awaitTermination()

