import os
import subprocess
import gradio as gr
from make_problems import problem_set
from copy import deepcopy

types = gr.Dropdown(["더하기", "곱하기"], value="더하기", label="Problem Type", multiselect=True)
lower = gr.Slider(minimum=1, maximum=10000, step=1, value=1000, label="Lower Bound")
upper = gr.Slider(minimum=1, maximum=10000, step=1, value=9999, label="Upper Bound")
num_problems = gr.Slider(minimum=1, maximum=100, step=1, value=30, label="Number of Problems")


def greet(type, lower, upper, num_problems):
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

    r = subprocess.check_call(['pdflatex', 'example.tex'])
    r = subprocess.check_call(['cp', 'example.pdf', 'problem.pdf'])

    all_chapter_str_sol = deepcopy(all_chapter_str)
    with open('chapters.tex', 'w') as f:
        f.write(all_chapter_str_sol.replace("resultstyle=\placeholder,", "").replace("carryadd=false","carryadd=true"))
    r = subprocess.check_call(['pdflatex', 'example.tex'])
    r = subprocess.check_call(['cp', 'example.pdf', 'solution.pdf'])
    # res = subprocess.check_call([f"python make_problems.py --num_problems {num_problems} --lower {lower} --upper {upper} --ptype {type}"], shell=True)
    return ["problem.pdf", "solution.pdf"]

iface = gr.Interface(fn=greet, inputs=[types, lower, upper, num_problems], outputs="file")
iface.queue()
iface.launch()