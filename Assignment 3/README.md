# CS B551 - Assignment 3: Probability, NLP, and Computer Vision

## Part 1: Part-of-speech tagging

### Problem statement: Find the parts of speech tags for a new sentence given you have a labelled data with pos tags already using the following models.

1)simplified
2)HMM
3)Complex
 

#### Simple Algorithm:
To calculate the probabilities, we counted all of the pos tags that appeared for each term.

We trained the data got the dictionary of words(P(w1|S), transition of words(P(N|N)) and POS probabilities (P(N)).

To perform part-of-speech tagging, we want to estimate the most-probable tags for each word Wi.first, we simply calculated the formula:
P(Si | Wi) = [ P(Wi | Si) * P(Si) / P(Wi) ]
As the denominator will remain same for all, we ignore the P(Wi) for better computational performance and simply calculate using the below formula:
P(Si | Wi) = [ P(Wi | Si) * P(Si) ]
For each word Wi, the pos-tag Si with the highest probability P(Si | Wi) is considered for classifying the word Wi.
We return Noun as the default POS for those for whom we don't have a frequency or in the event of a tie.

#### HMM algorithm:
We used the Emission and Transition Probability tables to train.
Emission Table - Probability of Occurrence of a word given pos tag P(tag = 't1'/word), if that is zero probability, give it a probability of 0.000000000001

Transition Probability - Probability of P(pos_tag2/pos_tag1), consider an example P('noun'/'noun')

find the maximum a posteriori (MAP) labeling for the sentence

            (s∗1, . . . , s∗N) = arg maxs1,...,sNP(Si=si|W)
We can solve this model by using viterbi (Dynamic Programming) to compute the most likely sequence using transition and emission probability.

#### Complex MCMC model:
Simple Algorithm: 1)Fix the values of the observed varibles 2)set the values of the non-observed varibles randomly. 3)Randomly go through the space of all the observed and unobserved varibles.one on each time. this is following the Markov blanket, which says most of the varibles are independent. 4)Repeat the process many times . 5)the probaility converges to true posterior when frequencies stop changing significantly.

Use the probability tables from previous viterbi and also caluculate the probaility of P(Sn/Sn-1,s0)

Initialize the word pos sequence to some random pos tags (Here I Initialized it to nouns).

Using Gibbs sampling sample the Probabilities each word by making all other values constant and after the healing period store the maximum occured sequences counts in a dictionary.

After sampling output the maximum occurred sequence for each word.

#### Note:
Accuracies for complex model may vary during runs as it takes random samples.

#### Posterior Probabilites:
Simple: Calculate the Posterior Probabilities of simple model as P = p(word/tag)*p(tag)

HMM: For HMM model P = p(word/tag)*prob(tag/prev_tag)

Complex_mcmc: Calculate the Posterior Probabilities of complex model as P = p(word/tag)*p(tag/prev_tag)*p(next_tag/tag)

Observations:
Simple algorithm is not efficient.
Viterbi decoding is great with better sequence prediction and fast computation
Gibbs Sampling takes more time as the sample size limit is increased!

#### For the bc.test data we get following results based on multiple runs:
    
    So far scored 1039 sentences with 14710 words.
                       Words correct:     Sentences correct: 
     0.Ground truth:     100.00%              100.00%
     1.Simple:            93.63%              47.55%
     2.HMM:               94.77%              53.71%
     3.Complex            94.83%              54.09%

#### Simple:         
93.63% of the test words are correctly classified with POS labels;

95.55% of the test sentences are correctly classified with POS labels sequence;

#### HMM:        
94.77% of the test words are correctly classified with POS labels;

96.71% of the test sentences are correctly classified with POS labels sequence;

#### Complex:         
94.83% of the test words are correctly classified with POS labels;

96.09% of the test sentences are correctly classified with POS labels sequence;

Reference:
https://github.com/surajgupta-git/Artificial-Intelligence-projects/tree/main/POS%20Tagging

   

## Part 2: Ice Tracking

### Problem Forumlation:
The goal of our program was to accurately predict air-ice and ice-rock boundaries from echograms taken of various glaciers. These barriers are denoted by a few different variables, but can prove to be difficult for subject matter experts to label. To find the various barriers, we formulated to use variables such as pixel color, edge strength, and, later, transition. For each of these values, we could calculate a probability of a certain point on the graph being a barrier. We knew that the lighter the pixel, the more probability it was that this was an edge. Also, the greater the edge strenght, the greater the probability as well. Utilizing these probabilities, we could create various models, such as a baye's net, and a HMM that could allow us to program these probabilities into actionable models. 

For each of these models, we would first have to create the emission probability, or the probability that this pixel at this point is a part of the air-ice or ice-rock barrier. To create this probability, we combined the probability based off of the pixel color and the edge strength. In addition to an emission probability, we also created an algorithm that also utilized the previously chosen pixel. Pixels further away from the previous pixel's row were given a lower probability than pixels that were closer.

### Brief Solution Description:
Our program solution to finding the air-ice ice-rock boundaries starts by reading in the echograms as two dimensional arrays. The value stored in the array corresponds to the pixel's color, or radar return. This array is also passed to the edge_weight function to compute a second array, whose x,y value corresponds to the edge strength in that pixel. 

After these arrays are saved, they are then passed to the first Bayes' Net. This algorithm computes the air-ice and ice-rock boundaries using only the emission probabilities. These probabilities are found utilizing both the pixel color and edge strength. We find the pixel color probability by finding the max value in the column. We then divide the current strength against the max strength. Since the lower values are actually greater indicators, we take the resulting fraction minus from one, so we can inverse the fraction. We then square the value to promote smoothness. We do a similar calculation for the edge strength, but we do not inverse it, since the higher the value, the higher chance there is an edge. These values are multiplied to find the combined probability. We loop through each column, pulling out the first max (air-ice), then the second max, which has to be at least 10 pixels lower then the first.

The next algorithm, which uses Veterbi, also utilizes the emission functions, but also takes into account the transition probability. For this probability, we just pull out the last accepted row, then calculate the fraction 1 / (last row position - current row position) (if the rows are the same, we assign 1 as the probability). This value is taken the square root of to promote smoothness again. This value is multiplied against the emission probability.

The last algorithm also utilizes the emission probability and the transition probability. The only change is that it also takes into account the two coordinates provided to teh program. The algorithm will take these provided rows and the first input into the answer and iterates first to the left of the provided columns, pulling out predicted rows, then iterates to the right.

After all predicted rows are generated, they are passed to the draw boundary and draw asterisks functions, which output images such as below.

![Air-Ice ouput for 30png](part2/output_images/30_air_ice_output.png)


### Problems, Assumptions, Decisions, etc. :
The first issue we encountered was how the array was saved (each row saved as their own entry). We realized this meant we would need to assign the, normally row loop, as a column and vice versa for row. After figuring this out, we were then able to continue on and generate the various probabilities. We initially decided to just use max values for the column for both the edge_strength and pixel color and encountered no issues utilizing these, besides on some pics, the initial air-ice boundary would be seen below the actual boundary.

![Air-Ice output for 09](part2/output_images/09_air_ice_output.png)

Others had no issues.

![Ice-Rock output for 30](part2/output_images/30_ice_rock_output.png)

We then had to experiment a bit for the transition probability. Initially, we decided to take a base weighted approach. Every pixel outside of a 10 pixel range would get a base probability of .05, while pixels within the 10 range would recieve the absolute value of row - previous row, which would be inversed against 1 and times by .1. This made the transition probability very strong and would prevent rows from moving at all. Various other weights were attempted, but we ultimately decided on doing away with the 10 pixel range and taking the ratio of the distance for all of the pixels in the column. We also square rooted the ratios, which even further smoothed out the probabilities. We still encounter some issues where it is hard for the algorithm to adapt to rapidly changing boundaries, such as:

![Ice-Rock output for 23](part2/output_images/23_ice_rock_output.png)

But for most cases, it works very well. The Verterbi algorithm, both with and without the human input, performed much better than just the simple bayes' net, as expected.

![Ice-Rock output for 31](part2/output_images/31_ice_rock_output.png)
![Air-Ice output for 23](part2/output_images/23_air_ice_output.png)


## Part 3: Reading Text

### Algorithms Used: Simple Bayes Net and Hidden Markov Model with MAP inference (Viterbi)

### Problem Formulation:
Since there were two separate outputs needed for this part (Simple Bayes output and HMM Viterbi output), we formulated this problem as two separate problems, with HMM being an extension of the Simple Bayes Net. To start, we needed to create transition and initial state probabilities using some text training data (which we decided to use bc.train). In order to get the emission probabilities, we compared each training letter to each testing letter and looked at which testing letter matched up closest to the training letter by comparing a ratio of correct black and white characters relative to the total number of characters. After identifying the emission probabilities, the Simple Bayes net used these probabilieis to get an optimal result for each hidden state (letter). Then, we implemented the initial state probabilities and the transition probabilities in addition to the emission probabilities into a HMM, where a viterbi matrix was created and then backpropagated to find the optimal output using MAP inference.

### Brief Solution Description:
The solution starts by reading in the text training data (bc.train) and using it to find the initial state probs and the transition probs. Since the text training data has POS words in it as well, we made sure to slice it in a way in which these words were removed from the dataset. Then, to find the initial state probabilities, for each letter we took a count of how many words start with that letter then divided it by the total # of words in the dataset. To find transition probabilities, we evaluated letters in pairs (i.e. "Then" becomes "T-->h", "h-->e", "e-->n") and determined for each letter, what percent of that letter's appearances are followed by a particular other letter. As an example, if the letter "T" appears 10 times and of those 10 times, 7 times it is followed by the letter "h", then the transition prob for "T-->h" would be 0.7. For the emission probabilities, we compared each test letter to each train letter and counted how many black and white characters matched to the train letter. We implemented a weighted system because we noticed that for test images with extra "black" noise, increasing the weights on correct white characters improved emission results while for test images with extra "white" noise, increasing the weight on correct black characters improved emission results. So we checked the ratio of black chars/total for both test image and train image and if the test image was more "black" noisy we increased the white correct/total weight and if the test image was less "black" noisy we increase the black correct/total weight. The Bayes net simply outputs the letters with the highest emission probs at each stage. For the HMM, in order to improve run times and since the emission probs were pretty successfull in the bayes net, we limited each stage (letter) to the top 5 emission probs, and then iterated through our viterbi algorithm for each. For a singular state, each of the top 5 emissions is iterated through and calcultated in the viterbi matrix using a weighted min log value of the emission probs, transition probs, and previous state viterbi value (except for the first state which incorporates initial state probs). Once the viterbi matrix is created, the algorithm backtracks through and minimizes the cost - if the new value has a lower cost than the previous value for each state, replace the output with the new state (letter).

### Problems, Assumptions, Decisions, etc. :
The first decision we had to make was to pick a text training dataset, and we decided to use bc.train with POS removal. When creating the initial state probabilities, one relatively important assumption we had to made was whether we wanted the initial state probs to be the likelihood that a *word* starts with a particular letter or if we wanted it to be the likelihood that a *sentence* starts with a particular letter. We decided to go with the first option since that gives us more instances to train on (more total words than total sentences). With the emission probabilities, we decided to use a weighted system since that greatly improved the simple bayes outputs. The weights we decided upon (0.6 & 0.4) vs (0.9 & 0.1) were determined after some parameter tuning and testing. When incorporating the emission and transition probs into the viterbi algorithm, we decided to use a weighted based approach again in order to emphasize the emission probabilities more since they worked so accurately in the simple bayes output, using the transition probs and the previous state vertibi outputs as additional components.
