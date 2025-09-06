import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data. To learn how to parse dates and set an index column I checked the
# pandas documentation(https://www.geeksforgeeks.org/pandas/python-read-csv-using-pandas-read_csv/) and learned that with the parameterindex_col, I can put a specific column as 
# de index, and that parse_dates allows me to pass the names of the columns I want to
# be as the type datetime, in this case, the date column.

df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data - Here we are only keeping the values that are not to extremy. The values
# above the 2.5% quantile and the values below the 97.5% quantile. In order to do this 
# we are using the method .quartile()
# that is used to return the value of that quantile. for example, the qauntile(0.025), means
# the value were 97.5% of the values in the dataframe are above that value, while
# 2.5% of the values in the dataframe are below that that value.
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    plt.clf() 
    df_line = df.copy()
    df_line.reset_index(inplace=True)
    # Draw line plot - In order to do that I searched the seaborn line plot documentation, and found the 
    # website: https://seaborn.pydata.org/generated/seaborn.lineplot.html
    # There I learned that in order to create that line plot I had to pass the dataframe
    # in the data parameter and the x and y axis values, it is which column should be in what axis.
    df_line = df.copy()
    df_line.reset_index(inplace=True)
    lineplot = sns.lineplot(data= df_line, x = 'date', # the date values will be displayed in the x axis
                             y = 'value', # the views will be displayed in the y axis
                            color='red') # setting the color as red so it looks more similar to the example
    # This works, but there is a problem, in this way the name of the x and y axis
    # are date and value, not Date and Page Views, also there is no title in the chart as the exercise required. In order to
    #change the name of the axis I had to search more. i found this website:
    # https://www.statology.org/seaborn-axis-labels/
    # There I discovered that to change the and y labels I could use the .set() 
    # method or the Matplotlib Functions, here I preferred to use the .set() method.
    lineplot.set(xlabel = 'Date', # Defines the name of the x axis on the chart
                 ylabel = 'Page Views',  # Defines the name of the y axis on the chart
                 title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019')  # Defines a title for this chart
    # To get acess to the figure object that will be returned later
    fig = lineplot.figure
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

draw_line_plot()

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    """ 
    df_bar['Years'] = df_bar['date'].dt.year
    df_bar['Months'] = df_bar['date'].dt.month_name
    df_bar['Average Page Views'] = df_bar.groupby(['year', 'month']).mean() 
    """
    # https://stackoverflow.com/questions/54110673/pandas-extracting-month-and-year-from-index
    df_bar['Years'] = df_bar.index.year
    #https://www.geeksforgeeks.org/python/python-strftime-function/
    df_bar['Months'] = df_bar.index.strftime('%B')
    df_bar = df_bar.groupby(['Years', 'Months'])['value'].mean().reset_index(name = 'Average Page Views')
    
    print(df_bar)
    plt.clf()  # Limpa o estado anterior
    # Draw bar plot
    barplot = sns.barplot(data = df_bar, x = 'Years', y = 'Average Page Views', hue = 'Months', hue_order=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                          palette = 'Paired')
    # To get acess to the figure ans axes object
    fig = barplot.figure

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

draw_bar_plot()

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    #https://www.geeksforgeeks.org/data-visualization/plotting-multiple-figures-in-a-row-using-seaborn/
    fig, axes = plt.subplots(1, 2, figsize=(18, 5))
    # Draw box plots (using Seaborn)
    box_plot1 = sns.boxplot(data = df_box, x= 'Year', y = 'value', ax = axes[0])
    box_plot1.set(ylabel = 'Page Views', title = 'Year-wise Box Plot (Trend)')

    box_plot2 = sns.boxplot(data =df_box, x='Month', y = 'value', ax = axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    box_plot2.set(ylabel= 'Page Views', title = 'Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
draw_box_plot()