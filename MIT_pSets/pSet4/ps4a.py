# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence)==1:
        return sequence

    first_letter=sequence[0]
    lst=get_permutations(sequence[1:])
    size=len(sequence)
    word=[]
    for i in range(size):
        word.append(0)
    words=[]

    for other_word in lst:
        for i in range(size):
            word[i] = first_letter
            a = 0
            for j in range(size):
                if i!=j:
                    word[j]=other_word[a]
                    a+=1

            new_word=""
            for i in range(size):
                new_word+=word[i]

            if new_word not in words:
                words.append(new_word)

    return words



if __name__ == '__main__':
    print()
    # #Test Case 1----------------------------
    # inpt="abc"
    # print("Expected Output: ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']")
    # print("Actual Output: ",get_permutations(inpt))
    #
    # # #Test Case 2-----------------------------
    # inpt="abb"
    # print("Expected Output: ['abb', 'bab', 'bba']")
    # print("Actual Output: ",get_permutations(inpt))
    #
    # #Test Case 3-------------------------------
    # inpt="abcd"
    # print("Expected Output: ['abcd', 'bacd', 'bcad', 'bcda', 'acbd', 'cabd', 'cbad', "
    #       "'cbda', 'acdb', 'cadb', 'cdab', 'cdba', 'abdc', 'badc', 'bdac', 'bdca', 'adbc', 'dabc',"
    #       " 'dbac', 'dbca', 'adcb', 'dacb', 'dcab', 'dcba']")
    # print("Actual Output: ",get_permutations(inpt))

