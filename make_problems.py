import click
import subprocess
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

def subtract_problem(lower, upper):
    input1 = random.randint(lower, upper)
    input2 = -random.randint(lower, upper)
    solution = input1 + input2
    return {"input1": input1, "input2": input2, "solution": solution}

def multiply_problem(lower, upper):
    input1 = random.randint(lower, upper)
    input2 = random.randint(lower, upper)
    solution = input1 + input2
    return {"input1": input1, "input2": input2, "solution": solution}

problem_set = {"더하기": (add_problem, TEMPLATE),
               "빼기": (subtract_problem, TEMPLATE),
               "곱하기": (multiply_problem, MULT_TEMPLATE)}

@click.command()
@click.option('--num_problems', default=10)
@click.option('--lower', default=1)
@click.option('--upper', default=10000)
@click.option('--ptype', default="addition")
def main(num_problems, lower, upper, ptype):
    pfunc, template = problem_set[ptype]
    problems = []
    for _ in range(num_problems):
        problems.append(template.format_map(pfunc(lower, upper)))

    with open('problems_list.tex', 'w') as f:
        f.write('\n'.join(problems))

    r = subprocess.check_call(['pdflatex', 'example.tex'])
    r = subprocess.check_call(['cp', 'example.pdf', 'problem.pdf'])

    with open('problems_list.tex', 'w') as f:
        f.write('\n'.join([p.replace("resultstyle=\placeholder,", "").replace("carryadd=false","carryadd=true") for p in problems]))

    r = subprocess.check_call(['pdflatex', 'example.tex'])
    r = subprocess.check_call(['cp', 'example.pdf', 'solution.pdf'])

if __name__ == "__main__":
    main()