# Author: Zequn Yu
# PID: A14712777

from __future__ import division
import numpy
from heapq import nlargest, nsmallest
from sklearn.metrics import confusion_matrix
from operator import itemgetter

train = numpy.loadtxt("pa3train.txt")
test = numpy.loadtxt("pa3test.txt")
feature_len = len(train[0])-1

def sign(number):
	return 1 if number >= 0 else -1

def train_perceptron(train, passes, label_one):
	w = numpy.zeros(feature_len)

	for p in range(passes):
		for point in train:
			label = 1 if label_one == point[feature_len] else -1
			if  label * numpy.dot(w, point[:feature_len]) <= 0:
				w = w + (label * point[:feature_len])

	return w


def perceptron_error(test, w, label):
	wrong = 0
	for point in test:
		sign = numpy.dot(w, point[:feature_len])
		if sign < 0 and point[feature_len] == label:
			wrong += 1
		elif sign >= 0 and point[feature_len] != label:
			wrong += 1

	return wrong / len(test)


def train_voted_perceptron(train, passes, label_one):
	w = numpy.zeros(feature_len)
	c = 1
	classifiers = []
	for p in range(passes):
		for point in train:
			label = 1 if label_one == point[feature_len] else -1
			if  label * numpy.dot(w, point[:feature_len]) <= 0:
				classifiers.append((w, c))
				w = w + (label * point[:feature_len])
				c = 1
			else:
				c += 1

	classifiers.append((w, c))
	return classifiers


def voted_perceptron_error(test, classifiers, label):
	wrong = 0

	for point in test:
		test_feat = point[:feature_len]
		pred = 0
		for c in classifiers:
			pred += c[1] * sign(numpy.dot(c[0], test_feat))
		if sign(pred) < 0 and point[feature_len] == label:
			wrong += 1
		elif sign(pred) >= 0 and point[feature_len] != label:
			wrong += 1
	return wrong / len(test)

def average_perceptron_error(test, classifers, label):
	wrong = 0
	w = sum([classi[0] * classi[1] for classi in classifers])
	for point in test:
		sign = numpy.dot(w, point[:feature_len])
		if  sign < 0 and point[feature_len] == label:
			wrong += 1
		elif sign >= 0 and point[feature_len] != label:
			wrong += 1
	return wrong/len(test)

one_two_subset = [point for point in train if point[len(point)-1] == 1 or point[len(point)-1] == 2]
one_two_subset_t = [point for point in test if point[len(point)-1] == 1 or point[len(point)-1] == 2]

'''
print("per")
for passes in range(2,5):
	w = train_percepie_boy(one_two_subset, passes, 1)
	print(perceptron_error(one_two_subset, w, 1))
	print(perceptron_error(one_two_subset_t, w, 1))
print("voted")
for passes in range(2,5):
	classis = train_voted_perceptron(one_two_subset, passes, 1)
	print(voted_perceptron_error(one_two_subset, classis, 1))
	print(voted_perceptron_error(one_two_subset_t, classis, 1))
print("aver")
for passes in range(2,5):
	classis = train_voted_perceptron(one_two_subset, passes, 1)
	print(average_perceptron_error(one_two_subset, classis, 1))
	print(average_perceptron_error(one_two_subset_t, classis, 1))
'''
# wavg from averaged perceptron and three passes
# call function to get 3 passes voted perceptron
avg_all = train_voted_perceptron(one_two_subset, 3, 1)
#print("Now the classis is: ", classis)
w = sum([avg_each[0] * avg_each[1] for avg_each in avg_all])

# use nlargest and nsmallest to get 3 highest and the three lowest
# get the index of 3 max and min value in pair
largest = nlargest(3, enumerate(w), key=lambda x: x[1])
lowest = nsmallest(3, enumerate(w), key=lambda x: x[1])
#print("largest is: ", top)
#print("lowest is: ", bot)

# set to save diction
diction = []

'''
# read ling by line
for line in open("pa3dictionary.txt", 'r'):
	diction.append(line.strip().split('/n'))

# get the answer
print("The three highest:", diction[largest[0][0]], diction[largest[1][0]], diction[largest[2][0]])
# print(max(classis,key=itemgetter(1))[0])
# print(diction[max(classis,key=itemgetter(1))[0]])
print("The three lowest:", diction[lowest[0][0]], diction[lowest[1][0]], diction[lowest[2][0]])
'''

# part 3: one vs all
# for each class i : 1 to 6 run 1 pass

class_one = train_perceptron(train, 1, 1)
class_two = train_perceptron(train, 1, 2)
class_three = train_perceptron(train, 1, 3)
class_four = train_perceptron(train, 1, 4)
class_five = train_perceptron(train, 1, 5)
class_six = train_perceptron(train, 1, 6)

# if ci(x) = i, then predict label i  ( exactly one i )
# if ci(x) = i ( more than one i ) or ci(x) = i ( no i , Don't know )
CX = []
CX.append(class_one)
CX.append(class_two)
CX.append(class_three)
CX.append(class_four)
CX.append(class_five)
CX.append(class_six)
# print("CX is: ", CX)

'''
For each test data, you will have {predicted label, true label}.
The predicted label can be {1, 2, 3, 4, 5, 6, Don't know} => 7 values
The true label can be {1, 2, 3, 4, 5, 6} => 6 values
'''
# function to predict the test example
def test_predict( test, CX ):
	# print("CX: ", CX )
	pred_result = []
	# for each line of feathre in testData
	for feature in test:
		#print("Now the feature is: ", feature)
		# set label as
		tmp_label = 0
		# loop to check each feature
		for i in range(0, len(CX)):
			if numpy.dot(CX[i], feature[0:-1]) > 0:
				print("legal")
				''' if has more than one label -> Don't know '''
				if tmp_label != 0:
					print("Dont know")
					tmp_label = 0
					break
				else:
					''' set the label '''
					print("Get label")
					tmp_label = i + 1
				''' add in to result '''
		print("tmp_label: ", tmp_label)
		pred_result.append(tmp_label)
	return pred_result



# build confusion matrix
pred_l = test_predict( test, CX )
''' set the true label'''
print("pred_l:", pred_l)
true_l = []
for tf in test:
	true_l.append(tf[feature_len])
print("true_l: ", true_l)
my_matrix = confusion_matrix( pred_l, true_l)

print("my_martixL ")
print(my_matrix)

''' set the number of label '''
test_label = [0,0,0,0,0,0,0]
for tf in test:
	tl_idx = int(tf[feature_len])
	test_label[tl_idx] += 1
res_matrix = numpy.zeros((7,6))

''' calculate C/N for each entry '''
for r in range(0, 7):
	for c in range(1, 7):
		print("My mat: ", my_matrix[r][c] )
		print("test_m: ", test_label[c] )
		res_matrix[r][c-1] = my_matrix[r][c] / test_label[c]

print("Now con_martix is: ")
print(res_matrix)
