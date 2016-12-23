# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Ploting data."""
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math
from scipy.interpolate import spline


def get_sec():
    """Get second."""
    return int(datetime.datetime.now().strftime("%S"))


def setup(graph, kind):
    """Setup pyplot graph."""
    if kind == 'time':
        graph.set_title('Data on time')
        graph.set_xlabel('Time (s)')
        graph.set_ylabel('s(t)')
        graph.axis([0, 60, -1, 1])
    elif kind == 'freq':
        graph.set_title('Data on freq')
        graph.set_xlabel('Freq (Hz)')
        graph.set_ylabel('|S(f)|')


def plot_sig(data):
    """Plot signal function."""
    t_plot.scatter(data['t'][-1], data['v'][-1])
    if len(data['t']) > 1:
        t_plot.plot(data['t'][-2:], data['v'][-2:])


def plot_fft(data):
    """Calculate and plot fft."""
    if len(data['t']) > 1:
        fft = np.fft.fft(data['v'])
        spec = np.abs(fft) ** 2
        freq = np.fft.fftfreq(len(fft), delta)
        freq, spec = zip(*sorted(zip(freq, spec)))

        f_plot.clear()
        setup(f_plot, 'freq')
        f_plot.scatter(freq, spec)

        if len(data['t']) > 10:
            x_sm = np.array(freq)
            x_smooth = np.linspace(x_sm.min(), x_sm.max(), 100)
            y_smooth = spline(freq, spec, x_smooth)

            f_plot.plot(x_smooth, y_smooth)

# Two subplots, the axes array is time
f, [t_plot, f_plot] = plt.subplots(2)
delta = 0.0005
max_freq = 1.0 / (2.0 * delta)

setup(t_plot, 'time')
setup(f_plot, 'freq')

plt.ion()

data = {'t': [], 'v': []}
for i in range(30):
    data['t'].append(get_sec())
    data['v'].append(math.sin(0.1047 * 5 * get_sec()))
    plot_sig(data)
    plot_fft(data)
    plt.pause(delta)

while True:
    plt.pause(delta)
