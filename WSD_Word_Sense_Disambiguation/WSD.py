import numpy as np
import sys
from collections import Counter

list_of_punctuations = ['(', '.', '/', ',', ':', ';', '[', '-']
try :
    with open(sys.argv[1], "r") as file:
        a = file.readlines()

    initial_array = np.empty((0, 3))
    for i in range(len(a)):
        if a[i] == '</instance>\n':
            col1 = a[i-5].split('"')[1]
            col2 = a[i-4].split('"')[-2]
            col3 = a[i-2]
            new_row = np.array([col1, col2, col3])
            initial_array = np.append(initial_array, [new_row], axis = 0)

    size1 = int(np.ceil(len(initial_array) / 5))
    size2 = len(initial_array)- 4*size1

    permutation = np.random.permutation(len(initial_array))
    initial_array = initial_array[permutation]
    train = [0] * 5
    for i in range(4):
        split, remaining_split = np.split(initial_array, [size1])
        train[i] = split
        initial_array = remaining_split
    train[4] = initial_array

    output_file_name = sys.argv[1].split('.')[0] + ".wsd.out"
    accuracies = []
    for i in range(5):
        print("With Fold " , i+1, "as Test Data")
        with open(output_file_name,"a+") as output_file:
            output_file.writelines(("For Fold " + str(i+1) + "\n"))
        test_data = train[i]
        train_data = np.vstack(train[:i] + train[i+1:])
        dict_words = {}
        for key in np.unique(train_data[:,1]):
            dict_words[key] = []

        for row in train_data:
            sentence_list = row[2].split()
            for word in sentence_list:
                if word[0] in list_of_punctuations:
                    word1 = word[1:len(word)]
                    lowercase_word = word1.lower()
                    sentence_list.remove(word)
                    if lowercase_word: sentence_list.append(lowercase_word)
                elif word[-1] in list_of_punctuations:
                    word1 = word[:-1]
                    lowercase_word = word1.lower()
                    sentence_list.remove(word)
                    if lowercase_word: sentence_list.append(lowercase_word)
            dict_words[row[1]] = dict_words[row[1]] + sentence_list
            
        for key, item in dict_words.items():
            dict_words[key] = Counter(item)

        predictions = []
        for row in test_data:
            test_sentence_list = row[2].split()
            for word in test_sentence_list:
                if word[0] in list_of_punctuations:
                    word1 = word[1:len(word)]
                    lowercase_word = word1.lower()
                    test_sentence_list.remove(word)
                    if lowercase_word: test_sentence_list.append(lowercase_word)
                elif word[-1] in list_of_punctuations:
                    word1 = word[:-1]
                    lowercase_word = word1.lower()
                    test_sentence_list.remove(word)
                    if lowercase_word: test_sentence_list.append(lowercase_word)

            scores = {}
            for key in np.unique(train_data[:,1]):
                scores[key] = 0.0
                
            for key in np.unique(train_data[:,1]):
                count_sense = np.sum(train_data[:, 1] == key)
                for word in test_sentence_list:
                    scores[key] += np.log((dict_words[key].get(word, 0)+1)/(count_sense + len(train_data)))
                scores[key] += np.log(count_sense/len(train_data))

            max_score = float('-inf')
            max_key = ''
            for k,v in scores.items():
                if v >= max_score:
                    max_score = v
                    max_key = k
            with open(output_file_name, "a+") as output_file:
                output_file.write((row[0] + " "))
                output_file.write((max_key + "\n"))
            predictions.append(max_key)
        acc = (sum(predictions == test_data[:,1])/len(predictions)) * 100
        accuracies.append(acc)
        print("Accuracy of Fold", i+1, ":", acc)
        print("------------------")
    print("Average accuracies over all folds:", np.average(accuracies))

except(FileNotFoundError):
    print("No such file or path not found")