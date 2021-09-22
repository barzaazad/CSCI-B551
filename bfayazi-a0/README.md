# Assignment 0
## Part 1 - Navigation

***State Space:*** Set of all states where the pichu is located in the "house" <br><br>
***Initial State:*** Starting coordinates of the pichu and you along with the corresponding placement of walls<br><br>
***Goal State:*** State of the "house" map where the pichu reaches you<br><br>
***Successor Function:*** Function that will account for the current status of the "house" map and the pichu's current position and return a set of possible moves the pichu can make as a next step given the constraints (1 move horizontal or vertical, walls, etc.)<br><br>
***Cost Function:*** Assuming a uniform cost function of 1<br><br>
***Assumptions:***
* The pichu can only move 1 square at a time in any of the 4 compass directions
* The pichu can not move through walls ("X")

***Why does the program it its initial state fail to find a solution?***
<br>
The original program gets stuck in a loop and fails to find a solution because it does not keep track of visited states
<br><br>
***Specific adjustments made to starter code (Summary of solution)***
<br>
* Within the **moves** function:
  * Added a parameter/variable to the moves function that will track the path of moves (current + successors) using 'U','D','L','R' characters
* Within the **search** function:
  * Added the current path variable to the fringe as its initial state, which is an empty string since there's no path yet at the beginning
  * Record a list of cell locations that have been visited already, initial state will be the pichu start position
  * Within the **fringe** while loop:
    * Adjust the pop method to account for the current path variable we've added to the fringe
    * Explicity record the coordinate of the next move via a variable
    * If the next move is goal state, return current distance + 1 as the # of moves and our path output from the moves function as the path taken in characters
    * If the next move is not a goal state and it has not been visited yet, then add it to the fringe and to our cells visited list
      * This additional if statement helps to ensure that we're not repeating cells and getting stuck in loops, which was the original issue
    * If no solution, return -1 as path length and empty string to represent "no path"

## Part 2 - Hide and Seek

***State Space:*** Set of all states where the pichus are located in non-conflicting positons within the "house" map (cannot see each other directly in either row, column, or diagonal) <br><br>
***Initial State:*** Starting coordinate of the pichu and you along with the corresponding placement of walls<br><br>
***Goal State:*** State of the "house" map where the pichus are arrainged in non-conflicitng positions (cannot see each other directly in either row, column, or diagonal) <br><br>
***Successor Function:*** Function that will account for the current status of the "house" map and the pichu(s) current position(s) and return a new "house" map with 1 additional pichu added in a non-conflicting position <br><br>
***Cost Function:*** Assuming a uniform cost function of 1<br><br>
***Assumptions:***
* The pichu cannot directly see another pichu (same row, column, or diagonal and unblocked)
* The pichus can be blocked by walls or you ("X", "@") from another pichu and be considered valid positioning
<br>

***Specific adjustments made to starter code (Summary of solution)***
<br> There needed to be a way to track the cells around a pichu to see if they could be considered valid positions for another pichu or not. In order to do this, I created 6 (3 main) different functions that would loop through the positions around a pichu and determine if it was a valid placement or not.
* Check for valid row (check columns behind and in front of pichu for conflicts)
* Check for valid column (check rows behind and in front of pichu for conflicts)
* Check for valid diagonal (4 functions that check the top left, bottom left, top right, and bottom right diagonals for conflicts)

Iterating through each of these functions for a cell space, it would only be considered valid positioning if either a "X" or "@" appeared before another pichu, or if the iteration ended without conflicts (only "." in the space)
The larger function that checks row, column and diagonal simultaneously was added to the **successors** function to make sure our successors satisfy those conditions as well.
<br><br>
Within the **solve** function:
* Added a visited states variable to track all the states that have been visited so far (initial empty value)
* If the successor map was not visited yet, add it to the fringe and to the visited states list

Initially, the row and column position checks were inherently obvious and fairly intuitive to write. The diagonals gave me a bit of trouble at first, both due to not exactly knowing what range to iterate through and because naturally combining them into one larger function can lead to more pain points where debugging is necessary.
<br><br>
However, once I broke out the digaonals into their own individual functions, the pattern of row range and column range became apparent, especially helped by the "zip" function that allows iteration through both values simultaneously.
