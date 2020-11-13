import search_functions as sf
import numpy as np
import urllib.request

def get_dictionary(file_name=''):
    """
    Loads the dictionary. Learn how to store this in stable place.
    i.e. so you dont have to copy the file into the folder of the puzzle. 
    """
    if file_name != '':
        dictionary = []
        with open(file_name) as fp:
            for line in fp:
                line = line.replace('\n','')
                dictionary.append(line)
    else:
        target_url = "https://raw.githubusercontent.com/andrewmummery/CodeWordSolver/main/list_of_words.txt"
        data = urllib.request.urlopen(target_url)
        dictionary = []
        for line in data:
            line = line.decode('utf-8')
            line = line.replace('\n','')
            dictionary.append(line)
    return dictionary 

def get_alphabet(file_name='alphabet.txt'):
    """
    Loads the alphabet. Same as above. 
    """
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    # with open(file_name) as fp:
    #     for line in fp:
    #         line = line.replace('\n','')
    #         alphabet.append(line)
    return alphabet


def load_initial_words(words_to_solve_file='words_to_find.txt'):
    """
    Loads the initial encoded words and converts them into a code-friendly format.
    Returns an array of encoded words, where each entry is a single letter.   
    """
    words_to_solve = []
    with open(words_to_solve_file) as fp:
        for line in fp:
            line = line.replace('\n','')
            words_to_solve.append(sf.input_2_word(line))
    return words_to_solve
    
def load_puzzle(words_to_solve_file='words_to_find.txt',initial_information_file='initial_information.txt'):
    """
    Returns the intial encoded words, and the given letters and their corresponding code values.
    This works only with correctly formatted input files.  
    """
    words_to_solve = []
    with open(words_to_solve_file) as fp:
        for line in fp:
            line = line.replace('\n','')
            words_to_solve.append(sf.input_2_word(line))
    initial = []
    with open(initial_information_file) as fp:
        for line in fp:
            initial.append(line)


    initial_letters = []
    initial_numbers = []

    for line in initial:
        k = 0
        num = ''
        let = ''
        for char in line:
            if char == '=':
                num = line[:k]
                let = line[k+1]
                initial_letters.append(let)
                initial_numbers.append(num)
            k += 1
    
    return words_to_solve, initial_letters, initial_numbers
    
def save_result(solved_letters, solved_numbers, words_to_solve, code_filename='code_solution.txt', solved_words_filename='solved_words.txt'):
    """
    Takes the key from the solved code and saves two files. 
    The first file is a text file of the key.
    The second file is the decoded words from the puzzle.
    """
    sn = np.zeros(len(solved_numbers))
    for k in range(len(sn)):
         sn[k] = int(solved_numbers[k])

    solved_letters = np.array(solved_letters)
    solved_numbers = np.array(solved_numbers)

    solved_letters = solved_letters[sn.argsort()] 
    solved_numbers = solved_numbers[sn.argsort()]
    
    # if print_result:
    #     print()
    #     print('The key of the code is ...')
    #     print()
    #     for k in range(len(solved_letters)):
    #         print(solved_numbers[k],'=',solved_letters[k])
    
    f = open(code_filename, 'w+')
    for k in range(len(solved_letters)):
        f.write(solved_numbers[k] + ' = ' + solved_letters[k])
        f.write('\n')
    f.close()

    
    f2 = open(solved_words_filename,'w+')
    
    for word in words_to_solve:
        k = 0
        for char in word:
            f2.write(char)
            if k != len(word)-1:
                f2.write(',')
            k += 1
            
        f2.write(' = ')
        for char in word:
            for k in range(len(solved_numbers)):
                if char == solved_numbers[k]:
                    f2.write(solved_letters[k])
            if char not in solved_numbers:
                f2.write('-'+char+'-')
        f2.write('\n')
            
    f2.close()
  
    # if print_result:
    #     print()
    #     print('The solved words are ...')
    #     print()
    #     with open(solved_words_filename) as f2:
    #         for line in f2:
    #             print(line)
    

    
   
# End. 