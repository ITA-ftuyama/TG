import numpy as n
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as graph
import sys

actions = ["idle", "punchleft"]
n_sessions = 6
full_test = True

# Function to read the features from file

def read_features(par_filename, label):
	vl, ll = [], []
	with open(par_filename, "r") as file_lines:
		#features = [[float(i) for i in line.split()] for line in file_lines]
		for line in file_lines:
			vl.append(line.split())
			ll.append(label)
	file_lines.close()
	return (vl, ll)

# Function to compute the classification using KNeighbors

def compute_KNeighbors(train_f, train_l):
  c = KNeighborsClassifier(n_neighbors=5)
  c.fit(train_f, train_l)
  return c

# Function to compute the classification using SVM

def compute_SVC(train_f, train_l):
	c = svm.SVC(C = 1.0, cache_size = 200, class_weight = None, coef0 = 0.0,
		decision_function_shape = None, degree = 3, gamma = 'auto', kernel='linear', max_iter = -1,
		probability = True, random_state = None, shrinking = True, tol = 0.001, verbose = False)
	c.fit(train_f, train_l)
	return c

# Function to calculate the accuracy

def compute_accuracy(test_f, test_l, c):
	pred = c.predict(test_f)
	#print pred
	pred_accu = accuracy_score(test_l, pred)
	return pred_accu

# Function to compute the confusion matrix

def compute_confusion_matrix(test_f, test_l, c):
	pred = c.predict(test_f)
	x = confusion_matrix(test_l, pred)
	return x

# Function to compute the error

def compute_error(t_f,t_l,c):
	err = 1 - c.score(t_f,t_l)
	return err;

# Function to split the data based on percentage

def split_data(f,percent):
	tot = len(f)
	req_xt = int((float(percent)/100)*(tot))
	return [f[0:(req_xt-1)], f[req_xt:tot]]

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
	graph.plot(percent_plt, test_plt, 'bo', label='Training Accuracy')
	graph.plot(percent_plt, train_plt, 'ro', label='Testing Accuracy')
	graph.plot(percent_plt, test_plt, 'b')
	graph.plot(percent_plt, train_plt, 'r')
	ax.set_xlabel('Percentage of Taining data')
	ax.set_ylabel('Accuracy (%)')
	graph.legend( loc='upper left', numpoints = 1 )
	graph.title("% Accuracy Vs % training Data")
	graph.show()
	return;

# Analyse the model

def analyse_model(method):
	global features, labels
	read_input()

	input_percent = [20, 30, 40, 50, 60, 70, 80]
	file_created1 = open('results/Generated_accuracy_table.dat','w')
	file_created2 = open('results/Generated_error_table.dat','w')

	for pri in range(0,len(input_percent)):
		x1 = split_data(features, input_percent[pri]);
		x2 = split_data(labels, input_percent[pri]);
		labels_train = x2[0];
		features_train = x1[0];
		labels_test = x2[1];
		features_test = x1[1];

		model = compute_model(method, features_train,labels_train);

		accu_percent_train = compute_accuracy(features_train,labels_train,model)*100;
		accu_percent_test = compute_accuracy(features_test, labels_test,model)*100;
		train_err = compute_error(features_train, labels_train,model);
		test_err = compute_error(features_test, labels_test,model);
		conf_mat = compute_confusion_matrix(features_train,labels_train,model);
		conf_mat1 = compute_confusion_matrix(features_test,labels_test,model);

		print "%d %% train 	Train Acc %.4f 	Test Acc %.4f" % (input_percent[pri], accu_percent_train, accu_percent_test)
		#print conf_mat
		#print conf_mat1

		file_created1.write("%f %f %f \n" %(accu_percent_train, accu_percent_test, input_percent[pri]))
		file_created2.write("%f %f %f \n" %(train_err,test_err, input_percent[pri]))

	file_created1.close()
	file_created2.close()

	construct_model(method)
	compute_plot("results/Generated_accuracy_table.dat");
	#compute_plot("results/Generated_error_table.dat");

# Test the generated model

def test_model(model):
	global features, labels
	accu_percent = compute_accuracy(features, labels, model) * 100
	conf_mat = compute_confusion_matrix(features,labels,model);

	print "Accuracy obtained over the whole training set is %0.4f %% ." % (accu_percent)
	print conf_mat

	#print model.predict_proba([features[0]])

# Starting of the flow of program

def read_input():
	global actions, features, labels
	path =  "../app/records/spec/"
	features, labels = [], []
	for session in range(n_sessions):
		for i, action in enumerate(actions):
			sub_features, sub_labels = read_features(path + action + "_" + str(session) + ".txt", i)
			features += sub_features
			labels   += sub_labels


# Compute model

def compute_model(method, f, l):
	return compute_SVC(f, l) if method == "svm" else compute_KNeighbors(f, l)

# Construct SVM model

def construct_model(method):
	read_input()
	model = compute_model(method, features, labels)
	test_model(model)
	return model

if __name__ == "__main__":
	method = "svm" if len(sys.argv) == 1 else sys.argv[1]
	if full_test:
		analyse_model(method)
