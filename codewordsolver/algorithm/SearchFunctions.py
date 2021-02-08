def input_2_word(word_in):
    """
    This function takes a string from the input file ''word_in'',
    and returns an array of that ''word'' in a format which is
    more useable by the rest of the code. 
    
    The input file is a .txt file written in the following way:
    1,13,18,25,... 
    5,11,12,19,...
    ...
    where each line is an individual word from the puzzle and
    the numbers correspond to letters (the code to be broken). 
    
    When this is read in by Python each line results in a single string
    '1,13,18,25,...'
    but we want the array ['1','13','18','25',...] to perform opperations on.
    
    This code performs the operation '1,13,18,25,...' -> ['1','13','18','25',...]
    
    MUST BE PERFORNED LINE BY LINE.
    """
    word = [] # Initialise the array we will return
    k = 0 # k to be looped over the size of the ''word_in''.
    switch = 1 # We need a switch because we need to check if the unsolved code is two letters in size.
    # i.e. it is import that '11,12' -> ['11','12'] not ['1','1','1','2']. 
    
    for char in word_in: # go through every character in the input. 
        k += 1 # k checks the index one ahead.  
        if switch == 1: # switch set to zero if the kth character already in word. 
            if char != ',': # We want to remove the commas. 
                if k != len(word_in): # dont want to go outside the size of input. 
                    if word_in[k] != ',': # This means we have a double sized coded letter (i.e. '11')
                        word.append(char + word_in[k]) # Append both characters of double sized letter to one array slot. 
                        switch = 0 # Prevents double storing of double characters. 
                    else:# Coded letter only one character long 
                        word.append(char)# Append to array.
                else:
                    word.append(char)#if k = len(word_in) then the last one can only be one letter character long. 
        elif switch == 0:
            switch = 1# This resets the switch after skipping the second of the double character code. 
    
    return word

def indices_2_find(word, alphabet):
    """
    This function takes in a ''word'' in mixed code format, 
    and returns the indices of the ''letters'' of the word
    which are still un-solved. This function assumes the 
    ''word'' is an array. (i.e. output of inout_2_word).
    
    The ''word'' will have the general format of:
    [1,2,3,'a','b','c',4,5,6]
    
    In performing ''code solving'' operations we are 
    interested in the parts of the word which contain
    un-sovled letters (in the above example indices 0,1,2,6,7,8).
    
    This code performs the operation
    [1,2,3,'a','b','c',4,5,6] -> [0,1,2,6,7,8]
    ''word'' -> ''indices of unsolved letters''.
    
    """

    indices_non_letters = []
    k = 0

    for char in word:
        if char not in alphabet:
            indices_non_letters.append(k)
            "The  test that is performed is whether the character in the word is in the alphabet."
            "If it is not, then the character corresponds to coded letter, and its index is returned."
        k += 1    
    
    return indices_non_letters


def get_words(dictionary,alphabet,forbidden_letters,word):
    """
    This function returns all the words from the dictionary 
    with an identical structure to the given input word.
    
    This involves passing the dictionary through four tests. 
    
    TEST 0: Which words from the dictionary have the right 
    number of letters and right number of unique letters. 
    
    TEST 1: Which of the potential words have all of the
    letters from the part-solved word in the correct locations? 
    
    TEST 2: Are the repeat letters (if they exist) in the 
    potential words in the same place as the real word. 
    
    TEST 3: Do the potential words have any of the previously
    solved letters in the locations of un-solved characters? 
    
    The output of this function is an array of words taken from 
    the dictionary which pass the four tests.  
    
    """
    ############################# ------------------------------------------------ ################################
    """
    TEST 0: LENGTH OF WORD AND NUMBER OF UNIQUE CHARACTERS. 
    """
    list_possible = [] # This will become a list of all the words in the dictionary with the correct basic structure. 
    # Having the correct basic structure is simply defined by having:
    # 1. The right number of total letters
    # 2. The right number of unique letters

    for line in dictionary:# loop through the whole dictionary
        if len(line) == len(word):#right number of total letters
            if len(set(line)) == len(set(word)): # right number of unique letters. 
                # For example, set('abcdeabc') = 'abcde', the list of letters that appear in the set. 
                list_possible.append(line)
    
    # We now define three different arrays.
    # The purpose of these three arrays is to further reduce the current 
    # list of words with the right structure. The current set ''list_possible'' 
    # only checks very basic structural properties (see above). We now want to check
    # whether the repeated indices are in the right place, and also whether the 
    # letters in these words conflict with any of the previously identified letters. 
    
    
    # We need to check all the words in the list of posssible words have the already identified
    # letters in the correct place
    letters_to_check = [] # Array of the letters which must be in the possible words
    indices_to_match = [] # Array of the indices of the above letters
    
    # The potential words must also have the correct structure of the non-solved letters.
    # Primarily this relates to the properties of repeated indices (TEST 2), and ensuring 
    # that no already-solved letters are in the coded parts of the potenital words (TEST 3).
    indices_non_letters = []
    
    # Simply sorts the different characters into ''solved letters'' or ''code'' based
    # on whether that character is in the alphabet.
    k = 0 
    for char in word:# word is the code word to be solved. 
        if char in alphabet:
            letters_to_check.append(char)
            indices_to_match.append(k)
        else:
            indices_non_letters.append(k)
        k += 1    

    
    """
    TEST 1: DO THE POTENTIAL WORDS HAVE THE PREVIOUSLY SOLVED LETTERS IN THE RIGHT PLACES?  
    """
    # We now go from list_possible -> reduced_list, removing words from list_possible 
    # which do not have the solved letters in the correct place. 
    
    reduced_list = []
    l = 0# counts the number of correct letters. 

    if len(letters_to_check) != 0:
        for words in list_possible:# goes through all the words with correct basic structure. 
            for k in range(len(letters_to_check)):# Goes through all the letters that have to be correct. 
                if words[indices_to_match[k]] == letters_to_check[k]:
                    # If the letter of the potential word in the position of the solved index equals the solved letter,
                    # then the word in list_possible does not fail the test on this letter. 
                    l += 1
            if l == len(letters_to_check):
                # if l = len(letters_to_check) then every letter that was checked was in the 
                # right place, so this word passes TEST 1. 
                reduced_list.append(words)# and is added to the reduced list. 
            l = 0# reset the counter 'l' for next word. 

    else: 
        reduced_list = list_possible# No additional information can be found with no letters to check.                    
                
    
    """
    TEST 2: ARE THE REPEATED INDICES OF THE POTENTIAL WORDS IN THE CORRECT PLACE?
    """
        
    # We have already checked that the reduced_list of words has the right number
    # of unique letters as the code word. If the number of unique is not equal to 
    # the total number of letters then some of the letters are repeated. 
    # Only those words with repeated letters at the right points in the word
    # can be acceptable. 
    
    if len(word) != len(set(word)):# If true, there are repeated letters. 
    
        # First we must find the locations of the repeated code letters. 
        k = 0
        l = 0

        index_1 = []# index_1 and index_2 will be arrays of the locations of repeated
        index_2 = []# 'letters' in the word to be decoded. 
        
        # Note that this only considers pairs of repeated characters. 
        # However, the sequence [1,2,1,3,1] contains two pairs of 1s
        # which will both be tested by the code. This identical to
        # testing a triplet, but easier to implement. 

        for char in word:# ''word'' is the code word to be considered. 
            k += 1
            l = 0
            if k != len(word):
                for char2 in word[k:]:
                    l += 1
                    if char == char2:
                        m = k + l - 1
                        index_1.append(k-1)
                        index_2.append(m)

        further_reduced_list = []# an array to be filled by words which pass TEST 2. 
        l = 0

        for words in reduced_list:# all surviving words. 
            for k in range(len(index_1)):
                if words[index_1[k]] == words[index_2[k]]:
                    # if one of the words has this property for one of the repeated indices then it 
                    # passes part of this test. 
                    l += 1
            if l == len(index_1):
                    # if l = len(index_1) then this word has passed the test for every repeated index
                    # and must therefore be added to the surviving list.
                    further_reduced_list.append(words)
            l = 0# reset counter for next word.
    

    else:# no repeated characters -> skip to TEST 3. 
        further_reduced_list = reduced_list

    
    """
    TEST 3: ARE THE REMAINING LETTERS IN THE WORDS ALREADY TAKEN?     
    """
    # if we have solved part of the code then we know that some of the letters are taken.
    # if a potential word which has passed all other tests has one of these letters in 
    # the place of an un-solved character then it cannot be a correct solution.
    # This assumption works on the premise of a 1-to-1 mapping from code to letters, 
    # which is true for codeword puzzles. 
     
    k = 0
    answers = []

    if len(forbidden_letters) != 0:
        for words in further_reduced_list:
            for index in indices_non_letters:# the locations of all the coded characters in the word to be solved. 
                    for letters in forbidden_letters:# pre-solved letters. 
                        if words[index] == letters:# This potential word fails the test.
                            k += 1# 
            if k == 0:
                # any use of a already taken letter (failure of test) makes k > 0.
                # only words which pass test included. 
                answers.append(words)
            k = 0

    else:# no letters previously solved. 
        answers = further_reduced_list
    
    return answers# the list of all words in the dictionary which pass the four tests. 

    
def letters_from_answer(word, answer, indices_non_letters):
    """
    If the get_words function returns only one world, then 
    this automatically decrypts all of the letters in the word. 
    
    This function takes in a word and returns two arrays. 
    The first is the numbers which have been decoded, the
    second is the letters they correspond to.  
    """
    letters_determined = []
    numbers_determined = []

    for index in indices_non_letters:# only checks un-solved indices 
        if index != len(word):
            if word[index] not in word[index+1:]:# only does the last of any repeated solves. 
                numbers_determined.append(word[index]) 
                letters_determined.append(answer[index])
    
    return numbers_determined, letters_determined

def letters_no_answer(word, answers, indices_non_letters):
    """
    If the get_words function returns more than one world, then 
    this does not automatically decrypts any of the letters in the word. 
    
    However, if every word has the same letter in the same location, 
    then that letter can be decrypted. 
    
    This function takes in a list of words and returns two arrays. 
    The first is the numbers which have been decoded, the
    second is the letters they correspond to.  
    """
    l = 0
    letters_determined = []
    numbers_determined = []
    
    for index in indices_non_letters:
        for k in range(len(answers)-1):
            if answers[k][index] == (answers[k+1])[index]:
                l += 1# If two words in the list have the same letter in the same location,
                # then increase the couter by one. 
        if l + 1 == len(answers):# all words have the same letter in the same location. 
            letters_determined.append(answers[0][index])
            numbers_determined.append(word[index])
        l = 0# reset counter. 
    
    """ 
        !!BUG!!
        
        This function has a slight bug in that it can return the same letter twice 
        this is compensated for in solver_1, but should be sorted here.
         
    """

    return numbers_determined, letters_determined  

def indices_of_characters(words_to_solve, character_to_find):
    """
    Returns the indices i,j of the number 'N'. 
    """
    word_index = []
    character_index = []
    i = 0
    j = 0
    for word in words_to_solve:
        j=0
        for char in word:
            if char == character_to_find:
                word_index.append(i)
                character_index.append(j)
            j+=1
        i+=1
    return word_index, character_index


def possible_letters(dictionary, alphabet, solved_letters, word, index):
    """
    Finds all the possible letters from a certain word. 
    """
    answers = get_words(dictionary, alphabet, solved_letters, word)
    possible_letter = []
    for ans in answers:
        if ans[index] not in possible_letter:
            possible_letter.append(ans[index])
    return possible_letter



# End. 