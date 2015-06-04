# -*- coding: utf-8 -*-

import numpy
import scipy
import math


bigrams = {}
vocab = {}
num_context_word_type = 0
text = open('dist_sim_data.txt').readlines()

for line in text:
    line = line.split()
    for i in range(len(line) - 1):
        vocab[line[i]] = vocab.get(line[i], 0) + 1
        bigram = tuple(line[i:i+2])
        bigrams[bigram] = bigrams.get(bigram, 0 ) + 1

vocab_size = len(vocab.keys())
num_context_word_type = vocab_size
C = numpy.zeros((vocab_size, num_context_word_type))
      
def pop_matrix(C,bigrams,vocab):
	contexts = bigrams.keys()
	for i in range(len(C)):
		w = vocab[i]
		for j in range(len(C[i])):
			c = vocab[j]
			if (w,c) in contexts:
				count = bigrams[w,c]
			else:
				count = 0
			C[i][j] = count
    
    
def matrix_op(C, factor, op):
	for i in range(len(C)):
		for j in range(len(C[i])):
			if op == "m":
				C[i][j] *= factor
			elif op == "a":
				C[i][j] += factor
	return C
    
pop_matrix(C, bigrams, vocab.keys())
C = matrix_op(C, 10, "m")  
C = matrix_op(C, 1, "a")  

def PPMI(wc, w, c):
	return max(math.log(wc / (w * c), 2) , 0)
 
def PMI(C, bigrams, vocab):
	new_C = numpy.zeros((len(vocab), len(vocab)))
	tokens = float(sum(vocab.values()))
	tot_bigrams = float(sum(bigrams.values()))
	types = vocab.keys()
	for i in range(len(C)):
		w = vocab[types[i]] / tokens
		for j in range(len(C[i])):
			c = vocab[types[j]] / tokens
			wc = C[i][j] / tot_bigrams
			if w is not 0 and c is not 0:
				new_C[i][j] = PPMI(wc, w, c)
			else: new_C[i][j] = 0
	return new_C
 
PMI_matrix = PMI(C, bigrams, vocab)
 
def element_wise_mult(A, B):
     C = numpy.zeros((len(A), len(A[0])))
     for i in range(len(A)):
         for j in range(len(A[i])):
             C[i][j] = float(A[i][j]) * B[i][j]
     return C
ppmi_weighted_count_matrix = element_wise_mult(C, PMI_matrix)

print "comparison of word vector for dogs before and after PPMI reweighing"
print "before weighing - after weighing"
for i in range(len(vocab)):
	print (vocab.keys()[5], vocab.keys()[i])
	print str(C[5][i]) + "            " + str(ppmi_weighted_count_matrix[5][i])
 
print "Euclidian distance between vector pairs"
feed = scipy.linalg.norm(ppmi_weighted_count_matrix[0])
like = scipy.linalg.norm(ppmi_weighted_count_matrix[1])
bite = scipy.linalg.norm(ppmi_weighted_count_matrix[2])
men = scipy.linalg.norm(ppmi_weighted_count_matrix[3])
the = scipy.linalg.norm(ppmi_weighted_count_matrix[4])
dogs = scipy.linalg.norm(ppmi_weighted_count_matrix[5])
women = scipy.linalg.norm(ppmi_weighted_count_matrix[6])

women_men = scipy.linalg.norm(women - men)
women_dogs = scipy.linalg.norm(women - dogs)
men_dogs = scipy.linalg.norm(men - dogs)
feed_like = scipy.linalg.norm(feed - like)
feed_bite = scipy.linalg.norm(feed - bite)
like_bite = scipy.linalg.norm(like - bite)
print "women and men: " + str(women_men)
print "women and dogs: " + str(women_dogs)
print "men and dogs: " + str(men_dogs)
print "feed and like: " + str(feed_like)
print "feed and bite: " + str(feed_bite)
print "like and bite: " + str(like_bite)
print 

U, E, V = scipy.linalg.svd(ppmi_weighted_count_matrix, full_matrices = False)
E = numpy.matrix(numpy.diag(E))
U = numpy.matrix(U)
V = numpy.matrix(V)

reduced_ppmi_weighted_count_matrix = ppmi_weighted_count_matrix * V[:,0:3]
feed = scipy.linalg.norm(reduced_ppmi_weighted_count_matrix[0])
like = scipy.linalg.norm(reduced_ppmi_weighted_count_matrix[1])
bite = scipy.linalg.norm(reduced_ppmi_weighted_count_matrix[2])
men = scipy.linalg.norm(reduced_ppmi_weighted_count_matrix[3])
the = scipy.linalg.norm(reduced_ppmi_weighted_count_matrix[4])
dogs = scipy.linalg.norm(reduced_ppmi_weighted_count_matrix[5])
women = scipy.linalg.norm(reduced_ppmi_weighted_count_matrix[6])

women_men = scipy.linalg.norm(women - men)
women_dogs = scipy.linalg.norm(women - dogs)
men_dogs = scipy.linalg.norm(men - dogs)
feed_like = scipy.linalg.norm(feed - like)
feed_bite = scipy.linalg.norm(feed - bite)
like_bite = scipy.linalg.norm(like - bite)

print "Euclidian distances on reduced PPMI-weighted count matrix"
print "women and men: " + str(women_men)
print "women and dogs: " + str(women_dogs)
print "men and dogs: " + str(men_dogs)
print "feed and like: " + str(feed_like)
print "feed and bite: " + str(feed_bite)
print "like and bite: " + str(like_bite)
