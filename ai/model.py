import numpy as n
from sklearn import svm, preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as graph
import random
import skflow
import sys

kind = ["raw", "spec"][1]
default = ["svm", "k", "dnn"][0]
actions = ["idle", "blink", "punchleft", "punchright", "head"]
n_sessions = 15
ten_time 	= False
full_test = True
normalize = True
times = 1

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
  c = KNeighborsClassifier(n_neighbors=7)
  c.fit(train_f, train_l)
  return c

# Function to compute the classification using SVM

def compute_SVC(train_f, train_l):
	c = svm.SVC(C = 1.0, cache_size = 200, class_weight = None, coef0 = 0.0,
		decision_function_shape = None, degree = 3, gamma = 'auto', kernel='linear', max_iter = -1,
		probability = True, random_state = None, shrinking = True, tol = 0.001, verbose = False)
	c.fit(train_f, train_l)
	return c

# Function to compute the classification using Deeplearning

def compute_DNN(train_f, train_l):
	c = skflow.TensorFlowDNNClassifier(hidden_units=[10, 20, 20, 10], n_classes=len(actions), learning_rate=0.1, verbose=0)
	#c = skflow.TensorFlowDNNClassifier(hidden_units=[10, 30, 80, 80, 30, 10], n_classes=len(actions), learning_rate=0.08, verbose=0)
	#c = skflow.TensorFlowDNNClassifier(hidden_units=[10, 30, 90, 120, 90, 30, 10], n_classes=len(actions), learning_rate=0.08, verbose=0)
	c.fit(cast(train_f), train_l)
	return c

# Function to calculate the accuracy

def compute_accuracy(test_f, test_l, c):
	pred = c.predict(cast(test_f))
	#print pred
	pred_accu = accuracy_score(test_l, pred)
	return pred_accu

# Function to compute the confusion matrix

def compute_confusion_matrix(test_f, test_l, c):
	pred = c.predict(cast(test_f))
	x = confusion_matrix(test_l, pred)
	return x

# Function to compute the error

def compute_error(t_f,t_l,c):
	err = 1 - c.score(cast(t_f),t_l)
	return err;

# Function to split the data based on percentage

def split_data(f,percent):
	tot = len(f)
	req_xt = int((float(percent)/100)*(tot))
	return [f[0:(req_xt-1)], f[req_xt:tot]]

# Cast to avoid mimimi

def cast(a):
	global m
	return a if m != "dnn" else n.array(a, dtype=n.float32)

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

# Computes mean accy

def ten_times(method, kind):
	global features, labels
	read_input(kind)

	accu_percent_train = 0
	accu_percent_test = 0

	for i in range(times):
		# Shuffle data order
		c = list(zip(features, labels))
		random.shuffle(c)
		features, labels = zip(*c)

		# Takes last 20% as validation data
		features_train, features_test = split_data(features, 80)
		labels_train, labels_test = split_data(labels, 80)

		model = compute_model(method, features_train,labels_train);

		accu_percent_train += compute_accuracy(features_train,labels_train,model)*100;
		accu_percent_test += compute_accuracy(features_test, labels_test,model)*100;

	accu_percent_train = accu_percent_train / (times * 1.0)
	accu_percent_test = accu_percent_test / (times * 1.0)

	print("Train Accy %s" % accu_percent_train)
	print("Test Accy %s" % accu_percent_test)

# Analyse the model

def analyse_model(method, kind):
	global features, labels
	read_input(kind)

	input_percent = [20, 30, 40, 50, 60, 70, 80]
	file_created1 = open('results/Generated_accuracy_table.dat','w')
	file_created2 = open('results/Generated_error_table.dat','w')

	# Shuffle data order
	c = list(zip(features, labels))
	random.shuffle(c)
	features, labels = zip(*c)

	# Takes last 20% as validation data
	features_test = split_data(features, 80)[1];
	labels_test = split_data(labels, 80)[1];

	for pri in range(0,len(input_percent)):
		features_train = split_data(features, input_percent[pri])[0];
		labels_train = split_data(labels, input_percent[pri])[0];

		model = compute_model(method, features_train,labels_train);

		accu_percent_train = compute_accuracy(features_train,labels_train,model)*100;
		accu_percent_test = compute_accuracy(features_test, labels_test,model)*100;
		train_err = compute_error(features_train, labels_train,model);
		test_err = compute_error(features_test, labels_test,model);
		conf_mat = compute_confusion_matrix(features_train,labels_train,model);
		conf_mat1 = compute_confusion_matrix(features_test,labels_test,model);

		print "%d %% train 	Train Acc %.4f 	Test Acc %.4f" % (input_percent[pri], accu_percent_train, accu_percent_test)
		if input_percent[pri] == 80:
			print "Conf. matrix training"
			print conf_mat
			print "Conf. matrix validation"
			print conf_mat1

		file_created1.write("%f %f %f \n" %(accu_percent_train, accu_percent_test, input_percent[pri]))
		file_created2.write("%f %f %f \n" %(train_err,test_err, input_percent[pri]))

	file_created1.close()
	file_created2.close()

	construct_model(method, kind)
	compute_plot("results/Generated_accuracy_table.dat");
	#compute_plot("results/Generated_error_table.dat");

# Compare training % (what old code really does)

def analyse_training_percent(method, kind):
	global features, labels
	read_input(kind)

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

	construct_model(method, kind)
	compute_plot("results/Generated_accuracy_table.dat");
	#compute_plot("results/Generated_error_table.dat");

# Test the generated model

def test_model(model, method):
	global features, labels
	accu_percent = compute_accuracy(features, labels, model) * 100
	conf_mat = compute_confusion_matrix(features,labels,model);

	print "Accuracy using %s method obtained over the whole %s training set is %0.4f %% for actions %s" % (method, kind, accu_percent, actions)
	print conf_mat

	#print model.predict_proba([features[0]])

# Starting of the flow of program

def read_input(kind):
	global actions, features, labels
	path =  "../app/records/%s/" % kind
	features, labels = [], []
	for session in range(n_sessions):
		for i, action in enumerate(actions):
			sub_features, sub_labels = read_features(path + action + "/" + action + "_" + str(session) + ".txt", i)
			features += sub_features
			labels   += sub_labels

	if normalize:
		features = preprocessing.normalize(features, norm='l2')

# Compute model

def compute_model(method, f, l):
	global m; m = method
	return {
		'svm': compute_SVC,
		'k': compute_KNeighbors,
		'dnn': compute_DNN
	}.get(method, None)(f, l)

# Construct classification model

def construct_model(method, kind):
	read_input(kind)
	model = compute_model(method, features, labels)
	test_model(model, method)
	return model

# Constructor

def constructor():
	return construct_model(default, kind), default, kind


if __name__ == "__main__":
	method = default if len(sys.argv) == 1 else sys.argv[1]
	global m; m = method
	if ten_time == True:
		ten_times(method, kind)
	elif full_test == True:
		analyse_model(method, kind)
	#else:
		#analyse_training_percent(method, kind)
