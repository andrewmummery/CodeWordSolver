# README #


### What is this repository for? ###

* Solving codeword puzzles.  

### How do I get set up? ###

* Pull into it's own folder
* Within the folder, run "python3 -m pip install -e ."

### How do I use? ###

#### Step 1: Get yourself a Codeword puzzle
<img src="https://github.com/andrewmummery/CodeWordSolver/blob/main/tst/trial9/Puzzle9.png" width="850" height="500">

#### Step 2: Open a python terminal and set up the problem
2a) import codewordsolver and use codewordsolver.get_blanck_puzzle_files()

2b) Fill in 'words_to_find.txt' with all the encrypted words in the puzzle

![](https://github.com/andrewmummery/CodeWordSolver/blob/main/example_words_to_find.png)
2c) Then fill in the 'initial_information.txt' file with any letters given to you at the start.
Surprsingly, the algorithms barely ever need any information to sovle the puzzle, so this can often be left blanck
![](https://github.com/andrewmummery/CodeWordSolver/blob/main/example_initial_information.png)

#### Step 3: Use codewordsolver to solve the puzzle 
There are four main functions which can be used to solve the codeword puzzle:
* Function 1: codewordsolver.get_number()
  *  Solves the puzzle and then returns the letter corresponding to the input number.
  *  For example, for the above puzzle, running codewordsolver.get_number(20) returns 't'
* Function 2: codewordsolver.get_letter()
  *  Solves the puzzle and then returns the number corresponding to the input letter.
  *  For example, for the above puzzle, running codewordsolver.get_letter('g') returns '6'
* Function 3: codewordsolver.get_word()
  * Solves the puzzle and then returns a decrypted word.
  * For example, for the above puzzle, running codewordsolver.get_word('14,16,25,22,26') returns 'vodka'
* Function 4: codewordsolver.solve_puzzle()
  * Solves the puzzle and then prints and saves both the key to code and the decrypted words.


For an example of this final function:

<img src="https://github.com/andrewmummery/CodeWordSolver/blob/main/example_output.png">
