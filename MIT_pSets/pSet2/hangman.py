# Problem Set 2, hangman.py
# Name: -
# Collaborators: -
# Time spent: 6 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    count=0
    for letter in secret_word:
        if letter in letters_guessed:
            count+=1
    if count == len(secret_word):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    my_dict={}
    guessed=""
    for i in range(0,len(secret_word)):
        for j in range(0,len(letters_guessed)):
            if letters_guessed[j]==secret_word[i]:
                my_dict[i]=letters_guessed[j]

    for i in range(0,len(secret_word)):
        if i in my_dict:
            guessed+=my_dict[i]
            guessed+=" "
        else:
            guessed+="_"
            guessed+=" "

    return guessed

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DEL
    letters="abcdefghijklmnopqrstuvwxyz"
    new_letters=""
    check_in=False
    for i in range(0,len(letters)):
        for j in range(0,len(letters_guessed)):
            if letters_guessed[j]==letters[i]:
                check_in=True
                break
        if check_in:
            new_letters+=""
            check_in=False
        else:
            new_letters+=letters[i]

    return new_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    num_of_guess = 6
    num_of_warn = 3
    num_of_correct_guess=0
    letters_guessed = []
    letters = " abcdefghijklmnopqrstuvwxyz"
    vowels="aeio"
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("You have",num_of_warn,"warnings left.")
    print("----------------------------")

    while True:
        print("You have",num_of_guess,"guess left.")
        print("Available letters:",get_available_letters(letters_guessed))
        guess=input("Please guess a letter: ")
        same_letter = ""
        myword = ""
        check_same_letters=False
        """
        Checking for same letter guessing
        """
        if guess in letters_guessed:
            check_same_letters=True
            same_letter+=guess

        letters_guessed += guess
        get_available_letters(letters_guessed)
        """
        firstly check if guess is the allowed 
        if its allowed secondly check if its same guess
        if its a same guess then give warning until no warnings left then decrease guess rights
        if its not a same guess check if its a correct guess then increase your unique correct guess number for point
        if its not then decrease guess rights
        depending letter type(vowel(-2 decrease) or not(-1 decrease))
        """
        if guess in letters and guess != '':
            if check_same_letters:
                num_of_warn -= 1
                if num_of_warn>0:
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Oops! You've already guessed that letter. You have",num_of_warn,"warnings left:",myword)
                else:
                    num_of_guess-=1
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Oops! You've already guessed that letter. You have no warnings left:", myword)
                letters_guessed.remove(same_letter)
            else:
                if guess in secret_word:
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Good Guess", myword)
                    num_of_correct_guess += 1
                else:
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Oops! That letter is not in my word.",myword)
                    if guess in vowels:
                        num_of_guess -= 2
                    else:
                        num_of_guess -= 1
        else:
            if num_of_warn>0:
                num_of_warn -= 1
                myword=get_guessed_word(secret_word,letters_guessed)
                print("Oops! That is not a valid letter. You have",num_of_warn,"warnings left:",myword)
            else:
                myword = get_guessed_word(secret_word, letters_guessed)
                print("Oops! That is not a valid letter. You have", num_of_warn, "warnings left:", myword)

        """
        if no guess chance left and not found the word then lose the game
        if found the correct word then calculate point=number of correct guess*number of guesses left
        """
        check_word_guessed=is_word_guessed(secret_word,letters_guessed)
        if num_of_guess<=0:
            if not check_word_guessed:
                print("---------------------------------------")
                print("Sorry, you ran out of guesses. The word was else. ")
                break
        if check_word_guessed:
            total_point=num_of_correct_guess*num_of_guess
            print("---------------------------------------")
            print("Congratulations, you won!")
            print("Your total score for this game is:",total_point)
            break
        print("---------------------------------------")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)

# -----------------------------------

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    count_for_check=0
    count_for_letter=0

    if len(my_word)==len(other_word):
        for i in range(0,len(my_word)):
            if my_word[i]!='_':
                count_for_letter+=1
                if my_word[i]==other_word[i]:
                    count_for_check+=1
            else:
                if other_word[i] in my_word:
                    return False
        if count_for_check == count_for_letter:
            return True
        else:
            return False
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    myword_nospace=""
    for i in range(0,len(my_word)):
        if my_word[i]!=' ':
            myword_nospace+=my_word[i]
    newline_count=0
    for i in range(0,len(wordlist)):
        if match_with_gaps(myword_nospace,wordlist[i]):
                print(wordlist[i],"  ",end="")
                newline_count+=1
                if newline_count%5==0:
                    print("\n")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    num_of_guess = 6
    num_of_warn = 3
    num_of_correct_guess=0
    letters_guessed = []
    letters = " abcdefghijklmnopqrstuvwxyz"
    vowels="aeio"
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("You have",num_of_warn,"warnings left.")
    print("----------------------------")
    while True:
        print("You have",num_of_guess,"guess left.")
        print("Available letters:",get_available_letters(letters_guessed))
        guess=input("Please guess a letter: ")
        same_letter = ""
        myword = ""
        check_same_letters=False
        """
        Checking for same letter guessing
        """
        if guess in letters_guessed:
            check_same_letters=True
            same_letter+=guess

        letters_guessed += guess
        get_available_letters(letters_guessed)
        """
        firstly check if guess is the * then give hints after check: 
        if its allowed then check if its same guess
        if its a same guess then give warning until no warnings left then decrease guess rights
        if its not a same guess check if its a correct guess then increase your unique correct guess number for point
        if its not then decrease guess rights
        depending letter type(vowel(-2 decrease) or not(-1 decrease))
        """
        if guess == '*':
            myword+=get_guessed_word(secret_word,letters_guessed)
            print("Possible word matches are:")
            show_possible_matches(myword)

        elif guess in letters and guess != '':
            if check_same_letters:
                num_of_warn -= 1
                if num_of_warn>0:
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Oops! You've already guessed that letter. You have",num_of_warn,"warnings left:",myword)
                else:
                    num_of_guess-=1
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Oops! You've already guessed that letter. You have no warnings left:", myword)
                letters_guessed.remove(same_letter)
            else:
                if guess in secret_word:
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Good Guess", myword)
                    num_of_correct_guess += 1
                else:
                    myword += get_guessed_word(secret_word, letters_guessed)
                    print("Oops! That letter is not in my word.",myword)
                    if guess in vowels:
                        num_of_guess -= 2
                    else:
                        num_of_guess -= 1
        else:
            if num_of_warn>0:
                num_of_warn -= 1
                myword=get_guessed_word(secret_word,letters_guessed)
                print("Oops! That is not a valid letter. You have",num_of_warn,"warnings left:",myword)
            else:
                myword = get_guessed_word(secret_word, letters_guessed)
                print("Oops! That is not a valid letter. You have", num_of_warn, "warnings left:", myword)

        """
        if no guess chance left and not found the word then lose the game
        if found the correct word then calculate point=number of correct guess*number of guesses left
        """
        check_word_guessed=is_word_guessed(secret_word,letters_guessed)
        if num_of_guess<=0:
            if not check_word_guessed:
                print("---------------------------------------")
                print("Sorry, you ran out of guesses. The word was else. ")
                break
        if check_word_guessed:
            total_point=num_of_correct_guess*num_of_guess
            print("---------------------------------------")
            print("Congratulations, you won!")
            print("Your total score for this game is:",total_point)
            break
        print("---------------------------------------")

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)