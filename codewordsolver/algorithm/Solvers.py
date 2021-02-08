import codewordsolver.algorithm.SearchFunctions as sf
import sys

def printProgressBar(Q,size,preText,postText=''):
    n_bar =30 #size of progress bar
    q = Q/size
    sys.stdout.write('\r')
    sys.stdout.write(f" {preText} [{'=' * int(n_bar * q):{n_bar}s}] {postText} ")
    sys.stdout.flush()

def print_results(encoded_words, solved_letters, solved_numbers):
    """
        Prints the key of the code and each solved word. 
    
    """
    print()
    print('The key of the code is ...')
    print()
    
    sn = [int(solved_numbers[k]) for k in range(len(solved_numbers))]
    solved_letters = [x for _,x in sorted(zip(sn,solved_letters))]
    solved_numbers = [x for _,x in sorted(zip(sn,solved_numbers))]
    
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
            if l!=len(word)-1:
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
    
    
def solver_1(dictionary, alphabet, words_to_solve, solved_letters=[], solved_numbers=[], print_progress=True, debug=False):
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
    if print_progress:
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
                    if debug:
                        print('WARNING: SIMPLE SOLVE IN TROUBLE.')
                        print('Solver believes that no words in the dictionary have the following format:')
                        print(word)
                        print('the following letters are taken:')
                        print(solved_letters)
                    
                if len(answers) == 1:# only one possible word -> some letters decrypted. 
                    answer = answers[0]
                    if debug:
                        print(answer)
                    num, let = sf.letters_from_answer(word, answer, index_2_find)# decrypted letters. 
                    k = 0
                    for number in num:
                        if (number not in numbers_found) and (let[k] not in letters_found):# updates letters_found (this loop). . 
                            if debug:
                                print(num[k] + ' = ' + let[k])
                            letters_found.append(let[k])
                            numbers_found.append(num[k])
                            nd += 1
                            if print_progress:
                                printProgressBar(nd,26,'Decrypting: ',num[k] + ' = ' + let[k])
                        k += 1
                else:# Even with multiple words may still find individual letters.
                    num, let = sf.letters_no_answer(word,answers,index_2_find)
                    if len(let) != 0:# some solutions found.
                        if debug:
                            print(word)
                        k = 0
                        for number in num:
                            if (number not in numbers_found) and (let[k] not in letters_found):# updates letters_found (this loop). 
                                if k != len(let)-2:
                                    if let[k] not in let[k+1:]:
                                        if debug:
                                            print(str(num[k]) + ' = ' + let[k])
                                        letters_found.append(let[k])
                                        numbers_found.append(num[k])
                                        nd += 1
                                        if print_progress:
                                            printProgressBar(nd,26,'Decrypting: ',num[k] + ' = ' + let[k])
                                else:
                                    if debug:
                                        print(str(num[k]) + ' = ' + let[k])
                                    letters_found.append(let[k])
                                    numbers_found.append(num[k])
                                    nd += 1
                                    if print_progress:
                                        printProgressBar(nd,26,'Decrypting: ',num[k] + ' = ' + let[k])
                            k += 1

        
        if len(letters_found) == 0:# Stops loop when no letters decrypted on full loop.
            break# works for when code fully decrpyted and when no more progress can be made.

        for k in range(len(letters_found)):# updates solved_letters.                    
            solved_letters.append(letters_found[k])
            solved_numbers.append(numbers_found[k])
            
        if debug:
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
        
        if debug:
            print('\n')              
            print(*words_to_solve, sep = '\n')
            print('\n')
    

    nf = len(solved_letters)# if nf > ni then this method has decrypted some of the code. 
    
    if nf == ni:
        print()
        print('Solver 1 FAILED. No new letters found.')
        print()
    elif nf == len(alphabet):
        print()
        print('Solver 1 SUCCESS. All letters found.')
        print()
    else:
        print()
        print('Solver 1 PARTIAL SUCCESS. %.0f new letters found.'%(nf-ni))
        print()
        
    return solved_letters, solved_numbers
    

def solver_2(dictionary, alphabet, words_to_solve, solved_letters = [], solved_numbers = [], print_progress = True, debug = False):
    """
        This function aims to solve a CodeWord puzzle.
        This function, in contrast to solver_1, considers
        all the words in the puzzle together. 
    
        This function takes as input the dictionary to be used
        as a reference, the alphabet of the solutions, and the
        encoded words to be decrypyted. 
    
        If a partial decryption is known, it can also takes as
        input those letters and their corresponding coded characters,
        but defaults to no initial knowledge.
    
        ** BRIEF DESCRIPTION OF ALGORITHM: **
    
        For any encoded word, e.g. '1,3,14,14,22' the function SearchFunctions.possible_letters() returns all the possible 
        letters that each number could represent. 
        
        e.g. the word '1,3,14,14,22' could be 'hello' or 'jelly', so we would infer that the number 1 could be either ['h', 'j'] 
        (obviously there could be more words than hello and jelly, but this is a simple example.)
    
        The algorithm progress by computing, for ever instance of '1' in the puzzle, a list of possible letters like the above.
        
        The solution for the number '1' is the only letter which occurs as one of these potential letters at every location 
        in the puzzle where there is a number '1'. 
    
        On each loop this function calculates the frequency with which each number could represent each letter. This is
        defined as the number of times, e.g. the letters 'a', 'b', 'c' can fit in the location of the number '12', divided
        by the total number of number 12's in the whole puzzle.
        
        If there are ten number 12's in the puzzle, of which eight times it could be an 'a', nine times a 'b', six times a 'c',
        but ten times a 'd', then the number 12 will represent the letter 'd', provided that no other letter can also fit the number 12 
        ten times. (This final requirement is more common for numbers which occur rarely, for example there may be 3 letters which can 
        represent the one occurance of the number 23 etc...). 
    
        This function loops through every number in the puzzle, and calculates the frequency of which this number can be represented by
        every un-used letter in the alphabet. If one and only one letter can represent every instance of that number, then that number is
        considered de-coded and is added to solved_numbers, and the letter added to solved_letters. 
    
        With every loop more letters are found, which constrains the possible solutions for other numbers, which eventually leads to the 
        solution of the puzzle. 
    
        ** NOTE: **
    
        I believe this algorithm is likely to be more robust to missing words than solver_1, as solver_1 considers words in isolation.

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
    if print_progress:
        printProgressBar(nd,26,'Decrypting: ')
    while True:
        numbers_found = []## numbers and letters found this
        letters_found = []## loop. Breaks if none found.
        for num in numberbet:
            word_index, character_index = sf.indices_of_characters(words_to_solve,num)
            n = len(word_index)
            if n != 0:
                total_letters = []## All the possible letters which could be equal to this number. 
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
                            for j in range(len(total_letters[k])):
                                letter_occurances += (total_letters[k][j] == lett)
        
                        letter_frequencies.append(letter_occurances/n)
                    
                    number_of_letters_which_work_everywhere = 0
                    for j in range(len(letter_frequencies)):
                        number_of_letters_which_work_everywhere += (letter_frequencies[j] == 1)
                    if number_of_letters_which_work_everywhere == 1:
                        numbers_found.append(num)
                        ix = max(range(len(letter_frequencies)), key=lambda x: letter_frequencies[x])
                        if alphabet[ix] not in letters_found:
                            letters_found.append(alphabet[ix])
                            nd += 1
                            if print_progress:
                                printProgressBar(nd,26,'Decrypting: ',num + ' = ' + alphabet[ix])
                            if debug:
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
        print('Solver 2 FAILED. No new letters found.')
        print()
    elif nf == len(alphabet):
        print()
        print('Solver 2 SUCCESS. All letters found.')
        print()
    else:
        print()
        print('Solver 2 PARTIAL SUCCESS. %.0f new letters found.'%(nf-ni))
        print()
        
    return solved_letters, solved_numbers


# End. 