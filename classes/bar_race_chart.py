from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 180


fig, ax = plt.subplots(2, figsize=(26, 15), gridspec_kw={
                       'height_ratios': [10, 1]}, dpi=180)
plt.box(False)
plt.subplots_adjust(bottom=0.05, right=0.95, left=0.05, hspace=0, wspace=0)
plt.margins(0, 0)
dates = set()


def preprocess(data_cum: pd.DataFrame, interpolate_num: int = 30, show_data_frame: int = 30) -> pd.DataFrame:
    # print(data_cum)
    # data_cum = data_cum.reset_index()
    # Interpolate
    data_cum.index = range(0, interpolate_num * len(data_cum), interpolate_num)
    data_cum = data_cum.reindex(index=range(interpolate_num * len(data_cum)))

    # Added time for stopping at the data point
    data_cum = pd.concat([data_cum[data_cum['date'].notnull()]]
                         * (show_data_frame-1) + [data_cum]).sort_index().reset_index()

    # Full everything
    data_cum.loc[:, data_cum.columns != 'date'] = data_cum.loc[:, data_cum.columns !=
                                                               'date'].interpolate(method='linear', limit_direction='forward')
    data_cum = data_cum.fillna(method='ffill')

    # Drop index column
    data_cum.drop('index', axis=1, inplace=True)

    return data_cum


def convert_type(value, target_type):
    """
    Attempts to convert a given value to a desired target type.

    Args:
        value (Any): The value to be converted into the target type.
        target_type (type): The type into which the value should be converted.

    Returns:
        The converted value if conversion is successful, otherwise None.

    Raises:
        Prints an error and returns None if conversion is not possible.
    """
    try:
        return target_type(value)
    except Exception as e:
        print(f"Couldn't convert '{value}' to type {target_type.__name__}.")
        print(f"Error message: {str(e)}")
        return None


def generate_images(index, title, date_format, bar_chart_text, bar_text, title_font_size=40, summary_type=int, bar_chart_amount=10):
    date_ = data_cummulative.iloc[index][0]
    pds = data_cummulative.iloc[index][1:].sort_values().tail(bar_chart_amount)
    values = pds.values
    indexs = pds.index
    colors = get_colors(indexs)
    sum_text = str(convert_type(
        data_cummulative.iloc[index][1:].sum(), summary_type)) + ' days'

    ax[0].clear()
    ax[1].clear()

    ax[0].barh(indexs, values, color=colors)
    dx = values.max() / 200
    for i, (value, name) in enumerate(zip(values, indexs)):
        ax[0].text(value-dx, i,     name,           size=26,
                   weight=200, ha='right', va='center')
        ax[0].text(value+dx, i,     f'{value:,.0f}',
                   size=24, ha='left',  va='center')
    ax[0].text(1, 0.3, date_.strftime(date_format),
               transform=ax[0].transAxes, color='#777777', size=62, ha='right', weight=800)
    ax[0].text(1, 0.2, sum_text, transform=ax[0].transAxes,
               color='#777777', size=62, ha='right', weight=800)
    ax[0].text(0, 1.06, bar_chart_text, transform=ax[0].transAxes,
               size=24, color='#777777')
    ax[0].xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax[0].xaxis.set_ticks_position('top')
    ax[0].tick_params(axis='x', colors='#777777', labelsize=12)
    ax[0].set_yticks([])
    ax[0].margins(0, 0.01)
    ax[0].grid(which='major', axis='x', linestyle='-')
    ax[0].set_axisbelow(True)
    ax[0].text(0, 1.15, title,
               transform=ax[0].transAxes, size=title_font_size, weight=600, ha='left', va='top')
    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["bottom"].set_visible(False)

    # Lower bar chart
    dates.add(date_)
    first_part = list(data[data['date'].isin(
        dates)].sum(axis=1, numeric_only=True))
    second_part = [0] * (len(data) - len(first_part))
    cmplet = first_part + second_part
    ax[1].text(0, -0.0, bar_text,
               transform=ax[0].transAxes, size=24, weight=100, ha='left', va='top', color='#777777')
    ax[1].bar(list(range(len(data))), cmplet, color='#777777', alpha=0.8)
    ax[1].axis('off')


color_map = {}


def build_color_map(columns, colors):
    for i, column in enumerate(columns):
        color_map[column] = colors[i % len(colors)]


def get_colors(columns):
    return [color_map[c] for c in columns]


def create_bar_race(
    data_,
    colors,
    fps=60,
    save_path='animation.mp4',
    interpolate_num=5,
    show_data_frame=5,
    title='TO-BE-FILLED',
    date_format='%Y-%m',
    bar_chart_text='TO-BE-FILLED',
    bar_text='TO-BE-FILLED',
    title_font_size=40,
    summary_type=int,
    bar_chart_amount=10
):
    # Use this data for the second (lower bar chart) bar chart
    global data

    # Use this bar chart for the main moving bars
    global data_cummulative

    data = data_.copy(deep=True)
    data_cum = data_.copy(deep=True)

    colors = colors
    data_cummulative = preprocess(data_cum, interpolate_num, show_data_frame)
    build_color_map(list(data_cummulative.columns), colors)

    animator = animation.FuncAnimation(
        fig,
        generate_images,
        frames=range(0, len(data_cummulative)),
        interval=200,
        fargs=(title, date_format, bar_chart_text, bar_text, title_font_size, summary_type, bar_chart_amount))

    # Determine the writer based on file extension
    if save_path.lower().endswith('.gif'):
        writer = animation.PillowWriter(fps=fps)
    elif save_path.lower().endswith('.mp4'):
        writer = animation.FFMpegWriter(fps=fps)
    else:
        raise ValueError('Unsupported file extension. Please use .gif or .mp4')
    animator.save(save_path, writer=writer)
