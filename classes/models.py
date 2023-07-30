
from pydantic import BaseModel, Field
from typing import List

class SettingsPreprocessModel(BaseModel):
    interpolate_num: int = Field(5, gt=0)
    show_data_frame: int = Field(5, gt=0)

class SettingsDesignModel(BaseModel):
    bar_colors: list = ["#adb0ff", "#ffb3ff", "#90d595", "#e48381", "#aafbff", "#f7bb5f", "#eafb50"]

class SettingsVideoModel(BaseModel):
    fps: int = Field(15, gt=0)
    # mp4 or gif
    save_path: str = 'anim.gif'
