import random


# only function used by anagram bot
def get_set_of_words(data_dir, length=5):
    """
    Returns list of words for guessing
    """
    upper_limit = length + 5
    final_word_list = []
    for x in range(length, upper_limit):
        my_file = open(data_dir.format(str(x)), "r")
        word_list = my_file.read().splitlines()
        my_file.close()
        final_word_list += list(random.sample(set(word_list), upper_limit-x))
    return final_word_list


# text preprocessing functions
def remove_anagram(word_list):
    # Create a counting dictionary by sorting letters in words
    sorted_dict = {}
    for word in word_list:
        word_sorted = ''.join(sorted(word))
        if word_sorted not in sorted_dict.keys():
            sorted_dict[word_sorted] = 1
        else:
            sorted_dict[word_sorted] += 1

    # iterate again
    word_list_clean = [x for x in word_list if sorted_dict[''.join(sorted(x))] == 1]
    return word_list_clean


def process_word_list(word_list):
    """
    Takes in list of words, splits them by length and remove anagrams
    :param word_list: list of words
    :return: dictionary where key is length of word, value is list of words
    """

    word_list = remove_anagram(word_list)

    # split by word length
    words_dict = {}
    for word in word_list:
        length = len(word)
        if length in words_dict.keys():
            words_dict[length].append(word)
        else:
            words_dict[length] = [word]

    return words_dict


if __name__ == "__main__":

    WORD_LIST_DIR = './../data/common_words_list.txt'  # raw text file
    DATA_DIR = './../data/length_{}.txt'  # processed text files

    # read word list
    # Note: plenty of repeated words, all removed via remove_anagram()
    # Note 2: some anagrams are not captured
    # e.g. 'owe' is in our list, but 'woe' is not
    read_file = open(WORD_LIST_DIR, "r")
    word_list = read_file.read().splitlines()
    word_list = [i.strip().lower() for i in word_list if i.isalpha()]  # remove words with non-letters
    read_file.close()

    # process word list
    word_dict = process_word_list(word_list)

    # save word dict separately as txt files
    for length in word_dict.keys():
        print(length, len(word_dict[length]))
        with open(DATA_DIR.format(str(length)), "w+") as my_file:
            my_file.write('\n'.join(word_dict[length]))

    # test main function
    print(get_set_of_words('../data/length_{}.txt'))

'''
Number of final words per word length:
1 2
2 26
3 144
4 405
5 479
6 556
7 556
8 462
9 336
10 268
11 159
12 66
13 41
14 20
'''
