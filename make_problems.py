import click
import json
import os
import random

TEMPLATE = "\item  \opadd[resultstyle=\placeholder,carryadd=false,displayintermediary=None,voperation=top,voperator=bottom]{{{input1}}}{{{input2}}}"
MULT_TEMPLATE = "\item  \opmul[resultstyle=\placeholder,carryadd=false,voperation=top,voperator=bottom]{{{input1}}}{{{input2}}}"
def add_problem(lower, upper):
    input1 = random.randint(lower, upper)
    input2 = random.randint(lower, upper)
    solution = input1 + input2
    return {"input1": input1, "input2": input2, "solution": solution}

def multiply_problem(lower, upper):
    input1 = random.randint(lower, upper)
    input2 = random.randint(lower, upper)
    solution = input1 + input2
    return {"input1": input1, "input2": input2, "solution": solution}

@click.command()
@click.option('--num_problems', default=10)
@click.option('--lower', default=1)
@click.option('--upper', default=10000)
def main(num_problems, lower, upper):
    add_problems = []
    for _ in range(num_problems):
        add_problems.append(TEMPLATE.format_map(add_problem(lower, upper)))

    with open('add_problem.tex', 'w') as f:
        f.write('\n'.join(add_problems))

    mul_problems = []
    for _ in range(num_problems):
        mul_problems.append(MULT_TEMPLATE.format_map(multiply_problem(lower, upper)))

    with open('multiply_problem.tex', 'w') as f:
        f.write('\n'.join(mul_problems))

    os.system('pdflatex example.tex')
    import time
    time.sleep(1)
    os.system('cp example.pdf problem.pdf')

    with open('add_problem.tex', 'w') as f:
        f.write('\n'.join([p.replace("resultstyle=\placeholder,", "").replace("carryadd=false","carryadd=true") for p in add_problems]))

    with open('multiply_problem.tex', 'w') as f:
        f.write('\n'.join([p.replace("resultstyle=\placeholder,", "").replace("carryadd=false","carryadd=true") for p in mul_problems]))

    os.system('pdflatex example.tex')
    time.sleep(1)
    os.system('cp example.pdf solution.pdf')

if __name__ == "__main__":
    main()