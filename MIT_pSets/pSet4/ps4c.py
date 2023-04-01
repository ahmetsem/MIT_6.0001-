# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text=text
        self.valid_words=load_words("words.txt")
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        dict={}

        for i in range(52):
            if i<5:
                dict[VOWELS_LOWER[i]]=vowels_permutation[i].lower()
            elif i>=5 and i<26:
                dict[CONSONANTS_LOWER[i-5]]=CONSONANTS_LOWER[i-5].lower()
            elif i>=26 and i<31:
                dict[VOWELS_UPPER[i-26]]=vowels_permutation[i-26].upper()
            else:
                dict[CONSONANTS_UPPER[i-31]]=CONSONANTS_UPPER[i-31].upper()

        return dict


    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        encryp_word=""
        for i in range(len(self.message_text)):
            if self.message_text[i] in transpose_dict.keys():
                encryp_word+=transpose_dict[self.message_text[i]]
            else:
                encryp_word+=self.message_text[i]

        return encryp_word

        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''

        permutations=get_permutations("aeiou")
        count_of_words= 0
        max_numb_words=0
        correct_per=""
        message_text=self.get_message_text()
        valid_words=self.get_valid_words()
        check=True

        for per in permutations:
            decryp_message=""
            decryp_messages=[]
            dict = self.build_transpose_dict(per)
            for i in range(len(message_text)):
                if message_text[i] in dict.keys():
                    decryp_message+=dict[message_text[i]]
                else:
                    check=False
                    decryp_messages.append(decryp_message)
                    decryp_message=""
            if check:
                decryp_messages.append(decryp_message)

            count_of_words = 0
            for word in decryp_messages:
                if word.lower() in valid_words:
                    count_of_words+=1

            if count_of_words > max_numb_words:
                max_numb_words=count_of_words
                correct_per=per

        if correct_per =="":
            return message_text

        else:
            dict=self.build_transpose_dict(correct_per)
            message=""

            for i in range(len(message_text)):
                if message_text[i] in dict.keys():
                    message+=dict[message_text[i]]
                else:
                    message+=message_text[i]

            return message


if __name__ == '__main__':

    print()
    # Test Case SubMes-------------------------------------------
    # message = SubMessage("Hello World!")
    # permutation = "eaiuo"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Hallu Wurld!")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # print()
    # message = SubMessage("How are you cat?")
    # permutation = "eauoi"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "How era yoi cet?")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # print()
    # message = SubMessage("Flexible")
    # permutation = "eauoi"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Flaxubla")
    # print("Actual encryption:", message.apply_transpose(enc_dict))


    #Test Case Encrypt-------------------------------------------------------
    # print()
    # enc_message = EncryptedSubMessage("fuisca")
    # print("Original Message:", enc_message.get_message_text())
    # print("Expected Decrypted message:", "fiasco")
    # print("Decrypted message:", enc_message.decrypt_message())
    # print()
    # enc_message = EncryptedSubMessage("1 Fash fands fashor fashang fuisca ruffash!")
    # print("Original Message:",enc_message.get_message_text())
    # print("Expected Decrypted message:", "1 Fish finds fisher fishing fiasco raffish!")
    # print("Decrypted message:", enc_message.decrypt_message())
    # print()
    # enc_message = EncryptedSubMessage("1 Fesh fends fashir fashang fuisca ruffash!")
    # print("Original Message:",enc_message.get_message_text())
    # print("Expected Decrypted message:", "1 Fesh fends fashir fishing fiasco raffish!, or at least 3 correct word")
    # print("Decrypted message:",enc_message.decrypt_message())
