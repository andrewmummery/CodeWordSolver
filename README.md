# README #


### What is this repository for? ###

* Solving codeword puzzles.  

### How do I get set up? ###

* Pull into it's own folder
* Within the folder, run "python3 -m pip install -e ."

### How do I use? ###

#### Step 1: Get yourself a Codeword puzzle
![](https://github.com/andrewmummery/CodeWordSolver/blob/main/tst/trial9/Puzzle9.png)

#### Step 2: Open a python terminal and set up the problem
2a) import codeword solver and use codewordsolver.get_blanck_puzzle_files()

2b) Fill in 'words_to_find.txt' with all the encrypted words in the puzzle

![](https://github.com/andrewmummery/CodeWordSolver/blob/main/example_words_to_find.png)
2c) Then fill in the 'initial_information.txt' file with any letters given to you at the start.
Surprsingly, the algorithms barely ever need any information to sovle the puzzle, so this can often be left blanck
![](https://github.com/andrewmummery/CodeWordSolver/blob/main/example_initial_information.png)
