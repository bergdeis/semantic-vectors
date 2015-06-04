# -*- coding: utf-8 -*-
"""
@author: Adam Berger
"""
from collections import defaultdict
import random
import scipy
import math
from scipy.spatial import distance

text = open('EN_syn_verb.txt').readlines()
syn_dict = defaultdict(list)
for line in text:
    line = line.split()
    w = line[0]
    syn = line[1]
    if syn is not '0':
	    if syn not in syn_dict[w]:
		    syn_dict[w].append(syn)
syn_dict.pop('Input.word')

multiple_choice_test_set = list()
syn_dict_words = syn_dict.keys()
syn_dict_size = len(syn_dict)

#creates the multiple choice synonym test. 
for i in range(1000):
    answers = list()
    #word to pick synonym for
    w = random.choice(syn_dict_words)
    while len(syn_dict[w]) < 1:
        w = random.choice(syn_dict_words)
    #the correct answer (always the first answr of each question for easier computation later)
    answers.append(random.choice(syn_dict[w]))
    incorrect_answers = list()
    j = 0
    while j < 3:
        #get a random synonym
        incorrect = syn_dict[random.choice(syn_dict_words)]
        while len(incorrect) < 1:
    		incorrect = syn_dict[random.choice(syn_dict_words)]
        incorrect = random.choice(incorrect)
        if incorrect is not w and incorrect is not answers:
           answers.append(incorrect)
           j += 1
    new_question = (w, answers)
    multiple_choice_test_set.append(new_question) 
  
google_vectors = open('GoogleNews-vectors-rcv_vocab.txt').readlines()
g_vectors = {}
for line in google_vectors:
    line = line.split()
    g_vectors[line[0]] = line[1:]
    
euclidian_choices = list()
cosine_choices = list()

def euclidian_dist(X,Y):
    X = [float(X[i]) for i in range(len(X))]
    Y = [float(Y[i]) for i in range(len(Y))]
    X = scipy.linalg.norm(X)
    Y = scipy.linalg.norm(Y)
    return distance.euclidean(X, Y)

def cosine_similarity(X,Y):
    num = 0.0
    for i in range(len(X)):
        num += float(X[i]) * float(Y[i])
    X_dist = 0
    Y_dist = 0
    for val in X:
        val = float(val)
        X_dist += val**2
    for val in Y:
        val = float(val)
        Y_dist += val**2
    X_dist = math.sqrt(X_dist)
    Y_dist = math.sqrt(Y_dist)
    denom = X_dist * Y_dist
    
    return num / denom

#answer each question in the test set
for question in multiple_choice_test_set:
    q = question[0].split('_')[1]
    answers = [x.split('_')[1] for x in question[1]]
    if q in g_vectors:
        X = g_vectors[q]
        euclidian_dist_answers = list()
        cosine_sim_answers = list()
        g_vect_q = g_vectors[q]
        for a in answers:
            if a in g_vectors:
                g_vect_a = g_vectors[a]
                euclidian_dist_answers.append(euclidian_dist(g_vect_q, g_vect_a))
                cosine_sim_answers.append(cosine_similarity(g_vect_q, g_vect_a))
        euclidian_choices.append(euclidian_dist_answers.index(min(euclidian_dist_answers)))
        cosine_choices.append(cosine_sim_answers.index(max(cosine_sim_answers)))
    
from nltk import FreqDist
euclidian_choices = FreqDist(euclidian_choices)
cosine_choices = FreqDist(cosine_choices)
print "euclidian choices:"
print euclidian_choices.most_common(4)
print "cosine choices:"
print cosine_choices.most_common(4)



SAT_package = open('SAT-package-V3.txt').readlines()
SAT_questions = list()
SAT_answers = list()
answer_list = list()
new_question = None
count = 0
#parse the analogy question set
for line in SAT_package:
	if '190' in line or 'ML' in line or 'KS type' in line:
		count = 1
	elif count == 1:
		if ':' in line:
			count += 1
			line = line.split()
			new_question = (line[0], line[1])
	elif count < 7:
		if ':' in line:
			line = line.split()
			new_answer = (line[0], line[1])
			answer_list.append(new_answer)
			count += 1
	elif count == 7:
		if len(line.split()) == 1:
			if 'a' in line:
				SAT_answers.append(0)
			elif 'b' in line:
				SAT_answers.append(1)
			elif 'c' in line:
				SAT_answers.append(2)
			elif 'd' in line:
				SAT_answers.append(3)
			elif 'e' in line:
				SAT_answers.append(4)
			whole_question = (new_question, answer_list)
			SAT_questions.append(whole_question)
			count = 0
			answer_list = list()
option_1_answers = list()
option_2_answers = list()

#take the cosine similarity of the two question words. Do the same 
#for each answer pair. Return the answer whose similarity is most similar
#to that of the question word pair
def option_1(question, answers):
	if question[0] not in g_vectors or question[1] not in g_vectors:
		return None
	first = g_vectors[question[0]]
	second = g_vectors[question[1]]
	q_sim = cosine_similarity(first, second)
	answer_vals = list()
	for i in range(len(answers)):
		answer = answers[i]
		if answer[0] in g_vectors and answer[1] in g_vectors:
			first = g_vectors[answer[0]]
			second = g_vectors[answer[1]]
			a_sim = cosine_similarity(first, second)
			answer_vals.append(a_sim)
	#find index of answer pair with closest cosine similarity to that of the question word pair
	sim_difs = [abs(q_sim - x) for x in answer_vals]
	closest_sim = min(sim_difs)
	closest_sim_index = sim_difs.index(closest_sim)
	return closest_sim_index
 
#concatenate the two word vectors from the question and find the cosine similarity
#or euclidian distance between that and the concatenated word vectors for each answer pair
#using the best distance value I got 21% accuracy. similarity gave 34.5%
def option_2(question, answers):
    if question[0] not in g_vectors or question[1] not in g_vectors:
		return None
    large_vec = g_vectors[question[0]] + g_vectors[question[1]]
    answer_vecs = list()
    for i in range(len(answers)):
        answer = answers[i]
        if answer[0] in g_vectors and answer[1] in g_vectors:
            answer_vec = g_vectors[answer[0]] + g_vectors[answer[1]]
            answer_vecs.append(answer_vec)
    #vec_dists = [euclidian_dist(large_vec, a) for a in answer_vecs]
    vec_sims = [cosine_similarity(large_vec, a) for a in answer_vecs]
    #best_dist = vec_dists.index(min(vec_dists))
    best_sim = vec_sims.index(max(vec_sims))
    return best_sim
     
for i in range(len(SAT_questions)):
    question = SAT_questions[i][0]
    answers = SAT_questions[i][1]
    option_1_answers.append(option_1(question, answers))
    option_2_answers.append(option_2(question, answers))

#determine the accuracy of each option's methodology
option_1_agreement = 0
option_2_agreement = 0
for j in range(len(SAT_answers)):
    if SAT_answers[j] == option_1_answers[j]:
        option_1_agreement += 1
    if SAT_answers[j] == option_2_answers[j]:
        option_2_agreement += 1
print "option 1 correct choices = " + str(option_1_agreement)
print "option 1 percentage correct = " + str(float(option_1_agreement) / len(SAT_answers) * 100)
print "option 2 correct choices = " + str(option_2_agreement)
print "option 2 percentage correct = " + str(float(option_2_agreement) / len(SAT
