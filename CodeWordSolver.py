import solvers as solve
import files as fi

def solve_puzzle(path_to_words_to_find='words_to_find.txt',path_to_initial_information='initial_information.txt',solver='2',save_results=True, print_results=True):
    dictionary = fi.get_dictionary()
    alphabet = fi.get_alphabet()
    words_to_solve, initial_letters, initial_numbers = fi.load_puzzle(path_to_words_to_find, path_to_initial_information)
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