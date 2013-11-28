import numpy as np
import pylab as pl
from scipy.interpolate import spline

def plot_error(X, y, xlabel, ylabel, title, legend):
    """
    ------------------------
    Plotting model metrics
    ----------------------
    """
    pl.figure()
    xnew = np.linspace(min(X),max(X),300)
    power_smooth = spline(X, y, xnew)
    pl.plot(xnew, power_smooth)
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)
    pl.title(title)
    pl.legend(legend)
    pl.show()

