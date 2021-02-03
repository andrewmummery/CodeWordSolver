import codewordsolver.algorithm.Solvers as solve
import codewordsolver.algorithm.Files as fi

def solve_puzzle(path_to_words_to_find='words_to_find.txt',path_to_initial_information='initial_information.txt',solver='2',save_results=True, print_results=True, dictionary_file=''):
    dictionary = fi.get_dictionary(dictionary_file)
    alphabet = fi.get_alphabet()
    words_to_solve, initial_letters, initial_numbers = fi.load_puzzle(path_to_words_to_find, path_to_initial_information)
    solver = str(solver)
    if solver == '2':
        solved_letters, solved_numbers = solve.better_solve(dictionary,alphabet, words_to_solve, initial_letters, initial_numbers, False)
    elif solver == '1':
        solved_letters, solved_numbers = solve.simple_solve(dictionary,alphabet, words_to_solve, initial_letters, initial_numbers, False)
    else:
        print('No solver method chosen, defaulting to solver 2.')
        solved_letters, solved_numbers = solve.better_solve(dictionary,alphabet, words_to_solve, initial_letters, initial_numbers, False)
    if save_results:
        initial_code = fi.load_initial_words(path_to_words_to_find)
        fi.save_result(solved_letters,solved_numbers,initial_code)
    if print_results:
        encoded_words = fi.load_initial_words(path_to_words_to_find)
        solve.print_results(encoded_words, solved_letters, solved_numbers)
    return 


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
    
    