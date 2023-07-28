import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 180


def preprocess(data_cum: pd.DataFrame, interpolate_num: int = 30, show_data_frame: int = 30) -> pd.DataFrame:
    data_cum = data_cum.reset_index()
    # Interpolate
    data_cum.index = range(0, interpolate_num * len(data_cum), interpolate_num)
    data_cum = data_cum.reindex(index = range(interpolate_num * len(data_cum)))

    # Added time for stopping at the data point
    data_cum = pd.concat([data_cum[data_cum['date'].notnull()]]*(show_data_frame-1) + [data_cum]).sort_index().reset_index()

    # Full everything
    data_cum.loc[:, data_cum.columns != 'date'] = data_cum.loc[:, data_cum.columns != 'date'].interpolate(method ='linear', limit_direction ='forward')
    data_cum = data_cum.fillna(method='ffill')

    # Drop index column
    data_cum.drop('index', axis=1, inplace=True)

    return data_cum

fig, ax = plt.subplots(2, figsize=(26, 15), gridspec_kw={'height_ratios': [10, 1]}, dpi=180)

plt.box(False)
plt.subplots_adjust(bottom = 0.05, right = 0.95, left=0.05, hspace = 0, wspace = 0)
# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
#         hspace = 0, wspace = 0)
plt.margins(0,0)
dates = set()


def draw(index, title, date_format, bar_chart_text, bar_text, title_font_size=40):
    date_ = data_cummulative.iloc[index][0]
    pds = data_cummulative.iloc[index][1:].sort_values().tail(10)
    values = pds.values
    indexs = pds.index
    colors = get_colors(indexs)
    sum_text = str(data_cummulative.iloc[index][1:].sum()) + ' days'
    
    ax[0].clear()
    ax[1].clear()

    ax[0].barh(indexs, values, color=colors)
    dx = values.max() / 200
    for i, (value, name) in enumerate(zip(values, indexs)):
        # ax[0].text(value-dx, i,     name,           size=26, weight=600, ha='right', va='bottom')
        ax[0].text(value-dx, i,     name,           size=26, weight=200, ha='right', va='center')
        # ax[0].text(value-dx, i-.25, group_lk[name], size=10, color='#444444', ha='right', va='baseline')
        ax[0].text(value+dx, i,     f'{value:,.0f}',  size=24, ha='left',  va='center')
    # ax[0].text(1, 0.2, date_, transform=ax[0].transAxes, color='#777777', size=62, ha='right', weight=800)
    ax[0].text(1, 0.3, datetime.date.strftime(date_, date_format), transform=ax[0].transAxes, color='#777777', size=62, ha='right', weight=800)
    ax[0].text(1, 0.2, sum_text, transform=ax[0].transAxes, color='#777777', size=62, ha='right', weight=800)
    ax[0].text(0, 1.06, bar_chart_text, transform=ax[0].transAxes, size=24, color='#777777')
    ax[0].xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax[0].xaxis.set_ticks_position('top')
    ax[0].tick_params(axis='x', colors='#777777', labelsize=12)
    ax[0].set_yticks([])
    ax[0].margins(0, 0.01)
    ax[0].grid(which='major', axis='x', linestyle='-')
    ax[0].set_axisbelow(True)
    ax[0].text(0, 1.15, title,
            transform=ax[0].transAxes, size=title_font_size, weight=600, ha='left', va='top')
    # ax[0].text(1, 0, 'Twitch Viz', transform=ax[0].transAxes, color='#777777', ha='right',
    #         bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["bottom"].set_visible(False)


    
    dates.add(date_)
    first_part = list(data[data['date'].isin(dates)].sum(axis=1, numeric_only=True))
    second_part = [0] * (len(data) - len(first_part))
    cmplet = first_part + second_part 
    ax[1].text(0, -0.0, bar_text,
            transform=ax[0].transAxes, size=24, weight=100, ha='left', va='top', color='#777777')
    ax[1].bar(list(range(len(data))), cmplet, color='#777777', alpha=0.8)
    # ax[1].plot(list(range(len(data_bar))), data_bar, color='#777777', alpha=0.8)
    ax[1].axis('off')
    # plt.savefig('foo.png')

color_map = {}
def build_color_map(columns, colors):
    for i, column in enumerate(columns):
        color_map[column] = colors[i % len(colors)]

def get_colors(columns):
    return [color_map[c] for c in columns]
    

def create_bar_race(
        data_, 
        data_cum, 
        colors, 
        fps=60, 
        save_path = 
        'animation.mp4', 
        interpolate_num=5,
        show_data_frame=5,
        title='TO-BE-FILLED',
        date_format='%Y-%m',
        bar_chart_text='TO-BE-FILLED', 
        bar_text='TO-BE-FILLED',
        title_font_size=40
    ):
    global data
    data = data_ 
    # TODO, muss vorher gemacht werden
    data = data.reset_index()
    # print(data)
    data['date'] = pd.to_datetime(data.date, format='%Y-%m-%d')
    colors = colors
    global data_cummulative
    data_cummulative = preprocess(data_cum, interpolate_num, show_data_frame)
    build_color_map(list(data_cummulative.columns), colors)
    # draw(50)

    animator = animation.FuncAnimation(
        fig, 
        draw, 
        frames=range(0, len(data_cummulative)), 
        interval=200, 
        fargs=(title,date_format, bar_chart_text, bar_text, title_font_size))
    # # # HTML(animator.to_jshtml())
    # animator.save('animation.gif', writer='imagemagick', fps=60)
    # MP4
    FFwriter = animation.FFMpegWriter(fps=fps)
    print(save_path)
    animator.save(save_path, writer = FFwriter)


# load data
# data_c = pd.read_csv('edo_cum.csv')
# data = pd.read_csv('edo.csv')

# # Colors
# colors = ["#adb0ff", "#ffb3ff", "#90d595", "#e48381", "#aafbff", "#f7bb5f", "#eafb50"]

# create_bar_race(data, data_c, colors)