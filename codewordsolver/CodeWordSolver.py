import codewordsolver.algorithm.Solvers as solve
import codewordsolver.algorithm.Files as fi

def solve_puzzle(path_to_words_to_find='words_to_find.txt',path_to_initial_information='initial_information.txt',
        solver='2',save_results=True, print_results=True, dictionary_file='',print_progress=True, debug=False):
    """
        Solves a CodeWord puzzle, with puzzle file path_to_words_to_find and initial infromation file path_to_initial_information.
        
        There are two algorithms which can be used to try and solve the puzzle: 
        Solver 1 only considers words individually, while Solver 2 considers all of the words in the puzzle at once.
        More information about the solving algorithms is available in the file codewordsolver/algorith/Solvers.py
        
        This function returns the key to the code, i.e. a list of the solved letters and the numbers they corresond to.
        
        The code solution can be saved using save_results, or printed using print_results. 
        
        To keep updated with the progress of the solver you can use print_progress=True, if something goes wrong you might want 
        to use debug=True to see a more detailed step-by-step analysis of the programs attempt to solve the puzzle. 
        
    """
    dictionary = fi.get_dictionary(dictionary_file)
    alphabet = fi.get_alphabet()
    words_to_solve, initial_letters, initial_numbers = fi.load_puzzle(path_to_words_to_find, path_to_initial_information)
    solver = str(solver)
    if solver == '2':
        solved_letters, solved_numbers = solve.solver_2(dictionary=dictionary,alphabet=alphabet,words_to_solve=words_to_solve,
         solved_letters=initial_letters, solved_numbers=initial_numbers,print_progress=print_progress,debug=debug)
    elif solver == '1':
        solved_letters, solved_numbers = solve.solver_1(dictionary=dictionary,alphabet=alphabet,words_to_solve=words_to_solve,
         solved_letters=initial_letters, solved_numbers=initial_numbers,print_progress=print_progress,debug=debug)
    else:
        print('No solver method chosen, defaulting to solver 2.')
        solved_letters, solved_numbers = solve.solver_2(dictionary=dictionary,alphabet=alphabet,words_to_solve=words_to_solve,
         solved_letters=initial_letters, solved_numbers=initial_numbers,print_progress=print_progress,debug=debug)
    if save_results:
        initial_code = fi.load_initial_words(path_to_words_to_find)
        fi.save_result(solved_letters,solved_numbers,initial_code)
    if print_results:
        encoded_words = fi.load_initial_words(path_to_words_to_find)
        solve.print_results(encoded_words, solved_letters, solved_numbers)
    
    return solved_letters, solved_numbers

def get_letter(letter, path_to_words_to_find='words_to_find.txt', path_to_initial_information='initial_information.txt',
    solver='2',dictionary_file=''):
    
    """
        Returns (if the algorithm finds a solution) the encoded number for a given input letter. 
    
        i.e. get_letter('a') will return e.g. 12 if a = 12 in the puzzle, or None if no solution could be found. 
        
    """
    
    if letter not in fi.get_alphabet():
        raise ValueError('You are trying to find a letter: %s not in the solution alphabet. \n If you are looking for a number, use get_number()'%letter)

    soln_letters, soln_numbers = solve_puzzle(path_to_words_to_find=path_to_words_to_find,path_to_initial_information=path_to_initial_information,
        solver=solver,save_results=False, print_results=False, dictionary_file=dictionary_file,print_progress=False, debug=False)
    
    if letter in soln_letters:
        print('Letter found:  %s = %s \n'%(letter, soln_numbers[soln_letters.index(letter)]))
        return soln_numbers[soln_letters.index(letter)]
    else:
        print('Could not find letter: %s \n'%letter)
        return None

def get_number(number, path_to_words_to_find='words_to_find.txt', path_to_initial_information='initial_information.txt',
    solver='2',dictionary_file=''):
    
    """
        Returns (if the algorithm finds a solution) the letter corresponding to a given input encoded number. 
    
        i.e. get_number('12') will return e.g. 'a' if a = 12 in the puzzle, or None if no solution could be found. 
        
    """
    
    soln_letters, soln_numbers = solve_puzzle(path_to_words_to_find=path_to_words_to_find,path_to_initial_information=path_to_initial_information,
        solver=solver,save_results=False, print_results=False, dictionary_file=dictionary_file,print_progress=False, debug=False)
    
    if number in soln_numbers:
        print('Number found:  %s = %s \n'%(number, soln_letters[soln_numbers.index(number)]))
    else:
        print('Could not find number: %s \n'%number)
    return None

def get_word(word, path_to_words_to_find='words_to_find.txt', path_to_initial_information='initial_information.txt',
    solver='2',dictionary_file=''):
    
    """
        Returns (if the algorithm finds a solution) the solution letters for each number in a given input 'word'. 
        
        The 'word' must be input in the following way: e.g. '1,22,4,4,12'
        
        i.e. get_letter('1,22,4,4,12') will return e.g. 'hello' if 1 = h, 22 = e, 4 = l, 12 = o.
        
        If only a subset of the letters can be found then it will return those letters. 
        
    """
    
    soln_letters, soln_numbers = solve_puzzle(path_to_words_to_find=path_to_words_to_find,path_to_initial_information=path_to_initial_information,
        solver=solver,save_results=False, print_results=False, dictionary_file=dictionary_file,print_progress=False, debug=False)
    
    word = word.split(',')
    solved_word = [val for val in word]
    for i, number in enumerate(word):
        if number in soln_numbers:
            solved_word[i] = soln_letters[soln_numbers.index(number)]
        else:
            solved_word[i] = number 
    if any(char in word for char in solved_word):
        print(','.join(word) +' = ' + ' , '.join(solved_word) +'\n')
    else:
        print(','.join(word) + ' = ' + ''.join(solved_word) +'\n')
    
    return None    
    
def get_blank_puzzle_files():
    initial_information_text = """# Write any decoded letters and the number they correspond to
# in this file. 
#
# Each decoded letter must be input on a new line. 
#
# These can be letters you are given at the start
# of the puzzle or ones you have worked out 
#
# The format they should be written in is
#  'number' 'equals' 'letter'.
#  e.g. 
# 10 = e
# 19 = q
# etc...
# 
# often no initial letters are required to break the code. 
# 
# Write information below, with no # at the start of the line.
# Letters must be in lower-case.
"""
    f1 = open('initial_information.txt', 'w+')
    f1.write(initial_information_text)
    f1.write('\n')
    f1.close()
    
    words_to_find_text = """# In this file type each of the encoded 'words'
# from the puzzle. The CodeWordSolver will use these
# 'words' to decrypt the puzzle.
#
# Each new word must be input on a new line. 
#
# These words must be typed in the format
# number1, number2, number3, ...
# 
# e.g. 
# 1,6,17,17,3,26
# 21,8,4,5,12,11
# etc.....
# 
# Do not include any pre-solved letters at 
# this point. Exclusively numbers.
#
# Write information below, with no # at the start of the line.     
"""        
    f2 = open('words_to_find.txt', 'w+')
    f2.write(words_to_find_text)
    f2.write('\n')
    f2.close()
    
    return 
    
    