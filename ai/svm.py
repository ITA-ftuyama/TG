import numpy as n
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as graph

actions = ["idle", "blink"]

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

# Analyse the model

def analyse_model():
    global features, labels
    read_input()

    input_percent = [40, 50, 60, 70, 80, 90]
    file_created1 = open('Generated_accuracy_table.dat','w')
    file_created2 = open('Generated_error_table.dat','w')

    for pri in range(0,len(input_percent)):
        x1 = split_data(features, input_percent[pri]);
        x2 = split_data(labels, input_percent[pri]);
        labels_train = x2[0];
        features_train = x1[0];
        labels_test = x2[1];
        features_test = x1[1];

        model_svc = compute_SVC(features_train,labels_train);
        test_model(model_svc)
            #print "train"
        accu_percent_train = compute_accuracy(features_train,labels_train,model_svc)*100;
            #print "test"
        accu_percent_test = compute_accuracy(features_test, labels_test,model_svc)*100;
        train_err = compute_error(features_train, labels_train,model_svc);
        test_err = compute_error(features_test, labels_test,model_svc);
        file_created1.write("%f %f %f \n" %(accu_percent_train, accu_percent_test, input_percent[pri]))
        file_created2.write("%f %f %f \n" %(train_err,test_err, input_percent[pri]))

    file_created1.close()
    file_created2.close()

    conf_mat = compute_confusion_matrix(features_train,labels_train,model_svc);
    print conf_mat
    conf_mat1 = compute_confusion_matrix(features_test,labels_test,model_svc);
    print conf_mat1
    compute_plot("Generated_accuracy_table.dat");
    compute_plot("Generated_error_table.dat");

# Test the generated model

def test_model(model_svc):
    global features, labels
    accu_percent = compute_accuracy(features, labels, model_svc) * 100
    conf_mat = compute_confusion_matrix(features,labels,model_svc);

    print "Accuracy obtained over the whole training set is %0.6f %% ." % (accu_percent)
    print conf_mat

    #print model_svc.predict_proba([features[0]])

# Starting of the flow of program

def read_input():
    global actions, features, labels
    path =  "../app/records/spec/"
    features, labels = [], []
    for session in range(4):
        for i, action in enumerate(actions):
            sub_features, sub_labels = read_features(path + action + "_" + str(session) + ".txt", i)
            features += sub_features
            labels   += sub_labels

# Construct SVM model

def construct_svm():
    read_input()   
    model_svc = compute_SVC(features, labels)
    test_model(model_svc)
    return model_svc

#construct_svm()
#analyse_model()
