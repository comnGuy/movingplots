import pandas as pd
from classes.bar_race_chart import create_bar_race
from classes.models import SettingsPreprocessModel, SettingsDesignModel, SettingsVideoModel


# Settings
# Process Settings
settings_preprocess = SettingsPreprocessModel(
    interpolate_num=5, 
    show_data_frame=5
)
# Design
settings_design = SettingsDesignModel(
    bar_colors=["#adb0ff", "#ffb3ff", "#90d595",
                "#e48381", "#aafbff", "#f7bb5f", "#eafb50"]
)

settings_video = SettingsVideoModel(
    fps=2,
    save_path='anim.gif'
)

# load data
data = pd.read_csv('datasets/edo_cum.csv')

# Preprocess
data['date'] = pd.to_datetime(data.date, format='%Y-%m-%d')
data = data[:15]

create_bar_race(
    data,
    settings_preprocess,
    settings_design,
    settings_video,
    title='Most played games by Edopeh',
    bar_chart_text='Accumulated average monthly views',
    bar_text='Average monthly views',
    progress_bar=True)
