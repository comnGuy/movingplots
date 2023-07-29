import pandas as pd
from classes.bar_race_chart import create_bar_race

# load data
data = pd.read_csv('datasets/edo_cum.csv')
data = data[:30]

# Colors
colors = ["#adb0ff", "#ffb3ff", "#90d595",
          "#e48381", "#aafbff", "#f7bb5f", "#eafb50"]

create_bar_race(
    data,
    colors,
    fps=15,
    save_path='anim.gif',
    title='Most played gamed by Edopeh',
    bar_chart_text='Accumulated average monthly views',
    bar_text='Average monthly views')
