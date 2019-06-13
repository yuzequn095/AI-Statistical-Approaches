# Author: Zequn Yu
# PID: A14712777

from __future__ import division
#import pandas as pd
import numpy
import math

# function to help add data to array
def add_data(line, data, file):
    while (line):
        data.append(line.split())
        line = file.readline()

# read data from files
# to save data from files
train_data = []
test_data = []
# to open files
train_file = open("pa5train.txt", "r")
test_file = open("pa5test.txt", "r")
# to read each line from files
train_line = train_file.readline()
test_line = test_file.readline()
# set label
label_idx = len(train_data[0]) - 1;
# call function to read
add_data(train_line, train_data, train_file)
add_data(test_line, test_data, test_file)
# test read
# print("train: ", train_data)
# print("test:", test_data


# implement given weak learners:
#   hi,+(x) = 1, if word i occurs in email x
#           = −1, otherwise
def classifier_h(data, idx, sign):
    # h+ case
    # print(" Now the sign is: ", sign)
    if(sign == "+"):
        if (data[idx] == 1):
            return 1
        else:
            return -1
    # h- case
    else:
        if (data[idx] == 0):
            return 1
        else:
            return -1

# function to get error
def cal_error(list):
    tol_err = 0
    # check each e-mail feature read in
    for email in list:
        # check each feature
        # for feature in range(0, label_idx):
        train_l = email[label_idx]
        should_l = classifier_h(email, label_idx, "+")
        if(train_l == should_l):
            tol_err = tol_err + 1
    return tol_err

# function to change alpha
def update_alpha(b_err):
    c_list = ()
    alpha = .5 * numpy.log((1 - b_err.e) / b_err.e)
    c_list.append((alpha, b_err.h, b_err.word))
    return c_list

# the main part of bossting
def boost(data):
    class_tuple = ()
    # for rounds test
    boost = [3, 7, 10, 15, 20]
    # check different boost
    for b in boost:
        # print("Now boost is: ", b )
        cur_err = 100.0
        cur_feature = -1
        cur_label = 2
        weight = [1/len(data)] * len(data)
        # run for rounds of range
        # update feature, label and error
        rounds = len(data[0]) - 1
        for r in range(rounds):
            # calculate the number of error
            tmp_err = cal_error(r)
            # check if need to update error
            if(tmp_err < cur_err):
                cur_err = tmp_err
                cur_feature = r
                cur_label = 1
            # check if flip label
            elif(1 - tmp_err < cur_err):
                cur_err = 1 - tmp_err
                cur_feature = 1
                cur_label = -1
        # update alpha
        class_tuple = update_alpha(cur_err)
        # update
        for i in range(len(data)):
            d = [weight[i] * numpy.e ** (-class_tuple[0] * y[i] * cur_err.h(x.iloc[i, :], cur_err.word))]
        # set normalize
        d = 0
        sum_d = sum(d)
        update_d = [(i / sum_d) for i in d]
        #return class_tuple
        print_stat(train_data, test_data, tuple)

# function to get label
def cal_label(feature, list):
	cur_l = 0
	for l in list:
		if l[1] == 1:
			if feature[l[0]] == 1:
				cur_l += l[2]
			else:
				cur_l -= l[2]
		else:
			if feature[l[0]] == 0:
				cur_l += l[2]
			else:
				cur_l -= l[2]
	return (cur_l / math.fabs(cur_l))

# predict
def predict (data, classif):
    pred = data.apply(lambda x: classify(x, classif), axis=1)
    return pred

# set final classify
def classify(x, classifiers):
    #print("classify turn")
    total = 0
    for c in classifiers:
        # update
        alpha = c[0]
        h = c[1]
        word = c[2]
        total += (alpha * h(x, word))
    # print(total)
    return numpy.sign(total)

# cal train error
def t_err(t_data, tuple):
    err = 0
    for t in t_data:
        currLabel = cal_label(t, tuple)
        if currLabel != t[-1]:
            err += 1
    err = (err / float(len(train_data)))
    return err
# cal test error
def e_err(e_data, tuple):
    err = 0
    for t in e_data:
        currLabel = cal_label(t, tuple)
        if currLabel != t[-1]:
            err += 1
    err = err / float(len(e_data))
    return err

def print_stat(t_data, e_data, tuple):
    # print("start training data:")
    t = boost(t_data)
    # print("run predict: ")
    p = predict(t_data, t)
    tr_err = t_err(t_data, tuple)
    #print("Now the data err is: ", tr_err)
    e = boost(e_data)
    # peinr("run predict: ")
    p2 = predict(e_data, e)
    te_err = e_err(e_data, tuple)

'''
rounds = [3,4,7,10,15,20]
for r in rounds:
		for t in dataList:
			curr_l = calLabel(t, tuple)
			if curLabel != t[-1]:
				errorCount += 1
		readFile("..\data\pa5test.txt")
		errorCount = 0

		for t in dataList:
			curr_l = calLabel(t, tuple)
			if curr_l != t[-1]:
				errorCount += 1

'''