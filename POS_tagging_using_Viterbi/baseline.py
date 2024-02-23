from collections import defaultdict
import sys

try:
    file1 = open(sys.argv[1], "r")
    a = file1.readlines()

    tags_count = defaultdict(lambda : 0)
    count = 0
    for sample in a:
        sample = sample.split()
        for i in range(len(sample)):
            index = 0
            for j in range(len(sample[i])-1, -1, -1):
                if sample[i][j] == '/':
                    word = sample[i][:j]
                    tag = sample[i][j+1:]
                    tags_count[tag] += 1
                    break

    tag_mapper = {}
    count = 1
    for key in tags_count.keys():
        tag_mapper[count] = key
        count += 1

    word_tag_count = defaultdict(dict)

    for sample in a:
        sample = sample.split()
        for i in range(len(sample)):
            for j in range(len(sample[i])-1, -1, -1):
                if sample[i][j] == '/':
                    word = sample[i][:j]
                    tag = sample[i][j+1:]
                    if word not in word_tag_count:
                        for key in tags_count.keys():
                            word_tag_count[word][key] = 0
                    word_tag_count[word][tag] += 1
                    break

    tag_first_count = defaultdict(lambda : 0)
    for sent in a:
        word = sent.split()
        for j in range(len(word[0])-1, -1, -1):
            if word[0][j] == '/':
                tag = word[0][j+1:]
                tag_first_count[tag] += 1
                break

    tag_pair_count = defaultdict(dict)
    for sample in a:
        sample = sample.split()
        prev_tag = ''
        for i in range(len(sample)):
            for j in range(len(sample[i])-1, -1, -1):
                if sample[i][j] == '/':
                    word = sample[i][:j]
                    tag = sample[i][j+1:]
                    if i == 0:
                        prev_tag = tag
                    else:
                        if prev_tag not in tag_pair_count:
                            for key in tags_count.keys():
                                tag_pair_count[prev_tag][key] = 0
                        tag_pair_count[prev_tag][tag] += 1
                        prev_tag = tag
                    break
        
    def cleanSentence(sent):
        clean_sentence = []
        tags = []
        sent = sent.split()
        for i in range(len(sent)):
            for j in range(len(sent[i])-1, -1, -1):
                if sent[i][j] == '/':
                    clean_sentence.append(sent[i][:j])
                    tags.append(sent[i][j+1:])
                    break
        return(clean_sentence, tags)
    
    freq_dict = defaultdict()
    for key, value_counts in word_tag_count.items():
        freq_dict[key] = max(value_counts, key=value_counts.get)

    try:
        file1 = open(sys.argv[2], "r")
        b = file1.readlines()
        correct_predictions = 0
        total_predictions = 0
        for test_sent in b:
            count += 1
            cleaned_sentence, tags = cleanSentence(test_sent)
            predictions = []
            for element in cleaned_sentence:
                predictions.append(freq_dict.get(element, 'UNK'))
            correct_predictions += len([1 for x, y in zip(predictions, tags) if x == y])
            total_predictions += len(tags)
        
        print("Accuracy:", (correct_predictions/total_predictions)*100)
    except(FileNotFoundError):
        print("No such file or directory: ", sys.argv[2])
except(FileNotFoundError):
        print("No such file or directory: ", sys.argv[1])