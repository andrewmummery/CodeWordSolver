import search_functions as sf
import numpy as np
import sys

def printProgressBar(Q,max,preText,postText=''):
    n_bar =30 #size of progress bar
    q = Q/max
    sys.stdout.write('\r')
    sys.stdout.write(f" {preText} [{'=' * int(n_bar * q):{n_bar}s}] {postText} ")
    sys.stdout.flush()

def print_results(encoded_words, solved_letters, solved_numbers):
    print()
    print('The key of the code is ...')
    print()
    sn = np.zeros(len(solved_numbers))
    for k in range(len(sn)):
         sn[k] = int(solved_numbers[k])

    solved_letters = np.array(solved_letters)
    solved_numbers = np.array(solved_numbers)

    solved_letters = solved_letters[sn.argsort()] 
    solved_numbers = solved_numbers[sn.argsort()]
    for k in range(len(solved_letters)):
        print(solved_numbers[k],'=',solved_letters[k])
    
    decrypted_words = []
    encrypted_words = []
    for word in encoded_words:
        decrypted_word = str()
        encrypted_word = str()
        l = 0
        for char in word:
            encrypted_word += char
            if l!=len(word):
                encrypted_word += ','
            l+=1
            for k in range(len(solved_numbers)):
                if char == solved_numbers[k]:
                    decrypted_word += solved_letters[k]
            if char not in solved_numbers:
                to_add = '-'+char+'-'
                decrypted_word += to_add
        decrypted_words.append(decrypted_word)
        encrypted_words.append(encrypted_word)
    
    print()
    k = 0
    for word in encrypted_words:
        print(word,'=',decrypted_words[k])
        k+=1
    print()
    
    
    
    
def simple_solve(dictionary, alphabet, words_to_solve, solved_letters=[], solved_numbers=[], print_progress=True):
    """
    This function aims to solve the codeword puzzle in a simple fashion. 
    The simplicity of this method results from it only considering each
    word in isolation -> there is no cross referencing of different words. 
    
    This function takes as input the dictionary to be used as a reference,
    the alphabet of the solutions, and the encoded words to be decrypyted. 
    
    If a partial decryption is known, it can also takes as input those letters
    and their corresponding coded characters, but defaults to no initial 
    knowledge. 
    
    This function loops through all the words in ''words_to_solve'' and
    passes each one to ''get_words'' and then ''get_letters_from_answers''. 
    If any encoded letters are found then solved_letters is updated, which 
    increases the chance of finding further letters. Each word is treated 
    entirely in isolation. 
    
    This function returns the 'key' of the code, a list of decrypted letters
    and their corresponding coded characters. 
    
    """
    
    # Update the list of coded words with the initially provided decrypted letters. 
    current_solution = words_to_solve
    for word in current_solution:
        l = 0
        for char in word:
            for k in range(len(solved_numbers)):
                if char == solved_numbers[k]:
                    word[l] = solved_letters[k]
            l += 1
    
    ni = len(solved_letters) # this will be used to check if the solver worked. 
    nd = ni
    printProgressBar(nd,26,'Decrypting: ')
    while True:# Will loop through until no further progress is possible. 
        letters_found = []# Both arrays used for one loop through all the encoded words.
        numbers_found = []# Will be used to update solved_letters. 
        for word in current_solution:
            num = []# Where we will store any found code characters
            let = []# and corresponding decrypted letters for a particular word. 
            index_2_find = sf.indices_2_find(word,alphabet)# Finds how many characters in word are unknown. 
            if len(index_2_find) != 0:# There are still characters to solve. 
                answers = sf.get_words(dictionary,alphabet,solved_letters,word)# finds all words with correct structure from dictionary.  
                if len(answers) == 0:
                    # no words in the dictionary with the correct structure.
                    # this is presumably due to the shortness of the dictionary. 
                    print('WARNING: SIMPLE SOLVE IN TROUBLE.')
                    print('Solver believes that no words in the dictionary have the following format:')
                    print(word)
                    print('the following letters are taken:')
                    print(solved_letters)
                    
                if len(answers) == 1:# only one possible word -> some letters decrypted. 
                    answer = answers[0]
                    if print_progress:
                        print(answer)
                    num, let = sf.letters_from_answer(word, answer, index_2_find)# decrypted letters. 
                    k = 0
                    for number in num:
                        if (number not in numbers_found) and (let[k] not in letters_found):# updates letters_found (this loop). . 
                            if print_progress:
                                print(num[k] + ' = ' + let[k])
                            letters_found.append(let[k])
                            numbers_found.append(num[k])
                            nd += 1
                            printProgressBar(nd,26,'Decrypting: ',num[k] + ' = ' + let[k])
                        k += 1
                else:# Even with multiple words may still find individual letters.
                    num, let = sf.letters_no_answer(word,answers,index_2_find)
                    if len(let) != 0:# some solutions found.
                        if print_progress:
                            print(word)
                        k = 0
                        for number in num:
                            if (number not in numbers_found) and (let[k] not in letters_found):# updates letters_found (this loop). 
                                if k != len(let)-2:
                                    if let[k] not in let[k+1:]:
                                        if print_progress:
                                            print(str(num[k]) + ' = ' + let[k])
                                        letters_found.append(let[k])
                                        numbers_found.append(num[k])
                                        nd += 1
                                        printProgressBar(nd,26,'Decrypting: ',num[k] + ' = ' + let[k])
                                else:
                                    if print_progress:
                                        print(str(num[k]) + ' = ' + let[k])
                                    letters_found.append(let[k])
                                    numbers_found.append(num[k])
                                    nd += 1
                                    printProgressBar(nd,26,'Decrypting: ',num[k] + ' = ' + let[k])
                            k += 1

        
        if len(letters_found) == 0:# Stops loop when no letters decrypted on full loop.
            break# works for when code fully decrpyted and when no more progress can be made.

        for k in range(len(letters_found)):# updates solved_letters.                    
            solved_letters.append(letters_found[k])
            solved_numbers.append(numbers_found[k])
            
        if print_progress:
            print('\n')
            print(solved_letters)
            print(solved_numbers)

        for word in current_solution:# updates the list of words which are looped over
            l = 0# with newly decrypted letters. 
            for char in word:
                for k in range(len(solved_numbers)):
                    if char == solved_numbers[k]:
                        word[l] = solved_letters[k]
                l += 1
        
        if print_progress:
            print('\n')              
            print(*words_to_solve, sep = '\n')
            print('\n')
    

    nf = len(solved_letters)# if nf > ni then this method has decrypted some of the code. 
    
    if nf == ni:
        print()
        print('Simple solver FAILED. No new letters found.')
        print()
    elif nf == len(alphabet):
        print()
        print('Simple solver SUCCESS. All letters found.')
        print()
    else:
        print()
        print('Simple solver PARTIAL SUCCESS. %.0f new letters found.'%(nf-ni))
        print()
        
    return solved_letters, solved_numbers
    

def better_solve(dictionary, alphabet, words_to_solve, solved_letters = [], solved_numbers = [], print_progress = True):
    """
    
    
    """
    numberbet = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26']
    
    # Update the list of coded words with the initially provided decrypted letters. 
    current_solution = words_to_solve
    for word in current_solution:
        l = 0
        for char in word:
            for k in range(len(solved_numbers)):
                if char == solved_numbers[k]:
                    word[l] = solved_letters[k]
            l += 1    
    
    ni = len(solved_letters) # this will be used to check if the solver worked. 
    nd = ni
    printProgressBar(nd,26,'Decrypting: ')
    while True:
        numbers_found = []
        letters_found = []
        for num in numberbet:
            word_index, character_index = sf.indices_of_characters(words_to_solve,num)
            n = len(word_index)
            if n != 0:
                total_letters = []
                for k in range(n):
                    new_let = sf.possible_letters(dictionary, alphabet, solved_letters, current_solution[word_index[k]], character_index[k])
                    if len(new_let) != 0:
                        total_letters.append(new_let)
                letter_frequencies = []
                n = len(total_letters)
                if n != 0:
                    for lett in alphabet:
                        letter_occurances = 0
                        for k in range(n):
                            letter_occurances += np.sum(np.array(total_letters[k]) == lett)
        
                        letter_frequencies.append(letter_occurances/n)
        
                    if np.sum(np.array(letter_frequencies)==1.0)==1:
                        numbers_found.append(num)
                        ix = np.argmax(np.array(letter_frequencies))
                        letters_found.append(alphabet[ix])
                        nd += 1
                        printProgressBar(nd,26,'Decrypting: ',num + ' = ' + alphabet[ix])
                        if print_progress:
                            print(num,'=',alphabet[ix])

                    
        
        if len(numbers_found) == 0:
            break
    
        else:
            for k in range(len(letters_found)):
                solved_letters.append(letters_found[k])
                solved_numbers.append(numbers_found[k])
    
        for word in current_solution:# updates the list of words which are looped over
            l = 0# with newly decrypted letters. 
            for char in word:
                for k in range(len(solved_numbers)):
                    if char == solved_numbers[k]:
                        word[l] = solved_letters[k]
                l += 1
    
    nf = len(solved_letters) # if nf > ni then this method has decrypted some of the code.  
    
    if nf == ni:
        print()
        print('Better solver FAILED. No new letters found.')
        print()
    elif nf == len(alphabet):
        print()
        print('Better solver SUCCESS. All letters found.')
        print()
    else:
        print()
        print('Better solver PARTIAL SUCCESS. %.0f new letters found.'%(nf-ni))
        print()
        
    return solved_letters, solved_numbers


# End. 