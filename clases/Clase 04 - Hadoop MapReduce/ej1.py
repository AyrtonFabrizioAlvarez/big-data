from pathlib import Path
from MRE import Job

root_path = Path(__file__).parent

inputDir = str(root_path / "inputEj1")
outputDir = str(root_path / "outputEj1")


def fmap(var, value, context):
    cols = value.strip().split('\t')
    b = float(cols[1])            # término independiente
    coefs = [float(c) for c in cols[2:]]  # coeficientes
    x_prev = context["x_prev"]    # vector de la iteración anterior

    # índice de la variable actual (var1 → 0, var2 → 1, …)
    idx = int(var.replace("var", "")) - 1

    # Jacobi: xᵢ^(k+1) = bᵢ - Σⱼ aᵢⱼ * xⱼ^(k)
    total = b
    for j, aij in enumerate(coefs):
        total -= aij * x_prev[j]

    context.write(var, total)

def fred(var, values, context):
    for v in values:
        context.write(var, v)

# ejemplo: vector inicial todo en 0
x0 = [0.0] * 15

params = {"x_prev": x0}
job = Job(inputDir, outputDir, fmap, fred)
job.setParams(params)
job.waitForCompletion()