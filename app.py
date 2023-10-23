import os
import gradio as gr

types = gr.Radio(["Addition", "Multiplication"], value="Addition", label="Problem Type")
lower = gr.Slider(minimum=1, maximum=10000, step=1, value=1000, label="Lower Bound")
upper = gr.Slider(minimum=1, maximum=10000, step=1, value=9999, label="Upper Bound")
num_problems = gr.Slider(minimum=1, maximum=100, step=1, value=30, label="Number of Problems")


def greet(types, lower, upper, num_problems):
    os.system(f"python make_problems.py --num_problems {num_problems} --lower {lower} --upper {upper}")
    return ["problem.pdf", "solution.pdf"]

iface = gr.Interface(fn=greet, inputs=[types, lower, upper, num_problems], outputs="file")
iface.queue()
iface.launch()