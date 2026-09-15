from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "inputEj2")
outputDir = str(root_path / "outputEj2")

def fmap(incog, value, context):
    # incog = primera columna (varX)
    parts = value.strip().split('\t')
    coef, val = parts
    val = float(val)
    x_prev = context["x_prev"]

    if coef == "TI":
        # término independiente b_i
        context.write(incog, ("TI", val))
    else:
        # contribución coef * x_prev[coef]
        contrib = val * x_prev.get(coef, 0.0)
        context.write(incog, ("SUM", contrib))

def fred(incog, values, context):
    b = 0.0
    suma = 0.0
    for tag, v in values:
        if tag == "TI":
            b = v
        else:
            suma += v
    nuevo = b - suma
    context.write(incog, nuevo)

# ejemplo: valores iniciales todos en 0
x0 = {"X": 0.0, "Y": 0.0, "Z": 0.0}

params = {"x_prev": x0}
job = Job(inputDir, outputDir, fmap, fred)
job.setParams(params)
job.waitForCompletion()