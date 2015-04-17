import sys
import random


class SimpleMarkovGenerator(object):
    """Basic version of Markov generator; by default, has no length limit."""

    def read_file(self, filename):
        corpus = open(filename)
        word_list = corpus.read().split()                           # read in text of file as a list
        for word in word_list:
            if word == "":
                word_list.remove(word)
        return word_list

    def make_chains(self, ngram, word_list):
        """Takes input text as string; returns dictionary of markov chains."""

        dictionary = {}                                             # initialize empty dictionary

        n = int(ngram)                                              # set n (number of items in tuples)
        for i in range(len(word_list)-n):                           # loop over list items to fill dictionary
            key = tuple(word_list[i:(i+n)])                         # make keys in dictionary tuples of n items
            dictionary.setdefault(key, []).append(word_list[i+n])   # use setdefault to create values of dictionary
        
        return dictionary

    def make_text(self, dictionary):
        """Takes dictionary of markov chains; returns random text."""

        capital_keys_list = [key for key in dictionary.keys() if key[0][0].isupper()]   # create list of only keys that start with an uppercase letter
        starting_key = random.choice(capital_keys_list)             # choose key (tuple) to start at
        new_text_string = " ".join(starting_key)           # add items in that tuple to string of created text
        limit = 140

        punctuation = "?.!"                                         # create punctuation string    

        while dictionary.get(starting_key) != None and len(new_text_string) < limit:             # Continue until the key is not found in the dictionary
            value_list = dictionary[starting_key]               # assign value of key (list)
            next_word = random.choice(value_list)               # choose random word w/in list
            new_text_string = new_text_string + " " + next_word     # add next_word to list of created text
            starting_key = tuple(list(starting_key[1:]) + [next_word])   # create new tuple from second word of previous tuple + item at that index
            #print "at start of while loop:", new_text_string

            if len(new_text_string) > limit:        # if length of the current string is greater than the limit, iterate through each character from the end to find punctuation
                for i in range(len(new_text_string)-1,-1,-1):
                    if new_text_string[i] in punctuation:
                        new_text_string = new_text_string[0:(i+1)] # cut off string at punctuation
                        #print "after cutting at punct:", new_text_string

                        if len(new_text_string) > limit:           # This will only be true if no puncutation was found! check again if the length is greater than the limit
                            new_text_string = new_text_string[:(limit-2)]   # cut off string according to given limit
                            #print "after chopping:", new_text_string
                break

        return new_text_string                                  # return new text


if __name__ == "__main__":
    script, filename, ngram = sys.argv                          # unpack sys.argv arguments
    generator = SimpleMarkovGenerator()        # change this line based on which generator you want to use
    dictionary = generator.make_chains(ngram, generator.read_file(filename))
    random_text = generator.make_text(dictionary)                   # Produce random text

    print random_text
