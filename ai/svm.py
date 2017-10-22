import numpy as n
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as graph

path =  "../app/records/"

# Function to read the features from file

def read_features(par_filename):
    vl = []
    with open(par_filename, "r") as file_lines:
        #features = [[float(i) for i in line.split()] for line in file_lines]
        for line in file_lines:
            vl.append(line.split())
    file_lines.close()
    for r in vl:
        del r[12]
    return vl

# Function to read the lables from file

def read_labels(par_filename):
    vl = []
    with open(par_filename, "r") as file_lines:
        for line in file_lines:
            vl.append(line.split())
    file_lines.close()
    ll = []
    for r in vl:
        ll.append(r[12])
    return ll

# Function to compute the classification using SVM

def compute_SVC(train_f, train_l):
    c = svm.SVC(C = 1.0, cache_size = 200, class_weight = None, coef0 = 0.0,
        decision_function_shape = None, degree = 3, gamma = 'auto', kernel='linear', max_iter = -1,
        probability = False, random_state = None, shrinking = True, tol = 0.001, verbose = False)
    c.fit(train_f, train_l)
    return c

# Function to calculate the accuracy

def compute_accuracy(test_f, test_l, c):
    pred = c.predict(test_f)
    print pred
    pred_accu = accuracy_score(test_l, pred)
    return pred_accu

# Function to compute the confusion matrix

def compute_confusion_matrix(test_f, test_l, c):
    pred = c.predict(test_f)
    x = confusion_matrix(test_l, pred)
    return x

# Function to compute the error

def compute_error(t_f,t_l,c):
	err = c.score(t_f,t_l)
	return err;

# Function to split the data based on percentage

def split_data(f,percent):
	tot = len(f)
	req_xt = int((float(percent)/100)*(tot))
	req_yt = tot - req_xt
	xt_get = []
	for s in range(0,(req_xt-1)):
		xt_get.append(f[s])
	yt_get = []
	for d in range(req_xt,tot):
		yt_get.append(f[d])
	xyt = []
	xyt.append(xt_get)
	xyt.append(yt_get)
	return xyt;

# Function to plot the training and testing errors

def compute_plot(filename):
	test_plt = []
	train_plt = []
	percent_plt = []
	with open(filename,"r") as lines_in_file:
		for c1 in lines_in_file:
			test_plt.append(c1.split()[0])
			train_plt.append(c1.split()[1])
			percent_plt.append(c1.split()[2])
	fig = graph.figure()
	ax = fig.add_subplot(111)
	graph.plot(percent_plt, test_plt, 'bo', label='Training Error')
	graph.plot(percent_plt, train_plt, 'ro', label='Testing Error')
	graph.plot(percent_plt, test_plt, 'b')
	graph.plot(percent_plt, train_plt, 'r')
	ax.set_xlabel('Percentage of Taining data')
	ax.set_ylabel('Percentage of Error')
	graph.legend( loc='upper left', numpoints = 1 )
	graph.title("% Error Vs % training Data")
	graph.show()
	return;


# Starting of the flow of program
read_data_features_train = read_features(path + "plrx.txt")
read_data_labels_train = read_labels(path + "plrx.txt")
model_svc = compute_SVC(read_data_features_train, read_data_labels_train)
accu_percent = compute_accuracy(
    read_data_features_train, read_data_labels_train, model_svc) * 100
print "Accuracy obtained over the whole training set is %0.6f %% ." % (accu_percent)
conf_mat = compute_confusion_matrix(read_data_features_train,read_data_labels_train,model_svc);
print conf_mat

print model_svc.predict([[-0.17936, -0.207, -0.20971, -0.09726,	-0.11921, -0.17322,	-0.28076, 0.22317, 0.41866,	-0.032886, 0.0033827, -0.33425]])
