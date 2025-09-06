# Import the libraries used in this project
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
# Call the pandas function that register pandas formatters and converters with matplotlib.
# It basically makes sure that pandas datatypes like pd.Timestamp can be used in matplotlib
register_matplotlib_converters()

# Import the CSV data. To learn how to parse dates and set an index column, I reviewed
# the pandas documentation: https://www.geeksforgeeks.org/pandas/python-read-csv-using-pandas-read_csv/
# With the parameter index_col I can set a specific column as the index, and with parse_dates
# I can specify which columns should be parsed as datetime. In this case, the 'date' column.
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data - Here we are only keeping the values that are not to extreme, we are 
# removing the outliers. The values above the 2.5% quantile and the values below the 
# 97.5% quantile. In order to do this we are using the method .quartile()
# that is used to return the value of that quantile. For example, the qauntile(0.025), means
# the value were 97.5% of the values in the dataframe are above that value, while
# 2.5% of the values in the dataframe are below that that value.
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & # The & operator is used to combine the filters
    (df['value'] <= df['value'].quantile(0.975))
]

# Define the function draw_line_plot
def draw_line_plot():
    plt.clf() # This line clears the current Matplotlib figure.
    # Before adding this line, running the code again would stack one plot on top of another.
    # I learned this at: https://www.activestate.com/resources/quick-reads/how-to-clear-a-plot-in-python/

    # Create a copy of the original DataFrame with the method .copy()
    df_line = df.copy()

    # Draw line plot - In order to do that I searched the seaborn line plot documentation and found the 
    # website: https://seaborn.pydata.org/generated/seaborn.lineplot.html
    # There, I learned that to create that line plot I had to pass the dataframe
    # in the data parameter and the x and y axis values, that is, which column should be in which axis.
    lineplot = sns.lineplot(data= df_line, x = 'date', # the date values will be displayed on the x axis
                             y = 'value', # the views will be displayed on the y axis
                            color='red') # setting the color as red so it looks more similar to the example
    # This works, but there is a problem: in this way the name of the x and y axis
    # are 'date' and 'value', not 'Date' and 'Page Views', and there is no title in the chart as the exercise required. 
    # In order to change the name of the axis I had to search more. I found this website:
    # https://www.statology.org/seaborn-axis-labels/
    # There I discovered that to change the x and y labels I could use the .set() 
    # method or the Matplotlib functions, here I preferred to use the .set() method.
    lineplot.set(xlabel = 'Date', # Defines the name of the x axis on the chart
                 ylabel = 'Page Views',  # Defines the name of the y axis on the chart
                 title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019')  # Defines a title for this chart
    
    # To get access to the figure object that will be returned later
    fig = lineplot.figure

    # Save image and return fig 
    fig.savefig('line_plot.png')
    return fig

# draw_line_plot() only for testing

# Define the draw_bar_plot function
def draw_bar_plot():
    # Create a copy of the original DataFrame using the .copy() method
    df_bar = df.copy()

    # To get a monthly bar plot, I knew I would have to access the month separately in the data.
    # In order to do that, I tried the following code:
    """
    df_bar['Years'] = df_bar['date'].dt.year
    df_bar['Months'] = df_bar['date'].dt.month_name
    df_bar['Average Page Views'] = df_bar.groupby(['year', 'month']).mean()
    """
    # It didn't work because 'date' isn't a column anymore; now it is
    # an index. So to learn how to access months in index dates, I found this site:
    # https://stackoverflow.com/questions/54110673/pandas-extracting-month-and-year-from-index
    # There I discovered that I could use .index.year to get the years.
    df_bar['Years'] = df_bar.index.year

    # To get the month, I had to search again and found this site:
    # https://www.geeksforgeeks.org/python/python-strftime-function/
    # There I learned that the .strftime function allows you to convert a datetime object into a formatted string.
    # I also learned that to get the full month name, as needed to create a bar plot similar to the example,
    # we can use '%B' as a parameter for this function.
    df_bar['Months'] = df_bar.index.strftime('%B')

    # To calculate the average page views per month, I used the .groupby method to group by year and month,
    # then applied .mean() to get the monthly average. Finally, I used .reset_index to convert the grouped indexes
    # ('Years' and 'Months') back into columns. By passing the name parameter as 'Average Page Views',
    # I set the name of the column that stores the monthly averages.
    df_bar = df_bar.groupby(['Years', 'Months'])['value'].mean().reset_index(name='Average Page Views')
    
    # Clears the current Matplotlib figure, so charts are not plotted on top of each other.
    plt.clf()  

    # Draw bar plot — To draw the bar plot, I searched the internet and found this
    # site: https://datagy.io/seaborn-barplot/. There I understood which parameters I should use.
    barplot = sns.barplot(
        data=df_bar,  # Use the sns.barplot() function to create the bar plot and pass df_bar as the data to be plotted
        x='Years',  # The values on the x-axis will be those in the 'Years' column
        y='Average Page Views',  # The values on the y-axis will be those in the 'Average Page Views' column
        hue='Months',  # This splits each bar into multiple bars, each representing a specific month
        hue_order=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],  # Orders the months correctly in the chart, otherwise, they appear in the order found in the data
        palette='Set1'  # Sets the colors of the bar plot to the 'Set1' palette. I chose this one, but there are several palettes available
    )

    # Acess the figure object and stores it on the fig variable
    fig = barplot.figure

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy() # Creates a copy of the original DataFrame
    df_box.reset_index(inplace=True) # Resets the index so that 'date' becomes a column instead of the DataFrame index,
    # making it easier to work with. So now I won't need to use the .index anymore to access the date.
    df_box['Year'] = [d.year for d in df_box.date] # Gets the year of the date column
    df_box['Month'] = [d.strftime('%b') for d in df_box.date] # Gets the month with the .strftime function that allows you to convert a
    # datetime object into a formatted string. But here, instead of what we did before, we don't use '%B', because now we want an
    # abbreviation of the month name, so we use '%b' instead.

    # To draw two adjacent box plots similar to "examples/Figure_3.png", I searched the internet and found this site:
    # https://www.geeksforgeeks.org/data-visualization/plotting-multiple-figures-in-a-row-using-seaborn/
    # There I learned that I could use the subplot functionality provided by Matplotlib. This allows you to create multiple plots side by side in a single figure.
    # Here, I created a figure with 1 row and 2 columns. I also set the figure size to (18, 5), which means the figure will be 18 inches wide and 5 inches tall. 
    fig, axes = plt.subplots(1, 2, figsize=(18, 5)) # I assign the subplot to the fig and axes variables so I can easily reference the figure and each individual axis later.
   
    # Draw box plots (using Seaborn) - To do this, I searched the Seaborn documentation at: https://seaborn.pydata.org/generated/seaborn.boxplot.html to find
    # the parameters I should use.
    box_plot1 = sns.boxplot(
                            data=df_box, # Use the sns.boxplot() function to create the box plot and pass df_box as the data to be plotted
                            x='Year', # The values on the x-axis will be those in the 'Year' column
                            y='value', # The values on the y-axis will be those in the 'value' column
                            ax=axes[0], # Specifies which axis (subplot) the plot should be drawn on
                            palette='Set2' # Sets the colors of the box plot to the 'Set2' palette. I chose this one, but there are several palettes available
    )

    # The .set method allows you to change properties of the plot, such as labels and title.
    box_plot1.set(ylabel='Page Views', # Changes the y-axis label to 'Page Views'
                  title='Year-wise Box Plot (Trend)') # Adds a title to the plot 

    # Creates the second box plot
    box_plot2 = sns.boxplot(
        data=df_box, # Use the sns.boxplot() function to create the box plot and pass df_box as the data to be plotted
        x='Month', # The values on the x-axis will be those in the 'Month' column (abbreviated month names)
        y='value', # The values on the y-axis will be those in the 'value' column
        ax=axes[1], # Specifies which axis (subplot) the plot should be drawn on (the second plot)
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], # Ensures the months are ordered correctly from January to December
        palette='Set2' # Sets the colors of the box plot to the 'Set2' palette. I chose this one, but there are several palettes available
    )

    # The .set method allows you to change properties of the plot, such as labels and title.
    box_plot2.set(ylabel='Page Views', # Changes the y-axis label to 'Page Views'
                  title='Month-wise Box Plot (Seasonality)') # Adds a title to the plot

    # Save image and return fig 
    fig.savefig('box_plot.png')
    return fig

