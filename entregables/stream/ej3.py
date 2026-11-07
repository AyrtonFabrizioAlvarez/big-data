from pathlib import Path
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

base_dir = Path(__file__).parent
input = str(base_dir / "input")

franja_horaria = 300

sc = SparkContext("local[2]", "Entrega Spark Streaming")
ssc = StreamingContext(sc, 5)
ssc.checkpoint("buffer")
stream = ssc.textFileStream(input)

def parser(x):
    x = x.split("\t")
    return ((int(x[3]) // franja_horaria, x[0]), 1)

def parser2(x):
    return (x[0][0], 1)
    
stream = stream.map(parser).reduceByKey(lambda a, b: 1)

def fUpdate(newValues, history):
    return 1

history = stream.updateStateByKey(fUpdate)
history = history.transform(lambda rdd: rdd.map(parser2).reduceByKey(lambda a, b: a + b)) 
history.pprint() 

ssc.start()
ssc.awaitTermination()

