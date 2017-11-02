from random import randint
import numpy as n
import matplotlib.pyplot as graph
import os.path
import sys

is_spec = True
default = "blink"

# Function to read the features from file

def read_features(par_filename):
  vl = []
  with open(par_filename, "r") as file_lines:
    #features = [[float(i) for i in line.split()] for line in file_lines]
    for line in file_lines:
      vl.append(line.split())
  file_lines.close()
  return vl

# Function to plot the training and testing errors

def compute_plot(action, spectrum, raw):
  fig = graph.figure()
  ax = fig.add_subplot(111)
  if is_spec:
    graph.bar(n.arange(len(spectrum)), spectrum, 0.8)
  else:
    graph.plot(raw, color="darkRed")
    ax.set_xlim(xmax=len(raw))
  ax.set_xlabel('Frequency (Hz)')
  ax.set_ylabel('Amplitude (dB)')
  #ax.set_axisbelow(True)
  #ax.yaxis.grid(color='gray', linestyle='dashed')
  #ax.xaxis.grid(color='gray', linestyle='dashed')
  graph.legend(loc='upper left', numpoints = 1 )
  graph.title("Mean Spectrum: %s" % action.title())
  graph.show()
  return;


def filename(action, session):
  folder = "spec/" if is_spec else "raw/"
  return "../app/records/" + folder + action + "_" + str(session) + ".txt"

# Starting of the flow of program

def read_input(action):
  features = []
  session = 0
  while(os.path.isfile(filename(action, session))):
    features += read_features(filename(action, session))
    session += 1
  return features

def cast(a):
  return n.array(a, dtype=n.float32)

def plot_spectrum(action):
  specs = cast(read_input(action))
  spec = n.mean(specs, axis=0)
  raw = specs[randint(0,len(specs))]
  compute_plot(action, spec, raw)


if __name__ == "__main__":
  action = default if len(sys.argv) == 1 else sys.argv[1]
  plot_spectrum(action)
