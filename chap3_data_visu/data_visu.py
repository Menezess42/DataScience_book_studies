import matplotlib.pyplot as plt
from collections import Counter
# Exemplo simples

years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]
movies  = ['Annie Hall', 'Ben-Hur', 'Casablanca', 'Grandhi', 'West side Story']
num_oscars = [5,11,3,8,10]
grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]
variance = [1,2,4,8,16,32,64,128,256]
bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]
total_error = [x+y for x,y in zip(variance, bias_squared)]
xs = [i for i, _ in enumerate(variance)]
friends = [70,65,72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


class SimpleGraph:
    # making a line grpah, yeaers is x axis, gdp is y axis
    def call(self):
        plt.plot(years, gdp, color='green', marker='o', linestyle='solid')
        #plt.plot(X_elemnts, Y_elements, Graph_Color, intersectionXY='o', typeOfLine='solid' )
        # Adding title
        plt.title('Normal GDP')

        # Adding y axies label
        plt.ylabel('Billions of $')

        # saving fig
        plt.savefig('./simple_line_graph.png')

        # Showing graph
        plt.show()

class BarGraph:
    """It's a good option to show how some quantities fluctuate
    in a discreate item set.
    You have to be careful, because it is a way to deceive people not initiate the Y axis in 0.
    """

    def simple_call(self):
        # plots the bars with X coordinates and the hight [num_oscars]
        plt.bar(range(len(movies)), num_oscars)

        # give a Title
        plt.title('My favorite Movies') 

        # gives a Y axies label
        plt.ylabel('# of Academy Awards')

        # Gives the X axies the movie names
        plt.xticks(range(len(movies)), movies)
        # plt.xticks(amount of ticks, ticks name[list like])

        plt.savefig('./simple_graph_bar.png')
        plt.show()

    def histograms_plot(self):
        """A bar's graph is useful to plot histogram for gruped numeric values
        and show the value's distribuiton"""

        # Grouping the grades per decil, but put the 100 with the 90
        histogram = Counter(min(grade//10*10, 90) for grade in grades)

        plt.bar([x+5 for x in histogram.keys()], # Moves the bars to right in 5
                histogram.values(), # Give every bar the correct hight
                10, # 10 for the width of each bar
                edgecolor=(0,0,0)) # darkens the edges of the bars
        plt.axis([-5, 105, 0, 5]) # x axies from -5 to 105,
                                  # y axies from 0 to 5

        plt.xticks([10*i for i in range(11)]) # labels for the X axies in 0, 10, .., 100

        plt.xlabel('Decile')
        plt.ylabel('# of Students')
        plt.title('distribuiton of Exam 1 Grades')

        plt.savefig('./bar_graph_4_histo_values.png')
        plt.show()

class LineGraph:
    '''Line graph is a good option to show trend'''
    def call(self):
        # We can make multiple layers to plt.plot
        plt.plot(xs, variance, 'g-', label='variance') # linha verde sólida
        plt.plot(xs, bias_squared, 'r-.', label='bias^2') # linha vermelha de ponto tracejado
        plt.plot(xs, total_error, 'b:', label='total error') # linha pontilhada azul

        # Because we apply labels to every series,
        # we can create a subtitle for free (loc=9 means 'top center')

        plt.legend(loc=9)
        plt.xlabel('Model Complexity')
        plt.xticks([])
        plt.title('The bias-variance tradeoff')
        plt.savefig('./simple_line_graph_show_bvariance_tradeoff.png')
        plt.show()

class ScatterGraph:
    '''Scatter plot is the correct option to display the relationship between dataset pairs'''

    def call(self):
        plt.scatter(friends, minutes)

        # Label witch plan
        for label, friend_count, minute_cont in zip(labels, friends, minutes):
            plt.annotate(label,
                         xy=(friend_count, minute_cont),  # Put the label in the respective point
                         xytext=(5,-5), # a little bit deslocate
                         textcoords='offset points')
        plt.title('Daily Minutes vs. Number of Friends')
        plt.xlabel('# of friends')
        plt.ylabel("Daily minutes spent on the site")
        plt.savefig('line_scatteer graph')
        plt.show()

    # If you let the matplotlib select the scale when scatter variables, maybe you have an 
    # incorrect or no so acurated positon plot

if __name__ == '__main__':
    simple_graph = SimpleGraph()
    bar_graph = BarGraph()
    # bar_graph.simple_call()
    # bar_graph.histograms_plot()
    line_graph = LineGraph()
    # line_graph.call()
    scatter_graph = ScatterGraph()
    scatter_graph.call()
