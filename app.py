import os
import time
import subprocess
import gradio as gr
from make_problems import problem_set
from copy import deepcopy

types = gr.Dropdown(["더하기", "빼기", "곱하기"], value=["더하기", "빼기", "곱하기"], label="Problem Type", multiselect=True)
lower = gr.Slider(minimum=1, maximum=10000, step=1, value=1, label="Lower Bound")
upper = gr.Slider(minimum=1, maximum=10000, step=1, value=99, label="Upper Bound")
num_problems = gr.Slider(minimum=1, maximum=100, step=1, value=20, label="Number of Problems")


def greet(type, lower, upper, num_problems):
    if os.path.exists("problem.pdf"):
        os.remove("problem.pdf")
    if os.path.exists("solution.pdf"):
        os.remove("solution.pdf")
    if os.path.exists("example.pdf"):
        os.remove("example.pdf")

    with open("chapter_template.tex", "r") as f:
        template = f.read()

    chapters = []
    for t in type:
        pfunc, item_template = problem_set[t]
        t_template = template.replace("CHAPTER_NAME", t)
        problems = []
        for _ in range(num_problems):
            problems.append(item_template.format_map(pfunc(lower, upper)))
        
        problem_str = '\n\t'.join(problems)
        t_template = t_template.replace("PROBLEM_LIST", problem_str)
        chapters.append(t_template)
    
    all_chapter_str = '\n'.join(chapters)
    with open('chapters.tex', 'w') as f:
        f.write(all_chapter_str)

    r = subprocess.check_call(['pdflatex', 'problem.tex'])
    all_chapter_str_sol = deepcopy(all_chapter_str)
    with open('chapters.tex', 'w') as f:
        f.write(all_chapter_str_sol.replace("resultstyle=\placeholder,", "").replace("carryadd=false","carryadd=true").replace("carrysub=false","carrysub=true"))
    r = subprocess.check_call(['pdflatex', 'solution.tex'])
    return ["problem.pdf", "solution.pdf"]

iface = gr.Interface(fn=greet, inputs=[types, lower, upper, num_problems], outputs="file")
iface.queue()
iface.launch()