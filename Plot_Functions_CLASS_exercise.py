
import numpy as np
import matplotlib.pyplot as plt


class Function():
    def __init__(self, f):
        self.f = f
    '''
        Newly created object used in this Class
    '''

    def __call__(self, x):
        return self.f(x)
    '''
        Make this callable as a function (important!)
        **return**
            The value of f(x), which f1, f2, f3 after calculation :
                *int, float*
    '''

    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return Function(lambda x: self(x) + other)
        else:
            return Function(lambda x: self(x) + other(x))

    def __sub__(self, other):
        if type(other) == float or type(other) == int:
            return Function(lambda x: self(x) - other)
        else:
            return Function(lambda x: self(x) - other(x))

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Function(lambda x: self(x) * other)
        else:
            return Function(lambda x: self(x) * other(x))

    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Function(lambda x: self(x) / other)
        else:
            return Function(lambda x: self(x) / other(x))
    '''
        This re-define add, substract, multiply, divide,
        becasue we can not calculate function with function
        **Parameters**
            self : *int, float*
                The object inserted from  "__name__"
            other :
                The object inserted from  "__name__"
        **return**
            The value of Function() : *int, float*
    '''


class Plotter():
    def __init__(self, low, high, interval):
        self.low = low
        self.high = high
        self.interval = interval
    '''
        This defines the new objects low, high, interval,
        which is the range of x_val
    '''

    def add_func(self, name, f):

        x_val = np.arange(self.low, self.high, self.interval)
        y_val = f(x_val)
        return plt.plot(x_val, y_val, label=name), plt.legend()
    '''
        This defines the new objects low, high, interval,
        which is the range of x_val, calculate y_val and
        plot the figure
        self : *int, float*
                The object inserted from  "__name__"
        name : *str*
                The name of the function f1, f2, f3, f4
        f : f(x_val)
            functions used to calculate the y_val
        **return**
            The plot of (x_val, y_val, and the label of the line)
        #information: https://stackoverflow.com/questions
        /16992038/inline-labels-in-matplotlib
    '''

    def plot(self):
        return plt.show()
    '''
        Show the figure
    '''


if __name__ == "__main__":
    # For each Function object, we simply input the lambda function to it.
    # Note: be sure to include "import numpy as np" at the beginning of your
    # Python script so that we can make use of numpy’s sine function.
    f1 = Function(lambda x: x ** 2)
    f2 = Function(lambda x: x + 3)
    f3 = Function(lambda x: np.sin(x))
    # Combine our first 3 Function objects together to create a new fourth
    # Function object.
    f4 = (f1 + f2) * f3 / 2.0
    # Create a new Plotter object, where our domain ranges from 0 to 20 and we
    # have a step size of 0.1.
    plot = Plotter(0, 20, 0.1)
    # Add all the functions to the Plotter object. The first argument specifies
    # the function’s label and the second argument is the actual Function
    # object. Keep in mind that you must write the functions add func
    # and plot. plot.add func("Function 1", f1)
    # plot.add func("Function 2", f2) plot.add func("Function 3", f3)
    # plot.add func("Function 4", f4) plot.plot()
    plot.add_func(" Function 1", f1)
    plot.add_func(" Function 2", f2)
    plot.add_func(" Function 3", f3)
    plot.add_func(" Function 4", f4)
    plot.plot()
