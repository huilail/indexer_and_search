from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer

import re

stop_word = "^((.*_.*)|be|am|is|are|was|were|i|she|he|my|her|his|a|an|the|do|does|did|not|don't|doesn't|didn't)$"

def my_tokenizer(string):
    """
    Take a str type parameter
    Convert the given string to lower case
    Tokenize the given string using nltk.tokenize.word_tokenize
    Tag the result (a list containing words and punctuation) 
    Append only alphanumeric tokens to result list
    
    Return a list of 2-tuples
    first element is the token string (lower case)
    second element is the token tag
    """
    wnl = WordNetLemmatizer()
    raw = []
    if (type(string) == unicode):
        string = string.encode('utf-8')
    
    
    for element in wordpunct_tokenize(string.lower()):
        if re.match("^\w*$", element):
            raw.append(element)
    
    result = [(wnl.lemmatize(word)).encode('utf-8') for word in raw]
    
    return result


if __name__ == "__main__":
    f = open("test.txt","r")
    for line in f:
        print my_tokenizer(line)
        