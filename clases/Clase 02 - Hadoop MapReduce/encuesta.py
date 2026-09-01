from pathlib import Path
from emulador_mapreduce import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "Encuesta")
outputDir = str(root_path / "encuesta-output")



def fmap(key, value, context):
        treated_word = value.lower().replace(" ", "")
        if treated_word == "muysatisfecho":
            context.write("Muy satisfecho", 1)

        elif treated_word == "algosatisfecho":
            context.write("Algo satisfecho", 1)

        elif treated_word == "pocosatisfecho":
            context.write("Poco satisfecho", 1)

        elif treated_word == "disconforme":
            context.write("Disconforme", 1)

        elif treated_word == "muydisconforme":
            context.write("Muy disconforme", 1)

        else:
            print(f"Palabra no reconocida: {value}")
            context.write("otros", 1)



def fred(key, values, context):
    c = 0
    for v in values:
        c = c + 1
    context.write(key, c)


job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()