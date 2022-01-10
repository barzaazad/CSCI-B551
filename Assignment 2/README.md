# CS B551 - Assignment 2: Games and Bayesian Classifiers

## Part 1: Raichu

State Space: Set of all states where the pichus, pikachus, and raichus can be placed on a NxN board (N >= 8)

Initial State: Initial board configuration shown in Assignment 2 PDF (but for testing purposes can be any valid state)

Goal State: State of the board when the opposing player has 0 total pieces remaining you

Successor Function: Function that will account for the current state of the board and the current player and returns a set of possible next moves that can be done to the board given the piece movement contraints


### Algorithm Used: Minimax with Alpha-Beta pruning

### Heuristic Evaluation Function:
We used a heuristic evaluation function that gave different weights to the differences between the # of each type of piece on the board for each player, combined with an additional weighted element of the # of possible "next" moves from the successor. The weights were determined arbitrarily initially based off of the general importance of each piece, and was then tuned after rounds of testing. For example, for player "w" the difference between the # of pichus was given a weight of 1 (1*(# of white pichus - # of black pichus)), the difference between the # of pikachus was given a weight of 5, the difference between the # of raichus was given a weight of 15, and the difference between the # of successors (next moves) was given a weight of 0.1.

### Problem Formulation:
Since the description of the game matches all of the requirements of an adversarial search based game (two player, turn taking, 0 sum, time constraints, etc.), We decided to use minimax at a max depth of 3 with alpha-beta pruning in order to optimize run times. Within the minimax algorithm, we had to determine a evaluation function to use to evaluate each state depending on the player. We decided to use a weighted evaluation function that placed weights on the difference between the # of each unique piece. The more important pieces (raichu) got greater weights than the less important pieces (pichu) so the algorithm would be motivated to try to elimitate the oppositions raichu pieces over a pichu piece for example. Additionally, since there are states thoroughout the game where it's not possible to capture an opponents piece within the next move, we added an additional piece that accounted for flexibility of moves by finding the difference between the # of successors for each move and gave this a weight of 0.1 (since the # can be extremely large). This way, in situations where the weighted piece components sum up to 0 (since you can't capture an opponents piece on every single move) the algorithm would account for moves that give you the most movement flexibility in the future as well. This portion definitely increases the run time of the algorithm, especially for states with a lot of raichus since they have a lot of successors, but it was a necessary component to add to handle those weighted 0 sum states effectively.

### Brief Solution Description:
The solution works by initializing alpha and beta values as +infinity and -infinity respectively with a max depth of 3. Then, it runs the alpha beta function using the initial board and current player from the command line arguments and the initial alpha and beta values and identifies all the successors from the current state. For each succcessor, the alpha beta script works to maximize the minimum value at (-infinity,infinity). To do this, it works through both the min and max functions, traversing +1 depth down the tree and pulling the min of beta and max_values for the min script and pulling the max of alpha and min_values for the max script. The algorithm will end this min/max back and forth when the max depth has been reached or a goal state has been reached, and will then output the move that gives the maximum evaluation function value. A goal state is reached when the opponent has 0 available pieces left on the board.

### Problems, Assumptions, Decisions, etc. :
The primary decision to be made was what to use as the evaluation function. In games like these where different pieces have different impacts (i.e. raichu can make more moves than pichu and pikachu), a weighted evaluation function seemed to be the most logical idea. For each piece, the difference between the # of pieces on the board between players is determed and then that number is given a particular weight, with the more valuable pieces getting more weight. There was some necessary tuning to the weights of each piece, but we eventually settled on 1 for pichu, 5 for pikachu, and 15 for raichu. Additionally, there are states (such as the initial state) where a single move won't eliminate any pieces and our evaluation function will return 0 for the successors. To account for this, we added an additional piece that accounted for how much future mobility a move will give you by taking the difference between the total # of successors from the current state between each player and multiplying it by 0.1. This definitely increases run times, especially for states with a lot of raichus, but it also helps greatly when trying to evaluation some of these "even" initial and mid game states.

## Part 2: The Game of Tetris

State Space: Set of all states where the tetris pieces can be placed.

Initial State: No tetris pieces placed, resulting in no score or placed piece hieght.

Goal State: A state where the placement of a piece results in the removement of a row (height of placed pieces) or does not increase the height of the placed pieces.

Successor function: Function that will evaluate the and return the possible placement of a given piece.

### Algorithm Used: Expectimax

### Heurisitc Evaluation Function:

The heuristic evaluation function of an expectimax algorithm has a some unique contraints that do not apply to a normal minimax algorithm. Since an aspect of chance is apparent in this game (the selection of the third piece), we cannot give logarithmic weights to preferred states. Our function must scale linearly between different states. To achieve this, our evaluation function evaluates the placement of the piece on the board. If this piece removes n lines, then the score will be +n. If the placement of the piece increases the height of the current lines, then the score will be -n. If the placement doesn't increase or decrease the heights, we will return 0.

### Chance Node Evaluation

The unknown of the third piece presents a chance factor. For these chance nodes, our evaulation will take the expected value of the leaf nodes. Initially, the probability of each piece being selected is 1/6. As noted in the assignmnet, the probablity actually follows a distribution. We can attempt to esimate this distribution and modify the probablity assigned to the chance nodes.

### Problem Forumlation:

The game of Tetris has the following characteristics: 1 player, element of chance (third piece), and time constrained. Taking into condierstaion these characteristics, we decided to impliment an expectimax algorithm. As with a minimax algorith, we again needed to implement an evaluation function that returned a score for a possible state. As stated earlier, with the element of probability, we decided to scale our scores linearly. This evaluation function would return +n, -n, or 0 based on how many rows a given piece would eliminate with its possible placement. This would allow the algorithm to prioritize reducing the number of rows on the board with the placements. To take into consideration of the unknown third piece, we would also implement the chance nodes as described previously. Since we cannot know what the third piece would be, our proposed probability of 1/6 would be used to calculate the expected value for each chance nodes.

### Brief Solution Description:



### Problems, Assumptions, Decisions, etc. :



## Part 3: Truth be Told

### Problem Statement:
Suppose there are classes A and B. For a given textual object D consisting of words w1, w2,...wn, a Bayesian clasifier evaluates decides that D belongs to A by computing the 
"odds" and comparing to a threshold, where P (A|w1, ...wn) is the posterior probability that D is in class A. Using the Naive Bayes assumption, the odds ratio can be factored
into P (A), P (B), and terms of the form P (wi|A) and P (wi|B). These are the parameters of the Naive Bayes model. AS a specific usecase we are provided with a dataset of user
generated reviews. We need to classify reviews into faked or legitimate, for 20 hotels in Chicago. Our job is write use a program that estimates the Naive Bayes parameters from
training data(where the correct label is given), and then uses these parameters to classify the reviews in the testing data.

### Approach Explanation:

Classifier function:

This function should take a train_data dictionary that has three entries. train_data["objects"] is a list of strings corresponding to reviews. train_data["labels"] is a list of
strings corresponding to ground truth labels for each review. train_data["classes"] is the list of possible class names (always two). we are also passing a test_data dictionary
that has objects and classes entries in the same format as above. We are declaring a frequency dictionary. train_length stores the length of list of strings corresponding to reviews. Now, we are going to traverse through the range of this train_length. String stores the strings corresponding to reviews for particular index. Now, we are going to call
strip function on this string and also converting the string into lower case. The split function is going to split a string into a list where each  word is a list item. We are 
storing this in parsed_string. For every term in parsed_string if the term is not present in the frequency we are going to declare a dictionary for that particular term  in the
frequency. If the ground truth label at that particular index is "deceptive" and if the deceptive is not in frequency[term] we are making frequency[term][deceptive] as 0 and then
incrementing it by 1. Else, if the truthful is not in frequency[term] we are making frequency[term]['truthful'] as 0 then incrementing by 1. Then we are taking a list named final.
The test_length stores the length of list of strings corresponding to reviews. Now, we are going to traverse through the range of this test_length. String stores the string corresponding to reviews for particular index. Like train_data we are going to call the strip(),lower() and split() functions on this test_data as well and store in parsed_string. 
For every term in parsed_string if the term not in frequency continue. Else if deceptive or truthful not in freqquency[term] continue. Else based on the frequency of 'truthful'
and 'deceptive' find the ratio by ratio = ratio*frequency[term]['truthful'] / frequency[term]['deceptive']. So, if the ratio is greater than 1 we are appending 'truthful' to the final else we are appending 'deceptive' to the final. We are going to return the final. Finally we are going to calculate the accuracy for our classified data.
