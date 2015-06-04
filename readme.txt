Adam Berger
Fundamentals of Computational Linguistics - PA6

Part 1: Create distributional semantic word vectors

Does PPMI do the right thing to the count matrix? Why? Explain intuitively 
how PPMI helps.

Reweighing the word vector with PPMI creates a greater discrepancy between the 
likelihood of the probability of a bigram being a collocation. Since each count
had been smoothed by one, any bigram that was not part of the data set had
an equal probability of occurring. PPMI: I(x,y) = log2(P(xy) / P(x)P(y)) 
factors in the probability of each word of the bigram in the data. If the 
bigram does not occur, but the words occur often, then there is a small
probability that those words will occur as a bigram in a larger corpus. 

Do the distances you compute above confirm our intuition from distributional 
semantics (i.e. similar words appear in similar context.)?

The euclidian distances for the vector pairs make sense. I don't think that 
feed and like should have the same vector as my results show, but the two 
words do occur in very similar contexts in the data. Men and women, very 
similar words also have a small distance compared to men and dogs and women
and dogs. However, since men and women are similar, the distances for men
and dogs and women and dogs being similar makes sense. Finally, in the data
only men and women are doing feeding  and liking and only dogs are doing 
biting, so the fact that feed and bite and like and bite have the same vector
distance confirms the semantic difference between them.

Part 2: Computing with semantic vectors (word vectors)

This is my output for Part 2.1

euclidian choices:
[(0, 282), (1, 237), (2, 198), (3, 178)]
cosine choices:
[(0, 673), (2, 80), (1, 78), (3, 64)]

My test consisted of a list of lists. Each index consisted of a question and 
answer list pairing. The first answer (0) was always the correct answer and the 
rest (1-3) were randomly chosen. Using the euclidian distance metric my program 
was able to choose the correct answer more than any other answer. Note: this 
output is one run of the program, but I got similar counts for each answer for 
multiple runs of the program. When I ran the program using cosine similarity as
the metric my program chose the correct answer around 75% of the time.

Output for Part 2.2
option 1 correct choices = 96
option 1 percentage correct = 25.6684491979
option 2 correct choices = 129
option 2 percentage correct = 34.4919786096

I created two methods of determining the correct answer for my test. Option 1
took the cosine similarity of the question word vectors. It compared this value
with the cosine similarities of each answer word vector pair and took the value
that was closest to the question similarity. I also tried this methodology with
euclidian distance, but got better results with cosine similarity. Option 1 
concatenated the two word vectors for both the question word pair and each
answer word pair. The cosine similarity between the concatenated question word
vectors and that of each answer vector was computed and the best similarity
was chosen. This methodology produced results of 34.5% accuracy in choosing
the correct analogy answer.